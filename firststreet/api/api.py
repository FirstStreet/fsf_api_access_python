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

        if product == 'adaptation':
            if product_subtype == 'detail':
                df = pd.DataFrame([vars(o) for o in data]).explode('type').explode('scenario').reset_index(drop=True)
                df.drop(["serving", "geometry"], axis=1, inplace=True)
                df = df[['adaptationId', 'name', 'type', 'scenario', 'conveyance', 'returnPeriod']]

            elif product_subtype == 'summary':
                df = pd.DataFrame([vars(o) for o in data]).explode('adaptation').reset_index(drop=True)
                df = df[['fsid', 'adaptation']]

            else:
                raise NotImplementedError

        elif product == 'probability':
            if product_subtype == 'chance':
                df = pd.DataFrame([vars(o) for o in data]).explode('chance').reset_index(drop=True)
                df = pd.concat([df.drop(['chance'], axis=1), df['chance'].apply(pd.Series)], axis=1)
                df = df.explode('data').reset_index(drop=True)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]

            elif product_subtype == 'count':
                df = pd.DataFrame([vars(o) for o in data]).explode('count').reset_index(drop=True)
                df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
                df = df.explode('data').reset_index(drop=True)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df.explode('data').reset_index(drop=True)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df[['fsid', 'year', 'returnPeriod', 'bin', 'low', 'mid', 'high']]

            elif product_subtype == 'cumulative':
                df = pd.DataFrame([vars(o) for o in data]).explode('cumulative').reset_index(drop=True)
                df = pd.concat([df.drop(['cumulative'], axis=1), df['cumulative'].apply(pd.Series)], axis=1)
                df = df.explode('data').reset_index(drop=True)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]

            elif product_subtype == 'depth':
                df = pd.DataFrame([vars(o) for o in data]).explode('depth').reset_index(drop=True)
                df = pd.concat([df.drop(['depth'], axis=1), df['depth'].apply(pd.Series)], axis=1)
                df = df.explode('data').reset_index(drop=True)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df[['fsid', 'year', 'returnPeriod', 'low', 'mid', 'high']]
            else:
                raise NotImplementedError

        elif product == 'environmental':
            if product_subtype == 'precipitation':
                df = pd.DataFrame([vars(o) for o in data]).explode('projected').reset_index(drop=True)
                df = pd.concat([df.drop(['projected'], axis=1), df['projected'].apply(pd.Series)], axis=1)
                df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series).drop(0, axis=1)], axis=1)
                df = df[['fsid', 'year', 'low', 'mid', 'high']]

            else:
                raise NotImplementedError

        elif product == 'historic':
            if product_subtype == 'event':
                df = pd.DataFrame([vars(o) for o in data])
                df.drop(["geometry"], axis=1, inplace=True)
                df = pd.concat([df.drop(['properties'], axis=1), df['properties'].apply(pd.Series)], axis=1)
                df = df[['eventId', 'name', 'month', 'year', 'returnPeriod', 'type', 'total', 'affected']]
                df.rename(columns={'total': 'propertiesTotal', 'affected': 'propertiesAffected'}, inplace=True)

            elif product_subtype == 'summary':
                df = pd.DataFrame([vars(o) for o in data]).explode('historic').reset_index(drop=True)
                df = pd.concat([df.drop(['historic'], axis=1), df['historic'].apply(pd.Series)], axis=1)
                df = df[['fsid', 'eventId', 'name', 'type', 'depth']]
            else:
                raise NotImplementedError

        elif product == 'location':
            if product_subtype == 'detail':
                if location_type == 'property':

                    df = pd.DataFrame([vars(o) for o in data]).explode('neighborhood').reset_index(drop=True)
                    df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    df = pd.concat([df.drop(['neighborhood'], axis=1), df['neighborhood'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'neighborhood_fips', 'name': 'neighborhood_name'}, inplace=True)
                    df = pd.concat([df.drop(['tract'], axis=1), df['tract'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'tract_fips', 'name': 'tract_name'}, inplace=True)
                    df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
                    df = pd.concat([df.drop(['cd'], axis=1), df['cd'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'cd_fips', 'name': 'cd_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
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
                    df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df.columns.values[2] = "name"
                    df['fsid'] = df['fsid'].apply(str)
                    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'name', 'city_fips', 'city_name', 'subtype', 'state_fips', 'state_name']]

                elif location_type == 'city':
                    df = pd.DataFrame([vars(o) for o in data]).explode('zcta')\
                        .explode('neighborhood').reset_index(drop=True)
                    df = pd.concat([df.drop(['zcta'], axis=1), df['zcta'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'zipCode', 'name': 'zcta_name'}, inplace=True)
                    df = pd.concat([df.drop(['neighborhood'], axis=1), df['neighborhood'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'neighborhood_fips', 'name': 'neighborhood_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df.columns.values[3] = "name"
                    df['fsid'] = df['fsid'].apply(str)
                    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
                    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'name', 'lsad', 'zipCode', 'neighborhood_fips', 'neighborhood_name',
                             'state_fips', 'state_name']]
                    print("")

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

                elif location_type == 'cd':
                    df = pd.DataFrame([vars(o) for o in data]).explode('county')
                    df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
                    df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
                    df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
                    df.columns.values[0] = "fsid"
                    df['fsid'] = df['fsid'].apply(str)
                    df['congress'] = df['congress'].astype('Int64').apply(str)
                    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
                    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
                    df = df[['fsid', 'district', 'county_fips', 'county_name', 'congress', 'state_fips', 'state_name']]

                elif location_type == 'state':
                    df = pd.DataFrame([vars(o) for o in data])
                    df['fsid'] = df['fsid'].apply(str)
                    df = df[['fsid', 'name', 'fips']]

                else:
                    raise NotImplementedError

            elif product_subtype == 'summary':
                df = pd.DataFrame([vars(o) for o in data])
                print("")
            else:
                raise NotImplementedError

        elif product == 'fema':
            if product_subtype == 'nfip':
                df = pd.DataFrame([vars(o) for o in data])
                print("")
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        print("")
        df.fillna(pd.NA, inplace=True)
        df.to_csv(output_dir + '/' + file_name)
