# Internal Imports
from firststreet.models._response import Response, ResultsData


class TidalRisk(Response):

    def __init__(self, data, FSID, results):
        super().__init__(data, FSID, results)

        self.FSID = FSID
        self.results = [ResultsData(results_data) for results_data in results]
