class ProbabilityDepth:

    def __init__(self, response):

        self.fsid = response.get('fsid')
        self.depth = response.get('depth')
