# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# External Imports
import pytest

pytest_plugins = 'aiohttp.pytest_plugin'


def pytest_addoption(parser):
    """Sets up command line arguments for pytest to skip the stress test
    """
    parser.addoption("--runstress", action="store_true", default=False, help="runs the stress test")


def pytest_collection_modifyitems(config, items):
    """Skips the stress test if the argument is not set
    """
    if config.getoption("--runstress"):
        return
    skip_stress = pytest.mark.skip(reason="need --runstress option to run")
    for item in items:
        if "stress" in item.keywords:
            item.add_marker(skip_stress)
