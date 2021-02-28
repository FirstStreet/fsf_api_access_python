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


class TestAALProperty:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.aal.get_summary([], "property")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.aal.get_summary(80000002, "property")

    def test_invalid_fsid(self):
        fsid = [00000000]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is None
        assert aal[0].annual_loss is None

    def test_not_property_fsid(self):
        fsid = [12]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is None
        assert aal[0].annual_loss is None

    def test_commercial_fsid(self):
        fsid = [1200171414]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is None
        assert aal[0].annual_loss is None

    def test_single(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_avm_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"avm": 150000})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_depths_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"depths": [30]})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_basement_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"basement": True})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_floor_elevation_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"floorElevation": 22})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_units_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"units": 2})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_single_stories_param(self):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", extra_param={"stories": 1})
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_multiple(self):
        fsid = [10000115, 80000002]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 2
        aal.sort(key=lambda x: x.fsid)
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None
        assert aal[1].fsid == str(fsid[1])
        assert aal[1].depth_loss is not None
        assert aal[1].annual_loss is not None

    def test_single_csv(self, tmpdir):
        fsid = [80000002]
        aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None

    def test_multiple_csv(self, tmpdir):
        fsid = [10000115, 80000002]
        aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(aal) == 2
        aal.sort(key=lambda x: x.fsid)
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None
        assert aal[1].fsid == str(fsid[1])
        assert aal[1].depth_loss is not None
        assert aal[1].annual_loss is not None

    def test_mixed_invalid(self):
        fsid = [0000000000, 80000002]
        aal = fs.aal.get_summary(fsid, "property")
        assert len(aal) == 2
        aal.sort(key=lambda x: x.fsid)
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is None
        assert aal[0].annual_loss is None
        assert aal[1].fsid == str(fsid[1])
        assert aal[1].depth_loss is not None
        assert aal[1].annual_loss is not None

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [0000000000, 80000002]
        aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(aal) == 2
        aal.sort(key=lambda x: x.fsid)
        assert aal[0].fsid == str(fsid[0])
        assert aal[0].depth_loss is None
        assert aal[0].annual_loss is None
        assert aal[1].fsid == str(fsid[1])
        assert aal[1].depth_loss is not None
        assert aal[1].annual_loss is not None

    def test_one_of_each(self, tmpdir):
        aal = fs.aal.get_summary([1200000342], "property", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "1200000342"
        assert aal[0].depth_loss is not None
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([1206631], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "1206631"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([3915406], "city", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "3915406"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([44654], "zcta", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "44654"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([39151712602], "tract", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "39151712602"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([39077], "county", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "39077"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([3904], "cd", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "3904"
        assert aal[0].annual_loss is not None
        aal = fs.aal.get_summary([39], "state", csv=True, output_dir=tmpdir)
        assert len(aal) == 1
        assert aal[0].fsid == "39"
        assert aal[0].annual_loss is not None
