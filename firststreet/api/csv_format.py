# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import datetime
import logging
import os
import shapely.geometry

# External Imports
import pandas as pd


def to_csv(data, product, product_subtype, location_type=None, output_dir=None):
    """Receives a list of data, a product, a product subtype, and a location to create a CSV

    Args:
        data (list): A list of FSF object
        product (str): The overall product to call
        product_subtype (str): The product subtype (if suitable)
        location_type (str): The location lookup type (if suitable)
        output_dir (str): The output directory to save the generated csvs
    """

    date = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

    # Set file name to the current date, time, and product
    if location_type:
        file_name = "_".join([date, product, product_subtype, location_type]) + ".csv"
    else:
        file_name = "_".join([date, product, product_subtype]) + ".csv"

    if not output_dir:
        output_dir = os.getcwd() + "/output_data"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Format the data for each product
    if product == 'adaptation':

        if product_subtype == 'detail':
            df = format_adaptation_detail(data)

        elif product_subtype == 'summary':
            df = format_adaptation_summary(data)

        elif product_subtype == 'summary_detail':
            df = format_adaptation_summary_detail(data)

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

        elif product_subtype == 'summary_event':
            if location_type == 'property':
                df = format_historic_summary_event_property(data)

            else:
                df = format_historic_summary_event(data)

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

    elif product == 'economic_aal':

        if product_subtype == 'summary':

            if location_type == 'property':
                df = format_aal_summary_property(data)

            else:
                df = format_aal_summary(data)

        else:
            raise NotImplementedError

    elif product == 'economic_avm':

        if product_subtype == 'avm':

            df = format_avm(data)

        elif product_subtype == "provider":

            df = format_avm_provider(data)

        else:
            raise NotImplementedError

    else:
        raise NotImplementedError

    # Export CSVs
    if df['valid_id'].all():
        df = df.drop(columns=['valid_id'])
    else:
        df['valid_id'] = df['valid_id'].fillna(True)

    # Export CSVs
    if 'error' in df and df['error'].isnull().all():
        df = df.drop(columns=['error'])

    df = df.fillna(pd.NA).astype(str)
    df.to_csv(output_dir + '/' + file_name, index=False)
    logging.info("CSV generated to '{}'.".format(output_dir + '/' + file_name))


def get_geom_center(geom):

    if hasattr(geom, "center"):
        if isinstance(geom.center, shapely.geometry.MultiPolygon) and not geom.center.is_empty:
            return {"latitude": geom.center.centroid.y, "longitude": geom.center.centroid.x}

        elif isinstance(geom.center, shapely.geometry.Point):
            return {"latitude": geom.center.y, "longitude": geom.center.x}

        else:
            return {"latitude": pd.NA, "longitude": pd.NA}

    elif hasattr(geom, "y") and hasattr(geom, "x"):
        return {"latitude": geom.y, "longitude": geom.x}

    return {"latitude": None, "longitude": None}


def format_adaptation_detail(data):
    """Reformat the list of data to Adaptation Detail format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data]).explode('type').explode('scenario').reset_index(drop=True)
    df['adaptationId'] = df['adaptationId'].apply(str)
    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
    df['geometry'] = df['geometry'].apply(get_geom_center)
    if ("serving.property" not in df and "serving" in df and df["serving"].isnull().all()) or \
            ("serving.property" in df and df["serving.property"].isnull().all()):
        df["serving_property"] = pd.NA
        df["serving_neighborhood"] = pd.NA
        df["serving_zcta"] = pd.NA
        df["serving_tract"] = pd.NA
        df["serving_city"] = pd.NA
        df["serving_county"] = pd.NA
        df["serving_cd"] = pd.NA
        df["serving_state"] = pd.NA
    else:
        df = df.rename(columns={"serving.property": "serving_property",
                                "serving.neighborhood": "serving_neighborhood",
                                "serving.zcta": "serving_zcta",
                                "serving.tract": "serving_tract",
                                "serving.city": "serving_city",
                                "serving.county": "serving_county",
                                "serving.cd": "serving_cd",
                                "serving.state": "serving_state"})

    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)

    return df[['adaptationId', 'valid_id', 'name', 'type', 'scenario', 'conveyance', 'returnPeriod', 'serving_property',
               'serving_neighborhood', 'serving_zcta', 'serving_tract', 'serving_city', 'serving_county', 'serving_cd',
               'serving_state', 'latitude', 'longitude', 'error']]


def format_adaptation_summary(data):
    """Reformat the list of data to Adaptation Summary Detail format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data]).explode('adaptation').reset_index(drop=True)
    df['fsid'] = df['fsid'].apply(str)
    df['adaptation'] = df['adaptation'].astype('Int64').apply(str)

    if "properties" not in df or df.properties.isnull().all():
        df["properties"] = pd.NA

    return df[['fsid', 'valid_id', 'adaptation', 'properties', 'error']]


def format_adaptation_summary_detail(data):
    """Reformat the list of data to Adaptation Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    summary = format_adaptation_summary(data[0])
    detail = format_adaptation_detail(data[1])

    return pd.merge(summary, detail, left_on=['adaptation', 'valid_id'],
                    right_on=['adaptationId', 'valid_id'], how='left').drop('adaptationId', axis=1)\
        .rename(columns={"error_x": "error"}).drop('error_y', axis=1)


def format_probability_chance(data):
    """Reformat the list of data to Probability Chance format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    depth_list = list()

    # Loop through data
    for d in data:

        try:
            # Normalize data to get df
            row_df = pd.json_normalize(d.chance, record_path='data', meta=['year'])

            # Add FSID to row
            row_df['fsid'] = d.fsid
            row_df['valid_id'] = d.valid_id
            row_df['error'] = d.error

            # Add rows to df - return periods matched to depths across scenarios
            depth_list.append(row_df)

        except TypeError:
            row_df = pd.DataFrame([[str(d.fsid), d.valid_id, d.error]], columns=['fsid', 'valid_id', 'error'])
            row_df['year'] = pd.NA
            row_df['threshold'] = pd.NA
            row_df['data.low'] = pd.NA
            row_df['data.mid'] = pd.NA
            row_df['data.high'] = pd.NA
            depth_list.append(row_df)

    # Get into df
    df = pd.concat(depth_list, axis=0).reset_index(drop=True)
    df.rename(columns={'data.low': 'low', 'data.mid': 'mid', 'data.high': 'high'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['threshold'] = df['threshold'].astype('Int64').apply(str)
    if df['low'] is None:
        df['low'] = df['low'].round(3)
    if df['mid'] is None:
        df['mid'] = df['mid'].round(3)
    if df['high'] is None:
        df['high'] = df['high'].round(3)

    return df[['fsid', 'valid_id', 'year', 'threshold', 'low', 'mid', 'high', 'error']]


def format_probability_count(data):
    """Reformat the list of data to Probability Count format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    depth_list = list()

    # Loop through data
    for d in data:

        try:
            # Normalize data to get df
            row_df = pd.json_normalize(d.count, record_path=['data', 'data'], meta=['year', ['data', 'returnPeriod']])

            # Add FSID to row
            row_df['fsid'] = d.fsid
            row_df['valid_id'] = d.valid_id
            row_df['error'] = d.error

            # Add rows to df - return periods matched to depths across scenarios
            depth_list.append(row_df)

        except TypeError:
            row_df = pd.DataFrame([[str(d.fsid), d.valid_id, d.error]], columns=['fsid', 'valid_id', 'error'])
            row_df['year'] = pd.NA
            row_df['data.returnPeriod'] = pd.NA
            row_df['bin'] = pd.NA
            row_df['count.low'] = pd.NA
            row_df['count.mid'] = pd.NA
            row_df['count.high'] = pd.NA
            depth_list.append(row_df)

    # Get into df
    df = pd.concat(depth_list, axis=0).reset_index(drop=True)
    df.rename(columns={'count.low': 'low', 'count.mid': 'mid', 'count.high': 'high',
                       'data.returnPeriod': 'returnPeriod'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
    df['bin'] = df['bin'].astype('Int64').apply(str)
    df['low'] = df['low'].astype('Int64').apply(str)
    df['mid'] = df['mid'].astype('Int64').apply(str)
    df['high'] = df['high'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'year', 'returnPeriod', 'bin', 'low', 'mid', 'high', 'error']]


def format_probability_count_summary(data):
    """Reformat the list of data to Probability Count-Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    listed_data = [{'fsid': attr.fsid, 'valid_id': attr.valid_id, 'error': attr.error,
                    'location': [{'location': 'state', 'data': attr.state},
                                 {'location': 'city', 'data': attr.city},
                                 {'location': 'zcta', 'data': attr.zcta},
                                 {'location': 'neighborhood', 'data': attr.neighborhood},
                                 {'location': 'tract', 'data': attr.tract},
                                 {'location': 'county', 'data': attr.county},
                                 {'location': 'cd', 'data': attr.cd}]} for attr in data]

    depth_list = list()

    # Loop through data
    for d in listed_data:

        try:
            # Normalize data to get df
            row_df = pd.json_normalize(d["location"], ['data', 'count'],
                                       ['location', ['location', 'fsid'], ['location', 'name'],
                                        ['location', 'subtype']], errors='ignore')

            # Add FSID to row
            row_df['fsid'] = d["fsid"]
            row_df['valid_id'] = d["valid_id"]
            row_df['error'] = d["error"]

            depth_list.append(row_df)

        except TypeError:
            row_df = pd.DataFrame([[str(d["fsid"]), d["valid_id"], d["error"]]], columns=['fsid', 'valid_id', 'error'])
            row_df['location'] = pd.NA
            row_df['location.fsid'] = pd.NA
            row_df['location.name'] = pd.NA
            row_df['location.subtype'] = pd.NA
            row_df['year'] = pd.NA
            row_df['data.low'] = pd.NA
            row_df['data.mid'] = pd.NA
            row_df['data.high'] = pd.NA

            depth_list.append(row_df)

    # Get into df
    df = pd.concat(depth_list, axis=0).reset_index(drop=True)
    df.rename(
        columns={'location.fsid': 'location_fips', 'location.name': 'location_name', 'location.subtype': 'subtype',
                 'data.low': 'low', 'data.mid': 'mid', 'data.high': 'high'},
        inplace=True)
    if 'subtype' not in df:
        df['subtype'] = pd.NA
    df['fsid'] = df['fsid'].apply(str)
    df['location_fips'] = df['location_fips'].astype('Int64').apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['low'] = df['low'].astype('Int64').apply(str)
    df['mid'] = df['mid'].astype('Int64').apply(str)
    df['high'] = df['high'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'location', 'location_fips',
               'location_name', 'subtype', 'year', 'low', 'mid', 'high', 'error']]


def format_probability_cumulative(data):
    """Reformat the list of data to Probability Cumulative format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    depth_list = list()

    # Loop through data
    for d in data:

        try:
            # Normalize data to get df
            row_df = pd.json_normalize(d.cumulative, record_path='data', meta='year')

            # Add FSID to row
            row_df['fsid'] = d.fsid
            row_df['valid_id'] = d.valid_id
            row_df['error'] = d.error

            # Add rows to df - return periods matched to depths across scenarios
            depth_list.append(row_df)

        except TypeError:
            row_df = pd.DataFrame([[str(d.fsid), d.valid_id, d.error]], columns=['fsid', 'valid_id', 'error'])
            row_df['year'] = pd.NA
            row_df['threshold'] = pd.NA
            row_df['data.low'] = pd.NA
            row_df['data.mid'] = pd.NA
            row_df['data.high'] = pd.NA
            depth_list.append(row_df)

    # Get into df
    df = pd.concat(depth_list, axis=0).reset_index(drop=True)
    df.rename(columns={'data.low': 'low', 'data.mid': 'mid', 'data.high': 'high'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['threshold'] = df['threshold'].astype('Int64').apply(str)
    if df['low'] is None:
        df['low'] = df['low'].round(3)
    if df['mid'] is None:
        df['mid'] = df['mid'].round(3)
    if df['high'] is None:
        df['high'] = df['high'].round(3)

    return df[['fsid', 'valid_id', 'year', 'threshold', 'low', 'mid', 'high', 'error']]


def format_probability_depth(data):
    """Reformat the list of data to Probability Depth format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    depth_list = list()

    # Loop through data
    for d in data:

        try:
            # Normalize data to get df
            row_df = pd.json_normalize(d.depth, record_path='data', meta=['year'])

            # Add FSID to row
            row_df['fsid'] = d.fsid
            row_df['valid_id'] = d.valid_id
            row_df['error'] = d.error

            # Add rows to df - return periods matched to depths across scenarios
            depth_list.append(row_df)

        except TypeError:
            row_df = pd.DataFrame([[str(d.fsid), d.valid_id, d.error]], columns=['fsid', 'valid_id', 'error'])
            row_df['year'] = pd.NA
            row_df['returnPeriod'] = pd.NA
            row_df['data.low'] = pd.NA
            row_df['data.mid'] = pd.NA
            row_df['data.high'] = pd.NA
            depth_list.append(row_df)

    # Get into df
    df = pd.concat(depth_list, axis=0).reset_index(drop=True)
    df.rename(columns={'data.low': 'low', 'data.mid': 'mid', 'data.high': 'high'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
    df['low'] = df['low'].astype('Int64').apply(str)
    df['mid'] = df['mid'].astype('Int64').apply(str)
    df['high'] = df['high'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'year', 'returnPeriod', 'low', 'mid', 'high', 'error']]


def format_environmental_precipitation(data):
    """Reformat the list of data to Environmental Precipitation format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    #
    df = pd.DataFrame([vars(o) for o in data]).explode('projected').reset_index(drop=True)
    if not df['projected'].isna().values.all():
        df = pd.concat([df.drop(['projected'], axis=1), df['projected'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df['fsid'] = df['fsid'].apply(str)
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

    return df[['fsid', 'valid_id', 'year', 'low', 'mid', 'high', 'error']]


def format_historic_event(data):
    """Reformat the list of data to Historic Event format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    df = pd.DataFrame([vars(o) for o in data])
    if not df['properties'].isna().values.all():
        df = pd.concat([df.drop(['properties'], axis=1), df['properties'].apply(pd.Series)], axis=1)
        df.rename(columns={'total': 'propertiesTotal', 'affected': 'propertiesAffected'}, inplace=True)
    else:
        df.drop(['properties'], axis=1, inplace=True)
        df['propertiesTotal'] = pd.NA
        df['propertiesAffected'] = pd.NA

    df['eventId'] = df['eventId'].apply(str)
    df['month'] = df['month'].astype('Int64').apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['returnPeriod'] = df['returnPeriod'].astype('Int64').apply(str)
    df['propertiesTotal'] = df['propertiesTotal'].astype('Int64').apply(str)
    df['propertiesAffected'] = df['propertiesAffected'].astype('Int64').apply(str)
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)

    return df[['eventId', 'valid_id', 'name', 'month', 'year', 'returnPeriod', 'type', 'propertiesTotal',
               'propertiesAffected', 'latitude', 'longitude', 'error']]


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
    else:
        df.drop(['historic'], axis=1, inplace=True)
        df['eventId'] = pd.NA
        df['name'] = pd.NA
        df['type'] = pd.NA
        df['depth'] = pd.NA

    df['fsid'] = df['fsid'].apply(str)
    df['eventId'] = df['eventId'].astype('Int64').apply(str)
    df['depth'] = df['depth'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'eventId', 'name', 'type', 'depth', 'error']]


def format_historic_summary(data):
    """Reformat the list of data to Historic Summary format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data]).explode('historic').reset_index(drop=True)
    if not df['historic'].isna().values.all():
        df = pd.concat([df.drop(['historic'], axis=1), df['historic'].apply(pd.Series)], axis=1)
        df = df.explode('data').reset_index(drop=True)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['historic'], axis=1, inplace=True)
        df['eventId'] = pd.NA
        df['name'] = pd.NA
        df['type'] = pd.NA
        df['bin'] = pd.NA
        df['count'] = pd.NA

    df['fsid'] = df['fsid'].apply(str)
    df['eventId'] = df['eventId'].apply(str)
    df['type'] = df['type'].apply(str)
    df['bin'] = df['bin'].astype('Int64').apply(str)
    df['count'] = df['count'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'eventId', 'name', 'type', 'bin', 'count', 'error']]


def format_historic_summary_event_property(data):
    """Reformat the list of data to Historic Summary Event Property format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    summary = format_historic_summary_property(data[0])
    event = format_historic_event(data[1])

    return pd.merge(summary, event, on=['eventId', 'valid_id', 'name', 'type'], how='left')\
        .rename(columns={"error_x": "error"}).drop(['error_y'], axis=1)


def format_historic_summary_event(data):
    """Reformat the list of data to Historic Summary Event format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """

    summary = format_historic_summary(data[0])
    event = format_historic_event(data[1])

    return pd.merge(summary, event, on=['eventId', 'valid_id', 'name', 'type'], how='left')\
        .rename(columns={"error_x": "error"}).drop(['error_y'], axis=1)


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
    df['elevation'] = df['elevation'].apply(str)
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)

    return df[['fsid', 'valid_id', 'streetNumber', 'route', 'city_fips', 'city_name', 'zipCode', 'neighborhood_fips',
               'neighborhood_name', 'tract_fips', 'county_fips', 'county_name', 'cd_fips', 'cd_name',
               'state_fips', 'state_name', 'footprintId', 'elevation', 'fema', 'latitude', 'longitude', 'error']]


def format_location_detail_neighborhood(data):
    """Reformat the list of data to Location Detail format for neighborhood

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('city').explode('county').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

    if not df['city'].isna().values.all():
        df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
    else:
        df.drop(['city'], axis=1, inplace=True)
        df['city_fips'] = pd.NA
        df['city_name'] = pd.NA

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
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'name', 'city_fips', 'city_name', 'county_fips', 'county_name', 'subtype',
               'state_fips', 'state_name', 'latitude', 'longitude', 'error']]


def format_location_detail_city(data):
    """Reformat the list of data to Location Detail format for city

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('zcta').explode('county') \
        .explode('neighborhood').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

    if not df['zcta'].isna().values.all():
        df = pd.concat([df.drop(['zcta'], axis=1), df['zcta'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'zipCode', 'name': 'zcta_name'}, inplace=True)
    else:
        df.drop(['zcta'], axis=1, inplace=True)
        df['zipCode'] = pd.NA
        df['zcta_name'] = pd.NA

    if not df['county'].isna().values.all():
        df = pd.concat([df.drop(['county'], axis=1), df['county'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'county_fips', 'name': 'county_name'}, inplace=True)
    else:
        df.drop(['county'], axis=1, inplace=True)
        df['county_fips'] = pd.NA
        df['county_name'] = pd.NA

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
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['neighborhood_fips'] = df['neighborhood_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'name', 'lsad', 'zipCode', 'neighborhood_fips', 'neighborhood_name',
               'county_fips', 'county_name', 'state_fips', 'state_name', 'latitude', 'longitude', 'error']]


def format_location_detail_zcta(data):
    """Reformat the list of data to Location Detail format for zip

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('city').explode('county')
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

    if not df['city'].isna().values.all():
        df = pd.concat([df.drop(['city'], axis=1), df['city'].apply(pd.Series)], axis=1)
        df.rename(columns={'fsid': 'city_fips', 'name': 'city_name'}, inplace=True)
    else:
        df.drop(['city'], axis=1, inplace=True)
        df['city_fips'] = pd.NA
        df['city_name'] = pd.NA

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
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['county_fips'] = df['county_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'name', 'city_fips', 'city_name', 'county_fips', 'county_name', 'state_fips',
               'state_name', 'latitude', 'longitude', 'error']]


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
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'fips', 'county_fips', 'county_name', 'state_fips', 'state_name',
               'latitude', 'longitude', 'error']]


def format_location_detail_county(data):
    """Reformat the list of data to Location Detail format for county

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data]).explode('city').explode('zcta') \
        .explode('cd').reset_index(drop=True)
    df.rename(columns={'fsid': 'fsid_placeholder', 'name': 'name_placeholder'}, inplace=True)

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

    df.rename(columns={'fsid_placeholder': 'fsid', 'name_placeholder': 'name'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['city_fips'] = df['city_fips'].astype('Int64').apply(str)
    df['zipCode'] = df['zipCode'].astype('Int64').apply(str)
    df['cd_fips'] = df['cd_fips'].astype('Int64').apply(str)
    df['state_fips'] = df['state_fips'].astype('Int64').apply(str).apply(lambda x: x.zfill(2))
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'name', 'isCoastal', 'city_fips', 'city_name', 'zipCode', 'fips', 'cd_fips',
               'cd_name', 'state_fips', 'state_name', 'latitude', 'longitude', 'error']]


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
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'district', 'county_fips', 'county_name', 'state_fips', 'state_name',
               'latitude', 'longitude', 'error']]


def format_location_detail_state(data):
    """Reformat the list of data to Location Detail format for state

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.DataFrame([vars(o) for o in data])
    df['fsid'] = df['fsid'].apply(str)
    df['geometry'] = df['geometry'].apply(get_geom_center)
    df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(pd.Series)], axis=1)
    return df[['fsid', 'valid_id', 'name', 'fips', 'latitude', 'longitude', 'error']]


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
    return df[['fsid', 'valid_id', 'floodFactor', 'riskDirection', 'environmentalRisk', 'historic',
               'adaptation', 'error']]


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
    return df[['fsid', 'valid_id', 'riskDirection', 'environmentalRisk', 'propertiesTotal',
               'propertiesAtRisk', 'historic', 'error']]


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
    return df[['fsid', 'valid_id', 'claimCount', 'policyCount', 'buildingPaid', 'contentPaid', 'buildingCoverage',
               'contentCoverage', 'iccPaid', 'error']]


def format_aal_summary_property(data):
    """Reformat the list of data to Location Summary format for property

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data]).explode('annual_loss')
    df = df.explode('depth_loss')

    if not df[['annual_loss', 'depth_loss']].isna().values.all():
        df = pd.concat([df.drop(['annual_loss'], axis=1), df['annual_loss'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['depth_loss'], axis=1), df['depth_loss'].apply(pd.Series)], axis=1)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['annual_loss'], axis=1, inplace=True)
        df.drop(['depth_loss'], axis=1, inplace=True)
        df['depth'] = pd.NA
        df['data'] = pd.NA
        df['year'] = pd.NA
        df['low'] = pd.NA
        df['mid'] = pd.NA
        df['high'] = pd.NA

    df.rename(columns={'data': 'damage'}, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['low'] = df['low'].astype('Int64').apply(str)
    df['mid'] = df['mid'].astype('Int64').apply(str)
    df['high'] = df['high'].astype('Int64').apply(str)
    df['depth'] = df['depth'].astype('Int64').apply(str)
    df['damage'] = df['damage'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'depth', 'damage', 'year', 'low', 'mid', 'high', 'error']]


def format_aal_summary(data):
    """Reformat the list of data to AAL format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data]).explode('annual_loss')

    if not df[['annual_loss']].isna().values.all():
        df = pd.concat([df.drop(['annual_loss'], axis=1), df['annual_loss'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['totalLoss'], axis=1), df['totalLoss'].apply(pd.Series)], axis=1)
        df.rename(columns={'low': 'total_loss_low', 'mid': 'total_loss_mid', 'high': 'total_loss_high'}, inplace=True)
        df = pd.concat([df.drop(['count'], axis=1), df['count'].apply(pd.Series)], axis=1)
        df.rename(columns={'low': 'count_low', 'mid': 'count_mid', 'high': 'count_high'}, inplace=True)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df.drop(['annual_loss'], axis=1, inplace=True)
        df['year'] = pd.NA
        df['floodFactor'] = pd.NA
        df['total_loss_low'] = pd.NA
        df['total_loss_mid'] = pd.NA
        df['total_loss_high'] = pd.NA
        df['count_low'] = pd.NA
        df['count_mid'] = pd.NA
        df['count_high'] = pd.NA

    df.rename(columns={'floodFactor': 'floodFactor_gr2'}, inplace=True)
    df = df.sort_values(by=['fsid', 'floodFactor_gr2', 'year'])
    df['fsid'] = df['fsid'].apply(str)
    df['year'] = df['year'].astype('Int64').apply(str)
    df['floodFactor_gr2'] = df['floodFactor_gr2'].astype('Int64').apply(str)
    df['total_loss_low'] = df['total_loss_low'].astype('Int64').apply(str)
    df['total_loss_mid'] = df['total_loss_mid'].astype('Int64').apply(str)
    df['total_loss_high'] = df['total_loss_high'].astype('Int64').apply(str)
    df['count_low'] = df['count_low'].astype('Int64').apply(str)
    df['count_mid'] = df['count_mid'].astype('Int64').apply(str)
    df['count_high'] = df['count_high'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'year', 'total_loss_low', 'total_loss_mid', 'total_loss_high', 'count_low',
               'count_mid', 'count_high', 'floodFactor_gr2', 'error']]


def format_avm(data):
    """Reformat the list of data to AVM format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data])

    if 'avm.mid' in df:
        df.rename(columns={'avm.mid': 'avm_mid'}, inplace=True)
    else:
        df['fsid'] = df['fsid'].apply(str)
        df['avm_mid'] = pd.NA

    if 'avm' in df:
        df.drop(['avm'], axis=1, inplace=True)
    df['fsid'] = df['fsid'].apply(str)
    df['avm_mid'] = df['avm_mid'].astype('Int64').apply(str)
    df['provider_id'] = df['provider_id'].astype('Int64').apply(str)

    return df[['fsid', 'valid_id', 'avm_mid', "provider_id", 'error']]


def format_avm_provider(data):
    """Reformat the list of data to AVM Provider format

    Args:
        data (list): A list of FSF object
    Returns:
        A pandas formatted DataFrame
    """
    df = pd.json_normalize([vars(o) for o in data])

    df['provider_id'] = df['provider_id'].astype('Int64').apply(str)

    return df[['provider_id', 'valid_id', 'provider_name', "provider_logo", 'error']]
