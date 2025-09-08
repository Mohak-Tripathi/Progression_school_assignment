try:
    num = int(input("Enter a number: "))
    result = 100 / num
    print(f"Result: {result}")
except (ValueError, ZeroDivisionError):
    print("Error: Invalid input or division by zero.")