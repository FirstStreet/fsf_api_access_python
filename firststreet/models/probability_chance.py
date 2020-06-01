class ProbabilityChance:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.chance = response.get('chance')
