# When you write a method inside a class, the first parameter should always be self. It represents the specific object you're working with.
# self lets you access that particular object's data and methods.

# Why self matters:

# dog1.bark() means "call bark on dog1"  inside that method, self = dog1
# dog2.bark() means "call bark on dog2"  inside that method, self = dog2
# Real-world analogy: Imagine a recipe that says "mix your flour with your sugar." The word "your" is like self-it refers to whoever is reading the recipe right now.



class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount  # Add to THIS account
        print(f"{self.owner} now has ${self.balance}")
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.owner} withdrew ${amount}")
        else:
            print("Insufficient funds")

account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)

account1.deposit(100)   # Alice now has $1100
account2.deposit(50)    # Bob now has $550
