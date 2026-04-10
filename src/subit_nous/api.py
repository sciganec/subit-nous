"""REST API + WebSocket for SUBIT-NOUS"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import networkx as nx

from .core import text_to_subit, subit_to_name, subit_to_coords, get_mode

app = FastAPI(title="SUBIT-NOUS API", version="2.0.0")

knowledge_graph = nx.DiGraph()

class TextRequest(BaseModel):
    text: str
    chunk_size: int = 1000

class AnalyzeResponse(BaseModel):
    subit_id: int
    archetype_name: str
    mode: Optional[str]
    coordinates: Dict[str, int]
    timestamp: str

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/analyze/text", response_model=AnalyzeResponse)
async def analyze_text(req: TextRequest):
    subit = text_to_subit(req.text, req.chunk_size)
    mode = get_mode(subit)
    who, where, when, why = subit_to_coords(subit)
    return AnalyzeResponse(
        subit_id=subit,
        archetype_name=subit_to_name(subit),
        mode=mode,
        coordinates={"WHO": who, "WHERE": where, "WHEN": when, "WHY": why},
        timestamp=datetime.now().isoformat()
    )

@app.get("/graph/stats")
async def graph_stats():
    return {
        "total_nodes": len(knowledge_graph.nodes),
        "total_edges": knowledge_graph.number_of_edges(),
        "communities": 0,
        "top_archetypes": []
    }

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            subit = text_to_subit(data)
            response = {
                "subit_id": subit,
                "archetype": subit_to_name(subit),
                "mode": get_mode(subit),
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass

@app.post("/search")
async def search_endpoint(
    query: str,
    mode: Optional[str] = None,
    who: Optional[str] = None,
    where: Optional[str] = None,
    when: Optional[str] = None,
    top_k: int = 10,
    alpha: float = 0.5,
):
    from .search import search as search_func
    results = search_func(query, mode=mode, who=who, where=where, when=when, top_k=top_k, alpha=alpha)
    return {"query": query, "results": results}

@app.post("/agent")
async def agent_endpoint(
    text: str,
    mode: str = "auto",
    model: str = "llama3.2:3b",
):
    from .agent import run_agent, classify_and_run
    if mode == "auto":
        result = classify_and_run(text, model)
        return {"mode": result["original_mode"], "response": result["agent_response"]}
    else:
        response = run_agent(text, mode, model)
        return {"mode": mode, "response": response}

@app.post("/pipeline")
async def pipeline_endpoint(
    text: str,
    modes: str,
    model: str = "llama3.2:3b",
):
    from .agent import run_pipeline
    mode_list = [m.strip().upper() for m in modes.split(",")]
    results = run_pipeline(text, mode_list, model)
    return {"modes": mode_list, "steps": results}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()