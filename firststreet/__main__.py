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

    repeat = True

    while repeat:
        parser = argparse.ArgumentParser(description="Description for my parser")
        parser.add_argument("-p", "--product", help="Example: adaptation_detail", required=False)
        parser.add_argument("-api_key", "--api_key", required=False)
        parser.add_argument("-v", "--version", required=False)
        parser.add_argument("-log", "--log", help="Example: False", required=False, default="True")
        parser.add_argument("-connection_limit", "--connection_limit", help="Example: 100",
                            required=False, default="100")
        parser.add_argument("-rate_limit", "--rate_limit", help="Example: 4990", required=False, default="4990")
        parser.add_argument("-rate_period", "--rate_period", help="Example: 60", required=False, default="60")
        parser.add_argument("-o", "--output_dir", help="Example: /output", required=False)
        parser.add_argument("-s", "--search_items", help="Example: 28,29", required=False,)
        parser.add_argument("-l", "--location_type", help="Example: property", required=False)
        parser.add_argument("-y", "--year", required=False)
        parser.add_argument("-rp", "--return_period", required=False)
        parser.add_argument("-eid", "--event_id", required=False)
        parser.add_argument("-e", "--extra_param", required=False)
        # deprecated file parameter. Will be removed in a later version
        parser.add_argument("-f", "--file", help="Example: ./sample.txt", required=False)

        argument = parser.parse_args()

        # Select product if not provided
        if not argument.product:
            argument.product = input("Input product (Ex: location.get_detail). Arguments and brackets are not needed: "
                                     ).lower()

            if argument.product not in ['adaptation.get_detail',
                                        'adaptation.get_summary',
                                        'adaptation.get_detail_by_location',
                                        'probability.get_depth',
                                        'probability.get_chance',
                                        'probability.get_count_summary',
                                        'probability.get_cumulative',
                                        'probability.get_count',
                                        'historic.get_event',
                                        'historic.get_summary',
                                        'historic.get_events_by_location',
                                        'location.get_detail',
                                        'location.get_summary',
                                        'fema.get_nfip',
                                        'environmental.get_precipitation',
                                        'tile.get_probability_depth',
                                        'tile.get_historic_event',
                                        'aal.get_summary',
                                        'avm.get_avm',
                                        'avm.get_provider',
                                        'economic.get_property_nfip']:
                logging.error("Product not found. Please check that the argument"
                              " provided is correct: {}".format(argument.product))
                input("Press Enter to continue...")
                sys.exit()

        if not argument.location_type and (argument.product == 'adaptation.get_summary'
                                           or argument.product == 'adaptation.get_detail_by_location'
                                           or argument.product == 'probability.get_count'
                                           or argument.product == 'historic.get_summary'
                                           or argument.product == 'historic.get_events_by_location'
                                           or argument.product == 'location.get_detail'
                                           or argument.product == 'location.get_summary'
                                           or argument.product == 'fema.get_nfip'
                                           or argument.product == 'aal.get_summary'):

            argument.location_type = input("Input location type (Ex: property): ").lower()
            if argument.location_type not in ['property', 'neighborhood', 'city', 'zcta',
                                              'tract', 'county', 'cd', 'state']:
                logging.error("Location type not found. Please check that the argument"
                              " provided is correct: {}".format(argument.location_type))
                input("Press Enter to continue...")
                sys.exit()

        if not argument.year and (argument.product == 'tile.get_probability_depth'):
            argument.year = input("Input probability depth tile year: ")

        if not argument.return_period and (argument.product == 'tile.get_probability_depth'):
            argument.return_period = input("Input probability depth tile return period: ")

        if not argument.event_id and (argument.product == 'tile.get_historic_event'):
            argument.event_id = input("Input historic event tile event id: ")

        if not argument.extra_param and (argument.product == 'aal.get_summary'):
            aal_variable = input("Adjust calculator variables (Y/N)? ")
            if aal_variable.lower() == "y":
                input_params = []

                calculator_avm = input("Input custom AVM value (Ex: 234212) or leave blank for default: ")
                if calculator_avm != '':
                    input_params += ["avm:{}".format(calculator_avm)]
                calculator_depths = input("Input depths list (Ex: [11,12,30]) or leave blank for default: ")
                if calculator_depths != '':
                    input_params += ["depths:{}".format(calculator_depths)]
                calculator_basement = input("Input basement boolean (Ex: True/False) or leave blank for default: ")
                if calculator_basement != '':
                    input_params += ["basement:{}".format(calculator_basement)]
                calculator_elevation = input("Input floor elevation value: (Ex: 22) or leave blank for default: ")
                if calculator_elevation != '':
                    input_params += ["floorElevation:{}".format(calculator_elevation)]
                calculator_units = input("Input number of units: (Ex: 2) or leave blank for default: ")
                if calculator_units != '':
                    input_params += ["units:{}".format(calculator_units)]
                calculator_stories = input("Input number of stories: (Ex: 1) or leave blank for default: ")
                if calculator_stories != '':
                    input_params += ["stories:{}".format(calculator_stories)]

                argument.extra_param = ";".join(input_params)

        if not argument.extra_param and (argument.product == 'avm.get_avm'):
            avm_provider = input("Adjust provider id (Y/N)? ")
            if avm_provider.lower() == "y":
                input_params = input("Input provider id (Ex: 2): ")
                if input_params != '':
                    argument.extra_param = "providerid:{}".format(input_params)

        # Try to get the API key either from env var or the parameter
        if not argument.api_key:
            env_var_name = 'FSF_API_KEY'
            try:
                api_key = os.environ[env_var_name]
            except KeyError:
                api_key = input("Input API key: ")
        else:
            api_key = argument.api_key

        # Input the search item file
        if not argument.search_items:
            argument.search_items = input("Input file name of search items. Either relative or absolute (Ex: "
                                          "'FSIDs_for_NY.csv', or 'C:\\Users\\test_user\\Documents\\prop_geo_sc.csv'): "
                                          )

            if not os.path.isfile(argument.search_items):
                logging.error("Input file not found, please check if the file is at the path: {}".format(
                    os.path.abspath(argument.search_items)))
                input("Press Enter to continue...")
                sys.exit()

        # Adjust the connection variables
        if not argument.connection_limit and not argument.rate_limit and not argument.rate_period:
            connection_adjust = input("Adjust connection parameters (Y/N)? Defaults to 100 connections, with a rate "
                                      "limit of 4990 calls per 60 seconds: ")
            if connection_adjust.lower() == "y":
                input_params = input("Input new connection limit (default 100): ")
                if input_params != '':
                    argument.connection_limit = "providerid:{}".format(input_params)
                input_params = input("Input new rate limit (default 5000): ")
                if input_params != '':
                    argument.rate_limit = "providerid:{}".format(input_params)
                input_params = input("Input new rate period in seconds (default 60): ")
                if input_params != '':
                    argument.rate_period = "providerid:{}".format(input_params)
            else:
                argument.connection_limit = 100
                argument.rate_limit = 4990
                argument.rate_period = 60

        # Adjust the output directory
        if not argument.output_dir:
            connection_adjust = input("Change output directory (Y/N)? Defaults to output_data folder in the "
                                      "current directory: ")
            if connection_adjust.lower() == "y":
                argument.output_dir = input("Input new output directory location: ")

        # Reads a file or converts search items into a list
        search_items = []
        if argument.search_items:

            # If file, read addresses from file
            if os.path.isfile(argument.search_items):
                search_items = read_search_items_from_file(argument.search_items)
            else:
                items = argument.search_items.strip().split(";")
                if len(items) == 1:
                    logging.warning("Could not find the file '{}'. Treating the input as a search_item instead. "
                                    "If this is unexpected, check the spelling or path of the input"
                                    .format(argument.search_items))
                for search_item in items:
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

            # Set to lower for case insensitive
            argument.product = argument.product.lower()

            try:
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
                        input("Press Enter to continue...")
                        sys.exit()

                    try:
                        int(argument.year)
                    except ValueError:
                        logging.error("The year argument could not be converted to an int. "
                                      "Provided argument: {}".format(argument.year))
                        input("Press Enter to continue...")
                        sys.exit()

                    if not argument.return_period:
                        logging.error("get_probability_depth is missing the return_period argument")
                        input("Press Enter to continue...")
                        sys.exit()

                    try:
                        int(argument.return_period)
                    except ValueError:
                        logging.error("The return_period argument could not be converted to an int. "
                                      "Provided argument: {}".format(argument.return_period))
                        input("Press Enter to continue...")
                        sys.exit()

                    fs.tile.get_probability_depth(year=int(argument.year),
                                                  return_period=int(argument.return_period),
                                                  search_items=search_items,
                                                  output_dir=argument.output_dir,
                                                  image=True)

                elif argument.product == 'tile.get_historic_event':

                    if not argument.event_id:
                        logging.error("get_probability_depth is missing the event_id argument")
                        input("Press Enter to continue...")
                        sys.exit()

                    try:
                        int(argument.event_id)
                    except ValueError:
                        logging.error("The event_id argument could not be converted to an int. "
                                      "Provided argument: {}".format(argument.event_id))
                        input("Press Enter to continue...")
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

                elif argument.product == 'economic.get_property_nfip':
                    fs.economic.get_property_nfip(search_items,
                                                  csv=True,
                                                  output_dir=argument.output_dir,
                                                  extra_param=formatted_params)

                else:
                    logging.error("Product not found. Please check that the argument"
                                  " provided is correct: {}".format(argument.product))

            finally:
                input("Press Enter to continue...")

        else:
            raise InvalidArgument("No search items were provided from either a search item list or a file. "
                                  "List: '{}', File Name: '{}'".format(argument.search_items, argument.file))

        repeat_prompt = input("Perform another data pull (Y/N)?")

        if repeat_prompt.lower() == "y":
            repeat = True
        else:
            repeat = False
