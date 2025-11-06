"""Command-line interface to interact with the banking system.
Usage examples:
    python -m src.cli create --type savings --acc S1 --name Alice --balance 100
    python -m src.cli deposit --acc S1 --amount 50
    python -m src.cli withdraw --acc S1 --amount 20
    python -m src.cli balance --acc S1
    python -m src.cli list
"""
import argparse
import os
from src.Account import Bank

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_accounts.csv')

def build_parser():
    p = argparse.ArgumentParser(description='Simple Banking CLI (UG friendly)')
    sub = p.add_subparsers(dest='cmd')

    # create
    c = sub.add_parser('create', help='Create a new account')
    c.add_argument('--type', default='base', help='Account type: savings or base')
    c.add_argument('--acc', required=True, help='Account number')
    c.add_argument('--name', required=True, help='Holder name')
    c.add_argument('--balance', type=float, default=0.0, help='Initial balance')
    c.add_argument('--interest', type=float, default=None, help='Interest rate for savings')

    # deposit
    d = sub.add_parser('deposit', help='Deposit amount')
    d.add_argument('--acc', required=True)
    d.add_argument('--amount', required=True, type=float)
    d.add_argument('--note', default='')

    # withdraw
    w = sub.add_parser('withdraw', help='Withdraw amount')
    w.add_argument('--acc', required=True)
    w.add_argument('--amount', required=True, type=float)
    w.add_argument('--note', default='')

    # balance
    b = sub.add_parser('balance', help='Show balance')
    b.add_argument('--acc', required=True)

    # list
    l = sub.add_parser('list', help='List all accounts')

    # export transactions
    e = sub.add_parser('export', help='Export transactions to CSV')
    e.add_argument('--acc', required=True)
    e.add_argument('--out', required=True)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()

    bank = Bank()
    # Try load sample data if it exists
    if os.path.exists(DATA_FILE):
        try:
            bank.load_from_csv(DATA_FILE)
        except Exception as e:
            print('Could not load sample data:', e)

    cmd = args.cmd
    if cmd == 'create':
        kwargs = {}
        if args.interest is not None:
            kwargs['interest_rate'] = args.interest
        bank.create_account(args.type, args.acc, args.name, args.balance, **kwargs)
    elif cmd == 'deposit':
        acc = bank.get_account(args.acc)
        if not acc:
            print('Account not found:', args.acc); return
        acc.deposit(args.amount, note=args.note)
    elif cmd == 'withdraw':
        acc = bank.get_account(args.acc)
        if not acc:
            print('Account not found:', args.acc); return
        acc.withdraw(args.amount, note=args.note)
    elif cmd == 'balance':
        acc = bank.get_account(args.acc)
        if not acc:
            print('Account not found:', args.acc); return
        print(acc.get_account_info())
    elif cmd == 'list':
        for k, v in bank.accounts.items():
            print(v.get_account_info())
    elif cmd == 'export':
        acc = bank.get_account(args.acc)
        if not acc:
            print('Account not found:', args.acc); return
        acc.export_transactions_csv(args.out)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
