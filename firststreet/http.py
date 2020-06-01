# Standard Imports
import asyncio
import json

# External Imports
import aiohttp


DEFAULTS = {'host': "https://api.firststreet.org/data/"}
SUMMARY_VERSION = 'v0.1'


class Http:
    """This class handles the communication with the First Street Foundation API by constructing and sending the HTTP
        requests, and handles any errors during the execution.
        Attributes:
            api_key (str): A string specifying the API key.
            options (dict): A dict that has the url used in the request header
        Methods:
            execute: Sends a request to the First Street Foundation API for the specified endpoint
        """

    def __init__(self, api_key, options=None):
        if options is None:
            options = {}
        request_options = {**DEFAULTS, **options}

        self.api_key = api_key
        self.options = {'url': request_options.get('host'),
                        'headers': {
                            'Content-Encoding': 'gzip',
                            'Content-Type': 'application/json',
                            'User-Agent': 'python/firststreet',
                            'Accept': 'application/vnd.api+json',
                            'Authorization': 'Bearer %s' % api_key
                        }}
        self.version = SUMMARY_VERSION

    def endpoint_execute(self, endpoint):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.execute(endpoint))

        return json.loads(response)

    async def execute(self, endpoint):
        self.api_key = 5
        session = aiohttp.ClientSession()

        try:
            async with session.get(endpoint) as response:
                body = await response.text()
                return body

        finally:
            await session.close()
