# Q21: Calculate Net Amount from Transactions in File

def calculate_net_amount(filename):
    balance = 0
    
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()   # remove spaces/newlines
            if not line:          # skip empty lines
                continue
            
            transaction, amount = line.split(":")
            amount = int(amount)
            
            if transaction.upper() == "D":   # Deposit
                balance += amount
            elif transaction.upper() == "W": # Withdraw
                balance -= amount
    
    return balance


# Example usage
file_name = "file.txt"
net_balance = calculate_net_amount(file_name)
print(net_balance)
