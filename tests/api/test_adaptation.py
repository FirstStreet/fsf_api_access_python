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

    def test_single(self):
        adaptation = fs.adaptation.get_detail([2739])
        assert len(adaptation) == 1

    def test_multiple(self):
        adaptation = fs.adaptation.get_detail([2739, 2741])
        assert len(adaptation) == 2

    def test_single_csv(self, tmpdir):
        adaptation = fs.adaptation.get_detail([2739], csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1

    def test_multiple_csv(self, tmpdir):
        adaptation = fs.adaptation.get_detail([2739, 2741], csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2

    def test_mixed_invalid(self):
        adaptation = fs.adaptation.get_detail([2739, 0000])
        assert len(adaptation) == 2

    def test_mixed_invalid_csv(self, tmpdir):
        adaptation = fs.adaptation.get_detail([2739, 0000], csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2


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
        adaptation = fs.adaptation.get_summary([1867176], "property")
        assert len(adaptation) == 1
        assert adaptation[0].adaptation is None

    def test_incorrect_lookup_type(self, tmpdir):
        adaptation = fs.adaptation.get_summary([190836953], "city", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1
        assert adaptation[0].adaptation is None

    def test_wrong_adaptation_type(self):
        with pytest.raises(TypeError):
            fs.adaptation.get_summary([190836953], 190)

    def test_single(self):
        adaptation = fs.adaptation.get_summary([190836953], "property")
        assert len(adaptation) == 1

    def test_multiple(self):
        adaptation = fs.adaptation.get_summary([190836953, 193139123], "property")
        assert len(adaptation) == 2

    def test_single_csv(self, tmpdir):
        adaptation = fs.adaptation.get_summary([190836953], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 1

    def test_multiple_csv(self, tmpdir):
        adaptation = fs.adaptation.get_summary([395133768, 193139123], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2

    def test_mixed_invalid(self):
        adaptation = fs.adaptation.get_summary([2739, 0000], "property")
        assert len(adaptation) == 2

    def test_mixed_invalid_csv(self, tmpdir):
        adaptation = fs.adaptation.get_summary([2739, 0000], "property", csv=True, output_dir=tmpdir)
        assert len(adaptation) == 2
