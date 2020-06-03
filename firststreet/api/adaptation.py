# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.adaptation import AdaptationDetail, AdaptationSummary


class Adaptation(Api):
    """This class receives a list of fsids and handles the creation of a adaptation product from the request.

        Methods:
            get_detail: Retrieves a list of Adaptation Details for the given list of IDs
            get_summary: Retrieves a list of Adaptation Summary for the given list of IDs
        """

    def get_detail(self, fsids, csv=False):
        """Retrieves adaptation detail product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Adaptation Detail objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Adaptation Detail
        """

        api_datas = self.call_api(fsids, "adaptation", "detail", None)
        product = [AdaptationDetail(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

    def get_summary(self, fsids, location_type, csv=False):
        """Retrieves adaptation summary product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Adaptation Summary objects.

        Args:
            fsids (list): A First Street ID
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Adaptation Summary
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        api_datas = self.call_api(fsids, "adaptation", "summary", location_type)
        product = [AdaptationSummary(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product
