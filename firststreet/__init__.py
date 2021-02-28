"""A Python module for interacting with the First Street Foundation API"""
# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api.adaptation import Adaptation
from firststreet.api.environmental import Environmental
from firststreet.api.fema import Fema
from firststreet.api.historic import Historic
from firststreet.api.location import Location
from firststreet.api.probability import Probability
from firststreet.api.tile import Tile
from firststreet.api.aal import AAL
from firststreet.api.avm import AVM
from firststreet.errors import MissingAPIKeyError
from firststreet.http_util import Http


class FirstStreet:
    """A FirstStreet allows communication with the First Street Foundation API. This handles constructing and sending
        HTTP requests to the First Street Foundation API, and parses any response received into the appropriate object.

        Attributes:
            api_key (str): A string specifying the API key.
            connection_limit (int): max number of connections to make
            rate_limit (int): max number of requests during the period
            rate_period (int): period of time for the limit
            version (str): The version to call the API with
            log (bool): To log the outputs on info level
        Example:
        ```python
            import os
            import firststreet

            fs = firststreet.FirstStreet(os.environ['FIRSTSTREET_API_KEY'])
            property_summary = fs.data_summary.get_property_by_fsid("450350223646")
        ```
        Raises:
            MissingAPIError: If the API is not provided
    """

    def __init__(self, api_key=None, connection_limit=100, rate_limit=20000, rate_period=1, version=None, log=True):

        if not api_key:
            raise MissingAPIKeyError('Missing API Key.')

        if log:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        self.http = Http(api_key, connection_limit, rate_limit, rate_period, version)
        self.location = Location(self.http)
        self.probability = Probability(self.http)
        self.historic = Historic(self.http)
        self.adaptation = Adaptation(self.http)
        self.environmental = Environmental(self.http)
        self.fema = Fema(self.http)
        self.tile = Tile(self.http)
        self.aal = AAL(self.http)
        self.avm = AVM(self.http)
