# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import os

# External Imports
import pytest

# Internal Imports
import firststreet
from firststreet.errors import InvalidArgument

api_key = os.environ['FSF_API_KEY']
fs = firststreet.FirstStreet(api_key)


class TestProbabilityTiles:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_probability_depth(year=2050, return_period=5, search_items=[])

    def test_wrong_coord_type(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_probability_depth(year=2050, return_period=5, search_items=(12, 942, 1715))

    def test_wrong_coord_tuple_type(self):
        with pytest.raises(TypeError):
            fs.tile.get_probability_depth(year=2050, return_period=500, search_items=[500])

    def test_invalid(self):
        coord = [(1, 1, 1)]
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=coord)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        assert tile[0].image is None
        assert tile[0].valid_id is False

    def test_wrong_year_type(self):
        with pytest.raises(TypeError):
            fs.tile.get_probability_depth(year="year", return_period=5, search_items=[(12, 942, 1715)])

    def test_wrong_return_period_type(self):
        with pytest.raises(TypeError):
            fs.tile.get_probability_depth(year=2050, return_period="rp", search_items=[(12, 942, 1715)])

    def test_bad_year(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_probability_depth(year=1000, return_period=5, search_items=[(12, 942, 1715)])

    def test_bad_return_period(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_probability_depth(year=1000, return_period=5, search_items=[(12, 942, 1715)])

    def test_single(self):
        coord = [(12, 942, 1715)]
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=coord)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        assert tile[0].image is not None
        assert tile[0].valid_id is True

    def test_multiple(self):
        coord = [(12, 942, 1715), (17, 30990, 54379)]
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=coord)
        assert len(tile) == 2
        tile.sort(key=lambda x: x.coordinate)
        assert tile[0].coordinate == coord[0]
        assert tile[1].coordinate == coord[1]
        assert tile[0].image is not None
        assert tile[0].valid_id is True
        assert tile[1].image is not None
        assert tile[1].valid_id is True

    def test_single_image(self):
        coord = [(12, 942, 1715)]
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=coord, image=True)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        assert tile[0].image is not None
        assert tile[0].valid_id is True

    def test_mixed_invalid(self):
        coord = [(12, 942, 1715), (1, 1, 1)]
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=coord)
        assert len(tile) == 2
        tile.sort(key=lambda x: x.coordinate, reverse=True)
        assert tile[0].coordinate == coord[0]
        assert tile[1].coordinate == coord[1]
        assert tile[0].image is not None
        assert tile[0].valid_id is True
        assert tile[1].image is None
        assert tile[1].valid_id is False

    def test_one_of_each(self):
        tile = fs.tile.get_probability_depth(year=2050, return_period=5, search_items=[(12, 942, 1715)])
        assert len(tile) == 1
        assert tile[0].valid_id is True
        assert tile[0].coordinate == (12, 942, 1715)
        assert tile[0].image is not None
        assert tile[0].return_period
        assert tile[0].year


class TestHistoricTiles:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_historic_event(event_id=2, search_items=[])

    def test_wrong_coord_type(self):
        with pytest.raises(InvalidArgument):
            fs.tile.get_historic_event(event_id=2, search_items=(12, 942, 1715))

    def test_invalid(self):
        coord = [(12, 1, 1)]
        tile = fs.tile.get_historic_event(event_id=2, search_items=coord)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        # No way to test if image is bad

    def test_wrong_event_id_type(self):
        with pytest.raises(TypeError):
            fs.tile.get_historic_event(event_id="event_id", search_items=[(12, 942, 1715)])

    def test_bad_event(self):
        coord = [(12, 942, 1715)]
        tile = fs.tile.get_historic_event(event_id=99999, search_items=coord)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        # No way to test if image is bad

    def test_single(self):
        coord = [(12, 942, 1715)]
        tile = fs.tile.get_historic_event(event_id=2, search_items=coord)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        assert tile[0].image is not None
        assert tile[0].valid_id is True

    def test_multiple(self):
        coord = [(12, 942, 1715), (17, 30990, 54379)]
        tile = fs.tile.get_historic_event(event_id=2, search_items=coord)
        assert len(tile) == 2
        tile.sort(key=lambda x: x.coordinate)
        assert tile[0].coordinate == coord[0]
        assert tile[1].coordinate == coord[1]
        assert tile[0].image is not None
        assert tile[0].valid_id is True
        assert tile[1].image is not None
        assert tile[1].valid_id is True

    def test_single_image(self):
        coord = [(12, 942, 1715)]
        tile = fs.tile.get_historic_event(event_id=2, search_items=coord, image=True)
        assert len(tile) == 1
        assert tile[0].coordinate == coord[0]
        assert tile[0].image is not None
        assert tile[0].valid_id is True

    def test_mixed_invalid(self):
        coord = [(12, 942, 1715), (2, 1, 1)]
        tile = fs.tile.get_historic_event(event_id=2, search_items=coord)
        assert len(tile) == 2
        tile.sort(key=lambda x: x.coordinate, reverse=True)
        assert tile[0].coordinate == coord[0]
        assert tile[1].coordinate == coord[1]
        assert tile[0].image is not None
        assert tile[0].valid_id is True
        # No way to test if image is bad

    def test_one_of_each(self):
        tile = fs.tile.get_historic_event(event_id=2, search_items=[(12, 942, 1715)])
        assert len(tile) == 1
        assert tile[0].valid_id is True
        assert tile[0].coordinate == (12, 942, 1715)
        assert tile[0].image is not None
        assert tile[0].event_id
