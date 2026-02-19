import os
import json
import google.generativeai as genai
from typing import Dict, Any
from app.models import AgentResponse
from app.utils.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback/Warning if no key is present, though strictly we should expect one.
    # We'll just set it to avoid import errors, but runtime errors will occur if not set.
    pass
else:
    genai.configure(api_key=api_key)

def evaluate_goal(user_text: str, context_data: Dict[str, Any]) -> AgentResponse:
    """
    Evaluates a user's goal using Google Gemini 1.5 Flash with JSON mode.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

        # Construct the prompt
        prompt = f"""
        {SYSTEM_PROMPT}

        USER DATA:
        Context: {json.dumps(context_data, indent=2)}
        User Message: "{user_text}"
        
        Generate the JSON response now:
        """

        response = model.generate_content(prompt)
        
        # Parse JSON response
        response_data = json.loads(response.text)
        
        # Validate with Pydantic model
        return AgentResponse(**response_data)

    except Exception as e:
        # Fallback error response
        print(f"Error calling Gemini: {e}")
        return AgentResponse(
            response_text="Lo siento, tuve un problema analizando tus datos. ¿Podrías intentarlo de nuevo?",
            suggested_action="Reintentar",
            chart_type=None,
            chart_data=None,
            agent_name="Copiloto (Modo de Fallo)"
        )

def generate_action_plan(financial_context: Dict[str, Any], goal_amount: float) -> Dict[str, Any]:
    """
    Generates a financial action plan using Gemini to help achieve the goal.
    Returns a dict matching the structure of DashboardResponse fields (action_plan, total_potential_savings).
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = f"""
        You are a financial advisor. Helper the user reach a goal of {goal_amount}€.
        
        Analyze their financial context to find savings opportunities.
        CONTEXT: {json.dumps(financial_context, indent=2)}

        Return a JSON object with this exact schema:
        {{
            "action_plan": [
                {{"title": "Action Title (max 40 chars)", "savings_text": "e.g. +50€/month"}}
            ],
            "total_potential_savings": 120.50 (number)
        }}
        Provide exactly 3 actionable tips.
        """

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        print(f"Error calling Gemini for Action Plan: {e}")
        return {
            "action_plan": [
                {"title": "Error generando plan", "savings_text": "0€"}
            ],
            "total_potential_savings": 0.0
        }

def evaluate_purchase(financial_context: Dict[str, Any], goal_amount: float, purchase_intention: str) -> Dict[str, Any]:
    """
    Evaluates a specific purchase decision against the user's goal.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

        prompt = f"""
        You are a strict but fair financial conscience (Pepito Grillo).
        User wants to buy: "{purchase_intention}".
        Their current goal is to save {goal_amount}€.
        
        CONTEXT: {json.dumps(financial_context, indent=2)}

        Evaluate if this purchase endangers the goal.
        - If it's a small expense or necessary, approve it.
        - If it's a large/unnecessary expense that hurts the goal, REJECT it sarcastically.
        - If it's borderline, give a WARNING.

        Return JSON:
        {{
            "evaluation_text": "Your advice here...",
            "status": "approved" | "warning" | "rejected"
        }}
        """

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        print(f"Error calling Gemini for Simulation: {e}")
        return {
            "evaluation_text": "No pude evaluar tu compra en este momento.",
            "status": "warning"
        }
