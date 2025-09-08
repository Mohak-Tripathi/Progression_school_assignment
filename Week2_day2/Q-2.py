# Q4: Age Validation

age = input("Enter your age: ")

try:
    age = int(input("Enter your age: "))
    print(f"Your age is {age}.")
except ValueError:
    print("Invalid input! Please enter a numeric value.")
