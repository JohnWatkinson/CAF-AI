---
topic: imu
region: italy
source: CAF-AI
generated: 2025-05-18
reviewed: ''
reviewer: ''
verified: false
status: staged
original_file: imu_formula_calculation_guide_2025-05-12.md
notes: Standard Italian IMU calculation, with all steps and example.
tags:
- imu
- formula
- tasse
- property_tax
- italy
retrieved: ''
agent: ''
---

# Q: Come si calcola l’IMU su un immobile in Italia?

## A: Formula ufficiale e guida completa

**IMU (Imposta Municipale Unica)** si calcola con la seguente procedura:

### 1. Calcola la base imponibile

1. Trova la **rendita catastale** dell'immobile (dal Catasto).
2. Calcola la **rendita rivalutata**:
Rendita rivalutata = Rendita catastale × 1,05

markdown
Copy
Edit
3. Applica il **coefficiente catastale** in base alla categoria:
- Abitazioni (A, escl. A10): **160**
- Uffici (A10): **80**
- Negozi (C1): **55**
- Altri immobili (D): **65**
4. Ottieni la **base imponibile**:
Base imponibile = Rendita rivalutata × Coefficiente catastale

markdown
Copy
Edit

### 2. Calcola l'IMU

**Formula completa:**
IMU = Base imponibile × Aliquota × (Percentuale di possesso / 100) × (Mesi di possesso / 12) × ((100 - Sconto) / 100)

markdown
Copy
Edit
Dove:
- **Aliquota**: stabilita dal Comune, espressa come decimale (es. 0,0076 per 0,76%)
- **Percentuale di possesso**: tua quota sull’immobile (100% se proprietario unico)
- **Mesi di possesso**: mesi di proprietà nell’anno (vedi note sotto)
- **Sconto**: percentuale di sconto applicabile (es. 25 per canone concordato, altrimenti 0)
- **Detrazione fissa**: se presente, va sottratta **dopo** il calcolo

**Nota:**
- Il mese viene conteggiato al proprietario che ha posseduto l’immobile per almeno 15 giorni in quel mese.

### 3. Detrazione fissa

Se è prevista una **detrazione fissa** (ad esempio per abitazione principale o casi speciali):

IMU finale = IMU - Detrazione fissa

yaml
Copy
Edit

---

## Esempi pratici

### Esempio 1: con sconto

- Rendita catastale: €1.000
- Coefficiente: 160
- Aliquota IMU: 0,76% (quindi 0,0076)
- Percentuale di possesso: 50%
- Mesi di possesso: 6
- Sconto: 25%
- Detrazione fissa: €0

**Calcolo:**

Base imponibile = 1.000 × 1,05 × 160 = €168.000

IMU = 168.000 × 0,0076 × 0,5 × 0,5 × 0,75 = €239,40

markdown
Copy
Edit

### Esempio 2: senza sconto

- Rendita catastale: €1.000
- Coefficiente: 160
- Aliquota IMU: 0,76% (0,0076)
- Percentuale di possesso: 100%
- Mesi di possesso: 3
- Sconto: 0%
- Detrazione fissa: €0

**Calcolo:**
Base imponibile = 1.000 × 1,05 × 160 = €168.000

IMU = 168.000 × 0,0076 × 1 × 0,25 × 1 = €319,20

yaml
Copy
Edit

---

## Note aggiuntive
- **Aliquota:** sempre in decimale (0,76% = 0,0076)
- **Percentuale di possesso e mesi:** sono frazioni (0,5 per 50%, 0,25 per 3 mesi)
- **Sconto:** solo se previsto dal Comune o da normativa
- **Detrazione fissa:** da sottrarre a fine calcolo, solo se prevista

---

## Formula universale per la KB:

IMU = Base imponibile × Aliquota × (Percentuale di possesso / 100) × (Mesi di possesso / 12) × ((100 - Sconto) / 100) - Detrazione fissa

css
Copy
Edit

> Se Sconto e Detrazione fissa non sono previsti, impostare a 0.
