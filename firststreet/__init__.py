"""A Python module for interacting with the First Street Foundation API"""

# Internal Imports
from firststreet.api.location import Location
from firststreet.api.probability import Probability
from firststreet.errors import MissingAPIKeyError
from firststreet.http import Http


class FirstStreet:
    """A FirstStreet allows communication with the First Street Foundation API. This handles constructing and sending
        HTTP requests to the First Street Foundation API, and parses any response received into the appropriate object.

        Attributes:
            api_key (str): A string specifying the API key.
            options (dict): A dict that has the url used in the request header
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

    def __init__(self, api_key=None, options=None):

        if not api_key:
            raise MissingAPIKeyError('Missing API Key.')

        if options is None:
            options = {}

        self.http = Http(api_key, options)
        self.location = Location(self.http)
        self.probability = Probability(self.http)
        # self.historic = Hurricane(self.http)
        # self.adaptation = Tidal(self.http)
        # self.fema = MVI(self.http)
        # self.environmental = MVI(self.http)
