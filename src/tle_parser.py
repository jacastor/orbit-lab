class TLE:
    """
    Represents a parsed Two-Line Element set.
    """

    def __init__(self, name: str, line1: str, line2: str):
        self.name = name.strip()
        self.line1 = line1.strip()
        self.line2 = line2.strip()

    def __repr__(self):
        return f"TLE(name={self.name!r})"


def parse_tle(raw: str) -> TLE:
    """
    Parse a raw 3-line TLE string into a TLE object.
    
    Args:
        raw: A string containing the satellite name, line 1, and line 2.
    
    Returns:
        A TLE object.
    """
    lines = [line.strip() for line in raw.strip().splitlines()]

    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    return TLE(name=lines[0], line1=lines[1], line2=lines[2])