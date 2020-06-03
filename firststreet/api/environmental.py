# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.api.api import Api
from firststreet.models.environmental import EnvironmentalPrecipitation


class Environmental(Api):
    """This class receives a list of fsids and handles the creation of a environmental product from the request.

        Methods:
            get_precipitation: Retrieves a list of Environmental Precipitation for the given list of IDs
        """

    def get_precipitation(self, fsids, csv=False):
        """Retrieves environmental precipitation product data from the First Street Foundation API given a list of FSIDs
        and returns a list of Environmental Precipitation objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Adaptation Detail
        """

        api_datas = self.call_api(fsids, "environmental", "precipitation", "county")
        product = [EnvironmentalPrecipitation(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product, "environmental", "precipitation", "county")

        return product
