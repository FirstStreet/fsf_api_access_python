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


class TestFemaNfip:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.fema.get_nfip([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.fema.get_nfip([], "tract")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.fema.get_nfip([19055950100], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.fema.get_nfip("19055950100", "tract")

    def test_wrong_fsid_number(self):
        fsid = [19027]
        fema = fs.fema.get_nfip(fsid, "tract")
        assert len(fema) == 1
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is None
        assert fema[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [19055950100]
        fema = fs.fema.get_nfip(fsid, "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is None
        assert fema[0].valid_id is False

    def test_wrong_fema_type(self):
        with pytest.raises(TypeError):
            fs.fema.get_nfip([19055950100], 190)

    def test_single(self):
        fsid = [19055950100]
        fema = fs.fema.get_nfip(fsid, "tract")
        assert len(fema) == 1
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[0].valid_id is True

    def test_multiple(self):
        fsid = [19055950100, 19153003200]
        fema = fs.fema.get_nfip(fsid, "tract")
        assert len(fema) == 2
        fema.sort(key=lambda x: x.fsid)
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[1].fsid == fsid[1]
        assert fema[1].claimCount is not None
        assert fema[0].valid_id is True
        assert fema[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [19055950100]
        fema = fs.fema.get_nfip(fsid, "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [19055950100, 19153003200]
        fema = fs.fema.get_nfip(fsid, "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 2
        fema.sort(key=lambda x: x.fsid)
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[1].fsid == fsid[1]
        assert fema[1].claimCount is not None
        assert fema[0].valid_id is True
        assert fema[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [19055950100, 00000000000]
        fema = fs.fema.get_nfip(fsid, "tract")
        assert len(fema) == 2
        fema.sort(key=lambda x: x.fsid, reverse=True)
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[1].fsid == fsid[1]
        assert fema[1].claimCount is None
        assert fema[0].valid_id is True
        assert fema[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [19055950100, 00000000000]
        fema = fs.fema.get_nfip(fsid, "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 2
        fema.sort(key=lambda x: x.fsid, reverse=True)
        assert fema[0].fsid == fsid[0]
        assert fema[0].claimCount is not None
        assert fema[1].fsid == fsid[1]
        assert fema[1].claimCount is None
        assert fema[0].valid_id is True
        assert fema[1].valid_id is False
        
    def test_coordinate_invalid(self, tmpdir):
        fema = fs.fema.get_nfip([(82.487671, -62.374322)], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is None
        assert fema[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        fema = fs.fema.get_nfip([(40.7079652311, -74.0021455387)], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is not None
        assert fema[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        fema = fs.fema.get_nfip(["Shimik, Nunavut"], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is None
        assert fema[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        fema = fs.fema.get_nfip(["Toronto, Ontario, Canada"], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is None
        assert fema[0].valid_id is False

    def test_single_address(self, tmpdir):
        fema = fs.fema.get_nfip(["247 Water St, New York, New York"], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is not None
        assert fema[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        fema = fs.fema.get_nfip([44074], "zcta", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].valid_id is True
        assert fema[0].fsid == 44074
        assert fema[0].claimCount is not None
        assert fema[0].policyCount is not None
        assert fema[0].buildingPaid is not None
        assert fema[0].contentPaid is not None
        assert fema[0].buildingCoverage is not None
        assert fema[0].contentCoverage is not None
        assert fema[0].iccPaid is not None
        fema = fs.fema.get_nfip([39013012300], "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].valid_id is True
        assert fema[0].fsid == 39013012300
        assert fema[0].claimCount is not None
        assert fema[0].policyCount is not None
        assert fema[0].buildingPaid is not None
        assert fema[0].contentPaid is not None
        assert fema[0].buildingCoverage is not None
        assert fema[0].contentCoverage is not None
        assert fema[0].iccPaid is not None
        fema = fs.fema.get_nfip([39093], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].valid_id is True
        assert fema[0].fsid == 39093
        assert fema[0].claimCount is not None
        assert fema[0].policyCount is not None
        assert fema[0].buildingPaid is not None
        assert fema[0].contentPaid is not None
        assert fema[0].buildingCoverage is not None
        assert fema[0].contentCoverage is not None
        assert fema[0].iccPaid is not None
        fema = fs.fema.get_nfip([39], "state", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].valid_id is True
        assert fema[0].fsid == 39
        assert fema[0].claimCount is not None
        assert fema[0].policyCount is not None
        assert fema[0].buildingPaid is not None
        assert fema[0].contentPaid is not None
        assert fema[0].buildingCoverage is not None
        assert fema[0].contentCoverage is not None
        assert fema[0].iccPaid is not None
