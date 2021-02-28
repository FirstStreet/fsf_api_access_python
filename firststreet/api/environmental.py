# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.models.environmental import EnvironmentalPrecipitation


class Environmental(Api):
    """This class receives a list of search_items and handles the creation of a environmental product from the request.

        Methods:
            get_precipitation: Retrieves a list of Environmental Precipitation for the given list of IDs
        """

    def get_precipitation(self, search_items, csv=False, output_dir=None, extra_param=None):
        """Retrieves environmental precipitation product data from the First Street Foundation API given a list of
        search_items and returns a list of Environmental Precipitation objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Adaptation Detail
        """

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "environmental", "precipitation", "county", extra_param=extra_param)
        product = [EnvironmentalPrecipitation(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "environmental", "precipitation", "county", output_dir=output_dir)

        logging.info("Environmental Precipitation Data Ready.")

        return product
