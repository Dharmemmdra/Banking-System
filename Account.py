"""Simple Banking System with transaction history and CLI-friendly methods."""
from typing import Dict, List
import csv
import datetime

class Account:
    """Base account class with simple transaction logging."""

    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0):
        self._account_number = account_number
        self._holder_name = holder_name
        self._balance = float(balance)
        # transactions: list of dicts: {ts, type, amount, balance_after, note}
        self._transactions: List[Dict] = []
        if balance != 0:
            self._transactions.append(self._txn_record('initial', balance, f'Initial deposit'))

    def _txn_record(self, ttype, amount, note=''):
        return {
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'type': ttype,
            'amount': float(amount),
            'balance': float(self._balance),
            'note': note
        }

    def deposit(self, amount: float, note: str = '') -> bool:
        if amount <= 0:
            print("[Deposit] Invalid amount. Must be > 0.")
            return False
        self._balance += amount
        self._transactions.append(self._txn_record('deposit', amount, note))
        print(f"[Deposit] {amount} deposited. New balance: {self._balance}")
        return True

    def withdraw(self, amount: float, note: str = '') -> bool:
        if amount <= 0:
            print("[Withdraw] Invalid amount. Must be > 0.")
            return False
        if amount > self._balance:
            print("[Withdraw] Insufficient funds.")
            return False
        self._balance -= amount
        self._transactions.append(self._txn_record('withdraw', amount, note))
        print(f"[Withdraw] {amount} withdrawn. New balance: {self._balance}")
        return True

    def get_balance(self) -> float:
        return self._balance

    def get_account_info(self) -> str:
        return f"Account[{self._account_number}] - Holder: {self._holder_name}, Balance: {self._balance}"

    def get_transactions(self) -> List[Dict]:
        return list(self._transactions)

    def export_transactions_csv(self, filepath: str):
        keys = ['timestamp', 'type', 'amount', 'balance', 'note']
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for t in self._transactions:
                writer.writerow({k: t.get(k, '') for k in keys})
        print(f"Exported {len(self._transactions)} transactions to {filepath}")


class SavingsAccount(Account):
    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0, interest_rate: float = 0.02):
        super().__init__(account_number, holder_name, balance)
        self._interest_rate = float(interest_rate)

    def apply_interest(self) -> float:
        interest = self.get_balance() * self._interest_rate
        # deposit will record txn
        self.deposit(interest, note='interest')
        print(f"[Interest] Applied interest: {interest}")
        return interest


class Bank:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def create_account(self, account_type: str, account_number: str, holder_name: str, balance: float = 0.0, **kwargs) -> Account:
        if account_number in self.accounts:
            raise ValueError(f"Account {account_number} already exists")
        if account_type.lower() == 'savings':
            interest_rate = kwargs.get('interest_rate', 0.02)
            account = SavingsAccount(account_number, holder_name, balance, interest_rate)
        else:
            account = Account(account_number, holder_name, balance)
        self.accounts[account_number] = account
        print(f"[Bank] Created {account_type} account {account_number} for {holder_name}")
        return account

    def get_account(self, account_number: str):
        return self.accounts.get(account_number)

    def load_from_csv(self, filepath: str):
        import csv
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                acct_type = row.get('account_type') or 'base'
                interest_rate = float(row['interest_rate']) if row.get('interest_rate') else None
                balance = float(row.get('balance') or 0)
                if interest_rate:
                    self.create_account(acct_type, row['account_number'], row['holder_name'], balance, interest_rate=interest_rate)
                else:
                    self.create_account(acct_type, row['account_number'], row['holder_name'], balance)

if __name__ == '__main__':
    bank = Bank()
    bank.create_account('savings', 'S1001', 'Alice', 1000)
    acc = bank.get_account('S1001')
    acc.deposit(200, note='payroll')
    acc.withdraw(50, note='groceries')
    acc.apply_interest()
    print(acc.get_account_info())
    acc.export_transactions_csv('alice_txns.csv')
