"""
IMU Calculator tests — driven by YAML fixtures.
Add new test cases by editing YAML files in tests/fixtures/, no code changes needed.
"""

import pytest
from datetime import date
import yaml
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def load_all_fixtures(prefix: str) -> list:
    cases = []
    for filepath in sorted(FIXTURES_DIR.glob(f"{prefix}*.yaml")):
        file_cases = yaml.safe_load(open(filepath, "r"))
        if file_cases:
            for case in file_cases:
                case["_fixture_file"] = filepath.name
            cases.extend(file_cases)
    return cases

from src.calculator.imu import calculate_imu, calculate_mesi_possesso


# --- IMU Calculation Tests ---

def get_calc_cases():
    """Load all calc_* fixtures, split into normal and error cases."""
    all_cases = load_all_fixtures("calc_")
    normal = [c for c in all_cases if "expected_error" not in c and "expected" in c and "imu_finale" in c.get("expected", {})]
    return normal


def get_error_cases():
    all_cases = load_all_fixtures("calc_")
    return [c for c in all_cases if "expected_error" in c]


def get_15day_cases():
    all_cases = load_all_fixtures("calc_15day")
    return [c for c in all_cases if "buyer_mesi" in c.get("expected", {})]


@pytest.mark.parametrize(
    "case",
    get_calc_cases(),
    ids=lambda c: c["name"],
)
def test_imu_calculation(case):
    """Test IMU calculation against expected values from YAML fixtures."""
    inp = case["input"]
    expected = case["expected"]

    result = calculate_imu(
        rendita_catastale=inp["rendita_catastale"],
        categoria=inp["categoria"],
        aliquota_per_mille=inp["aliquota_per_mille"],
        percentuale_possesso=inp.get("percentuale_possesso", 100),
        mesi_possesso=inp.get("mesi_possesso", 12),
        sconto_percentuale=inp.get("sconto_percentuale", 0),
        riduzione_base_percentuale=inp.get("riduzione_base_percentuale", 0),
    )

    if "base_imponibile" in expected:
        assert result["base_imponibile"] == expected["base_imponibile"], \
            f"[{case['name']}] base_imponibile: got {result['base_imponibile']}, expected {expected['base_imponibile']}"

    assert result["imu_finale"] == expected["imu_finale"], \
        f"[{case['name']}] imu_finale: got {result['imu_finale']}, expected {expected['imu_finale']}"


@pytest.mark.parametrize(
    "case",
    get_error_cases(),
    ids=lambda c: c["name"],
)
def test_imu_errors(case):
    """Test that invalid inputs raise expected errors."""
    inp = case["input"]

    with pytest.raises(ValueError, match=case["expected_error"]):
        calculate_imu(
            rendita_catastale=inp["rendita_catastale"],
            categoria=inp["categoria"],
            aliquota_per_mille=inp["aliquota_per_mille"],
            percentuale_possesso=inp.get("percentuale_possesso", 100),
            mesi_possesso=inp.get("mesi_possesso", 12),
            sconto_percentuale=inp.get("sconto_percentuale", 0),
        )


# --- 15-Day Rule Tests ---

@pytest.mark.parametrize(
    "case",
    get_15day_cases(),
    ids=lambda c: c["name"],
)
def test_mesi_possesso(case):
    """Test the 15-day rule for property transfers."""
    data_atto = date.fromisoformat(case["input"]["data_atto"])
    expected = case["expected"]

    buyer_mesi = calculate_mesi_possesso(data_atto, is_buyer=True)
    seller_mesi = calculate_mesi_possesso(data_atto, is_buyer=False)

    assert buyer_mesi == expected["buyer_mesi"], \
        f"[{case['name']}] buyer_mesi: got {buyer_mesi}, expected {expected['buyer_mesi']}"
    assert seller_mesi == expected["seller_mesi"], \
        f"[{case['name']}] seller_mesi: got {seller_mesi}, expected {expected['seller_mesi']}"
    assert buyer_mesi + seller_mesi == 12, \
        f"[{case['name']}] buyer + seller should equal 12, got {buyer_mesi + seller_mesi}"
