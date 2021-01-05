# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Internal Imports
from firststreet.models.api import Api


class FemaNfip(Api):
    """Creates a FEMA NFIP object given a response

    Args:
        response (JSON): A JSON response received from the API
    """

    def __init__(self, response):
        super().__init__(response)
        self.fsid = str(response.get('fsid'))
        self.claimCount = response.get('claimCount')
        self.policyCount = response.get('policyCount')
        self.buildingPaid = response.get('buildingPaid')
        self.contentPaid = response.get('contentPaid')
        self.buildingCoverage = response.get('buildingCoverage')
        self.contentCoverage = response.get('contentCoverage')
        self.iccPaid = response.get('iccPaid')
