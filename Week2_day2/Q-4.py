# Function to safely add two values after converting to int

def safe_add(a, b):
    try:
        num1 = a
        num2 = b
        return num1 + num2
    except ValueError:
        print("❌ ValueError: Both inputs must be numeric (convertible to int).")
        return None
    except TypeError:
        print("Wrong type is given by user")
        return None


# Example usage
print(safe_add("10", "20"))   # 30
print(safe_add(5, "15"))      # 20
print(safe_add("hello", 10))  # Error message + None
