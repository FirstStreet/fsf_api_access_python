# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import os

# External Imports
import pytest

# Internal Imports
import firststreet
from firststreet.errors import InvalidArgument, MissingAPIKeyError


class TestApi:

    def test_invalid_key(self):
        with pytest.raises(MissingAPIKeyError):
            firststreet.FirstStreet("")

    def test_vaid_key(self):
        api_key = os.environ['FSF_API_KEY']
        firststreet.FirstStreet(api_key)

    def test_valid_call(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        adap = fs.adaptation.get_detail([29], csv=False, connection_limit=100)
        assert len(adap) == 1
        assert adap[0].name == 'Riverfront Park'

    def test_invalid_call(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([392873515], "", csv=True)

    def test_file(self):
        with open(os.getcwd() + "/" + "sample.txt", "w+") as file:
            file.write("395133768\n")
            file.write("10212 BUCKEYE RD, Cleveland, Ohio\n")
            file.write("(41.48195701269418, -81.6138601319609)\n")

        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        loc = fs.location.get_detail("sample.txt", "property", csv=True)
        assert len(loc) == 3
        assert loc[0].route == 'BUCKEYE RD'
        assert loc[1].route == 'BUCKEYE RD'
        assert loc[2].route == 'BUCKEYE RD'

        os.remove(os.getcwd() + "/" + "sample.txt")

    def test_invalid_file(self):
        with open(os.getcwd() + "/" + "sample.txt", "w+") as file:
            file.write("395133768, 10212 BUCKEYE RD, Cleveland, Ohio, (41.48195701269418, -81.6138601319609)")

        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        loc = fs.location.get_detail("sample.txt", "property", csv=True)
        assert len(loc) == 1

        os.remove(os.getcwd() + "/" + "sample.txt")

    def test_multi_type(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        loc = fs.location.get_detail([395133768,
                                      "10212 BUCKEYE RD, Cleveland, Ohio",
                                      (41.48195701269418, -81.6138601319609)],
                                     "property", csv=True)
        assert len(loc) == 3
        assert loc[0].route == 'BUCKEYE RD'
        assert loc[1].route == 'BUCKEYE RD'
        assert loc[2].route == 'BUCKEYE RD'
