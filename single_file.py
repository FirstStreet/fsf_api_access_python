from functools import reduce

import pandas as pd
import os
import firststreet
import time
import shapely.geometry
import datetime

api_key = os.getenv("FSF_API_KEY")
fs = firststreet.FirstStreet(api_key, rate_limit=20000, rate_period=60)


def format_rows(row):

    fsid = row["fsid"]
    street_number = row["streetNumber"]
    route = row["route"]
    city_fips = "NA"
    city_name = "NA"
    zip_code = row["zipCode"]
    neighborhood_fips = row["neighborhood"][0]["fsid"] if row["neighborhood"] else "NA"
    neighborhood_name = row["neighborhood"][0]["name"] if row["neighborhood"] else "NA"
    tract_fips = row["tract.fsid"]
    county_fips = row["county.fsid"]
    county_name = row["county.name"]
    cd_fips = row["cd.fsid"]
    cd_name = row["cd.name"]
    state_fips = row["state.fsid"]
    state_name = row["state.name"]
    footprint_id = row["footprintId"]
    elevation = row["elevation"]
    fema = row["fema"]
    latitude = row["geometry"].centroid.y if row["geometry"] else "NA"
    longitude = row["geometry"].centroid.x if row["geometry"] else "NA"
    if 'historic' in row and row["historic"]:

        historic_event1 = row["historic"][0]["name"]
        historic_depth1 = row["historic"][0]["depth"]

        if len(row["historic"]) > 1:
            historic_event2 = row["historic"][1]["name"]
            historic_depth2 = row["historic"][1]["name"]

        else:
            historic_event2 = "NA"
            historic_depth2 = "NA"

    else:
        historic_event1 = "NA"
        historic_event2 = "NA"
        historic_depth1 = "NA"
        historic_depth2 = "NA"
    flood_factor = row["floodFactor"]
    prop_avm = row["avm.mid"]
    structure_avm = ""

    nfip_premium_1 = "NA"
    nfip_premium_2 = "NA"
    if isinstance(row["data"], list):
        nfip_premium_1 = row["data"][0]["estimate"]
        nfip_premium_2 = row["data"][1]["estimate"]

    aal_2020 = "NA"
    aal_2050 = "NA"
    # Not a float, then we have a list
    if isinstance(row["annual_loss"], list):

        for aal in row["annual_loss"]:
            if aal["year"] == 2020:
                aal_2020 = aal["data"]["mid"]
            elif aal["year"] == 2050:
                aal_2050 = aal["data"]["mid"]

    rps = [2, 5, 10, 20, 50, 100, 250, 500]
    years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
    probability_depth = {}

    for year in years:
        for rp in rps:
            probability_depth["flood_depth_{:03d}_{}_low".format(rp, str(year)[2:4])] = "NA"
            probability_depth["flood_depth_{:03d}_{}_mid".format(rp, str(year)[2:4])] = "NA"
            probability_depth["flood_depth_{:03d}_{}_high".format(rp, str(year)[2:4])] = "NA"

    try:
        for year in row["depth"]:
            is_coastal = False
            year_year = year['year']

            for rp in year['data']:
                if rp["returnPeriod"] == 2:
                    is_coastal = True
                rp_rp = rp["returnPeriod"]
                low = rp["data"]["low"]
                mid = rp["data"]["mid"]
                high = rp["data"]["high"]

                probability_depth["flood_depth_{:03d}_{}_low".format(rp_rp, str(year_year)[2:4])] = low
                probability_depth["flood_depth_{:03d}_{}_mid".format(rp_rp, str(year_year)[2:4])] = mid
                probability_depth["flood_depth_{:03d}_{}_high".format(rp_rp, str(year_year)[2:4])] = high

            if not is_coastal:
                probability_depth["flood_depth_002_{}_low".format(str(year_year)[2:4])] = "NA"
                probability_depth["flood_depth_002_{}_mid".format(str(year_year)[2:4])] = "NA"
                probability_depth["flood_depth_002_{}_high".format(str(year_year)[2:4])] = "NA"
    except (TypeError, KeyError):
        pass

    thresholds = [0, 15, 30]
    years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
    probability_chance = {}

    for year in years:
        for threshold in thresholds:
            probability_chance["flood_chance_{}_{}_low".format(threshold, str(year)[2:4])] = "NA"
            probability_chance["flood_chance_{}_{}_mid".format(threshold, str(year)[2:4])] = "NA"
            probability_chance["flood_chance_{}_{}_high".format(threshold, str(year)[2:4])] = "NA"

    try:
        for year in row["chance"]:
            year_year = year['year']
            for threshold in year['data']:
                threshold_threshold = threshold["threshold"]
                low = threshold["data"]["low"]
                mid = threshold["data"]["mid"]
                high = threshold["data"]["high"]

                probability_chance["flood_chance_{}_{}_low".format(threshold_threshold, str(year_year)[2:4])] = low
                probability_chance["flood_chance_{}_{}_mid".format(threshold_threshold, str(year_year)[2:4])] = mid
                probability_chance["flood_chance_{}_{}_high".format(threshold_threshold, str(year_year)[2:4])] = high
    except (TypeError, KeyError):
        pass

    thresholds = [0, 15, 30]
    years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
    probability_cumulative = {}

    for year in years:
        for threshold in thresholds:
            probability_cumulative["flood_cumulative_{}_{}_low".format(threshold, str(year)[2:4])] = "NA"
            probability_cumulative["flood_cumulative_{}_{}_mid".format(threshold, str(year)[2:4])] = "NA"
            probability_cumulative["flood_cumulative_{}_{}_high".format(threshold, str(year)[2:4])] = "NA"

    try:
        for year in row["cumulative"]:
            year_year = year['year']
            for threshold in year['data']:
                threshold_threshold = threshold["threshold"]
                low = threshold["data"]["low"]
                mid = threshold["data"]["mid"]
                high = threshold["data"]["high"]

                probability_cumulative["flood_cumulative_{}_{}_low".format(threshold_threshold, str(year_year)[2:4])] = low
                probability_cumulative["flood_cumulative_{}_{}_mid".format(threshold_threshold, str(year_year)[2:4])] = mid
                probability_cumulative["flood_cumulative_{}_{}_high".format(threshold_threshold, str(year_year)[2:4])] = high
    except (TypeError, KeyError):
        pass

    return pd.Series([fsid, street_number, route, city_fips, city_name, zip_code, neighborhood_fips, neighborhood_name,
                      tract_fips, county_fips, county_name, cd_fips, cd_name, state_fips, state_name, footprint_id,
                      elevation, fema, latitude, longitude, historic_event1, historic_event2, historic_depth1,
                      historic_depth2, flood_factor, prop_avm, structure_avm, nfip_premium_1, nfip_premium_2, aal_2020, aal_2050,
                      probability_depth["flood_depth_002_20_low"], probability_depth["flood_depth_005_20_low"],
                      probability_depth["flood_depth_010_20_low"], probability_depth["flood_depth_020_20_low"],
                      probability_depth["flood_depth_050_20_low"], probability_depth["flood_depth_100_20_low"],
                      probability_depth["flood_depth_250_20_low"], probability_depth["flood_depth_500_20_low"],
                      probability_depth["flood_depth_002_25_low"], probability_depth["flood_depth_005_25_low"],
                      probability_depth["flood_depth_010_25_low"], probability_depth["flood_depth_020_25_low"],
                      probability_depth["flood_depth_050_25_low"], probability_depth["flood_depth_100_25_low"],
                      probability_depth["flood_depth_250_25_low"], probability_depth["flood_depth_500_25_low"],
                      probability_depth["flood_depth_002_30_low"], probability_depth["flood_depth_005_30_low"],
                      probability_depth["flood_depth_010_30_low"], probability_depth["flood_depth_020_30_low"],
                      probability_depth["flood_depth_050_30_low"], probability_depth["flood_depth_100_30_low"],
                      probability_depth["flood_depth_250_30_low"], probability_depth["flood_depth_500_30_low"],
                      probability_depth["flood_depth_002_35_low"], probability_depth["flood_depth_005_35_low"],
                      probability_depth["flood_depth_010_35_low"], probability_depth["flood_depth_020_35_low"],
                      probability_depth["flood_depth_050_35_low"], probability_depth["flood_depth_100_35_low"],
                      probability_depth["flood_depth_250_35_low"], probability_depth["flood_depth_500_35_low"],
                      probability_depth["flood_depth_002_40_low"], probability_depth["flood_depth_005_40_low"],
                      probability_depth["flood_depth_010_40_low"], probability_depth["flood_depth_020_40_low"],
                      probability_depth["flood_depth_050_40_low"], probability_depth["flood_depth_100_40_low"],
                      probability_depth["flood_depth_250_40_low"], probability_depth["flood_depth_500_40_low"],
                      probability_depth["flood_depth_002_45_low"], probability_depth["flood_depth_005_45_low"],
                      probability_depth["flood_depth_010_45_low"], probability_depth["flood_depth_020_45_low"],
                      probability_depth["flood_depth_050_45_low"], probability_depth["flood_depth_100_45_low"],
                      probability_depth["flood_depth_250_45_low"], probability_depth["flood_depth_500_45_low"],
                      probability_depth["flood_depth_002_50_low"], probability_depth["flood_depth_005_50_low"],
                      probability_depth["flood_depth_010_50_low"], probability_depth["flood_depth_020_50_low"],
                      probability_depth["flood_depth_050_50_low"], probability_depth["flood_depth_100_50_low"],
                      probability_depth["flood_depth_250_50_low"], probability_depth["flood_depth_500_50_low"],
                      probability_depth["flood_depth_002_20_mid"], probability_depth["flood_depth_005_20_mid"],
                      probability_depth["flood_depth_010_20_mid"], probability_depth["flood_depth_020_20_mid"],
                      probability_depth["flood_depth_050_20_mid"], probability_depth["flood_depth_100_20_mid"],
                      probability_depth["flood_depth_250_20_mid"], probability_depth["flood_depth_500_20_mid"],
                      probability_depth["flood_depth_002_25_mid"], probability_depth["flood_depth_005_25_mid"],
                      probability_depth["flood_depth_010_25_mid"], probability_depth["flood_depth_020_25_mid"],
                      probability_depth["flood_depth_050_25_mid"], probability_depth["flood_depth_100_25_mid"],
                      probability_depth["flood_depth_250_25_mid"], probability_depth["flood_depth_500_25_mid"],
                      probability_depth["flood_depth_002_30_mid"], probability_depth["flood_depth_005_30_mid"],
                      probability_depth["flood_depth_010_30_mid"], probability_depth["flood_depth_020_30_mid"],
                      probability_depth["flood_depth_050_30_mid"], probability_depth["flood_depth_100_30_mid"],
                      probability_depth["flood_depth_250_30_mid"], probability_depth["flood_depth_500_30_mid"],
                      probability_depth["flood_depth_002_35_mid"], probability_depth["flood_depth_005_35_mid"],
                      probability_depth["flood_depth_010_35_mid"], probability_depth["flood_depth_020_35_mid"],
                      probability_depth["flood_depth_050_35_mid"], probability_depth["flood_depth_100_35_mid"],
                      probability_depth["flood_depth_250_35_mid"], probability_depth["flood_depth_500_35_mid"],
                      probability_depth["flood_depth_002_40_mid"], probability_depth["flood_depth_005_40_mid"],
                      probability_depth["flood_depth_010_40_mid"], probability_depth["flood_depth_020_40_mid"],
                      probability_depth["flood_depth_050_40_mid"], probability_depth["flood_depth_100_40_mid"],
                      probability_depth["flood_depth_250_40_mid"], probability_depth["flood_depth_500_40_mid"],
                      probability_depth["flood_depth_002_45_mid"], probability_depth["flood_depth_005_45_mid"],
                      probability_depth["flood_depth_010_45_mid"], probability_depth["flood_depth_020_45_mid"],
                      probability_depth["flood_depth_050_45_mid"], probability_depth["flood_depth_100_45_mid"],
                      probability_depth["flood_depth_250_45_mid"], probability_depth["flood_depth_500_45_mid"],
                      probability_depth["flood_depth_002_50_mid"], probability_depth["flood_depth_005_50_mid"],
                      probability_depth["flood_depth_010_50_mid"], probability_depth["flood_depth_020_50_mid"],
                      probability_depth["flood_depth_050_50_mid"], probability_depth["flood_depth_100_50_mid"],
                      probability_depth["flood_depth_250_50_mid"], probability_depth["flood_depth_500_50_mid"],
                      probability_depth["flood_depth_002_20_high"], probability_depth["flood_depth_005_20_high"],
                      probability_depth["flood_depth_010_20_high"], probability_depth["flood_depth_020_20_high"],
                      probability_depth["flood_depth_050_20_high"], probability_depth["flood_depth_100_20_high"],
                      probability_depth["flood_depth_250_20_high"], probability_depth["flood_depth_500_20_high"],
                      probability_depth["flood_depth_002_25_high"], probability_depth["flood_depth_005_25_high"],
                      probability_depth["flood_depth_010_25_high"], probability_depth["flood_depth_020_25_high"],
                      probability_depth["flood_depth_050_25_high"], probability_depth["flood_depth_100_25_high"],
                      probability_depth["flood_depth_250_25_high"], probability_depth["flood_depth_500_25_high"],
                      probability_depth["flood_depth_002_30_high"], probability_depth["flood_depth_005_30_high"],
                      probability_depth["flood_depth_010_30_high"], probability_depth["flood_depth_020_30_high"],
                      probability_depth["flood_depth_050_30_high"], probability_depth["flood_depth_100_30_high"],
                      probability_depth["flood_depth_250_30_high"], probability_depth["flood_depth_500_30_high"],
                      probability_depth["flood_depth_002_35_high"], probability_depth["flood_depth_005_35_high"],
                      probability_depth["flood_depth_010_35_high"], probability_depth["flood_depth_020_35_high"],
                      probability_depth["flood_depth_050_35_high"], probability_depth["flood_depth_100_35_high"],
                      probability_depth["flood_depth_250_35_high"], probability_depth["flood_depth_500_35_high"],
                      probability_depth["flood_depth_002_40_high"], probability_depth["flood_depth_005_40_high"],
                      probability_depth["flood_depth_010_40_high"], probability_depth["flood_depth_020_40_high"],
                      probability_depth["flood_depth_050_40_high"], probability_depth["flood_depth_100_40_high"],
                      probability_depth["flood_depth_250_40_high"], probability_depth["flood_depth_500_40_high"],
                      probability_depth["flood_depth_002_45_high"], probability_depth["flood_depth_005_45_high"],
                      probability_depth["flood_depth_010_45_high"], probability_depth["flood_depth_020_45_high"],
                      probability_depth["flood_depth_050_45_high"], probability_depth["flood_depth_100_45_high"],
                      probability_depth["flood_depth_250_45_high"], probability_depth["flood_depth_500_45_high"],
                      probability_depth["flood_depth_002_50_high"], probability_depth["flood_depth_005_50_high"],
                      probability_depth["flood_depth_010_50_high"], probability_depth["flood_depth_020_50_high"],
                      probability_depth["flood_depth_050_50_high"], probability_depth["flood_depth_100_50_high"],
                      probability_depth["flood_depth_250_50_high"], probability_depth["flood_depth_500_50_high"],
                      probability_chance["flood_chance_0_20_low"], probability_chance["flood_chance_15_20_low"],
                      probability_chance["flood_chance_30_20_low"], probability_chance["flood_chance_0_25_low"],
                      probability_chance["flood_chance_15_25_low"], probability_chance["flood_chance_30_25_low"],
                      probability_chance["flood_chance_0_30_low"], probability_chance["flood_chance_15_30_low"],
                      probability_chance["flood_chance_30_30_low"], probability_chance["flood_chance_0_35_low"],
                      probability_chance["flood_chance_15_35_low"], probability_chance["flood_chance_30_35_low"],
                      probability_chance["flood_chance_0_40_low"], probability_chance["flood_chance_15_40_low"],
                      probability_chance["flood_chance_30_40_low"], probability_chance["flood_chance_0_45_low"],
                      probability_chance["flood_chance_15_45_low"], probability_chance["flood_chance_30_45_low"],
                      probability_chance["flood_chance_0_50_low"], probability_chance["flood_chance_15_50_low"],
                      probability_chance["flood_chance_30_50_low"], probability_chance["flood_chance_0_20_mid"],
                      probability_chance["flood_chance_15_20_mid"], probability_chance["flood_chance_30_20_mid"],
                      probability_chance["flood_chance_0_25_mid"], probability_chance["flood_chance_15_25_mid"],
                      probability_chance["flood_chance_30_25_mid"], probability_chance["flood_chance_0_30_mid"],
                      probability_chance["flood_chance_15_30_mid"], probability_chance["flood_chance_30_30_mid"],
                      probability_chance["flood_chance_0_35_mid"], probability_chance["flood_chance_15_35_mid"],
                      probability_chance["flood_chance_30_35_mid"], probability_chance["flood_chance_0_40_mid"],
                      probability_chance["flood_chance_15_40_mid"], probability_chance["flood_chance_30_40_mid"],
                      probability_chance["flood_chance_0_45_mid"], probability_chance["flood_chance_15_45_mid"],
                      probability_chance["flood_chance_30_45_mid"], probability_chance["flood_chance_0_50_mid"],
                      probability_chance["flood_chance_15_50_mid"], probability_chance["flood_chance_30_50_mid"],
                      probability_chance["flood_chance_0_20_high"], probability_chance["flood_chance_15_20_high"],
                      probability_chance["flood_chance_30_20_high"], probability_chance["flood_chance_0_25_high"],
                      probability_chance["flood_chance_15_25_high"], probability_chance["flood_chance_30_25_high"],
                      probability_chance["flood_chance_0_30_high"], probability_chance["flood_chance_15_30_high"],
                      probability_chance["flood_chance_30_30_high"], probability_chance["flood_chance_0_35_high"],
                      probability_chance["flood_chance_15_35_high"], probability_chance["flood_chance_30_35_high"],
                      probability_chance["flood_chance_0_40_high"], probability_chance["flood_chance_15_40_high"],
                      probability_chance["flood_chance_30_40_high"], probability_chance["flood_chance_0_45_high"],
                      probability_chance["flood_chance_15_45_high"], probability_chance["flood_chance_30_45_high"],
                      probability_chance["flood_chance_0_50_high"], probability_chance["flood_chance_15_50_high"],
                      probability_chance["flood_chance_30_50_high"],
                      probability_cumulative["flood_cumulative_0_20_low"],
                      probability_cumulative["flood_cumulative_15_20_low"],
                      probability_cumulative["flood_cumulative_30_20_low"],
                      probability_cumulative["flood_cumulative_0_25_low"],
                      probability_cumulative["flood_cumulative_15_25_low"],
                      probability_cumulative["flood_cumulative_30_25_low"],
                      probability_cumulative["flood_cumulative_0_30_low"],
                      probability_cumulative["flood_cumulative_15_30_low"],
                      probability_cumulative["flood_cumulative_30_30_low"],
                      probability_cumulative["flood_cumulative_0_35_low"],
                      probability_cumulative["flood_cumulative_15_35_low"],
                      probability_cumulative["flood_cumulative_30_35_low"],
                      probability_cumulative["flood_cumulative_0_40_low"],
                      probability_cumulative["flood_cumulative_15_40_low"],
                      probability_cumulative["flood_cumulative_30_40_low"],
                      probability_cumulative["flood_cumulative_0_45_low"],
                      probability_cumulative["flood_cumulative_15_45_low"],
                      probability_cumulative["flood_cumulative_30_45_low"],
                      probability_cumulative["flood_cumulative_0_50_low"],
                      probability_cumulative["flood_cumulative_15_50_low"],
                      probability_cumulative["flood_cumulative_30_50_low"],
                      probability_cumulative["flood_cumulative_0_20_mid"],
                      probability_cumulative["flood_cumulative_15_20_mid"],
                      probability_cumulative["flood_cumulative_30_20_mid"],
                      probability_cumulative["flood_cumulative_0_25_mid"],
                      probability_cumulative["flood_cumulative_15_25_mid"],
                      probability_cumulative["flood_cumulative_30_25_mid"],
                      probability_cumulative["flood_cumulative_0_30_mid"],
                      probability_cumulative["flood_cumulative_15_30_mid"],
                      probability_cumulative["flood_cumulative_30_30_mid"],
                      probability_cumulative["flood_cumulative_0_35_mid"],
                      probability_cumulative["flood_cumulative_15_35_mid"],
                      probability_cumulative["flood_cumulative_30_35_mid"],
                      probability_cumulative["flood_cumulative_0_40_mid"],
                      probability_cumulative["flood_cumulative_15_40_mid"],
                      probability_cumulative["flood_cumulative_30_40_mid"],
                      probability_cumulative["flood_cumulative_0_45_mid"],
                      probability_cumulative["flood_cumulative_15_45_mid"],
                      probability_cumulative["flood_cumulative_30_45_mid"],
                      probability_cumulative["flood_cumulative_0_50_mid"],
                      probability_cumulative["flood_cumulative_15_50_mid"],
                      probability_cumulative["flood_cumulative_30_50_mid"],
                      probability_cumulative["flood_cumulative_0_20_high"],
                      probability_cumulative["flood_cumulative_15_20_high"],
                      probability_cumulative["flood_cumulative_30_20_high"],
                      probability_cumulative["flood_cumulative_0_25_high"],
                      probability_cumulative["flood_cumulative_15_25_high"],
                      probability_cumulative["flood_cumulative_30_25_high"],
                      probability_cumulative["flood_cumulative_0_30_high"],
                      probability_cumulative["flood_cumulative_15_30_high"],
                      probability_cumulative["flood_cumulative_30_30_high"],
                      probability_cumulative["flood_cumulative_0_35_high"],
                      probability_cumulative["flood_cumulative_15_35_high"],
                      probability_cumulative["flood_cumulative_30_35_high"],
                      probability_cumulative["flood_cumulative_0_40_high"],
                      probability_cumulative["flood_cumulative_15_40_high"],
                      probability_cumulative["flood_cumulative_30_40_high"],
                      probability_cumulative["flood_cumulative_0_45_high"],
                      probability_cumulative["flood_cumulative_15_45_high"],
                      probability_cumulative["flood_cumulative_30_45_high"],
                      probability_cumulative["flood_cumulative_0_50_high"],
                      probability_cumulative["flood_cumulative_15_50_high"],
                      probability_cumulative["flood_cumulative_30_50_high"]
                      ])


def get_all_products(file):
    print("Start {}".format(file))
    # addresses = [line.strip() for line in f]

    loc_det = fs.location.get_detail(file, "property")
    loc_det_df = pd.json_normalize([vars(o) for o in loc_det])
    if "zcta.fsid" in loc_det_df and "zcta.name" in loc_det_df:
        loc_det_df = loc_det_df.drop(["zcta.fsid", "zcta.name"], axis=1)
    # time.sleep(30)

    loc_sum = fs.location.get_summary(file, "property")
    loc_sum_df = pd.json_normalize([vars(o) for o in loc_sum])
    loc_sum_df = loc_sum_df.drop(["riskDirection", "environmentalRisk", "historic", "adaptation"], axis=1)
    # time.sleep(30)

    his_sum = fs.historic.get_events_by_location(file, "property")
    his_sum_df = pd.json_normalize([vars(o) for o in his_sum[0]])
    # time.sleep(30)

    prob_depth = fs.probability.get_depth(file)
    prob_depth_df = pd.json_normalize([vars(o) for o in prob_depth])
    # time.sleep(30)

    prob_chance = fs.probability.get_chance(file)
    prob_chance_df = pd.json_normalize([vars(o) for o in prob_chance])
    # time.sleep(30)

    prob_cumu = fs.probability.get_cumulative(file)
    prob_cumu_df = pd.json_normalize([vars(o) for o in prob_cumu])
    # time.sleep(30)

    avm_avm = fs.avm.get_avm(file)
    avm_avm_df = pd.json_normalize([vars(o) for o in avm_avm])
    # time.sleep(30)

    aal_summary = fs.aal.get_summary(file, "property")
    aal_summary_df = pd.json_normalize([vars(o) for o in aal_summary])
    # time.sleep(30)

    aal_nfip = fs.economic.get_property_nfip(file)
    aal_nfip_df = pd.json_normalize([vars(o) for o in aal_nfip])

    dataframes = [loc_det_df, loc_sum_df, his_sum_df, prob_depth_df, prob_chance_df, prob_cumu_df,
                  avm_avm_df, aal_summary_df, aal_nfip_df]

    # Merge all the dataframes
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['fsid', 'valid_id'], how='left'), dataframes)
    df_merged = df_merged.apply(lambda row: format_rows(row), axis=1)

    col_names = ["fsid", "streetNumber", "route", "city_fips", "city_name", "zipCode", "neighborhood_fips",
                 "neighborhood_name", "tract_fips", "county_fips", "county_name", "cd_fips", "cd_name", "state_fips",
                 "state_name", "footprintId", "elevation", "fema", "latitude", "longitude", "historic_event1",
                 "historic_event2", "historic_depth1", "historic_depth2", "floodFactor Risk Score",
                 "Prop AVM", "Structure AVM", "NFIP Premium Estimate 1", "NFIP Premium Estimate 2", "AAL 2020", "AAL 2050", "flood_depth_002_20_low",
                 "flood_depth_005_20_low", "flood_depth_010_20_low", "flood_depth_020_20_low", "flood_depth_050_20_low",
                 "flood_depth_100_20_low", "flood_depth_250_20_low", "flood_depth_500_20_low", "flood_depth_002_25_low",
                 "flood_depth_005_25_low", "flood_depth_010_25_low", "flood_depth_020_25_low", "flood_depth_050_25_low",
                 "flood_depth_100_25_low", "flood_depth_250_25_low", "flood_depth_500_25_low", "flood_depth_002_30_low",
                 "flood_depth_005_30_low", "flood_depth_010_30_low", "flood_depth_020_30_low", "flood_depth_050_30_low",
                 "flood_depth_100_30_low", "flood_depth_250_30_low", "flood_depth_500_30_low", "flood_depth_002_35_low",
                 "flood_depth_005_35_low", "flood_depth_010_35_low", "flood_depth_020_35_low", "flood_depth_050_35_low",
                 "flood_depth_100_35_low", "flood_depth_250_35_low", "flood_depth_500_35_low", "flood_depth_002_40_low",
                 "flood_depth_005_40_low", "flood_depth_010_40_low", "flood_depth_020_40_low", "flood_depth_050_40_low",
                 "flood_depth_100_40_low", "flood_depth_250_40_low", "flood_depth_500_40_low", "flood_depth_002_45_low",
                 "flood_depth_005_45_low", "flood_depth_010_45_low", "flood_depth_020_45_low", "flood_depth_050_45_low",
                 "flood_depth_100_45_low", "flood_depth_250_45_low", "flood_depth_500_45_low", "flood_depth_002_50_low",
                 "flood_depth_005_50_low", "flood_depth_010_50_low", "flood_depth_020_50_low", "flood_depth_050_50_low",
                 "flood_depth_100_50_low", "flood_depth_250_50_low", "flood_depth_500_50_low", "flood_depth_002_20_mid",
                 "flood_depth_005_20_mid", "flood_depth_010_20_mid", "flood_depth_020_20_mid", "flood_depth_050_20_mid",
                 "flood_depth_100_20_mid", "flood_depth_250_20_mid", "flood_depth_500_20_mid", "flood_depth_002_25_mid",
                 "flood_depth_005_25_mid", "flood_depth_010_25_mid", "flood_depth_020_25_mid", "flood_depth_050_25_mid",
                 "flood_depth_100_25_mid", "flood_depth_250_25_mid", "flood_depth_500_25_mid", "flood_depth_002_30_mid",
                 "flood_depth_005_30_mid", "flood_depth_010_30_mid", "flood_depth_020_30_mid", "flood_depth_050_30_mid",
                 "flood_depth_100_30_mid", "flood_depth_250_30_mid", "flood_depth_500_30_mid", "flood_depth_002_35_mid",
                 "flood_depth_005_35_mid", "flood_depth_010_35_mid", "flood_depth_020_35_mid", "flood_depth_050_35_mid",
                 "flood_depth_100_35_mid", "flood_depth_250_35_mid", "flood_depth_500_35_mid", "flood_depth_002_40_mid",
                 "flood_depth_005_40_mid", "flood_depth_010_40_mid", "flood_depth_020_40_mid", "flood_depth_050_40_mid",
                 "flood_depth_100_40_mid", "flood_depth_250_40_mid", "flood_depth_500_40_mid", "flood_depth_002_45_mid",
                 "flood_depth_005_45_mid", "flood_depth_010_45_mid", "flood_depth_020_45_mid", "flood_depth_050_45_mid",
                 "flood_depth_100_45_mid", "flood_depth_250_45_mid", "flood_depth_500_45_mid", "flood_depth_002_50_mid",
                 "flood_depth_005_50_mid", "flood_depth_010_50_mid", "flood_depth_020_50_mid", "flood_depth_050_50_mid",
                 "flood_depth_100_50_mid", "flood_depth_250_50_mid", "flood_depth_500_50_mid",
                 "flood_depth_002_20_high", "flood_depth_005_20_high", "flood_depth_010_20_high",
                 "flood_depth_020_20_high", "flood_depth_050_20_high", "flood_depth_100_20_high",
                 "flood_depth_250_20_high", "flood_depth_500_20_high", "flood_depth_002_25_high",
                 "flood_depth_005_25_high", "flood_depth_010_25_high", "flood_depth_020_25_high",
                 "flood_depth_050_25_high", "flood_depth_100_25_high", "flood_depth_250_25_high",
                 "flood_depth_500_25_high", "flood_depth_002_30_high", "flood_depth_005_30_high",
                 "flood_depth_010_30_high", "flood_depth_020_30_high", "flood_depth_050_30_high",
                 "flood_depth_100_30_high", "flood_depth_250_30_high", "flood_depth_500_30_high",
                 "flood_depth_002_35_high", "flood_depth_005_35_high", "flood_depth_010_35_high",
                 "flood_depth_020_35_high", "flood_depth_050_35_high", "flood_depth_100_35_high",
                 "flood_depth_250_35_high", "flood_depth_500_35_high", "flood_depth_002_40_high",
                 "flood_depth_005_40_high", "flood_depth_010_40_high", "flood_depth_020_40_high",
                 "flood_depth_050_40_high", "flood_depth_100_40_high", "flood_depth_250_40_high",
                 "flood_depth_500_40_high", "flood_depth_002_45_high", "flood_depth_005_45_high",
                 "flood_depth_010_45_high", "flood_depth_020_45_high", "flood_depth_050_45_high",
                 "flood_depth_100_45_high", "flood_depth_250_45_high", "flood_depth_500_45_high",
                 "flood_depth_002_50_high", "flood_depth_005_50_high", "flood_depth_010_50_high",
                 "flood_depth_020_50_high", "flood_depth_050_50_high", "flood_depth_100_50_high",
                 "flood_depth_250_50_high", "flood_depth_500_50_high", "flood_chance_0_20_low",
                 "flood_chance_15_20_low", "flood_chance_30_20_low", "flood_chance_0_25_low", "flood_chance_15_25_low",
                 "flood_chance_30_25_low", "flood_chance_0_30_low", "flood_chance_15_30_low", "flood_chance_30_30_low",
                 "flood_chance_0_35_low", "flood_chance_15_35_low", "flood_chance_30_35_low", "flood_chance_0_40_low",
                 "flood_chance_15_40_low", "flood_chance_30_40_low", "flood_chance_0_45_low", "flood_chance_15_45_low",
                 "flood_chance_30_45_low", "flood_chance_0_50_low", "flood_chance_15_50_low", "flood_chance_30_50_low",
                 "flood_chance_0_20_mid", "flood_chance_15_20_mid", "flood_chance_30_20_mid", "flood_chance_0_25_mid",
                 "flood_chance_15_25_mid", "flood_chance_30_25_mid", "flood_chance_0_30_mid", "flood_chance_15_30_mid",
                 "flood_chance_30_30_mid", "flood_chance_0_35_mid", "flood_chance_15_35_mid", "flood_chance_30_35_mid",
                 "flood_chance_0_40_mid", "flood_chance_15_40_mid", "flood_chance_30_40_mid", "flood_chance_0_45_mid",
                 "flood_chance_15_45_mid", "flood_chance_30_45_mid", "flood_chance_0_50_mid", "flood_chance_15_50_mid",
                 "flood_chance_30_50_mid", "flood_chance_0_20_high", "flood_chance_15_20_high",
                 "flood_chance_30_20_high", "flood_chance_0_25_high", "flood_chance_15_25_high",
                 "flood_chance_30_25_high", "flood_chance_0_30_high", "flood_chance_15_30_high",
                 "flood_chance_30_30_high", "flood_chance_0_35_high", "flood_chance_15_35_high",
                 "flood_chance_30_35_high", "flood_chance_0_40_high", "flood_chance_15_40_high",
                 "flood_chance_30_40_high", "flood_chance_0_45_high", "flood_chance_15_45_high",
                 "flood_chance_30_45_high", "flood_chance_0_50_high", "flood_chance_15_50_high",
                 "flood_chance_30_50_high", "flood_cumulative_0_20_low", "flood_cumulative_15_20_low",
                 "flood_cumulative_30_20_low", "flood_cumulative_0_25_low", "flood_cumulative_15_25_low",
                 "flood_cumulative_30_25_low", "flood_cumulative_0_30_low", "flood_cumulative_15_30_low",
                 "flood_cumulative_30_30_low", "flood_cumulative_0_35_low", "flood_cumulative_15_35_low",
                 "flood_cumulative_30_35_low", "flood_cumulative_0_40_low", "flood_cumulative_15_40_low",
                 "flood_cumulative_30_40_low", "flood_cumulative_0_45_low", "flood_cumulative_15_45_low",
                 "flood_cumulative_30_45_low", "flood_cumulative_0_50_low", "flood_cumulative_15_50_low",
                 "flood_cumulative_30_50_low", "flood_cumulative_0_20_mid", "flood_cumulative_15_20_mid",
                 "flood_cumulative_30_20_mid", "flood_cumulative_0_25_mid", "flood_cumulative_15_25_mid",
                 "flood_cumulative_30_25_mid", "flood_cumulative_0_30_mid", "flood_cumulative_15_30_mid",
                 "flood_cumulative_30_30_mid", "flood_cumulative_0_35_mid", "flood_cumulative_15_35_mid",
                 "flood_cumulative_30_35_mid", "flood_cumulative_0_40_mid", "flood_cumulative_15_40_mid",
                 "flood_cumulative_30_40_mid", "flood_cumulative_0_45_mid", "flood_cumulative_15_45_mid",
                 "flood_cumulative_30_45_mid", "flood_cumulative_0_50_mid", "flood_cumulative_15_50_mid",
                 "flood_cumulative_30_50_mid", "flood_cumulative_0_20_high", "flood_cumulative_15_20_high",
                 "flood_cumulative_30_20_high", "flood_cumulative_0_25_high", "flood_cumulative_15_25_high",
                 "flood_cumulative_30_25_high", "flood_cumulative_0_30_high", "flood_cumulative_15_30_high",
                 "flood_cumulative_30_30_high", "flood_cumulative_0_35_high", "flood_cumulative_15_35_high",
                 "flood_cumulative_30_35_high", "flood_cumulative_0_40_high", "flood_cumulative_15_40_high",
                 "flood_cumulative_30_40_high", "flood_cumulative_0_45_high", "flood_cumulative_15_45_high",
                 "flood_cumulative_30_45_high", "flood_cumulative_0_50_high", "flood_cumulative_15_50_high",
                 "flood_cumulative_30_50_high"]
    df_merged.columns = col_names

    # name = file.rsplit('.', 1)[0]
    # start_dir = name.split("\\")[0]
    # ending = name.split("\\")[1]
    # ending = ending.split("_")[-1]
    # final_name = "{}\\export_for_NY_36111_{}.csv".format(start_dir, ending)
    # df_merged.to_csv(final_name, index=False)
    # print("Done {}".format(file))
    df_merged.to_csv("{}_out.csv".format(file.rsplit('.', 1)[0]), index=False)


# import glob
#
# working_list = glob.glob('data_pull/FSIDs_for_CA_066000_*.csv')
# for lst in working_list:
#     get_all_products(lst)

get_all_products('test_coords.csv')
