# api/calc.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union

# If calculate.py is inside the same folder (api/), keep this:
from .calculate import Calculator
# If your calculate.py is at repo root instead, use:
# import calculate  # and later: calculate.Calculator(...)

app = FastAPI()

# CORS helps only for split-port local dev; harmless on Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Config(BaseModel):
    numbers: Union[List[float], List[int]]

# ---------- GET: health ----------
# Match: /, /calc, any subpath (so GET /api/calc works)
@app.api_route("", methods=["GET"])
@app.api_route("/", methods=["GET"])
@app.api_route("/{rest:path}", methods=["GET"])
async def health(req: Request, rest: str | None = None):
    return {"ok": True, "path": req.url.path}

# ---------- POST: compute ----------
# Match: /, /calc, any subpath (so POST /api/calc works)
@app.api_route("", methods=["POST"])
@app.api_route("/", methods=["POST"])
@app.api_route("/{rest:path}", methods=["POST"])
def compute(cfg: Config, rest: str | None = None):
    try:
        c = Calculator(cfg.numbers)
        return {"numbers": c.numbers, **c.summary()}
        # If using `import calculate` instead:
        # c = calculate.Calculator(cfg.numbers)
        # return {"numbers": c.numbers, **c.summary()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
