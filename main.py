# main.py
import json
from calculate import Calculator

# load config.json
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

# create calculator
calc = Calculator(cfg["numbers"])

# show results
print("Numbers:", calc.numbers)
print("Sum:", calc.total())
print("Product:", calc.product())
print("Mean:", calc.mean())
