from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class UserRequest(BaseModel):
    message: str = Field(..., description="The user's goal or purchase intent (e.g., 'Quiero ir a cenar sushi')")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class AgentResponse(BaseModel):
    response_text: str = Field(..., description="The AI's evaluation of the goal")
    suggested_action: Optional[str] = Field(None, description="Text for an action button (e.g., 'Crear Hucha')")
    chart_type: Optional[Literal["bar", "pie", "line"]] = Field(None, description="Type of chart to display")
    chart_data: Optional[List[Dict[str, float | str]]] = Field(None, description="Data for the chart")
    agent_name: str = Field("Copiloto de Ahorro", description="Name of the AI agent")
