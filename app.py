import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from cmc_agent import OmniAgentPipeline

load_dotenv()

app = FastAPI(
    title="CMC-OmniAgent: Autonomous Crypto Intelligence & Alpha Copilot",
    description="Multi-Agent Crypto Analytics Platform powered by CoinMarketCap API | Built for CMC API Hackathon Round 2",
    version="1.0.0"
)

pipeline = OmniAgentPipeline(api_key=os.getenv("CMC_API_KEY", ""))

class ChatRequest(BaseModel):
    query: str

class ConfigRequest(BaseModel):
    api_key: str

@app.on_event("startup")
async def startup_event():
    # Pre-warm pipeline on boot
    await pipeline.execute_cycle(limit=50)

@app.get("/api/health")
async def health_check():
    return {"status": "HEALTHY", "version": "1.0.0", "live_api": pipeline.client.is_live}

@app.get("/api/cycle")
async def run_pipeline_cycle(limit: int = 50):
    try:
        results = await pipeline.execute_cycle(limit=limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def copilot_chat(req: ChatRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return pipeline.chat_with_copilot(req.query)

@app.post("/api/config")
async def update_config(req: ConfigRequest):
    pipeline.client.api_key = req.api_key.strip()
    pipeline.client.is_live = bool(pipeline.client.api_key and pipeline.client.api_key != "your_coinmarketcap_api_key_here")
    await pipeline.execute_cycle(limit=50)
    return {"status": "UPDATED", "is_live": pipeline.client.is_live}

# Mount static frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "CMC-OmniAgent API Running. Open /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
