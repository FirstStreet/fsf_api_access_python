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
        fs.adaptation.get_detail([29], csv=False, limit=100)

    def test_invalid_call(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([392873515], "", csv=True)

    def test_file(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        fs.location.get_detail("sample.txt", "property", csv=True)

    def test_multi_type(self):
        api_key = os.environ['FSF_API_KEY']
        fs = firststreet.FirstStreet(api_key)
        fs.location.get_detail([395133768,
                                "10212 BUCKEYE RD, Cleveland, Ohio",
                                (41.48195701269418, -81.6138601319609)],
                               "property", csv=True)