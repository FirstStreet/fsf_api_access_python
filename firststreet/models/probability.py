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
        self.fsid = str(response.get('fsid'))
        self.chance = response.get('chance')


class ProbabilityCount(Api):
    """Creates a Probability Count object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.count = response.get('count')


class ProbabilityCountSummary(Api):
    """Creates a Probability Count Summary object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.state = response.get('state')
        if self.state and any(isinstance(el, list) for el in self.state):
            self.state = [item for sublist in self.state for item in sublist]
        self.city = response.get('city')
        if self.city and any(isinstance(el, list) for el in self.city):
            self.city = [item for sublist in self.city for item in sublist]
        self.zcta = response.get('zcta')
        if self.zcta and any(isinstance(el, list) for el in self.zcta):
            self.zcta = [item for sublist in self.zcta for item in sublist]
        self.neighborhood = response.get('neighborhood')
        if self.neighborhood and any(isinstance(el, list) for el in self.neighborhood):
            self.neighborhood = [item for sublist in self.neighborhood for item in sublist]
        self.tract = response.get('tract')
        if self.tract and any(isinstance(el, list) for el in self.tract):
            self.tract = [item for sublist in self.tract for item in sublist]
        self.county = response.get('county')
        if self.county and any(isinstance(el, list) for el in self.county):
            self.county = [item for sublist in self.county for item in sublist]
        self.cd = response.get('cd')
        if self.cd and any(isinstance(el, list) for el in self.cd):
            self.cd = [item for sublist in self.cd for item in sublist]


class ProbabilityCumulative(Api):
    """Creates a Probability Cumulative object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.cumulative = response.get('cumulative')


class ProbabilityDepth(Api):
    """Creates a Probability Depth object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.depth = response.get('depth')
