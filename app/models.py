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

# --- Dashboard & Simulation Models ---

class GoalSetupRequest(BaseModel):
    target_amount: float = Field(..., description="The financial goal amount (e.g., 3500.0)")
    target_date: Optional[str] = Field(None, description="Target date for the goal (YYYY-MM-DD)")

class ActionPlanItem(BaseModel):
    title: str = Field(..., description="Short title of the action (e.g., 'Cancel subscriptions')")
    savings_text: str = Field(..., description="Estimated savings text (e.g., '+85 €/month')")

class DashboardResponse(BaseModel):
    expense_distribution: List[Dict[str, float | str]] = Field(..., description="Data for Donut chart (e.g., [{'name': 'Rent', 'value': 1200}])")
    projection_chart: List[Dict[str, float | str]] = Field(..., description="Data for Bar chart (e.g., [{'month': 'Mar', 'amount': 500}])")
    action_plan: List[ActionPlanItem] = Field(..., description="List of recommended actions to save money")
    total_potential_savings: float = Field(..., description="Total estimated savings per month")

class SimulationRequest(BaseModel):
    purchase_intention: str = Field(..., description="The item/service the user wants to buy")
    current_goal_amount: float = Field(..., description="The current target amount of the goal")

class SimulationResponse(BaseModel):
    evaluation_text: str = Field(..., description="AI's feedback on the decision")
    status: Literal["approved", "warning", "rejected"] = Field(..., description="Decision status")

