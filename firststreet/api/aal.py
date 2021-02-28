# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.aal import AALSummaryProperty, AALSummaryOther


class AAL(Api):
    """This class receives a list of search_items and handles the creation of an aal product from the request.

        Methods:
            get_summary: Retrieves a list of AAL Summary for the given list of IDs
        """

    def get_summary(self, search_items, location_type, csv=False, output_dir=None, extra_param=None):
        """Retrieves AAL summary product data from the First Street Foundation API given a list of search_items and
        returns a list of AAL Summary objects.

        Args:
            search_items (list/file): A First Street Foundation IDs, lat/lng pair, address, or a
                file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            output_dir (str): The output directory to save the generated csvs
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of AAL Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        if extra_param and "depths" in extra_param:
            extra_param["depths"] = ','.join(map(str, extra_param["depths"]))

        api_datas = self.call_api(search_items, "economic/aal", "summary", location_type, extra_param=extra_param)

        if location_type == "property":
            product = []
            for api_data, fsid in zip(api_datas, search_items):
                api_data["fsid"] = fsid
                product.append(AALSummaryProperty(api_data))

        else:
            product = []
            for api_data, fsid in zip(api_datas, search_items):
                api_data["fsid"] = fsid
                product.append(AALSummaryOther(api_data))

        if csv:
            csv_format.to_csv(product, "economic_aal", "summary", location_type, output_dir=output_dir)

        logging.info("AAL Summary Data Ready.")

        return product
