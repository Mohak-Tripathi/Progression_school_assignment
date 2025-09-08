# Q7: JSON Config Access

import json

def read_config(filename):
    with open(filename, "r") as f:
        data = json.load(f)  # parse JSON into dictionary
    
    endpoint = data["api_settings"]["endpoint"]
    print(f"API Endpoint: {endpoint}")


# Example usage
read_config("config.json")
