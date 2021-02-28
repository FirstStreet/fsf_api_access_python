# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.models.avm import AVMProperty, AVMProvider


class AVM(Api):
    """This class receives a list of search_items and handles the creation of an AVM product from the request.

        Methods:
            get_avm: Retrieves a list of AVM for the given list of IDs
        """

    def get_avm(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves AVM product data from the First Street Foundation API given a list of search_items and
        returns a list of AVM objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AVM
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "economic", "avm", "property", extra_param=extra_param)

        product = [AVMProperty(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "economic_avm", "avm", "property", output_dir=output_dir)

        logging.info("AVM Data Ready.")

        return product

    def get_provider(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves AVM provider product data from the First Street Foundation API given a list of search_items and
        returns a list of AVM provider objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AVM Provider
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """
        # Get data from api and create objects
        api_datas = self.call_api(search_items, "economic/avm", "provider", extra_param=extra_param)

        product = [AVMProvider(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "economic_avm", "provider", output_dir=output_dir)

        logging.info("AVM Provider Data Ready.")

        return product
