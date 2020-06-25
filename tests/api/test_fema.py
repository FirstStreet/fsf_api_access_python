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
        fema = fs.fema.get_nfip([19027], "tract")
        assert len(fema) == 1
        assert fema[0].claimCount is None

    def test_incorrect_lookup_type(self, tmpdir):
        fema = fs.fema.get_nfip([19055950100], "county", csv=True, output_dir=tmpdir)
        assert len(fema) == 1
        assert fema[0].claimCount is None

    def test_wrong_fema_type(self):
        with pytest.raises(TypeError):
            fs.fema.get_nfip([19055950100], 190)

    def test_single(self):
        fema = fs.fema.get_nfip([19055950100], "tract")
        assert len(fema) == 1

    def test_multiple(self):
        fema = fs.fema.get_nfip([19055950100, 19153003200], "tract")
        assert len(fema) == 2

    def test_single_csv(self, tmpdir):
        fema = fs.fema.get_nfip([19055950100], "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 1

    def test_multiple_csv(self, tmpdir):
        fema = fs.fema.get_nfip([19055950100, 19153003200], "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 2

    def test_mixed_invalid(self):
        fema = fs.fema.get_nfip([19055950100, 19153003200], "tract")
        assert len(fema) == 2

    def test_mixed_invalid_csv(self, tmpdir):
        fema = fs.fema.get_nfip([19055950100, 19153003200], "tract", csv=True, output_dir=tmpdir)
        assert len(fema) == 2
