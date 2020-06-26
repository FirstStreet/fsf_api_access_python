# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import os

# Internal Imports
import firststreet


def test_full(tmpdir):
    api_key = os.environ['FSF_API_KEY']
    fs = firststreet.FirstStreet(api_key)
    fs.adaptation.get_detail([29], csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([395133768], "property", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([7924], "neighborhood", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([1935265], "city", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([50158], "zcta", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([39061007100], "tract", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([19047], "county", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([3915], "cd", csv=True, output_dir=tmpdir)
    fs.adaptation.get_summary([39], "state", csv=True, output_dir=tmpdir)
    fs.probability.get_chance([390000257], csv=True, output_dir=tmpdir)
    fs.probability.get_count([7935], 'neighborhood', csv=True, output_dir=tmpdir)
    fs.probability.get_count([1959835], 'city', csv=True, output_dir=tmpdir)
    fs.probability.get_count([44203], 'zcta', csv=True, output_dir=tmpdir)
    fs.probability.get_count([39035103400], 'tract', csv=True, output_dir=tmpdir)
    fs.probability.get_count([39047], 'county', csv=True, output_dir=tmpdir)
    fs.probability.get_count([3904], 'cd', csv=True, output_dir=tmpdir)
    fs.probability.get_count([39], 'state', csv=True, output_dir=tmpdir)
    fs.probability.get_count_summary([394406220], csv=True, output_dir=tmpdir)
    fs.probability.get_cumulative([390000439], csv=True, output_dir=tmpdir)
    fs.probability.get_depth([390000227], csv=True, output_dir=tmpdir)
    fs.environmental.get_precipitation([39057], csv=True, output_dir=tmpdir)
    fs.historic.get_event([2], csv=True, output_dir=tmpdir)
    fs.historic.get_summary([511447411], "property", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([540225], "neighborhood", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([1982200], "city", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([50156], "zcta", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([19153004900], "tract", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([19163], "county", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([1901], "cd", csv=True, output_dir=tmpdir)
    fs.historic.get_summary([39], "state", csv=True, output_dir=tmpdir)
    fs.location.get_detail([511447411], "property", csv=True, output_dir=tmpdir)
    fs.location.get_detail([1206631], "neighborhood", csv=True, output_dir=tmpdir)
    fs.location.get_detail([3915406], "city", csv=True, output_dir=tmpdir)
    fs.location.get_detail([44654], "zcta", csv=True, output_dir=tmpdir)
    fs.location.get_detail([39151712602], "tract", csv=True, output_dir=tmpdir)
    fs.location.get_detail([39077], "county", csv=True, output_dir=tmpdir)
    fs.location.get_detail([3904], "cd", csv=True, output_dir=tmpdir)
    fs.location.get_detail([39], "state", csv=True, output_dir=tmpdir)
    fs.location.get_summary([395112095], "property", csv=True, output_dir=tmpdir)
    fs.location.get_summary([631054], "neighborhood", csv=True, output_dir=tmpdir)
    fs.location.get_summary([3958002], "city", csv=True, output_dir=tmpdir)
    fs.location.get_summary([43935], "zcta", csv=True, output_dir=tmpdir)
    fs.location.get_summary([39153531702], "tract", csv=True, output_dir=tmpdir)
    fs.location.get_summary([39027], "county", csv=True, output_dir=tmpdir)
    fs.location.get_summary([3903], "cd", csv=True, output_dir=tmpdir)
    fs.location.get_summary([39], "state", csv=True, output_dir=tmpdir)
    fs.fema.get_nfip([44074], "zcta", csv=True, output_dir=tmpdir)
    fs.fema.get_nfip([39013012300], "tract", csv=True, output_dir=tmpdir)
    fs.fema.get_nfip([39093], "county", csv=True, output_dir=tmpdir)
    fs.fema.get_nfip([39], "state", csv=True, output_dir=tmpdir)