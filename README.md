# Peanut Business Ledger

A small business income and expense tracking web application built with Flask and SQLite.

## About the Project
The application helps record business transactions and view basic financial summaries.

## Features
- Login-protected dashboard
- Add, edit, and delete transactions
- Record income and expenses
- Search transactions by party name or date
- Filter transactions by income or expense
- View total income, total expenses, and net balance
- Download a PDF transaction report

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML templates
- ReportLab (PDF reports)

## Run Locally
1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the required packages:
   ```bash
   pip install flask flask-sqlalchemy reportlab
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open the local address shown in your terminal.

## Important Security Note
This project is a learning/demo application. Before deploying it publicly, move the Flask secret key and login credentials into environment variables, use secure password hashing, and protect destructive actions such as deleting records. Do not publish real passwords, secret keys, or private business data.

## Project Status
Learning project — security and deployment improvements are still recommended.

## Author
**Firoj Khan**  
GitHub: [@firojkhan-dev](https://github.com/firojkhan-dev)
