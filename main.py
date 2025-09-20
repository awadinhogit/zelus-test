# main.py (super simple orchestrator)
import json
from api.calculate import Calculator

with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

calc = Calculator(cfg["numbers"])
print("Numbers:", calc.numbers)
print("Sum:", calc.total())
print("Product:", calc.product())
print("Mean:", calc.mean())
