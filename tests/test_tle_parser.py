import sys
sys.path.insert(0, 'src')

from tle_parser import TLE, parse_tle
import pytest


RAW_TLE = """ISS (ZARYA)
1 25544U 98067A   24001.50000000  .00002182  00000-0  40768-4 0  9990
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.50377579404740"""


def test_parse_tle_name():
    tle = parse_tle(RAW_TLE)
    assert tle.name == "ISS (ZARYA)"


def test_parse_tle_lines():
    tle = parse_tle(RAW_TLE)
    assert tle.line1.startswith("1 ")
    assert tle.line2.startswith("2 ")


def test_parse_tle_invalid():
    with pytest.raises(ValueError):
        parse_tle("only one line")
