# Q10: Custom Exception Logger

try:
    num = 10 / 0   # this will raise ZeroDivisionError
except Exception as e:
    print(f"An error occurred: {e} ({type(e).__name__})")