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

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()