# Simple Banking System (UG-friendly)

This repository is a beginner-friendly Python project demonstrating object-oriented programming, simple file I/O, transaction logging, a CLI, and unit tests.

## Quickstart

1. Create & activate a virtual environment (recommended):

    python -m venv venv
    source venv/bin/activate  # Windows: venv\\Scripts\\activate

2. Install test dependency (optional):

    pip install -r requirements.txt

3. Run demo (loads sample CSV and performs operations):

    python examples/demo_usage.py

4. Use CLI (examples):

    python -m src.cli list
    python -m src.cli create --type savings --acc S9 --name Test --balance 100 --interest 0.02
    python -m src.cli deposit --acc S9 --amount 50 --note "top-up"
    python -m src.cli withdraw --acc S9 --amount 20 --note "atm"

5. Run tests:

    pytest

## Files of interest
- `src/Account.py`: core classes with transaction history
- `src/cli.py`: simple CLI using argparse
- `data/sample_accounts.csv`: small dataset to try
- `tests/test_account.py`: pytest unit tests

## CI (optional)
A GitHub Actions workflow is included to run tests on push.

## License
MIT
