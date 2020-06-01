import pytest

import firststreet
from firststreet.errors import InvalidArgument

fs = firststreet.FirstStreet("api-key")


class TestLocationDetail:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_detail_by_fsids([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(TypeError):
            fs.location.get_detail_by_fsids(190836953, "property")

    def test_incorrect_lookup_type(self):
        location = fs.location.get_detail_by_fsids([190836953], "city", csv=True)
        assert len(location) == 0

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_detail_by_fsids([190836953], 190)

    def test_single(self):
        location = fs.location.get_detail_by_fsids([190836953], "property")
        assert len(location) == 1

    def test_multiple(self):
        location = fs.location.get_detail_by_fsids([190836953, 193139123], "property")
        assert len(location) == 2

    def test_single_csv(self):
        location = fs.location.get_detail_by_fsids([190836953], "property", csv=True)
        assert len(location) == 1

    def test_multiple_csv(self):
        location = fs.location.get_detail_by_fsids([190836953, 193139123], "property", csv=True)
        assert len(location) == 2


class TestLocationSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.location.get_summary_by_fsids([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(TypeError):
            fs.location.get_summary_by_fsids(190836953, "property")

    def test_incorrect_lookup_type(self):
        location = fs.location.get_summary_by_fsids([190836953], "city", csv=True)
        assert len(location) == 0

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_summary_by_fsids([190836953], 190)

    def test_single(self):
        location = fs.location.get_summary_by_fsids([190836953], "property")
        assert len(location) == 1

    def test_multiple(self):
        location = fs.location.get_summary_by_fsids([190836953, 193139123], "property")
        assert len(location) == 2

    def test_single_csv(self):
        location = fs.location.get_summary_by_fsids([190836953], "property", csv=True)
        assert len(location) == 1

    def test_multiple_csv(self):
        location = fs.location.get_summary_by_fsids([190836953, 193139123], "property", csv=True)
        assert len(location) == 2
