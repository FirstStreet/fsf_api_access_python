# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation


class FemaNfip:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.claimCount = response.get('claimCount')
        self.policyCount = response.get('policyCount')
        self.buildingPaid = response.get('buildingPaid')
        self.contentPaid = response.get('contentPaid')
        self.buildingCoverage = response.get('buildingCoverage')
        self.contentCoverage = response.get('contentCoverage')
        self.iccPaid = response.get('iccPaid')
