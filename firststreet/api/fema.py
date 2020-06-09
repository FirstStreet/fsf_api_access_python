# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.fema import FemaNfip


class Fema(Api):
    """This class receives a list of fsids and handles the creation of a fema product from the request.

        Methods:
            get_nfip: Retrieves a list of Fema Nfip for the given list of IDs
        """

    def get_nfip(self, fsids, location_type, csv=False):
        """Retrieves fema nfip product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Fema Nfip objects.

        Args:
            fsids (list): A First Street ID
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Fema Nfip
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "fema", "nfip", location_type)
        product = [FemaNfip(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product, "fema", "nfip", location_type)

        return product
