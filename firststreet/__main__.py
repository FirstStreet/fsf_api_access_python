# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import argparse
import os
import logging
from distutils.util import strtobool
import sys

# Internal Imports
import firststreet
from firststreet.errors import InvalidArgument
from firststreet.util import read_search_items_from_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description for my parser")
    parser.add_argument("-p", "--product", help="Example: adaptation_detail", required=True)
    parser.add_argument("-api_key", "--api_key", required=False)
    parser.add_argument("-v", "--version", required=False)
    parser.add_argument("-i", "--fsids", help="Example: 28,29", required=False,)
    parser.add_argument("-l", "--location", help="Example: property", required=False)
    parser.add_argument("-limit", "--limit", help="Example: 100", required=False, default="100")
    parser.add_argument("-log", "--log", help="Example: False", required=False, default="True")
    parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False)

    argument = parser.parse_args()

    # Merge FSIDs from file and list input
    fsids = []
    if argument.fsids:
        try:
            fsids += list(map(int, argument.fsids.strip().split(",")))
        except ValueError:
            logging.warning("An invalid fsid list was provided. Please check this input list is a comma-separated " 
                            "list of integers: '{}'".format(argument.fsids))

    if argument.file:
        fsids += read_search_items_from_file(argument.file)

    # Ensure there is at least a product and FSID
    if fsids:

        # Try to get the API key either from env var or the parameter
        if not argument.api_key:
            env_var_name = 'FSF_API_KEY'
            try:
                api_key = os.environ[env_var_name]
            except KeyError:
                logging.error("`{}` is not set as an Environmental Variable".format(env_var_name))
                sys.exit()
        else:
            api_key = argument.api_key

        fs = firststreet.FirstStreet(api_key, version=argument.version, log=bool(strtobool(argument.log)))

        limit = int(argument.limit)

        if argument.product == 'adaptation.get_detail':
            fs.adaptation.get_detail(fsids, csv=True, limit=limit)

        elif argument.product == 'adaptation.get_summary':
            fs.adaptation.get_summary(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'adaptation.get_details_by_location':
            fs.adaptation.get_details_by_location(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'probability.get_depth':
            fs.probability.get_depth(fsids, csv=True, limit=limit)

        elif argument.product == 'probability.get_chance':
            fs.probability.get_chance(fsids, csv=True, limit=limit)

        elif argument.product == 'probability.get_count_summary':
            fs.probability.get_count_summary(fsids, csv=True, limit=limit)

        elif argument.product == 'probability.get_cumulative':
            fs.probability.get_cumulative(fsids, csv=True, limit=limit)

        elif argument.product == 'probability.get_count':
            fs.probability.get_count(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'historic.get_event':
            fs.historic.get_event(fsids, csv=True, limit=limit)

        elif argument.product == 'historic.get_summary':
            fs.historic.get_summary(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'historic.get_events_by_location':
            fs.historic.get_events_by_location(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'location.get_detail':
            fs.location.get_detail(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'location.get_summary':
            fs.location.get_summary(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'fema.get_nfip':
            fs.fema.get_nfip(fsids, argument.location, csv=True, limit=limit)

        elif argument.product == 'environmental.get_precipitation':
            fs.environmental.get_precipitation(fsids, csv=True, limit=limit)

        else:
            logging.error("Product not found. Please check that the argument"
                          " provided is correct: {}".format(argument.product))

    else:
        raise InvalidArgument("No fsids were provided from either a fsid list or a file. "
                              "List: '{}', File Name: '{}'".format(argument.fsids, argument.file))
