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


class TestLocationDetail:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail(190836953, "property")

    def test_wrong_fsid_number(self):
        fsid = [1867176]
        location = fs.location.get_detail(fsid, "property")
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].state is None
        assert location[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [190836953]
        location = fs.location.get_detail(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].name is None
        assert location[0].valid_id is False

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_detail([190836953], 190)

    def test_single(self):
        fsid = [190836953]
        location = fs.location.get_detail(fsid, "property")
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].state is not None
        assert location[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        location = fs.location.get_detail(fsid, "property")
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].state is not None
        assert location[1].state is not None
        assert location[0].valid_id is True
        assert location[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        location = fs.location.get_detail(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].state is not None
        assert location[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        location = fs.location.get_detail(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].state is not None
        assert location[1].state is not None
        assert location[0].valid_id is True
        assert location[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        location = fs.location.get_detail(fsid, "property")
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid, reverse=True)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].state is not None
        assert location[1].state is None
        assert location[0].valid_id is True
        assert location[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        location = fs.location.get_detail(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid, reverse=True)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].state is not None
        assert location[1].state is None
        assert location[0].valid_id is True
        assert location[1].valid_id is False
    
    def test_coordinate_invalid(self, tmpdir):
        location = fs.location.get_detail([(82.487671, -62.374322)], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].state is None
        assert location[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        location = fs.location.get_detail([(40.7079652311, -74.0021455387)], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].state is not None
        assert location[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        location = fs.location.get_detail(["Shimik, Nunavut"], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].state is None
        assert location[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        location = fs.location.get_detail(["Toronto, Ontario, Canada"], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].state is None
        assert location[0].valid_id is False

    def test_single_address(self, tmpdir):
        location = fs.location.get_detail(["247 Water St, New York, New York"], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].state is not None
        assert location[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        location = fs.location.get_detail([511447411], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 511447411
        assert location[0].streetNumber is not None
        assert location[0].route is not None
        assert location[0].city is not None
        assert location[0].zipCode is not None
        assert location[0].zcta is not None
        assert location[0].neighborhood is not None
        assert location[0].tract is not None
        assert location[0].county is not None
        assert location[0].cd is not None
        assert location[0].state is not None
        assert location[0].footprintId is None
        assert location[0].elevation is not None
        assert location[0].fema is None
        assert location[0].geometry is None
        location = fs.location.get_detail([1206631], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 1206631
        assert location[0].city is not None
        assert location[0].name is not None
        assert location[0].subtype is not None
        assert location[0].county is not None
        assert location[0].state is not None
        assert location[0].geometry is None
        location = fs.location.get_detail([3915406], "city", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 3915406
        assert location[0].name is not None
        assert location[0].lsad is not None
        assert location[0].zcta is not None
        assert location[0].neighborhood is not None
        assert location[0].county is not None
        assert location[0].state is not None
        assert location[0].geometry is not None
        location = fs.location.get_detail([44654], "zcta", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 44654
        assert location[0].name is not None
        assert location[0].county is not None
        assert location[0].city is not None
        assert location[0].state is not None
        assert location[0].geometry is not None
        location = fs.location.get_detail([39151712602], "tract", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fips == "39151712602"
        assert location[0].county is not None
        assert location[0].state is not None
        assert location[0].geometry is not None
        location = fs.location.get_detail([39077], "county", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 39077
        assert location[0].fips is not None
        assert location[0].name is not None
        assert location[0].isCoastal is not None
        assert location[0].city is not None
        assert location[0].zcta is not None
        assert location[0].cd is not None
        assert location[0].state is not None
        assert location[0].geometry is not None
        location = fs.location.get_detail([3904], "cd", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 3904
        assert location[0].district is not None
        assert location[0].congress is not None
        assert location[0].county is not None
        assert location[0].state is not None
        assert location[0].geometry is not None
        location = fs.location.get_detail([39], "state", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 39
        assert location[0].name is not None
        assert location[0].fips is not None
        assert location[0].geometry is not None


class TestLocationSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_summary([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_summary([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_summary([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_summary(190836953, "property")

    def test_wrong_fsid_number(self):
        fsid = [1867176]
        location = fs.location.get_summary(fsid, "property")
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].adaptation is None
        assert location[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [190836953]
        location = fs.location.get_summary(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].adaptation is None
        assert location[0].valid_id is False

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_summary([190836953], 190)

    def test_single(self):
        fsid = [190836953]
        location = fs.location.get_summary(fsid, "property")
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].adaptation is not None
        assert location[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        location = fs.location.get_summary(fsid, "property")
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].adaptation is not None
        assert location[1].adaptation is not None
        assert location[0].valid_id is True
        assert location[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        location = fs.location.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].fsid == fsid[0]
        assert location[0].adaptation is not None
        assert location[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        location = fs.location.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].adaptation is not None
        assert location[1].adaptation is not None
        assert location[0].valid_id is True
        assert location[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        location = fs.location.get_summary(fsid, "property")
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid, reverse=True)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].adaptation is not None
        assert location[1].adaptation is None
        assert location[0].valid_id is True
        assert location[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        location = fs.location.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(location) == 2
        location.sort(key=lambda x: x.fsid, reverse=True)
        assert location[0].fsid == fsid[0]
        assert location[1].fsid == fsid[1]
        assert location[0].adaptation is not None
        assert location[1].adaptation is None
        assert location[0].valid_id is True
        assert location[1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        location = fs.location.get_summary([(82.487671, -62.374322)], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].adaptation is None
        assert location[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        location = fs.location.get_summary([(40.7079652311, -74.0021455387)], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].adaptation is not None
        assert location[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        location = fs.location.get_summary(["Shimik, Nunavut"], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].adaptation is None
        assert location[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        location = fs.location.get_summary(["Toronto, Ontario, Canada"], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].adaptation is None
        assert location[0].valid_id is False

    def test_single_address(self, tmpdir):
        location = fs.location.get_summary(["247 Water St, New York, New York"], "property",
                                           csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].adaptation is not None
        assert location[0].valid_id is True
        
    def test_one_of_each(self, tmpdir):
        location = fs.location.get_summary([395112095], "property", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 395112095
        assert location[0].floodFactor is not None
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        location = fs.location.get_summary([631054], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 631054
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([3958002], "city", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 3958002
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([43935], "zcta", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 43935
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([39153531702], "tract", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 39153531702
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([39027], "county", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 39027
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([3903], "cd", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 3903
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
        location = fs.location.get_summary([39], "state", csv=True, output_dir=tmpdir)
        assert len(location) == 1
        assert location[0].valid_id is True
        assert location[0].fsid == 39
        assert location[0].riskDirection is not None
        assert location[0].historic is not None
        assert location[0].environmentalRisk is not None
        assert location[0].adaptation is not None
        assert location[0].properties is not None
        assert location[0].properties.get("total") is not None
        assert location[0].properties.get("atRisk") is not None
