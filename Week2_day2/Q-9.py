# Q11: Dictionary Key Access Error

data = {"name": "Alice"}

try:
    print(data["age"])   # Key doesn't exist
except KeyError:
    print("❌ KeyError: Key not found in dictionary")
