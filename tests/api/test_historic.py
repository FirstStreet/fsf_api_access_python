import os

import pytest

import firststreet
from firststreet.errors import InvalidArgument

api_key = os.environ['FSF_API_KEY']
fs = firststreet.FirstStreet(api_key)


class TestHistoricEvent:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.historic.get_event([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(TypeError):
            fs.historic.get_event(9)

    def test_single(self):
        historic = fs.historic.get_event([9])
        assert len(historic) == 1

    def test_multiple(self):
        historic = fs.historic.get_event([9, 13])
        assert len(historic) == 2

    def test_single_csv(self):
        historic = fs.historic.get_event([9], csv=True)
        assert len(historic) == 1

    def test_multiple_csv(self):
        historic = fs.historic.get_event([9, 13], csv=True)
        assert len(historic) == 2

    def test_mixed_invalid(self):
        historic = fs.historic.get_event([9, 0])
        assert len(historic) == 2

    def test_mixed_invalid_csv(self):
        historic = fs.historic.get_event([9, 0], csv=True)
        assert len(historic) == 2


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
        with pytest.raises(TypeError):
            fs.historic.get_summary(190836953, "property")

    def test_wrong_fsid_number(self):
        historic = fs.historic.get_summary([1867176], "property")
        assert len(historic) == 1
        assert historic[0].historic is None

    def test_incorrect_lookup_type(self):
        historic = fs.historic.get_summary([190836953], "city", csv=True)
        assert len(historic) == 1
        assert historic[0].historic is None

    def test_wrong_historic_type(self):
        with pytest.raises(TypeError):
            fs.historic.get_summary([190836953], 190)

    def test_single(self):
        historic = fs.historic.get_summary([190836953], "property")
        assert len(historic) == 1

    def test_multiple(self):
        historic = fs.historic.get_summary([190836953, 193139123], "property")
        assert len(historic) == 2

    def test_single_csv(self):
        historic = fs.historic.get_summary([190836953], "property", csv=True)
        assert len(historic) == 1

    def test_multiple_csv(self):
        historic = fs.historic.get_summary([190836953, 193139123], "property", csv=True)
        assert len(historic) == 2

    def test_mixed_invalid(self):
        historic = fs.historic.get_summary([190836953, 000000000], "property")
        assert len(historic) == 2

    def test_mixed_invalid_csv(self):
        historic = fs.historic.get_summary([190836953, 000000000], "property", csv=True)
        assert len(historic) == 2
