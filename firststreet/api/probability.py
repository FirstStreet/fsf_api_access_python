# Internal Imports
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.probability_depth import ProbabilityDepth
from firststreet.models.probability_chance import ProbabilityChance
from firststreet.models.probability_count import ProbabilityCount
from firststreet.models.probability_count_summary import ProbabilityCountSummary
from firststreet.models.probability_cumulative import ProbabilityCumulative


class Probability(Api):
    """This class receives a list of fsids and handles the creation of a probability product from the request.

        Methods:
            get_depth: Retrieves a list of Probability Depth for the given list of IDs
            get_chance: Retrieves a list of Probability Depth for the given list of IDs
            get_count: Retrieves a list of Probability Depth for the given list of IDs
            get_count_summary: Retrieves a list of Probability Depth for the given list of IDs
            get_cumulative: Retrieves a list of Probability Depth for the given list of IDs
        """

    def get_depth(self, fsids, csv=False):
        """Retrieves probability depth product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Probability Depth objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Probability Depth
        """

        api_datas = self.call_api(fsids, "probability", "depth", "property")
        product = [ProbabilityDepth(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

    def get_chance(self, fsids, csv=False):
        """Retrieves probability chance product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Probability Chance objects.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Probability Chance
        """

        api_datas = self.call_api(fsids, "probability", "chance", "property")
        product = [ProbabilityChance(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

    def get_count(self, fsids, location_type, csv=False):
        """Retrieves probability count product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Probability Count objects.

        Args:
            fsids (list): A First Street ID
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Probability Count
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        api_datas = self.call_api(fsids, "probability", "count", location_type)
        product = [ProbabilityCount(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

    def get_count_summary(self, fsids, location_type, csv=False):
        # todo
        """Retrieves probability count summary product data from the First Street Foundation API given a list of FSIDs
        and returns a list of Probability Chance objects.

        Args:
            fsids (list): A First Street ID
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Probability Chance
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        api_datas = self.call_api(fsids, "probability", "depth", location_type)
        product = [ProbabilityCountSummary(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product

    def get_cumulative(self, fsids, csv=False):
        """Retrieves probability cumulative product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Probability Chance object.

        Args:
            fsids (list): A First Street ID
            csv (bool): To output extracted data to a csv or not
        Returns:
            A list of Probability Cumulative
        """

        api_datas = self.call_api(fsids, "probability", "cumulative", "property")
        product = [ProbabilityCumulative(api_data) for api_data in api_datas]

        if csv:
            self.to_csv(product)

        return product
