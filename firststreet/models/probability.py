# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation


class ProbabilityChance:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.chance = response.get('chance')


class ProbabilityCount:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.count = response.get('count')


class CountSummary:

    def __init__(self, data):
        self.data = data.get('data')
        self.count = data.get('count')


class ProbabilityCountSummary:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.count = response.get('state')
        self.count = response.get('city')
        self.count = response.get('county')
        self.count = response.get('count')
        self.count = response.get('count')


class ProbabilityCumulative:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.cumulative = response.get('cumulative')


class ProbabilityDepth:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.depth = response.get('depth')
