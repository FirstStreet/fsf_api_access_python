import os

import pytest

import firststreet
from firststreet.errors import InvalidArgument

api_key = os.environ['FSF_API_KEY']
fs = firststreet.FirstStreet(api_key)


class TestHistoricSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_summary([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(TypeError):
            fs.historic.get_summary(190836953)

    def test_single(self):
        historic = fs.historic.get_summary([190836953])
        assert len(historic) == 1

    def test_multiple(self):
        historic = fs.historic.get_summary([190836953, 193139123])
        assert len(historic) == 2

    def test_single_csv(self):
        historic = fs.historic.get_summary([190836953], csv=True)
        assert len(historic) == 1

    def test_multiple_csv(self):
        historic = fs.historic.get_summary([190836953, 193139123], csv=True)
        assert len(historic) == 2
