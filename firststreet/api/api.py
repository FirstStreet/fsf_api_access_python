# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import asyncio
import datetime
import os

# External Imports
import pandas as pd

# Internal Imports
from firststreet.errors import InvalidArgument
import firststreet.api.csv_format as csv_format


class Api:
    """This class receives an FSID, coordinate, or address, and handles the
        creation of a data summary from the request.

        Attributes:
            http (Http): A http class to connect to the First Street Foundation API
        Methods:
            get_property_by_fsid: Retrieves a Property by specific ID
            get_property_by_coordinate: Retrieves a Property by a coordinate
            get_property_by_address: Retrieves a Property by address lookup
            get_city_by_fsid: Retrieves a City by specific ID
            get_city_by_coordinate: Retrieves a City by a coordinate
            get_city_by_address: Retrieves a City by address lookup
        """

    def __init__(self, http):
        self._http = http

    def call_api(self, fsids, product, product_subtype, location):

        if not fsids:
            raise InvalidArgument(fsids)
        elif not isinstance(fsids, list):
            raise TypeError("location is not a string")

        base_url = self._http.options.get('url')
        version = self._http.version

        if location:
            endpoints = [("/".join([base_url, version, product, product_subtype, location, str(fsid)]), fsid,
                          product, product_subtype) for fsid in fsids]
        else:
            endpoints = [("/".join([base_url, version, product, product_subtype, str(fsid)]), fsid,
                          product, product_subtype) for fsid in fsids]

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self._http.endpoint_execute(endpoints))

        return response

    @staticmethod
    def to_csv(data, product, product_subtype, location_type=None):
        date = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

        if location_type:
            file_name = "_".join([date, product, product_subtype, location_type]) + ".csv"
        else:
            file_name = "_".join([date, product, product_subtype]) + ".csv"

        output_dir = "/".join([os.getcwd(), "data_csv"])

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if product == 'adaptation':

            if product_subtype == 'detail':
                df = csv_format.format_adaptation_detail(data)

            elif product_subtype == 'summary':
                df = csv_format.format_adaptation_summary(data)

            else:
                raise NotImplementedError

            return df

        elif product == 'probability':
            if product_subtype == 'chance':
                df = csv_format.format_probability_chance(data)

            elif product_subtype == 'count':
                df = csv_format.format_probability_count(data)

            elif product_subtype == 'cumulative':
                df = csv_format.format_probability_cumulative(data)

            elif product_subtype == 'depth':
                df = csv_format.format_probability_depth(data)
            else:
                raise NotImplementedError

        elif product == 'environmental':
            if product_subtype == 'precipitation':
                df = csv_format.format_environmental_precipitation(data)

            else:
                raise NotImplementedError

        elif product == 'historic':
            if product_subtype == 'event':
                df = csv_format.format_historic_event(data)

            elif product_subtype == 'summary':
                if location_type == 'property':
                    df = csv_format.format_historic_summary_property(data)

                else:
                    df = csv_format.format_historic_summary(data)

            else:
                raise NotImplementedError

        elif product == 'location':
            if product_subtype == 'detail':
                if location_type == 'property':
                    df = csv_format.format_location_detail_property(data)

                elif location_type == 'neighborhood':
                    df = csv_format.format_location_detail_neighborhood(data)

                elif location_type == 'city':
                    df = csv_format.format_location_detail_city(data)

                elif location_type == 'zcta':
                    df = csv_format.format_location_detail_zcta(data)

                elif location_type == 'tract':
                    df = csv_format.format_location_detail_tract(data)

                elif location_type == 'county':
                    df = csv_format.format_location_detail_county(data)

                elif location_type == 'cd':
                    df = csv_format.format_location_detail_cd(data)

                elif location_type == 'state':
                    df = csv_format.format_location_detail_state(data)

                else:
                    raise NotImplementedError

            elif product_subtype == 'summary':

                if location_type == 'property':
                    df = csv_format.format_location_summary_property(data)

                else:
                    df = csv_format.format_location_summary(data)

            else:
                raise NotImplementedError

        elif product == 'fema':
            if product_subtype == 'nfip':
                df = csv_format.format_fema_nfip(data)
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        df.fillna(pd.NA, inplace=True)
        df.to_csv(output_dir + '/' + file_name)
