import os

import pytest

import firststreet
from firststreet.errors import InvalidArgument

api_key = os.environ['FSF_API_KEY']
fs = firststreet.FirstStreet(api_key)


class TestEnvironmentalEvent:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.environmental.get_precipitation([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(TypeError):
            fs.environmental.get_precipitation(19117)

    def test_single(self):
        environmental = fs.environmental.get_precipitation([19117])
        assert len(environmental) == 1

    def test_multiple(self):
        environmental = fs.environmental.get_precipitation([19117, 19135])
        assert len(environmental) == 2

    def test_single_csv(self):
        environmental = fs.environmental.get_precipitation([19117], csv=True)
        assert len(environmental) == 1

    def test_multiple_csv(self):
        environmental = fs.environmental.get_precipitation([19117, 19135], csv=True)
        assert len(environmental) == 2
