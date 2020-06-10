# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation


class EnvironmentalPrecipitation:
    """Creates an Environmental Precipitation object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        self.fsid = response.get("fsid")
        self.projected = response.get("projected")
