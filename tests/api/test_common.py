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


class TestApiGeometry:

    def test_adaptation_geom(self):
        ada = fs.adaptation.get_detail([29], csv=True)
        assert ada[0].geometry is not None

    def test_historic_geom(self):
        his = fs.historic.get_event([2], csv=True)
        assert his[0].geometry is not None

    def test_location_geom(self):
        loc = fs.location.get_detail([395112095], "property", csv=True)
        assert loc[0].geometry is None
        loc = fs.location.get_detail([39153531702], "tract", csv=True)
        assert loc[0].geometry is not None
