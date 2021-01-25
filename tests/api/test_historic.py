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


class TestHistoricEvent:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_event([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_event("9")

    def test_invalid(self):
        event_id = [0000]
        historic = fs.historic.get_event(event_id)
        assert len(historic) == 1
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is None
        assert historic[0].valid_id is False

    def test_single(self):
        event_id = [9]
        historic = fs.historic.get_event(event_id)
        assert len(historic) == 1
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[0].valid_id is True

    def test_multiple(self):
        event_id = [13, 14]
        historic = fs.historic.get_event(event_id)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.eventId)
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[1].eventId == str(event_id[1])
        assert historic[1].properties is not None
        assert historic[0].valid_id is True
        assert historic[1].valid_id is True

    def test_single_csv(self, tmpdir):
        event_id = [9]
        historic = fs.historic.get_event(event_id, csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        event_id = [13, 14]
        historic = fs.historic.get_event(event_id, csv=True, output_dir=tmpdir)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.eventId)
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[1].eventId == str(event_id[1])
        assert historic[1].properties is not None
        assert historic[0].valid_id is True
        assert historic[1].valid_id is True

    def test_mixed_invalid(self):
        event_id = [9, 0]
        historic = fs.historic.get_event(event_id)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.eventId, reverse=True)
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[1].eventId == str(event_id[1])
        assert not historic[1].properties
        assert historic[0].valid_id is True
        assert historic[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        event_id = [9, 0]
        historic = fs.historic.get_event(event_id, csv=True, output_dir=tmpdir)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.eventId, reverse=True)
        assert historic[0].eventId == str(event_id[0])
        assert historic[0].properties is not None
        assert historic[1].eventId == str(event_id[1])
        assert not historic[1].properties
        assert historic[0].valid_id is True
        assert historic[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        historic = fs.historic.get_event([2], csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].eventId == "2"
        assert historic[0].name is not None
        assert historic[0].type is not None
        assert historic[0].month is not None
        assert historic[0].year is not None
        assert historic[0].returnPeriod is not None
        assert historic[0].properties is not None
        assert historic[0].properties.get("total") is not None
        assert historic[0].properties.get("affected") is not None
        assert historic[0].geometry is not None


class TestHistoricSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_summary([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_summary([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_summary([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_summary(190836953, "property")

    def test_wrong_fsid_number(self):
        fsid = [1867176]
        historic = fs.historic.get_summary(fsid, "property")
        assert len(historic) == 1
        assert historic[0].fsid == str(fsid[0])
        assert not historic[0].historic
        assert historic[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [190836953]
        historic = fs.historic.get_summary(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].fsid == str(fsid[0])
        assert not historic[0].historic
        assert historic[0].valid_id is False

    def test_wrong_historic_type(self):
        with pytest.raises(TypeError):
            fs.historic.get_summary([190836953], 190)

    def test_single(self):
        fsid = [190836953]
        historic = fs.historic.get_summary(fsid, "property")
        assert len(historic) == 1
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        historic = fs.historic.get_summary(fsid, "property")
        assert len(historic) == 2
        historic.sort(key=lambda x: x.fsid)
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[1].fsid == str(fsid[1])
        assert historic[1].historic is not None
        assert historic[0].valid_id is True
        assert historic[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        historic = fs.historic.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        historic = fs.historic.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.fsid)
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[1].fsid == str(fsid[1])
        assert historic[1].historic is not None
        assert historic[0].valid_id is True
        assert historic[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        historic = fs.historic.get_summary(fsid, "property")
        assert len(historic) == 2
        historic.sort(key=lambda x: x.fsid, reverse=True)
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[1].fsid == str(fsid[1])
        assert not historic[1].historic
        assert historic[0].valid_id is True
        assert historic[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        historic = fs.historic.get_summary(fsid, "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 2
        historic.sort(key=lambda x: x.fsid, reverse=True)
        assert historic[0].fsid == str(fsid[0])
        assert historic[0].historic is not None
        assert historic[1].fsid == str(fsid[1])
        assert not historic[1].historic
        assert historic[0].valid_id is True
        assert historic[1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        historic = fs.historic.get_summary([(82.487671, -62.374322)], "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert not historic[0].historic
        assert historic[0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        historic = fs.historic.get_summary([(40.7079652311, -74.0021455387)], "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].historic is not None
        assert historic[0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        historic = fs.historic.get_summary(["Shimik, Nunavut, Canada"], "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert not historic[0].historic
        assert historic[0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        historic = fs.historic.get_summary(["Toronto, Ontario, Canada"], "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert not historic[0].historic
        assert historic[0].valid_id is False

    def test_single_address(self, tmpdir):
        historic = fs.historic.get_summary(["247 Water St, New York, New York"], "property",
                                           csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].historic is not None
        assert historic[0].valid_id is True

    def test_one_of_each(self, tmpdir):
        historic = fs.historic.get_summary([511447411], "property", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "511447411"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("depth") is not None
        historic = fs.historic.get_summary([540225], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "540225"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([1982200], "city", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "1982200"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([50156], "zcta", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "50156"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([19153004900], "tract", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "19153004900"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([19163], "county", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "19163"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([1901], "cd", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "1901"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None
        historic = fs.historic.get_summary([39], "state", csv=True, output_dir=tmpdir)
        assert len(historic) == 1
        assert historic[0].valid_id is True
        assert historic[0].fsid == "39"
        assert historic[0].historic is not None
        assert historic[0].historic[0].get("eventId") is not None
        assert historic[0].historic[0].get("name") is not None
        assert historic[0].historic[0].get("type") is not None
        assert historic[0].historic[0].get("data") is not None
        assert historic[0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0].historic[0].get("data")[0].get("count") is not None


class TestHistoricSummaryDetail:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_events_by_location([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_events_by_location([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_events_by_location([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_events_by_location(190836953, "city")

    def test_wrong_fsid_number(self):
        fsid = [11]
        historic = fs.historic.get_events_by_location([11], "city")
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].fsid == str(fsid[0])
        assert not historic[0][0].historic
        assert historic[0][0].valid_id is False
        assert not historic[1][0].properties
        assert historic[0][0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [1982200]
        historic = fs.historic.get_events_by_location(fsid, "state", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].fsid == str(fsid[0])
        assert not historic[0][0].historic
        assert historic[0][0].valid_id is False
        assert not historic[1][0].properties
        assert historic[0][0].valid_id is False

    def test_wrong_historic_type(self):
        with pytest.raises(TypeError):
            fs.historic.get_events_by_location([1982200], 190)

    def test_single(self):
        fsid = [1982200]
        historic = fs.historic.get_events_by_location(fsid, "city")
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True

    def test_multiple(self):
        fsid = [1982200, 3905074]
        historic = fs.historic.get_events_by_location(fsid, "city")
        assert len(historic[0]) == 2
        assert len(historic[1]) == 2
        historic[0].sort(key=lambda x: x.fsid)
        historic[1].sort(key=lambda x: x.eventId)
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[0][1].fsid == str(fsid[1])
        assert historic[0][1].historic is not None
        assert historic[1][0].properties is not None
        assert historic[1][1].properties is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][1].valid_id is True
        assert historic[1][1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [1982200]
        historic = fs.historic.get_events_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        historic[0].sort(key=lambda x: x.fsid)
        historic[1].sort(key=lambda x: x.eventId)
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [1982200, 3905074]
        historic = fs.historic.get_events_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 2
        assert len(historic[1]) == 2
        historic[0].sort(key=lambda x: x.fsid)
        historic[1].sort(key=lambda x: x.eventId)
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[0][1].fsid == str(fsid[1])
        assert historic[0][1].historic is not None
        assert historic[1][0].properties is not None
        assert historic[1][1].properties is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][1].valid_id is True
        assert historic[1][1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [1982200, 000000000]
        historic = fs.historic.get_events_by_location(fsid, "city")
        assert len(historic[0]) == 2
        assert len(historic[1]) == 1
        historic[0].sort(key=lambda x: x.fsid, reverse=True)
        historic[1].sort(key=lambda x: x.eventId, reverse=True)
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[0][1].fsid == str(fsid[1])
        assert not historic[0][1].historic
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [1982200, 000000000]
        historic = fs.historic.get_events_by_location(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 2
        assert len(historic[1]) == 1
        historic[0].sort(key=lambda x: x.fsid, reverse=True)
        historic[1].sort(key=lambda x: x.eventId, reverse=True)
        assert historic[0][0].fsid == str(fsid[0])
        assert historic[0][0].historic is not None
        assert historic[0][1].fsid == str(fsid[1])
        assert not historic[0][1].historic
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][1].valid_id is False

    def test_coordinate_invalid(self, tmpdir):
        historic = fs.historic.get_events_by_location([(82.487671, -62.374322)], "property",
                                                      csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert not historic[0][0].historic
        assert historic[0][0].valid_id is False
        assert not historic[1][0].properties
        assert historic[0][0].valid_id is False

    def test_single_coordinate(self, tmpdir):
        historic = fs.historic.get_events_by_location([(40.7079652311, -74.0021455387)], "property",
                                                      csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].historic is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True

    def test_address_invalid_404(self, tmpdir):
        historic = fs.historic.get_events_by_location(["Shimik, Nunavut, Canada"], "property",
                                                      csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert not historic[0][0].historic
        assert historic[0][0].valid_id is False
        assert not historic[1][0].properties
        assert historic[0][0].valid_id is False

    def test_address_invalid_500(self, tmpdir):
        historic = fs.historic.get_events_by_location(["Toronto, Ontario, Canada"], "property",
                                                      csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert not historic[0][0].historic
        assert historic[0][0].valid_id is False
        assert not historic[1][0].properties
        assert historic[0][0].valid_id is False

    def test_single_address(self, tmpdir):
        historic = fs.historic.get_events_by_location(["247 Water St, New York, New York"], "property",
                                                      csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].historic is not None
        assert historic[0][0].valid_id is True
        assert historic[1][0].properties is not None
        assert historic[0][0].valid_id is True

    def test_one_of_each(self, tmpdir):
        historic = fs.historic.get_events_by_location([511447411], "property", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 2
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "511447411"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("depth") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([540225], "neighborhood", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "540225"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([1982200], "city", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "1982200"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([50156], "zcta", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "50156"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([19153004900], "tract", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 2
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "19153004900"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([19163], "county", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 1
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "19163"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([1901], "cd", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 2
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "1901"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
        historic = fs.historic.get_events_by_location([39], "state", csv=True, output_dir=tmpdir)
        assert len(historic[0]) == 1
        assert len(historic[1]) == 4
        assert historic[0][0].valid_id is True
        assert historic[1][0].valid_id is True
        assert historic[0][0].fsid == "39"
        assert historic[0][0].historic is not None
        assert historic[0][0].historic[0].get("eventId") is not None
        assert historic[0][0].historic[0].get("name") is not None
        assert historic[0][0].historic[0].get("type") is not None
        assert historic[0][0].historic[0].get("data") is not None
        assert historic[0][0].historic[0].get("data")[0].get("bin") is not None
        assert historic[0][0].historic[0].get("data")[0].get("count") is not None
        assert historic[1][0].name is not None
        assert historic[1][0].type is not None
        assert historic[1][0].month is not None
        assert historic[1][0].year is not None
        assert historic[1][0].returnPeriod is not None
        assert historic[1][0].properties is not None
        assert historic[1][0].properties.get("total") is not None
        assert historic[1][0].properties.get("affected") is not None
        assert historic[1][0].geometry is not None
