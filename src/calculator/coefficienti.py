"""
Loads and provides access to national IMU figures.
All values come from data/imu_national.json — nothing hardcoded.
"""

import json
from pathlib import Path

# Load national data once at import
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
NATIONAL_DATA_PATH = DATA_DIR / "imu_national.json"

with open(NATIONAL_DATA_PATH, "r") as f:
    NATIONAL_DATA = json.load(f)

RIVALUTAZIONE = NATIONAL_DATA["rivalutazione"]
RIVALUTAZIONE_TERRENI = NATIONAL_DATA["rivalutazione_terreni"]
COEFFICIENTI = NATIONAL_DATA["coefficienti"]
COEFFICIENTE_TERRENI = NATIONAL_DATA["coefficiente_terreni_agricoli"]
CATEGORIE_PRIMA_CASA_TASSATA = NATIONAL_DATA["categorie_prima_casa_tassata"]
SCONTI_NAZIONALI = NATIONAL_DATA["sconti_nazionali"]


def get_national_data():
    """Return the full national data dict."""
    return NATIONAL_DATA


def get_coefficiente(categoria: str) -> int:
    """Lookup the coefficiente for a given categoria catastale.

    Args:
        categoria: e.g. "A/2", "C/1", "D/5"

    Returns:
        The multiplier (e.g. 160 for A/2)

    Raises:
        ValueError: if the categoria is not found
    """
    categoria = categoria.upper().strip()
    if categoria in COEFFICIENTI:
        return COEFFICIENTI[categoria]
    raise ValueError(f"Categoria catastale sconosciuta: {categoria}")


def get_rivalutazione(is_terreno: bool = False) -> float:
    """Return the rivalutazione multiplier.

    Args:
        is_terreno: True for terreni agricoli (uses 1.25), False for fabbricati (uses 1.05)
    """
    return RIVALUTAZIONE_TERRENI if is_terreno else RIVALUTAZIONE


def get_aliquote(comune: str, anno: int) -> dict:
    """Load aliquote for a given comune and year.

    Args:
        comune: e.g. "torino"
        anno: e.g. 2025

    Returns:
        The full aliquote data dict

    Raises:
        FileNotFoundError: if no data file exists for this comune/anno
    """
    filename = f"{comune.lower()}_{anno}.json"
    filepath = DATA_DIR / "aliquote" / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Nessun dato aliquote per {comune} {anno}: {filepath}")
    with open(filepath, "r") as f:
        return json.load(f)
