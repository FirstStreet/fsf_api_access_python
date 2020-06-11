# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import datetime
import os

# External Imports
import pandas as pd


def to_csv(data, product, product_subtype, location_type=None):
    """Receives a list of data, a product, a product subtype, and a location to create a CSV

    Args:
        data (list): A list of FSF object
        product (str): The overall product to call
        product_subtype (str): The product subtype (if suitable)
        location_type (str): The location lookup type (if suitable)
    """

    date = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

    # Set file name to the current date, time, and product
    if location_type:
        file_name = "_".join([date, product, product_subtype, location_type]) + ".csv"
    else:
        file_name = "_".join([date, product, product_subtype]) + ".csv"

    output_dir = "/".join([os.getcwd(), "data_csv"])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Format the data for each product
    if product == 'adaptation':

        if product_subtype == 'detail':
            df = format_adaptation_detail(data)

        elif product_subtype == 'summary':
            df = format_adaptation_summary(data)

        else:
            raise NotImplementedError

    elif product == 'probability':
        if product_subtype == 'chance':
            df = format_probability_chance(data)

        elif product_subtype == 'count':
            df = format_probability_count(data)

        elif product_subtype == 'count-summary':
            df = format_probability_count_summary(data)

        elif product_subtype == 'cumulative':
            df = format_probability_cumulative(data)

        elif product_subtype == 'depth':
            df = format_probability_depth(data)
        else:
            raise NotImplementedError

    elif product == 'environmental':
        if product_subtype == 'precipitation':
            df = format_environmental_precipitation(data)

        else:
            raise NotImplementedError

    elif product == 'historic':
        if product_subtype == 'event':
            df = format_historic_event(data)

        elif product_subtype == 'summary':
            if location_type == 'property':
                df = format_historic_summary_property(data)

            else:
                df = format_historic_summary(data)

        else:
            raise NotImplementedError

    elif product == 'location':
        if product_subtype == 'detail':
            if location_type == 'property':
                df = format_location_detail_property(data)

            elif location_type == 'neighborhood':
                df = format_location_detail_neighborhood(data)

            elif location_type == 'city':
                df = format_location_detail_city(data)

            elif location_type == 'zcta':
                df = format_location_detail_zcta(data)

            elif location_type == 'tract':
                df = format_location_detail_tract(data)

            elif location_type == 'county':
                df = format_location_detail_county(data)

            elif location_type == 'cd':
                df = format_location_detail_cd(data)

            elif location_type == 'state':
                df = format_location_detail_state(data)

            else:
                raise NotImplementedError

        elif product_subtype == 'summary':

            if location_type == 'property':
                df = format_location_summary_property(data)

            else:
                df = format_location_summary(data)

        else:
            raise NotImplementedError

    elif product == 'fema':
        if product_subtype == 'nfip':
            df = format_fema_nfip(data)
        else:
            raise NotImplementedError

    else:
        raise NotImplementedError

    # Export CSVs
    df.fillna(pd.NA, inplace=True)
    df.to_csv(output_dir + '/' + file_name, index=False)


def format_adaptation_detail(data):
    """Reformat the list of data to Adaptation Detail format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('type').explode('scenario').reset_index(drop=True)
    df.drop(["serving", "geometry"], axis=1, inplace=True)
    df['adaptationId'] = df['adaptationId'].astype('Int64').apply(str)
    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
    return df[['adaptationId', 'name', 'type', 'scenario', 'conveyance', 'returnPeriod']]


def format_adaptation_summary(data):
    """Reformat the list of data to Adaptation Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('adaptation').reset_index(drop=True)
    df['fsid'] = df['fsid'].apply(str)
    return df[['fsid', 'adaptation']]


def format_probability_chance(data):
    """Reformat the list of data to Probability Chance format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('chance').reset_index(drop=True)
    if not df['chance'].isna().values.all():
        df = pd.concat([df.drop(['chance'], axis=1), df['chance'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['threshold'] = df['threshold'].astype('Int64').apply(str)
        df['low'] = df['low'].round(3)
        df['mid'] = df['mid'].round(3)
        df['high'] = df['high'].round(3)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['chance'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['threshold'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]


def format_probability_count(data):
    """Reformat the list of data to Probability Count format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('count').reset_index(drop=True)
    if not df['count'].isna().values.all():
        df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
        df['bin'] = df['bin'].astype('Int64').apply(str)
        df['low'] = df['low'].astype('Int64').apply(str)
        df['mid'] = df['mid'].astype('Int64').apply(str)
        df['high'] = df['high'].astype('Int64').apply(str)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['count'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['returnPeriod'] = pd.NA
        df['bin'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'year', 'returnPeriod', 'bin', 'low', 'mid', 'high']]


def format_probability_count_summary(data):
    """Reformat the list of data to Probability Count-Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    # listed_data = [{'fsid': attr.fsid, 'location': [{'state': attr.state}, {'city': attr.city}, {'zcta': attr.zcta},
    #                                                 {'neighborhood': attr.neighborhood}, {'tract': attr.tract},
    #                                                 {'county': attr.county}, {'cd': attr.cd}]} for attr in data]
    listed_data = [{'fsid': attr.fsid, 'location': [{'location': 'state', 'data': attr.state},
                                                    {'location': 'city', 'data': attr.city},
                                                    {'location': 'zcta', 'data': attr.zcta},
                                                    {'location': 'neighborhood', 'data': attr.neighborhood},
                                                    {'location': 'tract', 'data': attr.tract},
                                                    {'location': 'county', 'data': attr.county},
                                                    {'location': 'cd', 'data': attr.cd}]} for attr in data]

    df = pd.DataFrame(listed_data).explode('location').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder'}, inplace=True)
    df = pd.concat([df.drop(['location'], axis=1), df['location'].apply(pd.Series)], axis=1)
    df = df.explode('data').reset_index(drop=True)
    df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
    df.rename(columns={'fsid': 'location_fips', 'name': 'location_name'}, inplace=True)

    if 'count' in df:
        df = df.explode('count').reset_index(drop=True)
        df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid_placeholder': 'fsid'}, inplace=True)
        if 'subtype' not in df:
            df['subtype'] = pd.NA
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['location_fips'] = df['location_fips'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['low'] = df['low'].astype('Int64').apply(str)
        df['mid'] = df['mid'].astype('Int64').apply(str)
        df['high'] = df['high'].astype('Int64').apply(str)

    else:
        df['location_fips'] = pd.NA
        df['location_name'] = pd.NA
        df['year'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'location', 'location_fips', 'location_name', 'subtype', 'year', 'low', 'mid', 'high']]


def format_probability_cumulative(data):
    """Reformat the list of data to Probability Cumulative format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('cumulative').reset_index(drop=True)
    if not df['cumulative'].isna().values.all():
        df = pd.concat([df.drop(['cumulative'], axis=1), df['cumulative'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['threshold'] = df['threshold'].astype('Int64').apply(str)
        df['low'] = df['low'].round(3)
        df['mid'] = df['mid'].round(3)
        df['high'] = df['high'].round(3)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['cumulative'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['threshold'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'year', 'threshold', 'low', 'mid', 'high']]


def format_probability_depth(data):
    """Reformat the list of data to Probability Depth format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('depth').reset_index(drop=True)
    if not df['depth'].isna().values.all():
        df = pd.concat([df.drop(['depth'], axis=1), df['depth'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
        df['low'] = df['low'].astype('Int64').apply(str)
        df['mid'] = df['mid'].astype('Int64').apply(str)
        df['high'] = df['high'].astype('Int64').apply(str)
    else:
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df.drop(['depth'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['returnPeriod'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'year', 'returnPeriod', 'low', 'mid', 'high']]


def format_environmental_precipitation(data):
    """Reformat the list of data to Environmental Precipitation format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('projected').reset_index(drop=True)
    if not df['projected'].isna().values.all():
        df = pd.concat([df.drop(['projected'], axis=1), df['projected'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['year'] = df['year'].astype('Int64').apply(str)
        df['low'] = df['low'].round(3)
        df['mid'] = df['mid'].round(3)
        df['high'] = df['high'].round(3)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['projected'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    return df[['fsid', 'year', 'low', 'mid', 'high']]


def format_historic_event(data):
    """Reformat the list of data to Historic Event format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
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
    else:
        df['eventId'] = df['eventId'].astype('Int64').apply(str)
        df.drop(['properties'], axis=1, inplace=True)
        df['propertiesTotal'] = pd.NA
        df['propertiesAffected'] = pd.NA

    return df[['eventId', 'name', 'month', 'year', 'returnPeriod', 'type', 'propertiesTotal', 'propertiesAffected']]


def format_historic_summary_property(data):
    """Reformat the list of data to Historic Summary format for property

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('historic').reset_index(drop=True)
    if not df['historic'].isna().values.all():
        df = pd.concat([df.drop(['historic'], axis=1), df['historic'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df['eventId'] = df['eventId'].astype('Int64').apply(str)
        df['depth'] = df['depth'].astype('Int64').apply(str)
    else:
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df.drop(['historic'], axis=1, inplace=True)
        df['eventId'] = pd.NA
        df['name'] = pd.NA
        df['type'] = pd.NA
        df['depth'] = pd.NA

    return df[['fsid', 'eventId', 'name', 'type', 'depth']]


def format_historic_summary(data):
    """Reformat the list of data to Historic Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('historic').reset_index(drop=True)
    if not df['historic'].isna().values.all():
        df = pd.concat([df.drop(['historic'], axis=1), df['historic'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['eventId'] = df['eventId'].astype('Int64').apply(str)
        df['bin'] = df['bin'].astype('Int64').apply(str)
        df['count'] = df['count'].astype('Int64').apply(str)
    else:
        df['fsid'] = df['fsid'].astype('Int64').apply(str)
        df.drop(['historic'], axis=1, inplace=True)
        df['eventId'] = pd.NA
        df['name'] = pd.NA
        df['type'] = pd.NA
        df['bin'] = pd.NA
        df['count'] = pd.NA

    return df[['fsid', 'eventId', 'name', 'type', 'bin', 'count']]


def format_location_detail_property(data):
    """Reformat the list of data to Location Detail format for property

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('neighborhood').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder'}, inplace=True)

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

    df.rename(columns={'fsid_placeholder': 'fsid'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
    df['tract_fips'] = df['tract_fips'].astype('Int64').apply(str)
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['cd_fips'] = df['cd_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    df['footprintId'] = df['footprintId'].astype('Int64').apply(str)
    df['elevation'] = df['city_fips'].apply(str)
    return df[['fsid', 'streetNumber', 'route', 'city_fips', 'city_name', 'zipCode', 'neighborhood_fips',
               'neighborhood_name', 'tract_fips', 'county_fips', 'county_name', 'cd_fips',
               'cd_name', 'state_fips', 'state_name', 'footprintId', 'elevation', 'fema']]


def format_location_detail_neighborhood(data):
    """Reformat the list of data to Location Detail format for neighborhood

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('city').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

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

    df.rename(columns={'fsid_placeholder': 'fsid', 'name_placeholder': 'name'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'name', 'city_fips', 'city_name', 'subtype', 'state_fips', 'state_name']]


def format_location_detail_city(data):
    """Reformat the list of data to Location Detail format for city

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('zcta') \
        .explode('neighborhood').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

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

    df.rename(columns={'fsid_placeholder': 'fsid', 'name_placeholder': 'name'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'name', 'lsad', 'zipCode', 'neighborhood_fips', 'neighborhood_name', 'state_fips', 'state_name']]


def format_location_detail_zcta(data):
    """Reformat the list of data to Location Detail format for zip

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

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

    df.rename(columns={'fsid_placeholder': 'fsid', 'name_placeholder': 'name'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'name', 'city_fips', 'city_fips', 'state_fips', 'state_name']]


def format_location_detail_tract(data):
    """Reformat the list of data to Location Detail format for tract

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df.rename(columns={'fsid': 'fsid_placeholder'}, inplace=True)

    if not df['county'].isna().values.all():
        df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
    else:
        df.drop(['county'], axis=1, inplace=True)
        df['county_fips'] = pd.NA
        df['county_name'] = pd.NA

    if not df['state'].isna().values.all():
        df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
    else:
        df.drop(['state'], axis=1, inplace=True)
        df['state_fips'] = pd.NA
        df['state_name'] = pd.NA

    df.rename(columns={'fsid_placeholder': 'fsid', 'name_placeholder': 'name'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'fips', 'county_fips', 'county_name', 'state_fips', 'state_name']]


def format_location_detail_county(data):
    """Reformat the list of data to Location Detail format for county

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('city').explode('zcta')\
        .explode('cd').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder'}, inplace=True)

    if not df['city'].isna().values.all():
        df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
    else:
        df.drop(['city'], axis=1, inplace=True)
        df['city_fips'] = pd.NA
        df['city_name'] = pd.NA

    if not df['zcta'].isna().values.all():
        df = pd.concat([df.drop(['zcta'], axis=1), df['zcta'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'zipCode', 'name': 'zcta_name'}, inplace=True)
    else:
        df.drop(['zcta'], axis=1, inplace=True)
        df['zipCode'] = pd.NA
        df['zcta_name'] = pd.NA

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

    df.rename(columns={'fsid_placeholder': 'fsid'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
    df['cd_fips'] = df['cd_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'city_fips', 'city_name', 'zipCode', 'fips', 'isCoastal', 'cd_fips',
               'cd_name', 'state_fips', 'state_name']]


def format_location_detail_cd(data):
    """Reformat the list of data to Location Detail format for congressional district

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('county')
    df.rename(columns={'fsid': 'fsid_placeholder'}, inplace=True)

    if not df['county'].isna().values.all():
        df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
    else:
        df.drop(['county'], axis=1, inplace=True)
        df['county_fips'] = pd.NA
        df['county_name'] = pd.NA

    if not df['state'].isna().values.all():
        df = pd.concat([df.drop(['state'], axis=1), df['state'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'state_fips', 'name': 'state_name'}, inplace=True)
    else:
        df.drop(['state'], axis=1, inplace=True)
        df['state_fips'] = pd.NA
        df['state_name'] = pd.NA

    df.rename(columns={'fsid_placeholder': 'fsid'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    return df[['fsid', 'district', 'county_fips', 'county_name', 'state_fips', 'state_name']]


def format_location_detail_state(data):
    """Reformat the list of data to Location Detail format for state

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df['fsid'] = df['fsid'].apply(str)
    return df[['fsid', 'name', 'fips']]


def format_location_summary_property(data):
    """Reformat the list of data to Location Summary format for property

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df['fsid'] = df['fsid'].apply(str)
    df['riskDirection'] = df['riskDirection'].astype('Int64').apply(str)
    df['environmentalRisk'] = df['environmentalRisk'].astype('Int64').apply(str)
    df['historic'] = df['historic'].astype('Int64').apply(str)
    df['adaptation'] = df['adaptation'].astype('Int64').apply(str)
    df['floodFactor'] = df['floodFactor'].astype('Int64').apply(str)
    return df[['fsid', 'floodFactor', 'riskDirection', 'environmentalRisk', 'historic', 'adaptation']]


def format_location_summary(data):
    """Reformat the list of data to Location Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])

    if not df['properties'].isna().values.all():
        df = pd.concat([df.drop(['properties'], axis=1), df['properties'].apply(pd.Series)], axis=1)
        df.rename(columns={'total': 'propertiesTotal', 'atRisk': 'propertiesAtRisk'}, inplace=True)
    else:
        df.drop(['properties'], axis=1, inplace=True)
        df['propertiesTotal'] = pd.NA
        df['propertiesAtRisk'] = pd.NA

    df['fsid'] = df['fsid'].apply(str)
    df['riskDirection'] = df['riskDirection'].astype('Int64').apply(str)
    df['environmentalRisk'] = df['environmentalRisk'].astype('Int64').apply(str)
    df['historic'] = df['historic'].astype('Int64').apply(str)
    df['adaptation'] = df['adaptation'].astype('Int64').apply(str)
    df['propertiesTotal'] = df['propertiesTotal'].astype('Int64').apply(str)
    df['propertiesAtRisk'] = df['propertiesAtRisk'].astype('Int64').apply(str)
    return df[['fsid', 'riskDirection', 'environmentalRisk', 'propertiesTotal', 'propertiesAtRisk', 'historic']]


def format_fema_nfip(data):
    """Reformat the list of data to Fema Nfip format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df['fsid'] = df['fsid'].apply(str)
    df['claimCount'] = df['claimCount'].astype('Int64').apply(str)
    df['policyCount'] = df['policyCount'].astype('Int64').apply(str)
    df['buildingPaid'] = df['buildingPaid'].astype('Int64').apply(str)
    df['contentPaid'] = df['contentPaid'].astype('Int64').apply(str)
    df['buildingCoverage'] = df['buildingCoverage'].astype('Int64').apply(str)
    df['contentCoverage'] = df['contentCoverage'].astype('Int64').apply(str)
    df['iccPaid'] = df['iccPaid'].astype('Int64').apply(str)
    return df[['fsid', 'claimCount', 'policyCount', 'buildingPaid', 'contentPaid', 'buildingCoverage',
               'contentCoverage', 'iccPaid']]