# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import argparse
import os
import logging

# Internal Imports
import sys

import firststreet
from firststreet import MissingAPIKeyError
from firststreet.util import read_fsid_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description for my parser")
    parser.add_argument("-a", "--api_key", required=False, default="")
    parser.add_argument("-p", "--product", help="Example: adaptation_detail", required=True, default="")
    parser.add_argument("-i", "--fsids", help="Example: 28,29", required=False, default="")
    parser.add_argument("-l", "--location", help="Example: property", required=False, default="")
    parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False, default="")

    argument = parser.parse_args()

    fsids = []
    if argument.fsids:
        fsids += list(map(int, argument.fsids.strip().split(",")))

    if argument.file:
        fsids += read_fsid_file(argument.file)

    if argument.product and fsids:

        if not argument.api_key:
            env_var_name = 'FSF_APfI_KEY'
            try:
                api_key = os.environ[env_var_name]
            except KeyError:
                logging.error("`{}` is not set as an Environmental Variable".format(env_var_name))
                sys.exit()
        else:
            api_key = argument.api_key

        fs = firststreet.FirstStreet(api_key)

        if argument.product == 'adaptation.get_detail':
            fs.adaptation.get_detail(fsids, csv=True)

        elif argument.product == 'adaptation.get_summary':
            fs.adaptation.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'probability.get_depth':
            fs.probability.get_depth(fsids, csv=True)

        elif argument.product == 'probability.get_chance':
            fs.probability.get_chance(fsids, csv=True)

        elif argument.product == 'probability.get_count_summary':
            fs.probability.get_count_summary(fsids, csv=True)

        elif argument.product == 'probability.get_cumulative':
            fs.probability.get_cumulative(fsids, csv=True)

        elif argument.product == 'probability.get_count':
            fs.probability.get_count(fsids, argument.location, csv=True)

        elif argument.product == 'historic.get_event':
            fs.historic.get_event(fsids, csv=True)

        elif argument.product == 'historic.get_summary':
            fs.historic.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'location.get_detail':
            fs.location.get_detail(fsids, argument.location, csv=True)

        elif argument.product == 'location.get_summary':
            fs.location.get_summary(fsids, argument.location, csv=True)

        elif argument.product == 'fema.get_nfip':
            fs.fema.get_nfip(fsids, argument.location, csv=True)

        elif argument.product == 'environmental.get_precipitation':
            fs.environmental.get_precipitation(fsids, csv=True)

        else:
            logging.error("Product not found. Please check that the argument"
                          " provided is correct: {}".format(argument.product))
