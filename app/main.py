from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import UserRequest, AgentResponse
from app.services.mock_data import get_financial_context
from app.services.llm_service import evaluate_goal
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
