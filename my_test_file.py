import os
import firststreet
import time
import pandas as pd

api_key = os.getenv("FSF_API_KEY")
fs = firststreet.FirstStreet(api_key, connection_limit=100, rate_period=60, rate_limit=10000)


def get_all_products(file):
    loc_det = fs.location.get_detail(file, "property", csv=True)
    # # time.sleep(360)
    # loc_sum = fs.location.get_summary(file, "property", csv=True)
    # # # # time.sleep(360)
    # prob_depth = fs.probability.get_depth(file, csv=True)
    # # # time.sleep(360)
    # prob_chance = fs.probability.get_chance(file, csv=True)
    # # # time.sleep(360)
    # prob_cumu = fs.probability.get_cumulative(file, csv=True)
    # # time.sleep(360)
    # prob_count_sum = fs.probability.get_count_summary(file, csv=True)
    # # time.sleep(360)
    # ada_sum = fs.adaptation.get_detail_by_location(file, "property", csv=True)
    # # time.sleep(360)
    # his_sum = fs.historic.get_events_by_location(file, location_type="property", csv=True)
    # # time.sleep(360)
    # fs.avm.get_avm(file, csv=True)
    # # time.sleep(360)
    # fs.aal.get_summary(file, location_type="property", csv=True)
    # # time.sleep(360)
    # fs.economic.get_property_nfip(file, csv=True)
    # # print()

get_all_products("test_coords.csv")

# fs_aal = fs.aal.get_summary(
#     search_items="citi_lats.csv",
#     csv=True,
#     location_type="property",
#     output_dir="output_data/"
# )