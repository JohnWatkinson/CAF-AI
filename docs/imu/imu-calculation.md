# IMU - Imposta Municipale Propria

Italian municipal property tax on real estate.

---

## Who Pays

- All property owners EXCEPT primary residence (prima casa / abitazione principale)
- **Exception**: prima casa IS taxed if luxury category: A/1, A/8, A/9
- Second homes, rental properties, commercial properties, land — all taxed

## Categorie Catastali & Coefficienti

| Categoria | Descrizione | Coefficiente |
|-----------|-------------|-------------|
| A (escluso A/10) | Abitazioni | 160 |
| A/10 | Uffici / studi privati | 80 |
| B | Collegi, ospedali, uffici pubblici | 140 |
| C/1 | Negozi e botteghe | 55 |
| C/2, C/6, C/7 | Magazzini, autorimesse, tettoie | 160 |
| C/3, C/4, C/5 | Laboratori, palestre, stabilimenti | 140 |
| D (escluso D/5) | Immobili industriali/commerciali | 65 |
| D/5 | Istituti di credito | 80 |
| Terreni agricoli | — | 135 |

## The Formula

```
Base imponibile = Rendita catastale × 1.05 × Coefficiente catastale

IMU = Base imponibile × Aliquota × (% Possesso / 100) × (Mesi di possesso / 12) × ((100 - Sconto) / 100)
```

### Input Variables

| Variable | Description | Source |
|----------|-------------|--------|
| Rendita catastale | Cadastral income of the property | Visura catastale (Catasto) |
| Categoria catastale | Property category (A/2, C/1, etc.) | Visura catastale (Catasto) |
| Coefficiente catastale | Multiplier based on categoria | National table (above) |
| Aliquota IMU | Tax rate (e.g. 0.76%) | Set by each Comune, changes yearly |
| % Possesso | Ownership percentage | Deed / atto di proprieta |
| Mesi di possesso | Months of possession in the year | See 15-day rule below |
| Sconto | Discount percentage (e.g. 25%) | Depends on conditions (see below) |

## The 15-Day Rule (Mesi di Possesso)

IMU is calculated monthly. For property transfers:

- The month of sale is charged to whoever had possession for **more than 15 days** in that month
- If exactly equal days (e.g. sale on 15th of a 30-day month), the month goes to the **buyer**

Examples:
- Deed signed **4 April**: seller pays 3 months, buyer pays 9 months
- Deed signed **17 October**: seller pays 10 months, buyer pays 2 months
- Deed signed **15 May** (31-day month): seller pays 4 months, buyer pays 8 months
- Deed signed **15 November** (30-day month): equal split — by law goes to buyer. Buyer pays 2 months, seller pays 10 months

## Sconti / Deductions

Common discounts:
- **Canone concordato**: 25% reduction for properties rented under regulated-rate contracts (3+2)
- **Comodato d'uso gratuito**: 50% reduction on base imponibile if property is lent to direct relatives (parents/children) — conditions apply
- **Immobili inagibili/inabitabili**: 50% reduction on base imponibile for uninhabitable properties

Each Comune may define additional deductions.

## Aliquote

- Each Comune sets its own aliquote annually
- There is a national baseline (aliquota base) that Comuni can adjust within limits
- Typical range: 0.46% to 1.06% depending on property type and Comune
- Must be looked up on the Comune's website or via MEF (Ministero dell'Economia e delle Finanze) database

## Payment Schedule

| Scadenza | Data | Calcolo |
|----------|------|---------|
| Acconto (1st installment) | **16 June** | 50% of total annual IMU |
| Saldo (2nd installment) | **16 December** | Remaining 50% (adjusted if Comune changed rates) |

If the deadline falls on a weekend/holiday, it moves to the next working day.

Single annual payment on 16 June is also allowed (full amount based on prior year rates).

## Worked Examples

### Example 1: Simple case (full ownership, full year)

- Rendita catastale: 1.000
- Categoria: A/2 (abitazione) → Coefficiente: 160
- Aliquota: 0,76%
- Possesso: 100%
- Mesi: 12
- Sconto: 0%

```
Base = 1.000 × 1,05 × 160 = 168.000
IMU = 168.000 × 0,0076 × 1,0 × 1,0 × 1,0 = 1.276,80
```

### Example 2: Partial ownership + discount

- Rendita catastale: 1.000
- Categoria: A/2 → Coefficiente: 160
- Aliquota: 0,76%
- Possesso: 50%
- Mesi: 6 (bought on 4 July — buyer pays July-December)
- Sconto: 25% (canone concordato)

```
Base = 1.000 × 1,05 × 160 = 168.000
IMU = 168.000 × 0,0076 × 0,50 × (6/12) × 0,75 = 239,40
```

---

## Notes

- Rendita catastale rivalutazione of 5% (× 1.05) is fixed by law, not variable
- For terreni agricoli, the base uses reddito dominicale × 1.25 × 135 (different rivalutazione)
- AIRE residents (Italians abroad) may have different rules depending on Comune
