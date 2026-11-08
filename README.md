# Peanut Business Ledger

A Flask and SQLite web application for recording business income and expenses, reviewing balances, and generating PDF transaction reports.

## Overview

Peanut Business Ledger is a small-business bookkeeping project. It provides a login-protected dashboard for managing transaction records and viewing a simple financial summary.

## Features

- **Dashboard access** — login-protected application area.
- **Transaction management** — add, edit, and delete income or expense records.
- **Income and expense tracking** — keep both transaction types in one place.
- **Search** — find records by party name or date.
- **Filtering** — view income and expense entries separately.
- **Financial summary** — review total income, total expenses, and net balance.
- **PDF reporting** — download a transaction report.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework |
| Flask-SQLAlchemy | Database integration |
| SQLite | Data storage |
| HTML templates | User interface |
| ReportLab | PDF report generation |

## Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/firojkhan-dev/AashMohd.git
   cd AashMohd
   ```

2. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install flask flask-sqlalchemy reportlab
   ```

4. Start the application:
   ```bash
   python app.py
   ```

5. Open the local URL printed in the terminal.

## Security Notes

This repository is a learning/demo project. Before using it with real business data or deploying it publicly:

- Store the Flask secret key and credentials in environment variables.
- Use a secure password-hashing method; never store plain-text passwords.
- Add CSRF protection and validate all user input.
- Restrict and confirm destructive actions such as deleting records.
- Use production-ready configuration and avoid committing secrets or private data.

## Project Information

- **Type:** Flask web application
- **Database:** SQLite
- **Status:** Learning / portfolio project
- **Repository:** [firojkhan-dev/AashMohd](https://github.com/firojkhan-dev/AashMohd)

## Future Improvements

- Add automated tests for authentication and transaction workflows.
- Add pagination and clearer validation/error messages.
- Improve mobile responsiveness and accessibility.
- Add environment-based configuration and deployment documentation.

## Author

**Firoj Khan**  
[GitHub Profile](https://github.com/firojkhan-dev)
