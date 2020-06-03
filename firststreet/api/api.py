# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import datetime
import os
from json import JSONDecodeError

# External Imports
import pandas as pd

# Internal Imports
from firststreet.errors import InvalidArgument


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

        api_data = []

        for fsid in fsids:

            base_url = self._http.options.get('url')
            version = self._http.version

            if location:
                endpoint = "/".join([base_url, version, product, product_subtype, location, str(fsid)])
            else:
                endpoint = "/".join([base_url, version, product, product_subtype, str(fsid)])

            try:
                response = self._http.endpoint_execute(endpoint)

                error = response.get("error")

                if error:
                    if product == 'adaptation' and product_subtype == 'detail':
                        api_data.append({'adaptationId': fsid})

                    elif product == 'historical' and product_subtype == 'event':
                        api_data.append({'eventId': fsid})

                    else:
                        api_data.append({'fsid': fsid})

                else:
                    api_data.append(response)

            except JSONDecodeError:
                print("")

        return api_data

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

        df = pd.DataFrame([vars(o) for o in data])
        df.to_csv(output_dir + '/' + file_name)
