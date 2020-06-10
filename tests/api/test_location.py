import os

import pytest

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
        with pytest.raises(TypeError):
            fs.location.get_detail(190836953, "property")

    def test_wrong_fsid_number(self):
        location = fs.location.get_detail([1867176], "property")
        assert len(location) == 1
        assert location[0].streetNumber is None

    def test_incorrect_lookup_type(self):
        location = fs.location.get_detail([190836953], "city", csv=True)
        assert len(location) == 1
        assert location[0].name is None

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_detail([190836953], 190)

    def test_single(self):
        location = fs.location.get_detail([190836953], "property")
        assert len(location) == 1

    def test_multiple(self):
        location = fs.location.get_detail([190836953, 193139123], "property")
        assert len(location) == 2

    def test_single_csv(self):
        location = fs.location.get_detail([190836953], "property", csv=True)
        assert len(location) == 1

    def test_multiple_csv(self):
        location = fs.location.get_detail([190836953, 193139123], "property", csv=True)
        assert len(location) == 2

    def test_mixed_invalid(self):
        location = fs.location.get_detail([190836953, 000000000], "property")
        assert len(location) == 2

    def test_mixed_invalid_csv(self):
        location = fs.location.get_detail([190836953, 000000000], "property", csv=True)
        assert len(location) == 2


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
        with pytest.raises(TypeError):
            fs.location.get_summary(190836953, "property")

    def test_wrong_fsid_number(self):
        location = fs.location.get_summary([1867176], "property")
        assert len(location) == 1
        assert location[0].adaptation is None

    def test_incorrect_lookup_type(self):
        location = fs.location.get_summary([190836953], "city", csv=True)
        assert len(location) == 1
        assert location[0].adaptation is None

    def test_wrong_location_type(self):
        with pytest.raises(TypeError):
            fs.location.get_summary([190836953], 190)

    def test_single(self):
        location = fs.location.get_summary([190836953], "property")
        assert len(location) == 1

    def test_multiple(self):
        location = fs.location.get_summary([190836953, 193139123], "property")
        assert len(location) == 2

    def test_single_csv(self):
        location = fs.location.get_summary([190836953], "property", csv=True)
        assert len(location) == 1

    def test_multiple_csv(self):
        location = fs.location.get_summary([190836953, 193139123], "property", csv=True)
        assert len(location) == 2

    def test_mixed_invalid(self):
        location = fs.location.get_summary([190836953, 000000000], "property")
        assert len(location) == 2

    def test_mixed_invalid_csv(self):
        location = fs.location.get_summary([190836953, 000000000], "property", csv=True)
        assert len(location) == 2
