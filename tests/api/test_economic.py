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


# class TestAALProperty:
#
#     def test_empty(self):
#         with pytest.raises(InvalidArgument):
#             fs.aal.get_summary([], "property")
#
#     def test_wrong_fsid_type(self):
#         with pytest.raises(InvalidArgument):
#             fs.aal.get_summary(80000002, "property")
#
#     def test_invalid_fsid(self):
#         fsid = [00000000]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is None
#         assert aal[0].annual_loss is None
#
#     def test_not_property_fsid(self):
#         fsid = [12]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is None
#         assert aal[0].annual_loss is None
#
#     def test_commercial_fsid(self):
#         fsid = [1200171414]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is None
#         assert aal[0].annual_loss is None
#
#     def test_single(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_avm_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"avm": 150000})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_depths_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"depths": [30]})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_basement_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"basement": True})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_floor_elevation_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"floorElevation": 22})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_units_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"units": 2})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_single_stories_param(self):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", extra_param={"stories": 1})
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_multiple(self):
#         fsid = [10000115, 80000002]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 2
#         aal.sort(key=lambda x: x.fsid)
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#         assert aal[1].fsid == str(fsid[1])
#         assert aal[1].depth_loss is not None
#         assert aal[1].annual_loss is not None
#
#     def test_single_csv(self, tmpdir):
#         fsid = [80000002]
#         aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#
#     def test_multiple_csv(self, tmpdir):
#         fsid = [10000115, 80000002]
#         aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
#         assert len(aal) == 2
#         aal.sort(key=lambda x: x.fsid)
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#         assert aal[1].fsid == str(fsid[1])
#         assert aal[1].depth_loss is not None
#         assert aal[1].annual_loss is not None
#
#     def test_mixed_invalid(self):
#         fsid = [0000000000, 80000002]
#         aal = fs.aal.get_summary(fsid, "property")
#         assert len(aal) == 2
#         aal.sort(key=lambda x: x.fsid)
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is None
#         assert aal[0].annual_loss is None
#         assert aal[1].fsid == str(fsid[1])
#         assert aal[1].depth_loss is not None
#         assert aal[1].annual_loss is not None
#
#     def test_mixed_invalid_csv(self, tmpdir):
#         fsid = [0000000000, 80000002]
#         aal = fs.aal.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
#         assert len(aal) == 2
#         aal.sort(key=lambda x: x.fsid)
#         assert aal[0].fsid == str(fsid[0])
#         assert aal[0].depth_loss is None
#         assert aal[0].annual_loss is None
#         assert aal[1].fsid == str(fsid[1])
#         assert aal[1].depth_loss is not None
#         assert aal[1].annual_loss is not None
#
#     def test_one_of_each(self, tmpdir):
#         aal = fs.aal.get_summary([1200000342], "property", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "1200000342"
#         assert aal[0].depth_loss is not None
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([1206631], "neighborhood", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "1206631"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([3915406], "city", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "3915406"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([44654], "zcta", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "44654"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([39151712602], "tract", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "39151712602"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([39077], "county", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "39077"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([3904], "cd", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "3904"
#         assert aal[0].annual_loss is not None
#         aal = fs.aal.get_summary([39], "state", csv=True, output_dir=tmpdir)
#         assert len(aal) == 1
#         assert aal[0].fsid == "39"
#         assert aal[0].annual_loss is not None
#
#
# class TestAVMProperty:
#
#     def test_empty(self):
#         with pytest.raises(InvalidArgument):
#             fs.avm.get_avm([])
#
#     def test_wrong_fsid_type(self):
#         with pytest.raises(InvalidArgument):
#             fs.avm.get_avm(2739)
#
#     def test_invalid(self):
#         fsid = [0000]
#         avm = fs.avm.get_avm(fsid)
#         assert len(avm) == 1
#         assert avm[0].fsid == str(fsid[0])
#         assert avm[0].provider_id is None
#         assert avm[0].valid_id is False
#         assert avm[0].avm is None
#
#     def test_single(self):
#         fsid = [1200171414]
#         avm = fs.avm.get_avm(fsid)
#         assert len(avm) == 1
#         assert avm[0].fsid == str(fsid[0])
#         assert avm[0].avm['mid'] >= 0
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#
#     def test_multiple(self):
#         fsid = [1200000342, 1200171414]
#         avm = fs.avm.get_avm(fsid)
#         assert len(avm) == 2
#         avm.sort(key=lambda x: x.fsid)
#         assert avm[0].fsid == str(fsid[0])
#         assert avm[0].avm['mid'] >= 0
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#         assert avm[1].fsid == str(fsid[1])
#         assert avm[1].avm['mid'] >= 0
#         assert avm[1].provider_id == 2
#         assert avm[1].valid_id is True
#
#     def test_single_csv(self, tmpdir):
#         fsid = [1200000342]
#         avm = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
#         assert len(avm) == 1
#         assert avm[0].fsid == str(fsid[0])
#         assert avm[0].avm['mid'] >= 0
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#
#     def test_multiple_csv(self, tmpdir):
#         fsid = [1200000342, 1200171414]
#         avm = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
#         assert len(avm) == 2
#         avm.sort(key=lambda x: x.fsid)
#         assert avm[0].fsid == str(fsid[0])
#         assert avm[0].avm['mid'] >= 0
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#         assert avm[1].fsid == str(fsid[1])
#         assert avm[1].avm['mid'] >= 0
#         assert avm[1].provider_id == 2
#         assert avm[1].valid_id is True
#
#     def test_mixed_invalid(self):
#         fsid = [0000000000, 1200000342]
#         avm_out = fs.avm.get_avm(fsid)
#         assert len(avm_out) == 2
#         avm_out.sort(key=lambda x: x.fsid)
#         assert avm_out[0].fsid == str(fsid[0])
#         assert avm_out[0].provider_id is None
#         assert avm_out[0].valid_id is False
#         assert avm_out[0].avm is None
#         assert avm_out[1].fsid == str(fsid[1])
#         assert avm_out[1].avm['mid'] >= 0
#         assert avm_out[1].provider_id == 2
#         assert avm_out[1].valid_id is True
#
#     def test_mixed_invalid_csv(self, tmpdir):
#         fsid = [0000000000, 1200000342]
#         avm_out = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
#         assert len(avm_out) == 2
#         avm_out.sort(key=lambda x: x.fsid)
#         assert avm_out[0].fsid == str(fsid[0])
#         assert avm_out[0].provider_id is None
#         assert avm_out[0].valid_id is False
#         assert avm_out[0].avm is None
#         assert avm_out[1].fsid == str(fsid[1])
#         assert avm_out[1].avm['mid'] >= 0
#         assert avm_out[1].provider_id == 2
#         assert avm_out[1].valid_id is True
#
#     def test_one_of_each(self, tmpdir):
#         avm = fs.avm.get_avm([1200000342], csv=True, output_dir=tmpdir)
#         assert len(avm) == 1
#         assert avm[0].fsid == "1200000342"
#         assert avm[0].avm['mid'] >= 0
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#
#
# class TestAVMProvider:
#
#     def test_empty(self):
#         with pytest.raises(InvalidArgument):
#             fs.avm.get_provider([])
#
#     def test_wrong_provider_id_type(self):
#         with pytest.raises(InvalidArgument):
#             fs.avm.get_provider(2)
#
#     def test_invalid(self):
#         provider_id = [999]
#         avm = fs.avm.get_provider(provider_id)
#         assert len(avm) == 1
#         assert avm[0].provider_id == provider_id[0]
#         assert avm[0].valid_id is False
#         assert avm[0].provider_logo is None
#         assert avm[0].provider_name is None
#
#     def test_single(self):
#         provider_id = [2]
#         avm = fs.avm.get_provider(provider_id)
#         assert len(avm) == 1
#         assert avm[0].provider_id == provider_id[0]
#         assert avm[0].valid_id is True
#         assert avm[0].provider_logo == ""
#         assert avm[0].provider_name == "First Street Foundation"
#
#     def test_single_csv(self, tmpdir):
#         provider_id = [2]
#         avm = fs.avm.get_provider(provider_id, csv=True, output_dir=tmpdir)
#         assert len(avm) == 1
#         assert avm[0].provider_id == provider_id[0]
#         assert avm[0].valid_id is True
#         assert avm[0].provider_logo == ""
#         assert avm[0].provider_name == "First Street Foundation"
#
#     def test_mixed_invalid(self):
#         provider_id = [2, 3]
#         avm = fs.avm.get_provider(provider_id)
#         assert len(avm) == 2
#         avm.sort(key=lambda x: x.provider_id)
#         assert avm[0].provider_id == provider_id[0]
#         assert avm[0].valid_id is True
#         assert avm[0].provider_logo == ""
#         assert avm[0].provider_name == "First Street Foundation"
#         assert avm[1].provider_id == provider_id[1]
#         assert avm[1].valid_id is False
#         assert avm[1].provider_logo is None
#         assert avm[1].provider_name is None
#
#     def test_mixed_invalid_csv(self, tmpdir):
#         provider_id = [2, 3]
#         avm = fs.avm.get_provider(provider_id, csv=True, output_dir=tmpdir)
#         assert len(avm) == 2
#         avm.sort(key=lambda x: x.provider_id)
#         assert avm[0].provider_id == provider_id[0]
#         assert avm[0].valid_id is True
#         assert avm[0].provider_logo == ""
#         assert avm[0].provider_name == "First Street Foundation"
#         assert avm[1].provider_id == provider_id[1]
#         assert avm[1].valid_id is False
#         assert avm[1].provider_logo is None
#         assert avm[1].provider_name is None
#
#     def test_one_of_each(self, tmpdir):
#         avm = fs.avm.get_provider([2], csv=True, output_dir=tmpdir)
#         assert len(avm) == 1
#         assert avm[0].provider_id == 2
#         assert avm[0].valid_id is True
#         assert avm[0].provider_logo == ""
#         assert avm[0].provider_name == "First Street Foundation"


class TestEconomicPropertyNFIP:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.economic.get_property_nfip([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.economic.get_property_nfip(18)

    def test_invalid(self):
        fsid = [0000000]
        nfip = fs.economic.get_property_nfip(fsid)
        assert len(nfip) == 1
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[0].data is None
        assert nfip[0].valid_id is False

    def test_single(self):
        fsid = [190836953]
        nfip = fs.economic.get_property_nfip(fsid)
        assert len(nfip) == 1
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        nfip = fs.economic.get_property_nfip(fsid)
        assert len(nfip) == 2
        nfip.sort(key=lambda x: x.fsid)
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[1].fsid == str(fsid[1])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True
        assert nfip[1].data is not None
        assert nfip[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        nfip = fs.economic.get_property_nfip(fsid, csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        nfip = fs.economic.get_property_nfip(fsid, csv=True, output_dir=tmpdir)
        assert len(nfip) == 2
        nfip.sort(key=lambda x: x.fsid)
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[1].fsid == str(fsid[1])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True
        assert nfip[1].data is not None
        assert nfip[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        nfip = fs.economic.get_property_nfip(fsid)
        assert len(nfip) == 2
        nfip.sort(key=lambda x: x.fsid, reverse=True)
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[1].fsid == str(fsid[1])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True
        assert nfip[1].data is None
        assert nfip[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        nfip = fs.economic.get_property_nfip(fsid, csv=True, output_dir=tmpdir)
        assert len(nfip) == 2
        nfip.sort(key=lambda x: x.fsid, reverse=True)
        assert nfip[0].fsid == str(fsid[0])
        assert nfip[1].fsid == str(fsid[1])
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True
        assert nfip[1].data is None
        assert nfip[1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        nfip = fs.economic.get_property_nfip([(82.487671, -62.374322)], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].data is None
        assert nfip[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        nfip = fs.economic.get_property_nfip([(40.7079652311, -74.0021455387)], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        nfip = fs.economic.get_property_nfip(["Shimik, Nunavut, Canada"], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].data is None
        assert nfip[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        nfip = fs.economic.get_property_nfip(["Toronto, Ontario, Canada"], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].data is None
        assert nfip[0].valid_id is False

    def test_single_address(self, tmpdir):
        nfip = fs.economic.get_property_nfip(["247 Water St, New York, New York"], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].data is not None
        assert nfip[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        nfip = fs.economic.get_property_nfip([390000257], csv=True, output_dir=tmpdir)
        assert len(nfip) == 1
        assert nfip[0].valid_id is True
        assert nfip[0].fsid == "390000257"
        assert nfip[0].data is not None
