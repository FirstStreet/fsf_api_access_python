# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.probability import ProbabilityChance, ProbabilityCount, ProbabilityCountSummary, \
    ProbabilityCumulative, ProbabilityDepth


class Probability(Api):
    """This class receives a list of search_items and handles the creation of a probability product from the request.

        Methods:
            get_depth: Retrieves a list of Probability Depth for the given list of IDs
            get_chance: Retrieves a list of Probability Depth for the given list of IDs
            get_count: Retrieves a list of Probability Depth for the given list of IDs
            get_count_summary: Retrieves a list of Probability Depth for the given list of IDs
            get_cumulative: Retrieves a list of Probability Depth for the given list of IDs
        """

    def get_chance(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves probability chance product data from the First Street Foundation API given a list of search_items
         and returns a list of Probability Chance objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Chance
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "probability", "chance", "property", extra_param=extra_param)
        product = [ProbabilityChance(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "probability", "chance", output_dir=output_dir)

        logging.info("Probability Chance Data Ready.")

        return product

    def get_count(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves probability count product data from the First Street Foundation API given a list of search_items
         and returns a list of Probability Count objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Count
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "probability", "count", location_type, extra_param=extra_param)
        product = [ProbabilityCount(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "probability", "count", location_type, output_dir=output_dir)

        logging.info("Probability Count Data Ready.")

        return product

    def get_count_summary(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves probability Count-Summary product data from the First Street Foundation API given a list of
        search_items and returns a list of Probability Count-Summary object.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Count-Summary
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "probability", "count-summary", "property", extra_param=extra_param)
        product = [ProbabilityCountSummary(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "probability", "count-summary", output_dir=output_dir)

        logging.info("Probability Count-Summary Data Ready.")

        return product

    def get_cumulative(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves probability cumulative product data from the First Street Foundation API given a list of
        search_items and returns a list of Probability Cumulative object.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Cumulative
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "probability", "cumulative", "property", extra_param=extra_param)
        product = [ProbabilityCumulative(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "probability", "cumulative", output_dir=output_dir)

        logging.info("Probability Cumulative Data Ready.")

        return product

    def get_depth(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves probability depth product data from the First Street Foundation API given a list of search_items
         and returns a list of Probability Depth objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Depth
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "probability", "depth", "property", extra_param=extra_param)
        product = [ProbabilityDepth(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "probability", "depth", output_dir=output_dir)

        logging.info("Probability Depth Data Ready.")

        return product
