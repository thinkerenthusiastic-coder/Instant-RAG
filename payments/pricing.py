import json
import os

# Load pricing configuration from JSON file
_pricing_file = os.path.join(os.path.dirname(__file__), "pricing.json")
with open(_pricing_file) as f:
    data = json.load(f)

# Export the prices dict directly for easy access
prices = data["prices"]

# Also export other config if needed
CHAIN = data["chain"]
TOKEN = data["token"]
DECIMALS = data["decimals"]
