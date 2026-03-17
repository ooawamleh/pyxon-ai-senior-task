# api.py
from fastapi import FastAPI
from fastapi import FastAPI, BackgroundTasks 
from backend.src.swarm import run_gil_swarm, finalize_cache 
from pydantic import BaseModel
import uvicorn
from backend.src.swarm import run_gil_swarm

app = FastAPI(title="GIL Swarm Backend API")

# Define the request structure
class ChatRequest(BaseModel):
    message: str
    history: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    print(f"📥 [API] Processing Query...")
    
    try:
        final_answer = run_gil_swarm(request.message, request.history)
        
        background_tasks.add_task(finalize_cache, request.message, final_answer)
        
        return {"response": final_answer}
        
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

if __name__ == "__main__":
    # Run the backend server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)