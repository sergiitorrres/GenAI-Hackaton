from typing import Dict, Any

def get_financial_context() -> Dict[str, Any]:
    """
    Simulates fetching financial data for the user.
    """
    return {
        "current_balance": 1200.0,
        "currency": "EUR",
        "recent_expenses": [
            {"category": "Ocio/Comida", "description": "Sushi", "amount": 150.0},
            {"category": "Transporte", "description": "Uber", "amount": 45.0},
            {"category": "Ocio/Entretenimiento", "description": "Netflix", "amount": 15.0},
            {"category": "Vivienda", "description": "Alquiler", "amount": 400.0}
        ],
        "savings_goal": "Ninguno definido"
    }
