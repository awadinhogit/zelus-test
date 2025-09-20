# api/calc.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
from .calculate import Calculator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Config(BaseModel):
    numbers: Union[List[float], List[int]]

# --- Health ---
@app.get("/")
@app.get("")          # /api/calc/
@app.get("/calc")     # /api/calc
async def health(req: Request):
    return {"ok": True, "path": req.url.path}

# --- Compute ---
@app.post("/")
@app.post("")         # /api/calc/ (POST)
@app.post("/calc")    # /api/calc (POST)
def compute(cfg: Config):
    try:
        c = Calculator(cfg.numbers)
        return {"numbers": c.numbers, **c.summary()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
