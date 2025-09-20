# api/calc.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Union
from .calculate import Calculator

app = FastAPI()

class Config(BaseModel):
    numbers: Union[List[float], List[int]]

@app.get("")
@app.get("/")
async def health(req: Request):
    return {"ok": True, "path": req.url.path}

@app.post("")
@app.post("/")
def compute(cfg: Config):
    try:
        c = Calculator(cfg.numbers)
        return {"numbers": c.numbers, **c.summary()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
