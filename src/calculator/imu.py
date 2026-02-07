"""
IMU Calculator — pure deterministic calculation.
All figures loaded from data files, never hardcoded.
"""

from calendar import monthrange
from datetime import date
from .coefficienti import get_coefficiente, get_rivalutazione


def calculate_base_imponibile(rendita_catastale: float, categoria: str) -> float:
    """Calculate the base imponibile.

    base = rendita_catastale × rivalutazione × coefficiente
    """
    rivalutazione = get_rivalutazione(is_terreno=False)
    coefficiente = get_coefficiente(categoria)
    return rendita_catastale * rivalutazione * coefficiente


def calculate_mesi_possesso(data_atto: date, is_buyer: bool) -> int:
    """Calculate months of possession using the 15-day rule.

    The month of sale is charged to whoever had possession for more than 15 days.
    If exactly equal days, the month goes to the buyer.

    Args:
        data_atto: date of the deed/transfer
        is_buyer: True for buyer, False for seller

    Returns:
        Number of months of possession in the year
    """
    day = data_atto.day
    days_in_month = monthrange(data_atto.year, data_atto.month)[1]

    # Seller has days 1..day (day days), buyer has days day+1..end (days_in_month - day days)
    seller_days = day
    buyer_days = days_in_month - day

    # Who gets the transfer month?
    # More than 15 days → that person. Equal → buyer.
    if seller_days > buyer_days:
        # seller had more days — seller gets the month
        seller_months = data_atto.month
        buyer_months = 12 - data_atto.month
    else:
        # buyer had more days, OR equal — buyer gets the month
        seller_months = data_atto.month - 1
        buyer_months = 12 - (data_atto.month - 1)

    return buyer_months if is_buyer else seller_months


def calculate_imu(
    rendita_catastale: float,
    categoria: str,
    aliquota_per_mille: float,
    percentuale_possesso: float = 100.0,
    mesi_possesso: int = 12,
    sconto_percentuale: float = 0.0,
    riduzione_base_percentuale: float = 0.0,
) -> dict:
    """Calculate IMU and return a full breakdown.

    Formula:
        base = rendita × rivalutazione × coefficiente
        base = base × (100 - riduzione_base) / 100   (for comodato/inagibile)
        imu = base × (aliquota/1000) × (%possesso/100) × (mesi/12) × ((100-sconto)/100)

    Args:
        rendita_catastale: from visura catastale
        categoria: e.g. "A/2"
        aliquota_per_mille: the comune's rate (e.g. 10.6 means 10.6 per mille)
        percentuale_possesso: ownership percentage (default 100)
        mesi_possesso: months of possession in the year (default 12)
        sconto_percentuale: discount on final IMU (e.g. 25 for canone concordato)
        riduzione_base_percentuale: reduction on base imponibile (e.g. 50 for comodato/inagibile)

    Returns:
        dict with full breakdown of the calculation
    """
    rivalutazione = get_rivalutazione(is_terreno=False)
    coefficiente = get_coefficiente(categoria)

    # Step 1: base imponibile
    rendita_rivalutata = rendita_catastale * rivalutazione
    base_imponibile = rendita_rivalutata * coefficiente

    # Step 2: apply base reduction (comodato, inagibile)
    if riduzione_base_percentuale > 0:
        base_imponibile = base_imponibile * (100 - riduzione_base_percentuale) / 100

    # Step 3: IMU calculation
    imu_lorda = base_imponibile * (aliquota_per_mille / 1000)
    imu_possesso = imu_lorda * (percentuale_possesso / 100)
    imu_periodo = imu_possesso * (mesi_possesso / 12)

    # Step 4: apply sconto (canone concordato)
    if sconto_percentuale > 0:
        imu_finale = imu_periodo * (100 - sconto_percentuale) / 100
    else:
        imu_finale = imu_periodo

    # Round to 2 decimal places
    imu_finale = round(imu_finale, 2)

    return {
        "rendita_catastale": rendita_catastale,
        "categoria": categoria,
        "rivalutazione": rivalutazione,
        "coefficiente": coefficiente,
        "rendita_rivalutata": round(rendita_rivalutata, 2),
        "base_imponibile": round(base_imponibile, 2),
        "riduzione_base_percentuale": riduzione_base_percentuale,
        "aliquota_per_mille": aliquota_per_mille,
        "percentuale_possesso": percentuale_possesso,
        "mesi_possesso": mesi_possesso,
        "sconto_percentuale": sconto_percentuale,
        "imu_lorda": round(imu_lorda, 2),
        "imu_finale": imu_finale,
        "acconto": round(imu_finale / 2, 2),
        "saldo": round(imu_finale - round(imu_finale / 2, 2), 2),
    }


def calculate_acconto_saldo(imu_annuale: float) -> dict:
    """Split annual IMU into acconto (June 16) and saldo (December 16).

    Args:
        imu_annuale: total annual IMU amount

    Returns:
        dict with acconto, saldo, and total
    """
    acconto = round(imu_annuale / 2, 2)
    saldo = round(imu_annuale - acconto, 2)
    return {
        "acconto": acconto,
        "saldo": saldo,
        "totale": round(imu_annuale, 2),
        "scadenza_acconto": "16 giugno",
        "scadenza_saldo": "16 dicembre",
    }
