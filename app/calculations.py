from re import L


def add(num1: int, num2: int):
    return num1 + num2

def substract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2

# dummy class
class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, strating_balance=0):
        self.balance = strating_balance
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1