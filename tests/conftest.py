"""
Shared test helpers — loads YAML fixtures from tests/fixtures/.
"""

import yaml
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(filename: str) -> list:
    """Load a YAML fixture file and return the list of test cases."""
    filepath = FIXTURES_DIR / filename
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def load_all_fixtures(prefix: str) -> list:
    """Load all YAML fixtures matching a prefix (e.g. 'calc_').

    Returns a flat list of all test cases across matching files,
    with the source filename added to each case.
    """
    cases = []
    for filepath in sorted(FIXTURES_DIR.glob(f"{prefix}*.yaml")):
        file_cases = yaml.safe_load(open(filepath, "r"))
        if file_cases:
            for case in file_cases:
                case["_fixture_file"] = filepath.name
            cases.extend(file_cases)
    return cases
