class Account:
    def __init__(self, account_number, holder_name, balance=0):
        self.__account_number = account_number
        self.__holder_name = holder_name
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds")

    def get_balance(self):
        return self.__balance

    def get_account_info(self):
        return f"Account Number: {self.__account_number}, Holder Name: {self.__holder_name}, Balance: {self.__balance}"

class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, balance=0, interest_rate=0.02):
        super().__init__(account_number, holder_name, balance)
        self.__interest_rate = interest_rate

    def apply_interest(self):
        interest = self.get_balance() * self.__interest_rate
        self.deposit(interest)
        print(f"Applied interest: {interest}. New balance: {self.get_balance()}")

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type, account_number, holder_name, balance=0):
        if account_type == "savings":
            account = SavingsAccount(account_number, holder_name, balance)
        # More account types can be added here
        self.accounts[account_number] = account
        print(f"Created {account_type} account for {holder_name}")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

# Example usage
bank = Bank()
bank.create_account("savings", "12345", "John Doe", 1000)
account = bank.get_account("12345")
account.deposit(500)
account.withdraw(200)
account.apply_interest()
print(account.get_account_info())
