# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import datetime
import logging

# Internal Imports
import os

from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.tile import ProbabilityDepthTile, HistoricEventTile


class Tile(Api):
    """This class receives a list of coordinate and parameters, and handles the return of a tile from the request.

        Methods:
            get_probability_depth: Retrieves a list of Probability Depth for the given list of IDs
            get_historic_event: Retrieves a list of Probability Depth for the given list of IDs
        """

    def get_probability_depth(self, search_items, year, return_period, image=False, output_dir=None, extra_param=None):
        """Retrieves probability depth tile data from the First Street Foundation API given a list of search_items
         and returns a list of Probability Depth Tile objects.

        Args:
            year (int): The year to get the tile
            return_period (int): The return period to get the tile
            search_items (list of tuple): A list of coordinates in the form of [(x_1, y_1, z_1), (x_2, y_2, z_2), ...]
            image (bool): To output extracted image to a png or not
            output_dir (str): The output directory to save the generated tile
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Depth tiles
        """

        if not year:
            raise InvalidArgument(year)
        elif not isinstance(year, int):
            raise TypeError("year is not an int")
        elif year not in [2020, 2035, 2050]:
            logging.error("Year provided is not one of: 2020, 2035, 2050")
            raise InvalidArgument(year)

        if not return_period:
            raise InvalidArgument(return_period)
        elif not isinstance(return_period, int):
            raise TypeError("return period is not an int")
        elif return_period not in [500, 100, 20, 5, 2]:
            logging.error("Return period provided is not one of: 500, 100, 20, 5, 2. "
                          "(2 year return period is only available for coastal areas.)")
            raise InvalidArgument(return_period)

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "tile", "probability", tile_product="depth", year=year,
                                  return_period=return_period, extra_param=extra_param)

        if image:
            for data in api_datas:
                if data:
                    date = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

                    # Set file name to the current date, time, and product
                    file_name = "_".join([date, "probability_depth", str(year), str(return_period),
                                          str(data.get("coordinate"))]) + ".png"

                    if not output_dir:
                        output_dir = os.getcwd() + "/output_data"

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    with open(output_dir + '/' + file_name, "wb") as f:
                        f.write(data['image'])

            logging.info("Image(s) generated to '{}'.".format(output_dir))

        product = [ProbabilityDepthTile(api_data, year, return_period) for api_data in api_datas]

        logging.info("Probability Depth Tile Ready.")

        return product

    def get_historic_event(self, search_items, event_id, image=False, output_dir=None, extra_param=None):
        """Retrieves historic event tile data from the First Street Foundation API given a list of search_items
         and returns a list of Historic Event Tile objects.

        Args:
            search_items (list of tuple): A list of coordinates in the form of [(x_1, y_1, z_1), (x_2, y_2, z_2), ...]
            event_id (int): A First Street Foundation eventId
            image (bool): To output extracted image to a png or not
            output_dir (str): The output directory to save the generated tile
            extra_param (dict): Extra parameter to be added to the url

        Returns:
            A list of Probability Count
        Raises:
            InvalidArgument: The event id provided is empty
            TypeError: The event id provided is not an int
        """

        if not event_id:
            raise InvalidArgument(event_id)
        elif not isinstance(event_id, int):
            raise TypeError("event id is not an int")

        # Get data from api and create objects
        api_datas = self.call_api(search_items, "tile", "historic", tile_product="event", event_id=event_id,
                                  extra_param=extra_param)

        if image:
            for data in api_datas:
                if data:
                    date = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

                    # Set file name to the current date, time, and product
                    file_name = "_".join([date, "historic_event", str(event_id), str(data.get("coordinate"))]) + ".png"

                    if not output_dir:
                        output_dir = os.getcwd() + "/output_data"

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    with open(output_dir + '/' + file_name, "wb") as f:
                        f.write(data.get("image"))

            logging.info("Image(s) generated to '{}'.".format(output_dir))

        product = [HistoricEventTile(api_data, event_id) for api_data in api_datas]

        logging.info("Historic Event Tile Ready.")

        return product
