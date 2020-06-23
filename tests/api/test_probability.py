import os

import pytest

import firststreet
from firststreet.errors import InvalidArgument

api_key = os.environ['FSF_API_KEY']
fs = firststreet.FirstStreet(api_key)


class TestProbabilityChance:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_chance([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_chance(190836953)

    def test_single(self):
        probability = fs.probability.get_chance([190836953])
        assert len(probability) == 1

    def test_multiple(self):
        probability = fs.probability.get_chance([190836953, 193139123])
        assert len(probability) == 2

    def test_single_csv(self):
        probability = fs.probability.get_chance([190836953], csv=True)
        assert len(probability) == 1

    def test_multiple_csv(self):
        probability = fs.probability.get_chance([190836953, 193139123], csv=True)
        assert len(probability) == 2

    def test_mixed_invalid(self):
        probability = fs.probability.get_chance([190836953, 000000000])
        assert len(probability) == 2

    def test_mixed_invalid_csv(self):
        probability = fs.probability.get_chance([190836953, 000000000], csv=True)
        assert len(probability) == 2


class TestProbabilityCount:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count([], "")

    def test_empty_fsid(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count([], "property")

    def test_empty_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count([190836953], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count(1867176, 'city')

    def test_wrong_fsid_number(self):
        location = fs.probability.get_count([1867176], "property")
        assert len(location) == 1
        assert location[0].count is None

    def test_incorrect_lookup_type(self):
        location = fs.probability.get_count([190836953], "city", csv=True)
        assert len(location) == 1
        assert location[0].count is None

    def test_single(self):
        probability = fs.probability.get_count([1867176], 'city')
        assert len(probability) == 1

    def test_multiple(self):
        probability = fs.probability.get_count([1867176, 1867176], 'city')
        assert len(probability) == 2

    def test_single_csv(self):
        probability = fs.probability.get_count([1867176], 'city', csv=True)
        assert len(probability) == 1

    def test_multiple_csv(self):
        probability = fs.probability.get_count([1867176, 1857780], 'city', csv=True)
        assert len(probability) == 2

    def test_mixed_invalid(self):
        probability = fs.probability.get_count([1867176, 0000000], 'city')
        assert len(probability) == 2

    def test_mixed_invalid_csv(self):
        probability = fs.probability.get_count([1867176, 0000000], 'city', csv=True)
        assert len(probability) == 2


class TestProbabilityCountSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count_summary([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count_summary(19)

    def test_single(self):
        probability = fs.probability.get_count_summary([394406220])
        assert len(probability) == 1

    def test_multiple(self):
        probability = fs.probability.get_count_summary([394406220, 193139123])
        assert len(probability) == 2

    def test_single_csv(self):
        probability = fs.probability.get_count_summary([394406220], csv=True)
        assert len(probability) == 1

    def test_multiple_csv(self):
        probability = fs.probability.get_count_summary([394406220, 193139123], csv=True)
        assert len(probability) == 2

    def test_mixed_invalid(self):
        probability = fs.probability.get_count_summary([394406220, 000000000])
        assert len(probability) == 2

    def test_mixed_invalid_csv(self):
        probability = fs.probability.get_count_summary([394406220, 000000000], csv=True)
        assert len(probability) == 2


class TestProbabilityCumulative:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_cumulative([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_cumulative(190836953)

    def test_single(self):
        probability = fs.probability.get_cumulative([190836953])
        assert len(probability) == 1

    def test_multiple(self):
        probability = fs.probability.get_cumulative([190836953, 193139123])
        assert len(probability) == 2

    def test_single_csv(self):
        probability = fs.probability.get_cumulative([190836953], csv=True)
        assert len(probability) == 1

    def test_multiple_csv(self):
        probability = fs.probability.get_cumulative([190836953, 193139123], csv=True)
        assert len(probability) == 2

    def test_mixed_invalid(self):
        probability = fs.probability.get_cumulative([190836953, 000000000])
        assert len(probability) == 2

    def test_mixed_invalid_csv(self):
        probability = fs.probability.get_cumulative([190836953, 000000000], csv=True)
        assert len(probability) == 2


class TestProbabilityDepth:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_depth([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_depth(190836953)

    def test_single(self):
        probability = fs.probability.get_depth([190836953])
        assert len(probability) == 1

    def test_multiple(self):
        probability = fs.probability.get_depth([190836953, 193139123])
        assert len(probability) == 2

    def test_single_csv(self):
        probability = fs.probability.get_depth([190836953], csv=True)
        assert len(probability) == 1

    def test_multiple_csv(self):
        probability = fs.probability.get_depth([190836953, 193139123], csv=True)
        assert len(probability) == 2

    def test_mixed_invalid(self):
        probability = fs.probability.get_depth([190836953, 000000000])
        assert len(probability) == 2

    def test_mixed_invalid_csv(self):
        probability = fs.probability.get_depth([190836953, 000000000], csv=True)
        assert len(probability) == 2
