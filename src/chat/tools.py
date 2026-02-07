"""
Tool definitions for Claude API and execution mapping.
"""

from src.calculator.imu import calculate_imu, calculate_mesi_possesso
from src.calculator.coefficienti import get_aliquote
from datetime import date

# Tool definitions in Claude API format
TOOLS = [
    {
        "name": "calculate_imu",
        "description": "Calcola l'IMU per un immobile. Usa questo strumento quando hai raccolto tutte le informazioni necessarie dall'utente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "rendita_catastale": {
                    "type": "number",
                    "description": "Rendita catastale dell'immobile (dalla visura catastale)"
                },
                "categoria": {
                    "type": "string",
                    "description": "Categoria catastale (es. A/2, C/1, D/1)"
                },
                "aliquota_per_mille": {
                    "type": "number",
                    "description": "Aliquota IMU del comune in per mille (es. 10.6)"
                },
                "percentuale_possesso": {
                    "type": "number",
                    "description": "Percentuale di possesso (default 100)"
                },
                "mesi_possesso": {
                    "type": "integer",
                    "description": "Mesi di possesso nell'anno (default 12)"
                },
                "sconto_percentuale": {
                    "type": "number",
                    "description": "Sconto sull'IMU in percentuale (es. 25 per canone concordato)"
                },
                "riduzione_base_percentuale": {
                    "type": "number",
                    "description": "Riduzione della base imponibile in percentuale (es. 50 per comodato o inagibile)"
                }
            },
            "required": ["rendita_catastale", "categoria", "aliquota_per_mille"]
        }
    },
    {
        "name": "calculate_mesi_possesso",
        "description": "Calcola i mesi di possesso per acquirente e venditore in base alla data dell'atto, usando la regola dei 15 giorni.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data_atto": {
                    "type": "string",
                    "description": "Data dell'atto di compravendita in formato YYYY-MM-DD"
                },
                "is_buyer": {
                    "type": "boolean",
                    "description": "True per l'acquirente, False per il venditore"
                }
            },
            "required": ["data_atto", "is_buyer"]
        }
    },
    {
        "name": "get_aliquote_comune",
        "description": "Recupera le aliquote IMU di un comune. Usa questo per trovare l'aliquota corretta prima di calcolare l'IMU.",
        "input_schema": {
            "type": "object",
            "properties": {
                "comune": {
                    "type": "string",
                    "description": "Nome del comune (es. torino)"
                },
                "anno": {
                    "type": "integer",
                    "description": "Anno di riferimento (es. 2025)"
                }
            },
            "required": ["comune", "anno"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """Execute a tool call and return the result."""

    if tool_name == "calculate_imu":
        return calculate_imu(
            rendita_catastale=tool_input["rendita_catastale"],
            categoria=tool_input["categoria"],
            aliquota_per_mille=tool_input["aliquota_per_mille"],
            percentuale_possesso=tool_input.get("percentuale_possesso", 100),
            mesi_possesso=tool_input.get("mesi_possesso", 12),
            sconto_percentuale=tool_input.get("sconto_percentuale", 0),
            riduzione_base_percentuale=tool_input.get("riduzione_base_percentuale", 0),
        )

    elif tool_name == "calculate_mesi_possesso":
        data_atto = date.fromisoformat(tool_input["data_atto"])
        is_buyer = tool_input["is_buyer"]
        mesi = calculate_mesi_possesso(data_atto, is_buyer)
        return {
            "data_atto": tool_input["data_atto"],
            "ruolo": "acquirente" if is_buyer else "venditore",
            "mesi_possesso": mesi,
        }

    elif tool_name == "get_aliquote_comune":
        comune = tool_input["comune"]
        anno = tool_input.get("anno", 2025)
        try:
            data = get_aliquote(comune, anno)
            return data
        except FileNotFoundError as e:
            return {"errore": str(e)}

    else:
        return {"errore": f"Strumento sconosciuto: {tool_name}"}
