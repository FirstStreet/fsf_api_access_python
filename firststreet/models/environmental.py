# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation


class EnvironmentalPrecipitation:

    def __init__(self, response):
        self.fsid = response.get("fsid")
        self.projected = response.get("projected")
