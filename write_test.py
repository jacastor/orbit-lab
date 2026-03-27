content = (
    "import sys\n"
    "sys.path.insert(0, 'src')\n"
    "\n"
    "from tle_parser import TLE, parse_tle\n"
    "import pytest\n"
    "\n"
    "\n"
    "RAW_TLE = \"\"\"ISS (ZARYA)\n"
    "1 25544U 98067A   24001.50000000  .00002182  00000-0  40768-4 0  9990\n"
    "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.50377579404740\"\"\"\n"
    "\n"
    "\n"
    "def test_parse_tle_name():\n"
    "    tle = parse_tle(RAW_TLE)\n"
    "    assert tle.name == \"ISS (ZARYA)\"\n"
    "\n"
    "\n"
    "def test_parse_tle_lines():\n"
    "    tle = parse_tle(RAW_TLE)\n"
    "    assert tle.line1.startswith(\"1 \")\n"
    "    assert tle.line2.startswith(\"2 \")\n"
    "\n"
    "\n"
    "def test_parse_tle_invalid():\n"
    "    with pytest.raises(ValueError):\n"
    "        parse_tle(\"only one line\")\n"
)

with open('tests/test_tle_parser.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")