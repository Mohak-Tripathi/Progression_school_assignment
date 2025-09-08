# Q8: Robo as Capsule (Encapsulation Example)

class Account:
    def __init__(self, initial_balance=0):
        self.__balance = initial_balance   # private attribute

    def credit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("❌ Invalid credit amount")

    def debit(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("❌ Insufficient balance or invalid debit")

    def get_balance(self):
        return self.__balance


# Example usage
acc = Account(1000)
acc.credit(500)    # deposit money
acc.debit(300)     # withdraw money
print(f"Balance: {acc.get_balance()}")
acc.__balance = 9000
print(f"Balance: {acc.get_balance()}")
