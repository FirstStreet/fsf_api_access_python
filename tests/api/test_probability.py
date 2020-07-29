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


class TestProbabilityChance:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_chance([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_chance(190836953)

    def test_invalid(self):
        fsid = [0000000]
        probability = fs.probability.get_chance(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].chance is None
        assert probability[0].valid_id is False

    def test_single(self):
        fsid = [190836953]
        probability = fs.probability.get_chance(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_chance(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True
        assert probability[1].chance is not None
        assert probability[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        probability = fs.probability.get_chance(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_chance(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True
        assert probability[1].chance is not None
        assert probability[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_chance(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True
        assert probability[1].chance is None
        assert probability[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_chance(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].chance is not None
        assert probability[0].valid_id is True
        assert probability[1].chance is None
        assert probability[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        probability = fs.probability.get_chance([390000257], csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 390000257
        assert probability[0].chance is not None
        assert probability[0].chance[0].get("year") is not None
        assert probability[0].chance[0].get("data") is not None
        assert probability[0].chance[0].get("data")[0].get("threshold") is not None
        assert probability[0].chance[0].get("data")[0].get("data") is not None
        assert probability[0].chance[0].get("data")[0].get("data").get("low") is not None
        assert probability[0].chance[0].get("data")[0].get("data").get("mid") is not None
        assert probability[0].chance[0].get("data")[0].get("data").get("high") is not None


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
        fsid = [1867176]
        probability = fs.probability.get_count(fsid, "property")
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].count is None
        assert probability[0].valid_id is False

    def test_incorrect_lookup_type(self, tmpdir):
        fsid = [190836953]
        probability = fs.probability.get_count(fsid, "city", csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].count is None
        assert probability[0].valid_id is False

    def test_single(self):
        fsid = [1867176]
        probability = fs.probability.get_count(fsid, 'city')
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].count is not None
        assert probability[0].valid_id is True

    def test_multiple(self):
        fsid = [1867176, 1867176]
        probability = fs.probability.get_count(fsid, 'city')
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].count is not None
        assert probability[0].valid_id is True
        assert probability[1].count is not None
        assert probability[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [1867176]
        probability = fs.probability.get_count(fsid, 'city', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].count is not None
        assert probability[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [1867176, 1857780]
        probability = fs.probability.get_count(fsid, 'city', csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].count is not None
        assert probability[0].valid_id is True
        assert probability[1].count is not None
        assert probability[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [1867176, 0000000]
        probability = fs.probability.get_count(fsid, 'city')
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].count is not None
        assert probability[0].valid_id is True
        assert probability[1].count is None
        assert probability[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [1867176, 0000000]
        probability = fs.probability.get_count(fsid, 'city', csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].count is not None
        assert probability[0].valid_id is True
        assert probability[1].count is None
        assert probability[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        probability = fs.probability.get_count([7935], 'neighborhood', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 7935
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is None
        probability = fs.probability.get_count([1959835], 'city', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 1959835
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is None
        probability = fs.probability.get_count([44203], 'zcta', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 44203
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is None
        probability = fs.probability.get_count([39035103400], 'tract', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 39035103400
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is not None
        probability = fs.probability.get_count([39047], 'county', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 39047
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is None
        probability = fs.probability.get_count([3904], 'cd', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 3904
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is None
        probability = fs.probability.get_count([39], 'state', csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 39
        assert probability[0].count is not None
        assert probability[0].count[0].get("year") is not None
        assert probability[0].count[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].count[0].get("data")[0].get("data") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("bin") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("low") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("mid") is not None
        assert probability[0].count[0].get("data")[0].get("data")[0].get("count").get("high") is not None


class TestProbabilityCountSummary:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count_summary([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_count_summary(19)

    def test_invalid(self):
        fsid = [0000000]
        probability = fs.probability.get_count_summary(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].state is None
        assert probability[0].valid_id is False

    def test_single(self):
        fsid = [394406220]
        probability = fs.probability.get_count_summary(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].state is not None
        assert probability[0].valid_id is True

    def test_multiple(self):
        fsid = [394406220, 193139123]
        probability = fs.probability.get_count_summary(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].state is not None
        assert probability[0].valid_id is True
        assert probability[1].state is not None
        assert probability[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [394406220]
        probability = fs.probability.get_count_summary(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].state is not None
        assert probability[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [394406220, 193139123]
        probability = fs.probability.get_count_summary(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].state is not None
        assert probability[0].valid_id is True
        assert probability[1].state is not None
        assert probability[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [394406220, 000000000]
        probability = fs.probability.get_count_summary(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].state is not None
        assert probability[0].valid_id is True
        assert probability[1].state is None
        assert probability[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [394406220, 000000000]
        probability = fs.probability.get_count_summary(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].state is not None
        assert probability[0].valid_id is True
        assert probability[1].state is None
        assert probability[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        probability = fs.probability.get_count_summary([394406220], csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 394406220
        assert probability[0].neighborhood is not None
        assert probability[0].city is not None
        assert probability[0].state is not None
        assert probability[0].zcta is not None
        assert probability[0].county is not None
        assert probability[0].cd is not None
        assert probability[0].tract is not None


class TestProbabilityCumulative:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_cumulative([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_cumulative(190836953)

    def test_invalid(self):
        fsid = [0000000]
        probability = fs.probability.get_cumulative(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].cumulative is None
        assert probability[0].valid_id is False

    def test_single(self):
        fsid = [190836953]
        probability = fs.probability.get_cumulative(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_cumulative(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True
        assert probability[1].cumulative is not None
        assert probability[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        probability = fs.probability.get_cumulative(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_cumulative(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True
        assert probability[1].cumulative is not None
        assert probability[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_cumulative(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True
        assert probability[1].cumulative is None
        assert probability[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_cumulative(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].cumulative is not None
        assert probability[0].valid_id is True
        assert probability[1].cumulative is None
        assert probability[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        probability = fs.probability.get_cumulative([390000439], csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 390000439
        assert probability[0].cumulative is not None
        assert probability[0].cumulative[0].get("year") is not None
        assert probability[0].cumulative[0].get("data") is not None
        assert probability[0].cumulative[0].get("data")[0].get("threshold") is not None
        assert probability[0].cumulative[0].get("data")[0].get("data") is not None
        assert probability[0].cumulative[0].get("data")[0].get("data").get("low") is not None
        assert probability[0].cumulative[0].get("data")[0].get("data").get("mid") is not None
        assert probability[0].cumulative[0].get("data")[0].get("data").get("high") is not None


class TestProbabilityDepth:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_depth([], "")

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.probability.get_depth(190836953)

    def test_invalid(self):
        fsid = [0000000]
        probability = fs.probability.get_depth(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].depth is None
        assert probability[0].valid_id is False

    def test_single(self):
        fsid = [190836953]
        probability = fs.probability.get_depth(fsid)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True

    def test_multiple(self):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_depth(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True
        assert probability[1].depth is not None
        assert probability[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [190836953]
        probability = fs.probability.get_depth(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].fsid == fsid[0]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [190836953, 193139123]
        probability = fs.probability.get_depth(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True
        assert probability[1].depth is not None
        assert probability[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_depth(fsid)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True
        assert probability[1].depth is None
        assert probability[1].valid_id is False

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [190836953, 000000000]
        probability = fs.probability.get_depth(fsid, csv=True, output_dir=tmpdir)
        assert len(probability) == 2
        probability.sort(key=lambda x: x.fsid, reverse=True)
        assert probability[0].fsid == fsid[0]
        assert probability[1].fsid == fsid[1]
        assert probability[0].depth is not None
        assert probability[0].valid_id is True
        assert probability[1].depth is None
        assert probability[1].valid_id is False

    def test_one_of_each(self, tmpdir):
        probability = fs.probability.get_depth([390000227], csv=True, output_dir=tmpdir)
        assert len(probability) == 1
        assert probability[0].valid_id is True
        assert probability[0].fsid == 390000227
        assert probability[0].depth is not None
        assert probability[0].depth[0].get("year") is not None
        assert probability[0].depth[0].get("data") is not None
        assert probability[0].depth[0].get("data")[0].get("returnPeriod") is not None
        assert probability[0].depth[0].get("data")[0].get("data") is not None
        assert probability[0].depth[0].get("data")[0].get("data").get("low") is not None
        assert probability[0].depth[0].get("data")[0].get("data").get("mid") is not None
        assert probability[0].depth[0].get("data")[0].get("data").get("high") is not None
