# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api


class EnvironmentalPrecipitation(Api):
    """Creates an Environmental Precipitation object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get("fsid"))
        self.projected = response.get("projected")
