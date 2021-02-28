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


class TestAVMProperty:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.avm.get_avm([])

    def test_wrong_fsid_type(self):
        with pytest.raises(InvalidArgument):
            fs.avm.get_avm(2739)

    def test_invalid(self):
        fsid = [0000]
        avm = fs.avm.get_avm(fsid)
        assert len(avm) == 1
        assert avm[0].fsid == str(fsid[0])
        assert avm[0].provider_id is None
        assert avm[0].valid_id is False
        assert avm[0].avm is None

    def test_single(self):
        fsid = [1200171414]
        avm = fs.avm.get_avm(fsid)
        assert len(avm) == 1
        assert avm[0].fsid == str(fsid[0])
        assert avm[0].avm['mid'] >= 0
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True

    def test_multiple(self):
        fsid = [1200000342, 1200171414]
        avm = fs.avm.get_avm(fsid)
        assert len(avm) == 2
        avm.sort(key=lambda x: x.fsid)
        assert avm[0].fsid == str(fsid[0])
        assert avm[0].avm['mid'] >= 0
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True
        assert avm[1].fsid == str(fsid[1])
        assert avm[1].avm['mid'] >= 0
        assert avm[1].provider_id == 2
        assert avm[1].valid_id is True

    def test_single_csv(self, tmpdir):
        fsid = [1200000342]
        avm = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
        assert len(avm) == 1
        assert avm[0].fsid == str(fsid[0])
        assert avm[0].avm['mid'] >= 0
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True

    def test_multiple_csv(self, tmpdir):
        fsid = [1200000342, 1200171414]
        avm = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
        assert len(avm) == 2
        avm.sort(key=lambda x: x.fsid)
        assert avm[0].fsid == str(fsid[0])
        assert avm[0].avm['mid'] >= 0
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True
        assert avm[1].fsid == str(fsid[1])
        assert avm[1].avm['mid'] >= 0
        assert avm[1].provider_id == 2
        assert avm[1].valid_id is True

    def test_mixed_invalid(self):
        fsid = [0000000000, 1200000342]
        avm_out = fs.avm.get_avm(fsid)
        assert len(avm_out) == 2
        avm_out.sort(key=lambda x: x.fsid)
        assert avm_out[0].fsid == str(fsid[0])
        assert avm_out[0].provider_id is None
        assert avm_out[0].valid_id is False
        assert avm_out[0].avm is None
        assert avm_out[1].fsid == str(fsid[1])
        assert avm_out[1].avm['mid'] >= 0
        assert avm_out[1].provider_id == 2
        assert avm_out[1].valid_id is True

    def test_mixed_invalid_csv(self, tmpdir):
        fsid = [0000000000, 1200000342]
        avm_out = fs.avm.get_avm(fsid, csv=True, output_dir=tmpdir)
        assert len(avm_out) == 2
        avm_out.sort(key=lambda x: x.fsid)
        assert avm_out[0].fsid == str(fsid[0])
        assert avm_out[0].provider_id is None
        assert avm_out[0].valid_id is False
        assert avm_out[0].avm is None
        assert avm_out[1].fsid == str(fsid[1])
        assert avm_out[1].avm['mid'] >= 0
        assert avm_out[1].provider_id == 2
        assert avm_out[1].valid_id is True

    def test_one_of_each(self, tmpdir):
        avm = fs.avm.get_avm([1200000342], csv=True, output_dir=tmpdir)
        assert len(avm) == 1
        assert avm[0].fsid == "1200000342"
        assert avm[0].avm['mid'] >= 0
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True


class TestAVMProvider:

    def test_empty(self):
        with pytest.raises(InvalidArgument):
            fs.avm.get_provider([])

    def test_wrong_provider_id_type(self):
        with pytest.raises(InvalidArgument):
            fs.avm.get_provider(2)

    def test_invalid(self):
        provider_id = [999]
        avm = fs.avm.get_provider(provider_id)
        assert len(avm) == 1
        assert avm[0].provider_id == provider_id[0]
        assert avm[0].valid_id is False
        assert avm[0].provider_logo is None
        assert avm[0].provider_name is None

    def test_single(self):
        provider_id = [2]
        avm = fs.avm.get_provider(provider_id)
        assert len(avm) == 1
        assert avm[0].provider_id == provider_id[0]
        assert avm[0].valid_id is True
        assert avm[0].provider_logo == ""
        assert avm[0].provider_name == "First Street Foundation"

    def test_single_csv(self, tmpdir):
        provider_id = [2]
        avm = fs.avm.get_provider(provider_id, csv=True, output_dir=tmpdir)
        assert len(avm) == 1
        assert avm[0].provider_id == provider_id[0]
        assert avm[0].valid_id is True
        assert avm[0].provider_logo == ""
        assert avm[0].provider_name == "First Street Foundation"

    def test_mixed_invalid(self):
        provider_id = [2, 3]
        avm = fs.avm.get_provider(provider_id)
        assert len(avm) == 2
        avm.sort(key=lambda x: x.provider_id)
        assert avm[0].provider_id == provider_id[0]
        assert avm[0].valid_id is True
        assert avm[0].provider_logo == ""
        assert avm[0].provider_name == "First Street Foundation"
        assert avm[1].provider_id == provider_id[1]
        assert avm[1].valid_id is False
        assert avm[1].provider_logo is None
        assert avm[1].provider_name is None

    def test_mixed_invalid_csv(self, tmpdir):
        provider_id = [2, 3]
        avm = fs.avm.get_provider(provider_id, csv=True, output_dir=tmpdir)
        assert len(avm) == 2
        avm.sort(key=lambda x: x.provider_id)
        assert avm[0].provider_id == provider_id[0]
        assert avm[0].valid_id is True
        assert avm[0].provider_logo == ""
        assert avm[0].provider_name == "First Street Foundation"
        assert avm[1].provider_id == provider_id[1]
        assert avm[1].valid_id is False
        assert avm[1].provider_logo is None
        assert avm[1].provider_name is None

    def test_one_of_each(self, tmpdir):
        avm = fs.avm.get_provider([2], csv=True, output_dir=tmpdir)
        assert len(avm) == 1
        assert avm[0].provider_id == 2
        assert avm[0].valid_id is True
        assert avm[0].provider_logo == ""
        assert avm[0].provider_name == "First Street Foundation"
