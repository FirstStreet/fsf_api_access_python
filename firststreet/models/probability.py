# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api


class ProbabilityChance(Api):
    """Creates a Probability Chance object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.chance = response.get('chance')


class ProbabilityCount(Api):
    """Creates a Probability Count object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.count = response.get('count')


class ProbabilityCountSummary(Api):
    """Creates a Probability Count Summary object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.state = response.get('state')
        self.city = response.get('city')
        self.zcta = response.get('zcta')
        self.neighborhood = response.get('neighborhood')
        self.tract = response.get('tract')
        self.county = response.get('county')
        self.cd = response.get('cd')


class ProbabilityCumulative(Api):
    """Creates a Probability Cumulative object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.cumulative = response.get('cumulative')


class ProbabilityDepth(Api):
    """Creates a Probability Depth object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = response.get('fsid')
        self.depth = response.get('depth')
