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


class TestAdaptationDetail:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail(2739)

    def test_invalid(self):
        adaptation_id = [0000]
        adaptation = fs.adaptation.get_detail(adaptation_id)
        assert len(adaptation) == 1
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is None
        assert adaptation[0].valid_id is False

    def test_single(self):
        adaptation_id = [2739]
        adaptation = fs.adaptation.get_detail(adaptation_id)
        assert len(adaptation) == 1
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[0].valid_id is True

    def test_multiple(self):
        adaptation_id = [2739, 2741]
        adaptation = fs.adaptation.get_detail(adaptation_id)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.adaptationId)
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[1].adaptationId == str(adaptation_id[1])
        assert adaptation[1].type is not None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is True

    def test_single_csv(self, tmpdir):
        adaptation_id = [2739]
        adaptation = fs.adaptation.get_detail(adaptation_id, csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        adaptation_id = [2739, 2741]
        adaptation = fs.adaptation.get_detail(adaptation_id, csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.adaptationId)
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[1].adaptationId == str(adaptation_id[1])
        assert adaptation[1].type is not None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is True

    def test_mixed_invalid(self):
        adaptation_id = [2739, 0000]
        adaptation = fs.adaptation.get_detail(adaptation_id)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[1].adaptationId == str(adaptation_id[1])
        assert adaptation[1].type is None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        adaptation_id = [2739, 0000]
        adaptation = fs.adaptation.get_detail(adaptation_id, csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0].adaptationId == str(adaptation_id[0])
        assert adaptation[0].type is not None
        assert adaptation[1].adaptationId == str(adaptation_id[1])
        assert adaptation[1].type is None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        adaptation = fs.adaptation.get_detail([29], csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].adaptationId == "29"
        assert adaptation[0].name is not None
        assert adaptation[0].type is not None
        assert adaptation[0].scenario is not None
        assert adaptation[0].conveyance is not None
        assert adaptation[0].returnPeriod is not None
        assert adaptation[0].serving is not None
        assert adaptation[0].serving.get("property") is not None
        assert adaptation[0].serving.get("neighborhood") is not None
        assert adaptation[0].serving.get("zcta") is not None
        assert adaptation[0].serving.get("tract") is not None
        assert adaptation[0].serving.get("city") is not None
        assert adaptation[0].serving.get("county") is not None
        assert adaptation[0].serving.get("cd") is not None
        assert adaptation[0].serving.get("state") is not None
        assert adaptation[0].geometry is not None


class TestAdaptationSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_summary([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_summary([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_summary([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_summary(190836953, "property")

    def test_wrong_fsid_number(self):
        fsid = [1867176]
        adaptation = fs.adaptation.get_summary(fsid, "property")
        assert len(adaptation) == 1
        assert adaptation[0].fsid == str(fsid[0])
        assert not adaptation[0].adaptation
        assert adaptation[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [190836953]
        adaptation = fs.adaptation.get_summary(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].fsid == str(fsid[0])
        assert not adaptation[0].adaptation
        assert adaptation[0].valid_id is False

    def test_wrong_adaptation_type(self):
        with pytest.raises(TypeError):
            fs.adaptation.get_summary([395133768], 190)

    def test_single(self):
        fsid = [395133768]
        adaptation = fs.adaptation.get_summary(fsid, "property")
        assert len(adaptation) == 1
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[0].valid_id is True

    def test_multiple(self):
        fsid = [395133768, 193139123]
        adaptation = fs.adaptation.get_summary(fsid, "property")
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.fsid, reverse=True)
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[1].fsid == str(fsid[1])
        assert adaptation[1].adaptation is not None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [395133768]
        adaptation = fs.adaptation.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [395133768, 193139123]
        adaptation = fs.adaptation.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.fsid, reverse=True)
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[1].fsid == str(fsid[1])
        assert adaptation[1].adaptation is not None
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [395133768, 0000]
        adaptation = fs.adaptation.get_summary(fsid, "property")
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.fsid, reverse=True)
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[1].fsid == str(fsid[1])
        assert not adaptation[1].adaptation
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [395133768, 0000]
        adaptation = fs.adaptation.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2
        adaptation.sort(key=lambda x: x.fsid, reverse=True)
        assert adaptation[0].fsid == str(fsid[0])
        assert adaptation[0].adaptation is not None
        assert adaptation[1].fsid == str(fsid[1])
        assert not adaptation[1].adaptation
        assert adaptation[0].valid_id is True
        assert adaptation[1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        adaptation = fs.adaptation.get_summary([(41.70808, -72.860217)], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert not adaptation[0].adaptation
        assert adaptation[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        adaptation = fs.adaptation.get_summary([(40.7079652311, -74.0021455387)], "property",
                                               csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].adaptation is not None
        assert adaptation[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        adaptation = fs.adaptation.get_summary(["Shimik, Nunavut"], "property",
                                               csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert not adaptation[0].adaptation
        assert adaptation[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        adaptation = fs.adaptation.get_summary(["Toronto, Ontario, Canada"], "property",
                                               csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert not adaptation[0].adaptation
        assert adaptation[0].valid_id is False

    def test_single_address(self, tmpdir):
        adaptation = fs.adaptation.get_summary(["247 Water St, New York, New York"], "property",
                                               csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].adaptation is not None
        assert adaptation[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        adaptation = fs.adaptation.get_summary([395133768], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([7924], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([1935265], "city", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([50158], "zcta", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([39061007100], "tract", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([19047], "county", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([3915], "cd", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None
        adaptation = fs.adaptation.get_summary([39], "state", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].valid_id is True
        assert adaptation[0].properties is not None
        assert adaptation[0].adaptation is not None


class TestAdaptationSummaryDetail:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail_by_location([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail_by_location([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail_by_location([1935265], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.adaptation.get_detail_by_location(190836953, "city")

    def test_wrong_fsid_number(self):
        fsid = [11]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city")
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 1
        assert adaptation[0][0].fsid == str(fsid[0])
        assert not adaptation[0][0].adaptation
        assert not adaptation[1][0].type
        assert adaptation[0][0].valid_id is False
        assert adaptation[1][0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [1935265]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "state", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 1
        assert adaptation[0][0].fsid == str(fsid[0])
        assert not adaptation[0][0].adaptation
        assert not adaptation[1][0].type
        assert adaptation[0][0].valid_id is False
        assert adaptation[1][0].valid_id is False

    def test_wrong_adaptation_type(self):
        with pytest.raises(TypeError):
            fs.adaptation.get_detail_by_location([1935265], 190)

    def test_single(self):
        fsid = [1935265]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city")
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 2
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[1][0].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True

    def test_multiple(self):
        fsid = [1935265, 1714000]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city")
        assert len(adaptation[0]) == 2
        assert len(adaptation[1]) == 5
        adaptation[0].sort(key=lambda x: x.fsid, reverse=True)
        adaptation[1].sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][1].fsid == str(fsid[1])
        assert adaptation[0][1].adaptation is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][1].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[0][1].valid_id is True
        assert adaptation[1][1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [1935265]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 2
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[1][0].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [1935265, 1714000]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 2
        assert len(adaptation[1]) == 5
        adaptation[0].sort(key=lambda x: x.fsid, reverse=True)
        adaptation[1].sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][1].fsid == str(fsid[1])
        assert adaptation[0][1].adaptation is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][1].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[0][1].valid_id is True
        assert adaptation[1][1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [1935265, 000000000]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city")
        assert len(adaptation[0]) == 2
        assert len(adaptation[1]) == 2
        adaptation[0].sort(key=lambda x: x.fsid, reverse=True)
        adaptation[1].sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][1].fsid == str(fsid[1])
        assert not adaptation[0][1].adaptation
        assert adaptation[1][0].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[0][1].valid_id is False
        assert adaptation[1][1].valid_id is True

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [1935265, 000000000]
        adaptation = fs.adaptation.get_detail_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 2
        assert len(adaptation[1]) == 2
        adaptation[0].sort(key=lambda x: x.fsid, reverse=True)
        adaptation[1].sort(key=lambda x: x.adaptationId, reverse=True)
        assert adaptation[0][0].fsid == str(fsid[0])
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][1].fsid == str(fsid[1])
        assert not adaptation[0][1].adaptation
        assert adaptation[1][0].type is not None
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[0][1].valid_id is False
        assert adaptation[1][1].valid_id is True

    def test_coordinate_invalid(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location([(41.70808, -72.860217)], "property",
                                                          csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert not adaptation[0][0].adaptation
        assert adaptation[0][0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location([(40.7079652311, -74.0021455387)], "property",
                                                          csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location(["Shimik, Nunavut"], "property",
                                                          csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert not adaptation[0][0].adaptation
        assert adaptation[0][0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location(["Toronto, Ontario, Canada"], "property",
                                                          csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert not adaptation[0][0].adaptation
        assert adaptation[0][0].valid_id is False

    def test_single_address(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location(["247 Water St, New York, New York"], "property",
                                                          csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert adaptation[0][0].adaptation is not None
        assert adaptation[0][0].valid_id is True

    def test_one_of_each(self, tmpdir):
        adaptation = fs.adaptation.get_detail_by_location([395133768], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 1
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "395133768"
        assert adaptation[0][0].properties is None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([7924], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 6
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "7924"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([1935265], "city", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 2
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "1935265"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([50158], "zcta", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 4
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "50158"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([39061007100], "tract", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 1
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "39061007100"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([19047], "county", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 3
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "19047"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([3915], "cd", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 5
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "3915"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
        adaptation = fs.adaptation.get_detail_by_location([39], "state", csv=True, output_dir=tmpdir)
        assert len(adaptation[0]) == 1
        assert len(adaptation[1]) == 299
        assert adaptation[0][0].valid_id is True
        assert adaptation[1][0].valid_id is True
        assert adaptation[1][0].name is not None
        assert adaptation[1][0].type is not None
        assert adaptation[1][0].scenario is not None
        assert adaptation[1][0].conveyance is not None
        assert adaptation[1][0].returnPeriod is not None
        assert adaptation[1][0].serving is not None
        assert adaptation[1][0].serving.get("property") is not None
        assert adaptation[1][0].serving.get("neighborhood") is not None
        assert adaptation[1][0].serving.get("zcta") is not None
        assert adaptation[1][0].serving.get("tract") is not None
        assert adaptation[1][0].serving.get("city") is not None
        assert adaptation[1][0].serving.get("county") is not None
        assert adaptation[1][0].serving.get("cd") is not None
        assert adaptation[1][0].serving.get("state") is not None
        assert adaptation[1][0].geometry is not None
        assert adaptation[0][0].fsid == "39"
        assert adaptation[0][0].properties is not None
        assert adaptation[0][0].adaptation is not None
