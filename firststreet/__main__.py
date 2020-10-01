# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import argparse
import ast
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
    parser.add_argument("-i", "--search_items", help="Example: 28,29", required=False,)
    parser.add_argument("-l", "--location", help="Example: property", required=False)
    parser.add_argument("-connection_limit", "--connection_limit", help="Example: 100", required=False, default="100")
    parser.add_argument("-rate_limit", "--rate_limit", help="Example: 5000", required=False, default="20000")
    parser.add_argument("-rate_period", "--rate_period", help="Example: 3600", required=False, default="1")
    parser.add_argument("-log", "--log", help="Example: False", required=False, default="True")
    parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False)
    parser.add_argument("-e", "--extra_param", required=False)
    parser.add_argument("-year", "--year", required=False)
    parser.add_argument("-return_period", "--return_period", required=False)
    parser.add_argument("-event_id", "--event_id", required=False)

    argument = parser.parse_args()

    # Merge search_item from file and list input
    search_items = []
    if argument.search_items:
        for search_item in argument.search_items.strip().split(";"):
            try:
                search_items.append(ast.literal_eval(search_item))
            except (SyntaxError, ValueError):
                search_items.append(search_item)

    if argument.file:
        search_items += read_search_items_from_file(argument.file)

    # Ensure there is at least a product and search item
    if search_items:

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

        limit = int(argument.connection_limit)
        rate_limit = int(argument.rate_limit)
        rate_period = int(argument.rate_period)

        fs = firststreet.FirstStreet(api_key, version=argument.version, connection_limit=limit,
                                     rate_limit=rate_limit, rate_period=rate_period,
                                     log=bool(strtobool(argument.log)))

        if argument.product == 'adaptation.get_detail':
            fs.adaptation.get_detail(search_items,
                                     csv=True,
                                     extra_param=argument.extra_param)

        elif argument.product == 'adaptation.get_summary':
            fs.adaptation.get_summary(search_items,
                                      argument.location,
                                      csv=True,
                                      extra_param=argument.extra_param)

        elif argument.product == 'adaptation.get_details_by_location':
            fs.adaptation.get_details_by_location(search_items,
                                                  argument.location,
                                                  csv=True,
                                                  extra_param=argument.extra_param)

        elif argument.product == 'probability.get_depth':
            fs.probability.get_depth(search_items,
                                     csv=True,
                                     extra_param=argument.extra_param)

        elif argument.product == 'probability.get_chance':
            fs.probability.get_chance(search_items,
                                      csv=True,
                                      extra_param=argument.extra_param)

        elif argument.product == 'probability.get_count_summary':
            fs.probability.get_count_summary(search_items,
                                             csv=True,
                                             extra_param=argument.extra_param)

        elif argument.product == 'probability.get_cumulative':
            fs.probability.get_cumulative(search_items,
                                          csv=True,
                                          extra_param=argument.extra_param)

        elif argument.product == 'probability.get_count':
            fs.probability.get_count(search_items,
                                     argument.location,
                                     csv=True,
                                     extra_param=argument.extra_param)

        elif argument.product == 'historic.get_event':
            fs.historic.get_event(search_items,
                                  csv=True,
                                  extra_param=argument.extra_param)

        elif argument.product == 'historic.get_summary':
            fs.historic.get_summary(search_items,
                                    argument.location,
                                    csv=True,
                                    extra_param=argument.extra_param)

        elif argument.product == 'historic.get_events_by_location':
            fs.historic.get_events_by_location(search_items,
                                               argument.location,
                                               csv=True,
                                               extra_param=argument.extra_param)

        elif argument.product == 'location.get_detail':
            fs.location.get_detail(search_items,
                                   argument.location,
                                   csv=True,
                                   extra_param=argument.extra_param)

        elif argument.product == 'location.get_summary':
            fs.location.get_summary(search_items,
                                    argument.location,
                                    csv=True,
                                    extra_param=argument.extra_param)

        elif argument.product == 'fema.get_nfip':
            fs.fema.get_nfip(search_items,
                             argument.location,
                             csv=True,
                             extra_param=argument.extra_param)

        elif argument.product == 'environmental.get_precipitation':
            fs.environmental.get_precipitation(search_items,
                                               csv=True,
                                               extra_param=argument.extra_param)

        elif argument.product == 'tile.get_probability_depth':
            fs.tile.get_probability_depth(year=int(argument.year), return_period=int(argument.return_period),
                                          coordinate=search_items,
                                          image=True)

        elif argument.product == 'tile.get_historic_event':
            fs.tile.get_historic_event(event_id=int(argument.event_id), coordinate=search_items,
                                       image=True)

            # AND FILES

        else:
            logging.error("Product not found. Please check that the argument"
                          " provided is correct: {}".format(argument.product))

    else:
        raise InvalidArgument("No search items were provided from either a search item list or a file. "
                              "List: '{}', File Name: '{}'".format(argument.search_items, argument.file))
