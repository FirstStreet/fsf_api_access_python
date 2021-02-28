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
    # Convert log default to an actual boolean
    parser.add_argument("-log", "--log", help="Example: False", required=False, default="True")
    parser.add_argument("-connection_limit", "--connection_limit", help="Example: 100", required=False, default="100")
    parser.add_argument("-rate_limit", "--rate_limit", help="Example: 5000", required=False, default="20000")
    parser.add_argument("-rate_period", "--rate_period", help="Example: 3600", required=False, default="1")
    parser.add_argument("-o", "--output_dir", help="Example: /output", required=False)
    parser.add_argument("-s", "--search_items", help="Example: 28,29", required=False,)
    parser.add_argument("-l", "--location_type", help="Example: property", required=False)
    parser.add_argument("-y", "--year", required=False)
    parser.add_argument("-rp", "--return_period", required=False)
    parser.add_argument("-eid", "--event_id", required=False)
    # deprecated file parameter. Will be removed in a later version
    parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False)
    # deprecated extra_param parameter. Will be removed in a later version
    parser.add_argument("-e", "--extra_param", required=False)

    argument = parser.parse_args()

    # Reads a file or converts search items into a list
    search_items = []
    if argument.search_items:

        # If file, read addresses from file
        if os.path.isfile(argument.search_items):
            search_items = read_search_items_from_file(argument.search_items)
        else:
            for search_item in argument.search_items.strip().split(";"):
                try:
                    search_items.append(ast.literal_eval(search_item))
                except (SyntaxError, ValueError):
                    search_items.append(search_item)

    if argument.file:
        logging.warning("'file' argument deprecated and will be removed. Use `-s path_to_file` instead. "
                        "Ex: `-s testing/sample.txt`")
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

        formatted_params = {}

        if argument.extra_param:
            for element in argument.extra_param.split(";"):
                key, value = element.split(":")
                formatted_params[key] = ast.literal_eval(value)

        fs = firststreet.FirstStreet(api_key,
                                     version=argument.version,
                                     connection_limit=limit,
                                     rate_limit=rate_limit,
                                     rate_period=rate_period,
                                     log=bool(strtobool(argument.log)))

        if argument.product == 'adaptation.get_detail':
            fs.adaptation.get_detail(search_items,
                                     csv=True,
                                     output_dir=argument.output_dir,
                                     extra_param=formatted_params)

        elif argument.product == 'adaptation.get_summary':
            fs.adaptation.get_summary(search_items,
                                      argument.location_type,
                                      csv=True,
                                      output_dir=argument.output_dir,
                                      extra_param=formatted_params)

        elif argument.product == 'adaptation.get_detail_by_location':
            fs.adaptation.get_detail_by_location(search_items,
                                                 argument.location_type,
                                                 csv=True,
                                                 output_dir=argument.output_dir,
                                                 extra_param=formatted_params)

        elif argument.product == 'probability.get_depth':
            fs.probability.get_depth(search_items,
                                     csv=True,
                                     output_dir=argument.output_dir,
                                     extra_param=formatted_params)

        elif argument.product == 'probability.get_chance':
            fs.probability.get_chance(search_items,
                                      csv=True,
                                      output_dir=argument.output_dir,
                                      extra_param=formatted_params)

        elif argument.product == 'probability.get_count_summary':
            fs.probability.get_count_summary(search_items,
                                             csv=True,
                                             output_dir=argument.output_dir,
                                             extra_param=formatted_params)

        elif argument.product == 'probability.get_cumulative':
            fs.probability.get_cumulative(search_items,
                                          csv=True,
                                          output_dir=argument.output_dir,
                                          extra_param=formatted_params)

        elif argument.product == 'probability.get_count':
            fs.probability.get_count(search_items,
                                     argument.location_type,
                                     csv=True,
                                     output_dir=argument.output_dir,
                                     extra_param=formatted_params)

        elif argument.product == 'historic.get_event':
            fs.historic.get_event(search_items,
                                  csv=True,
                                  output_dir=argument.output_dir,
                                  extra_param=formatted_params)

        elif argument.product == 'historic.get_summary':
            fs.historic.get_summary(search_items,
                                    argument.location_type,
                                    csv=True,
                                    output_dir=argument.output_dir,
                                    extra_param=formatted_params)

        elif argument.product == 'historic.get_events_by_location':
            fs.historic.get_events_by_location(search_items,
                                               argument.location_type,
                                               csv=True,
                                               output_dir=argument.output_dir,
                                               extra_param=formatted_params)

        elif argument.product == 'location.get_detail':
            fs.location.get_detail(search_items,
                                   argument.location_type,
                                   csv=True,
                                   output_dir=argument.output_dir,
                                   extra_param=formatted_params)

        elif argument.product == 'location.get_summary':
            fs.location.get_summary(search_items,
                                    argument.location_type,
                                    csv=True,
                                    output_dir=argument.output_dir,
                                    extra_param=formatted_params)

        elif argument.product == 'fema.get_nfip':
            fs.fema.get_nfip(search_items,
                             argument.location_type,
                             csv=True,
                             output_dir=argument.output_dir,
                             extra_param=formatted_params)

        elif argument.product == 'environmental.get_precipitation':
            fs.environmental.get_precipitation(search_items,
                                               csv=True,
                                               output_dir=argument.output_dir,
                                               extra_param=formatted_params)

        elif argument.product == 'tile.get_probability_depth':
            if not argument.year:
                logging.error("get_probability_depth is missing the year argument")
                sys.exit()

            try:
                int(argument.year)
            except ValueError:
                logging.error("The year argument could not be converted to an int. "
                              "Provided argument: {}".format(argument.year))
                sys.exit()

            if not argument.return_period:
                logging.error("get_probability_depth is missing the return_period argument")
                sys.exit()

            try:
                int(argument.return_period)
            except ValueError:
                logging.error("The return_period argument could not be converted to an int. "
                              "Provided argument: {}".format(argument.return_period))
                sys.exit()

            fs.tile.get_probability_depth(year=int(argument.year),
                                          return_period=int(argument.return_period),
                                          search_items=search_items,
                                          output_dir=argument.output_dir,
                                          image=True)

        elif argument.product == 'tile.get_historic_event':

            if not argument.event_id:
                logging.error("get_probability_depth is missing the event_id argument")
                sys.exit()

            try:
                int(argument.event_id)
            except ValueError:
                logging.error("The event_id argument could not be converted to an int. "
                              "Provided argument: {}".format(argument.event_id))
                sys.exit()

            fs.tile.get_historic_event(event_id=int(argument.event_id),
                                       search_items=search_items,
                                       output_dir=argument.output_dir,
                                       image=True)

        elif argument.product == 'aal.get_summary':
            fs.aal.get_summary(search_items,
                               argument.location_type,
                               csv=True,
                               output_dir=argument.output_dir,
                               extra_param=formatted_params)

        elif argument.product == 'avm.get_avm':
            fs.avm.get_avm(search_items,
                           csv=True,
                           output_dir=argument.output_dir,
                           extra_param=formatted_params)

        elif argument.product == 'avm.get_provider':
            fs.avm.get_provider(search_items,
                                csv=True,
                                output_dir=argument.output_dir,
                                extra_param=formatted_params)

        else:
            logging.error("Product not found. Please check that the argument"
                          " provided is correct: {}".format(argument.product))

    else:
        raise InvalidArgument("No search items were provided from either a search item list or a file. "
                              "List: '{}', File Name: '{}'".format(argument.search_items, argument.file))
