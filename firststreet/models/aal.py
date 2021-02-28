# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api


class AALSummary(Api):
    """A AAL Summary Object parent

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.annual_loss = response.get('annualLoss')


class AALSummaryProperty(AALSummary):
    """Creates a AAL Detail Property object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.depth_loss = response.get('depthLoss')


class AALSummaryOther(AALSummary):
    """Creates a AAL Detail Property object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
