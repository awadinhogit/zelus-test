# api/calc.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
from .calculate import Calculator

app = FastAPI()

# --- CORS setup (important for local dev with Next.js at :3000) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev; in prod you can restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic model for input ---
class Config(BaseModel):
    numbers: Union[List[float], List[int]]

# --- Health endpoint ---
@app.get("")
@app.get("/")
async def health(req: Request):
    return {"ok": True, "path": req.url.path}

# --- Compute endpoint ---
@app.post("")
@app.post("/")
def compute(cfg: Config):
    try:
        c = Calculator(cfg.numbers)
        return {"numbers": c.numbers, **c.summary()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
