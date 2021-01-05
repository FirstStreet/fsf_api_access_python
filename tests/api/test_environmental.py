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


class TestEnvironmentalEvent:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.environmental.get_precipitation([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.environmental.get_precipitation(19117)

    def test_invalid(self):
        fsid = [0000]
        environmental = fs.environmental.get_precipitation(fsid)
        assert len(environmental) == 1
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is None
        assert environmental[0].valid_id is False

    def test_single(self):
        fsid = [19117]
        environmental = fs.environmental.get_precipitation(fsid)
        assert len(environmental) == 1
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[0].valid_id is True

    def test_multiple(self):
        fsid = [19117, 19135]
        environmental = fs.environmental.get_precipitation(fsid)
        assert len(environmental) == 2
        environmental.sort(key=lambda x: x.fsid)
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[1].fsid == str(fsid[1])
        assert environmental[1].projected is not None
        assert environmental[0].valid_id is True
        assert environmental[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [19117]
        environmental = fs.environmental.get_precipitation(fsid, csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [19117, 19135]
        environmental = fs.environmental.get_precipitation(fsid, csv=True, output_dir=tmpdir)
        assert len(environmental) == 2
        environmental.sort(key=lambda x: x.fsid)
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[1].fsid == str(fsid[1])
        assert environmental[1].projected is not None
        assert environmental[0].valid_id is True
        assert environmental[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [19117, 00000]
        environmental = fs.environmental.get_precipitation(fsid)
        assert len(environmental) == 2
        environmental.sort(key=lambda x: x.fsid, reverse=True)
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[1].fsid == str(fsid[1])
        assert environmental[1].projected is None
        assert environmental[0].valid_id is True
        assert environmental[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [19117, 00000]
        environmental = fs.environmental.get_precipitation(fsid, csv=True, output_dir=tmpdir)
        assert len(environmental) == 2
        environmental.sort(key=lambda x: x.fsid, reverse=True)
        assert environmental[0].fsid == str(fsid[0])
        assert environmental[0].projected is not None
        assert environmental[1].fsid == str(fsid[1])
        assert environmental[1].projected is None
        assert environmental[0].valid_id is True
        assert environmental[1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        environmental = fs.environmental.get_precipitation([(82.487671, -62.374322)], csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].projected is None
        assert environmental[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        environmental = fs.environmental.get_precipitation([(40.7079652311, -74.0021455387)],
                                                           csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].projected is not None
        assert environmental[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        environmental = fs.environmental.get_precipitation(["Shimik, Nunavut"], csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].projected is None
        assert environmental[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        environmental = fs.environmental.get_precipitation(["Toronto, Ontario, Canada"], csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].projected is None
        assert environmental[0].valid_id is False

    def test_single_address(self, tmpdir):
        environmental = fs.environmental.get_precipitation(["247 Water St, New York, New York"],
                                                           csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].projected is not None
        assert environmental[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        environmental = fs.environmental.get_precipitation([39057], csv=True, output_dir=tmpdir)
        assert len(environmental) == 1
        assert environmental[0].valid_id is True
        assert environmental[0].fsid == "39057"
        assert environmental[0].projected is not None
        assert environmental[0].projected[0].get("year") is not None
        assert environmental[0].projected[0].get("data") is not None
        assert environmental[0].projected[0].get("data").get("low") is not None
        assert environmental[0].projected[0].get("data").get("mid") is not None
        assert environmental[0].projected[0].get("data").get("high") is not None
