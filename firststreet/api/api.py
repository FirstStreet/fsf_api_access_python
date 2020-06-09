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
                df = pd.DataFrame([vars(o) for o in data]).explode('type').explode('scenario').reset_index(drop=True)
                df.drop(["serving", "geometry"], axis=1, inplace=True)
                df['adaptationId'] = df['adaptationId'].astype('Int64').apply(str)
                df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
                df = df[['adaptationId', 'name', 'type', 'scenario', 'conveyance', 'returnPeriod']]

            elif product_subtype == 'summary':
                df = pd.DataFrame([vars(o) for o in data]).explode('adaptation').reset_index(drop=True)
                df['fsid'] = df['fsid'].apply(str)
                df = df[['fsid', 'adaptation']]

            else:
                raise NotImplementedError

        elif product == 'probability':
            if product_subtype == 'chance':
                df = pd.DataFrame([vars(o) for o in data]).explode('chance').reset_index(drop=True)
                if not df['chance'].isna().values.all():
                    df = pd.concat([df.drop(['chance'], axis=1), df['chance'].apply(pd.Series)], axis=1)
                    df = df.explode('data').reset_index(drop=True)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['threshold'] = df['threshold'].astype('Int64').apply(str)
                    df['low'] = df['low'].round(3)
                    df['mid'] = df['mid'].round(3)
                    df['high'] = df['high'].round(3)
                    df = df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]
                else:
                    df['fsid'] = df['fsid'].apply(str)
                    df.drop(['chance'], axis=1, inplace=True)
                    df['year'] = pd.NA
                    df['threshold'] = pd.NA
                    df['low'] = pd.NA
                    df['mid'] = pd.NA
                    df['high'] = pd.NA
                    df = df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]

            elif product_subtype == 'count':
                df = pd.DataFrame([vars(o) for o in data]).explode('count').reset_index(drop=True)
                if not df['count'].isna().values.all():
                    df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
                    df = df.explode('data').reset_index(drop=True)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df = df.explode('data').reset_index(drop=True)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
                    df['bin'] = df['bin'].astype('Int64').apply(str)
                    df['low'] = df['low'].astype('Int64').apply(str)
                    df['mid'] = df['mid'].astype('Int64').apply(str)
                    df['high'] = df['high'].astype('Int64').apply(str)
                    df = df[['fsid', 'year', 'returnPeriod', 'bin', 'low', 'mid', 'high']]
                else:
                    df['fsid'] = df['fsid'].apply(str)
                    df.drop(['count'], axis=1, inplace=True)
                    df['year'] = pd.NA
                    df['returnPeriod'] = pd.NA
                    df['bin'] = pd.NA
                    df['low'] = pd.NA
                    df['mid'] = pd.NA
                    df['high'] = pd.NA
                    df = df[['fsid', 'year', 'returnPeriod', 'bin', 'low', 'mid', 'high']]

            elif product_subtype == 'cumulative':
                df = pd.DataFrame([vars(o) for o in data]).explode('cumulative').reset_index(drop=True)
                if not df['cumulative'].isna().values.all():
                    df = pd.concat([df.drop(['cumulative'], axis=1), df['cumulative'].apply(pd.Series)], axis=1)
                    df = df.explode('data').reset_index(drop=True)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['threshold'] = df['threshold'].astype('Int64').apply(str)
                    df['low'] = df['low'].round(3)
                    df['mid'] = df['mid'].round(3)
                    df['high'] = df['high'].round(3)
                    df = df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]
                else:
                    df['fsid'] = df['fsid'].apply(str)
                    df.drop(['cumulative'], axis=1, inplace=True)
                    df['year'] = pd.NA
                    df['threshold'] = pd.NA
                    df['low'] = pd.NA
                    df['mid'] = pd.NA
                    df['high'] = pd.NA

            elif product_subtype == 'depth':
                df = pd.DataFrame([vars(o) for o in data]).explode('depth').reset_index(drop=True)
                if not df['depth'].isna().values.all():
                    df = pd.concat([df.drop(['depth'], axis=1), df['depth'].apply(pd.Series)], axis=1)
                    df = df.explode('data').reset_index(drop=True)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
                    df['low'] = df['low'].astype('Int64').apply(str)
                    df['mid'] = df['mid'].astype('Int64').apply(str)
                    df['high'] = df['high'].astype('Int64').apply(str)
                    df = df[['fsid', 'year', 'returnPeriod', 'low', 'mid', 'high']]
                else:
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df.drop(['depth'], axis=1, inplace=True)
                    df['year'] = pd.NA
                    df['returnPeriod'] = pd.NA
                    df['low'] = pd.NA
                    df['mid'] = pd.NA
                    df['high'] = pd.NA
                    df = df[['fsid', 'year', 'returnPeriod', 'low', 'mid', 'high']]
            else:
                raise NotImplementedError

        elif product == 'environmental':
            if product_subtype == 'precipitation':
                df = pd.DataFrame([vars(o) for o in data]).explode('projected').reset_index(drop=True)
                if not df['projected'].isna().values.all():
                    df = pd.concat([df.drop(['projected'], axis=1), df['projected'].apply(pd.Series)], axis=1)
                    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['low'] = df['low'].round(3)
                    df['mid'] = df['mid'].round(3)
                    df['high'] = df['high'].round(3)
                    df = df[['fsid', 'year', 'low', 'mid', 'high']]
                else:
                    df['fsid'] = df['fsid'].apply(str)
                    df.drop(['projected'], axis=1, inplace=True)
                    df['year'] = pd.NA
                    df['low'] = pd.NA
                    df['mid'] = pd.NA
                    df['high'] = pd.NA
                    df = df[['fsid', 'year', 'low', 'mid', 'high']]

            else:
                raise NotImplementedError

        elif product == 'historic':
            if product_subtype == 'event':
                df = pd.DataFrame([vars(o) for o in data])
                df.drop(["geometry"], axis=1, inplace=True)
                if not df['properties'].isna().values.all():
                    df = pd.concat([df.drop(['properties'], axis=1), df['properties'].apply(pd.Series)], axis=1)
                    df['eventId'] = df['eventId'].astype('Int64').apply(str)
                    df['month'] = df['month'].astype('Int64').apply(str)
                    df['year'] = df['year'].astype('Int64').apply(str)
                    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
                    df['total'] = df['total'].astype('Int64').apply(str)
                    df['affected'] = df['affected'].astype('Int64').apply(str)
                    df.rename(columns={'total': 'propertiesTotal', 'affected': 'propertiesAffected'}, inplace=True)
                    df = df[['eventId', 'name', 'month', 'year', 'returnPeriod', 'type',
                             'propertiesTotal', 'propertiesAffected']]
                else:
                    df['eventId'] = df['eventId'].astype('Int64').apply(str)
                    df.drop(['properties'], axis=1, inplace=True)
                    df['propertiesTotal'] = pd.NA
                    df['propertiesAffected'] = pd.NA
                    df = df[['eventId', 'name', 'month', 'year', 'returnPeriod', 'type',
                             'propertiesTotal', 'propertiesAffected']]

            elif product_subtype == 'summary':
                df = pd.DataFrame([vars(o) for o in data]).explode('historic').reset_index(drop=True)
                if not df['historic'].isna().values.all():
                    df = pd.concat([df.drop(['historic'], axis=1), df['historic'].apply(pd.Series)], axis=1)
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df['eventId'] = df['eventId'].astype('Int64').apply(str)
                    df['data'] = df['data'].astype('Int64').apply(str)
                    df = df[['fsid', 'eventId', 'name', 'type', 'depth']]
                else:
                    df['fsid'] = df['fsid'].astype('Int64').apply(str)
                    df.drop(['historic'], axis=1, inplace=True)
                    df['eventId'] = pd.NA
                    df['name'] = pd.NA
                    df['type'] = pd.NA
                    df['depth'] = pd.NA
                    df = df[['fsid', 'eventId', 'name', 'type', 'depth']]

            else:
                raise NotImplementedError

        elif product == 'location':
            if product_subtype == 'detail':
                if location_type == 'property':

                    df = pd.DataFrame([vars(o) for o in data]).explode('neighborhood').reset_index(drop=True)
                    if not df['city'].isna().values.all():
                        df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    else:
                        df.drop(['city'], axis=1, inplace=True)
                        df['city_fips'] = pd.NA
                        df['city_name'] = pd.NA

                    if not df['neighborhood'].isna().values.all():
                        df = pd.concat([df.drop(['neighborhood'], axis=1), df['neighborhood'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'neighborhood_fips', 'name': 'neighborhood_name'}, inplace=True)
                    else:
                        df.drop(['neighborhood'], axis=1, inplace=True)
                        df['neighborhood_fips'] = pd.NA
                        df['neighborhood_name'] = pd.NA

                    if not df['tract'].isna().values.all():
                        df = pd.concat([df.drop(['tract'], axis=1), df['tract'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'tract_fips', 'name': 'tract_name'}, inplace=True)
                    else:
                        df.drop(['tract'], axis=1, inplace=True)
                        df['tract_fips'] = pd.NA
                        df['tract_name'] = pd.NA

                    if not df['county'].isna().values.all():
                        df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
                    else:
                        df.drop(['county'], axis=1, inplace=True)
                        df['county_fips'] = pd.NA
                        df['county_name'] = pd.NA

                    if not df['cd'].isna().values.all():
                        df = pd.concat([df.drop(['cd'], axis=1), df['cd'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'cd_fips', 'name': 'cd_name'}, inplace=True)
                    else:
                        df.drop(['cd'], axis=1, inplace=True)
                        df['cd_fips'] = pd.NA
                        df['cd_name'] = pd.NA

                    if not df['state'].isna().values.all():
                        df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    else:
                        df.drop(['state'], axis=1, inplace=True)
                        df['state_fips'] = pd.NA
                        df['state_name'] = pd.NA

                    df.columns.values[0] = "fsid"
                    df['fsid'] = df['fsid'].apply(str)
                    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
                    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
                    df['tract_fips'] = df['tract_fips'].astype('Int64').apply(str)
                    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
                    df['cd_fips'] = df['cd_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df['footprintId'] = df['footprintId'].astype('Int64').apply(str)
                    df['elevation'] = df['city_fips'].apply(str)
                    df = df[['fsid', 'streetNumber', 'route', 'city_fips', 'city_name', 'zipCode', 'neighborhood_fips',
                             'neighborhood_name', 'tract_fips', 'county_fips', 'county_name', 'cd_fips',
                             'cd_name', 'state_fips', 'state_name', 'footprintId', 'elevation', 'fema']]

                elif location_type == 'neighborhood':
                    df = pd.DataFrame([vars(o) for o in data]).explode('city').reset_index(drop=True)

                    if not df['city'].isna().values.all():
                        df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    else:
                        df.drop(['city'], axis=1, inplace=True)
                        df['city_fips'] = pd.NA
                        df['city_name'] = pd.NA

                    if not df['state'].isna().values.all():
                        df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    else:
                        df.drop(['state'], axis=1, inplace=True)
                        df['state_fips'] = pd.NA
                        df['state_name'] = pd.NA

                    df.columns.values[0] = "fsid"
                    df.columns.values[2] = "name"
                    df['fsid'] = df['fsid'].apply(str)
                    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'name', 'city_fips', 'city_name', 'subtype', 'state_fips', 'state_name']]

                elif location_type == 'city':
                    df = pd.DataFrame([vars(o) for o in data]).explode('zcta')\
                        .explode('neighborhood').reset_index(drop=True)

                    if not df['zcta'].isna().values.all():
                        df = pd.concat([df.drop(['zcta'], axis=1), df['zcta'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'zipCode', 'name': 'zcta_name'}, inplace=True)
                    else:
                        df.drop(['zcta'], axis=1, inplace=True)
                        df['zipCode'] = pd.NA
                        df['zcta_name'] = pd.NA

                    if not df['neighborhood'].isna().values.all():
                        df = pd.concat([df.drop(['neighborhood'], axis=1), df['neighborhood'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'neighborhood_fips', 'name': 'neighborhood_name'}, inplace=True)
                    else:
                        df.drop(['neighborhood'], axis=1, inplace=True)
                        df['neighborhood_fips'] = pd.NA
                        df['neighborhood_name'] = pd.NA

                    if not df['state'].isna().values.all():
                        df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                        df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    else:
                        df.drop(['state'], axis=1, inplace=True)
                        df['state_fips'] = pd.NA
                        df['state_name'] = pd.NA

                    df.columns.values[0] = "fsid"
                    df.columns.values[3] = "name"
                    df['fsid'] = df['fsid'].apply(str)
                    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
                    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'name', 'lsad', 'zipCode', 'neighborhood_fips', 'neighborhood_name',
                             'state_fips', 'state_name']]

                elif location_type == 'zcta':
                    df = pd.DataFrame([vars(o) for o in data])
                    df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df.columns.values[2] = "name"
                    df['fsid'] = df['fsid'].apply(str)
                    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'name', 'city_fips', 'city_fips',
                             'state_fips', 'state_name']]
                    print("")

                elif location_type == 'tract':
                    df = pd.DataFrame([vars(o) for o in data])
                    df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df['fsid'] = df['fsid'].apply(str)
                    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'fips', 'county_fips', 'county_name',
                             'state_fips', 'state_name']]
                    print("")

                elif location_type == 'county':
                    df = pd.DataFrame([vars(o) for o in data]).explode('city').explode('zcta')\
                        .explode('cd').reset_index(drop=True)
                    df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    df = pd.concat([df.drop(['zcta'], axis=1), df['zcta'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'zipCode', 'name': 'zcta_name'}, inplace=True)
                    df = pd.concat([df.drop(['cd'], axis=1), df['cd'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'cd_fips', 'name': 'cd_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df['fsid'] = df['fsid'].apply(str)
                    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
                    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
                    df['cd_fips'] = df['cd_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'city_fips', 'city_name', 'zipCode', 'fips', 'isCoastal', 'cd_fips',
                             'cd_name', 'state_fips', 'state_name']]
                    print("")

                elif location_type == 'cd':
                    df = pd.DataFrame([vars(o) for o in data]).explode('county')
                    df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df['fsid'] = df['fsid'].apply(str)
                    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'district', 'county_fips', 'county_name', 'state_fips', 'state_name']]
                    print("")

                elif location_type == 'state':
                    df = pd.DataFrame([vars(o) for o in data])
                    df['fsid'] = df['fsid'].apply(str)
                    df = df[['fsid', 'name', 'fips']]
                    print("")

                else:
                    raise NotImplementedError

            elif product_subtype == 'summary':

                if location_type == 'property':
                    df = pd.DataFrame([vars(o) for o in data])
                    df['fsid'] = df['fsid'].apply(str)
                    df['riskDirection'] = df['riskDirection'].astype('Int64').apply(str)
                    df['environmentalRisk'] = df['environmentalRisk'].astype('Int64').apply(str)
                    df['historic'] = df['historic'].astype('Int64').apply(str)
                    df['adaptation'] = df['adaptation'].astype('Int64').apply(str)
                    df['floodFactor'] = df['floodFactor'].astype('Int64').apply(str)
                    df = df[['fsid', 'floodFactor', 'riskDirection', 'environmentalRisk', 'historic', 'adaptation']]
                    print("")

                else:
                    df = pd.DataFrame([vars(o) for o in data])
                    df['fsid'] = df['fsid'].apply(str)
                    df['riskDirection'] = df['riskDirection'].astype('Int64').apply(str)
                    df['environmentalRisk'] = df['environmentalRisk'].astype('Int64').apply(str)
                    df['historic'] = df['historic'].astype('Int64').apply(str)
                    df['adaptation'] = df['adaptation'].astype('Int64').apply(str)
                    df['properties'] = df['properties'].astype('Int64').apply(str)
                    df = df[['fsid', 'floodFactor', 'riskDirection', 'environmentalRisk', 'properties', 'historic']]
                    print("")

            else:
                raise NotImplementedError

        elif product == 'fema':
            if product_subtype == 'nfip':
                df = pd.DataFrame([vars(o) for o in data])
                df['fsid'] = df['fsid'].apply(str)
                df['claimCount'] = df['claimCount'].astype('Int64').apply(str)
                df['policyCount'] = df['policyCount'].astype('Int64').apply(str)
                df['buildingPaid'] = df['buildingPaid'].astype('Int64').apply(str)
                df['contentPaid'] = df['contentPaid'].astype('Int64').apply(str)
                df['buildingCoverage'] = df['buildingCoverage'].astype('Int64').apply(str)
                df['contentCoverage'] = df['contentCoverage'].astype('Int64').apply(str)
                df['iccPaid'] = df['iccPaid'].astype('Int64').apply(str)
                df = df[['fsid', 'claimCount', 'policyCount', 'buildingPaid', 'contentPaid', 'buildingCoverage',
                         'contentCoverage', 'iccPaid']]
                print("")
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        df.fillna(pd.NA, inplace=True)
        df.to_csv(output_dir + '/' + file_name)
