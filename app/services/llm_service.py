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
