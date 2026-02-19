from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import UserRequest, AgentResponse, GoalSetupRequest, DashboardResponse, SimulationRequest, SimulationResponse
from app.services.mock_data import get_financial_context
from app.services.llm_service import evaluate_goal, generate_action_plan, evaluate_purchase
import dotenv

dotenv.load_dotenv()

app = FastAPI(title="Goal Copilot Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for Lovable.dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/evaluate-goal", response_model=AgentResponse)
async def evaluate_goal_endpoint(request: UserRequest):
    """
    Evaluates a financial goal based on the user's request and mock financial context.
    """
    try:
        # 1. Get Financial Context (Mock)
        financial_context = get_financial_context()
        
        # 2. Call LLM Service
        response = evaluate_goal(request.message, financial_context)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/setup-dashboard", response_model=DashboardResponse)
async def setup_dashboard_endpoint(request: GoalSetupRequest):
    """
    Sets up the dashboard with charts and an AI-generated action plan.
    """
    try:
        context = get_financial_context()
        
        # Generar Action Plan con IA
        ai_plan = generate_action_plan(context, request.target_amount)
        
        # Construir respuesta
        # Nota: En un caso real, 'expense_distribution' y 'projection_chart' se calcularían
        # o vendrían de una DB. Aquí usamos datos mock/estáticos o derivados simples.
        
        # Simple proyección simulada (Ahorro mensual estimado 200€)
        monthly_savings = 200.0
        months_to_goal = int(request.target_amount / monthly_savings) + 1
        projection = []
        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        import datetime
        current_month_idx = datetime.datetime.now().month - 1
        
        accumulated = 0
        for i in range(min(6, months_to_goal)): # Proyección a 6 meses vista
             idx = (current_month_idx + i) % 12
             accumulated += monthly_savings
             projection.append({"month": months[idx], "amount": accumulated})

        # Mapear gastos de mock_data a expense_distribution format
        # mock_data expenses es una lista de dicts. Agrupamos por categoría.
        # Asumimos que mock_data['recent_expenses'] existe y tiene estructura.
        # Adaptar según la estructura real de mock_data.py
        
        # De mock_data.py actual: "recent_expenses": [{"category":...}]
        expenses = context.get("recent_expenses", [])
        dist_map = {}
        for item in expenses:
            cat = item["category"]
            amt = item["amount"]
            dist_map[cat] = dist_map.get(cat, 0) + amt
            
        expense_distribution = [{"name": k, "value": v} for k, v in dist_map.items()]

        return DashboardResponse(
            expense_distribution=expense_distribution,
            projection_chart=projection,
            action_plan=ai_plan.get("action_plan", []),
            total_potential_savings=ai_plan.get("total_potential_savings", 0.0)
        )

    except Exception as e:
        print(f"Error in setup_dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/api/simulate-decision", response_model=SimulationResponse)
async def simulate_decision_endpoint(request: SimulationRequest):
    """
    Simulates a purchase decision impact on the goal.
    """
    try:
        context = get_financial_context()
        result = evaluate_purchase(context, request.current_goal_amount, request.purchase_intention)
        return SimulationResponse(**result)
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
