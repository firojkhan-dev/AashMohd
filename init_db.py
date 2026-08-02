import sqlite3

conn = sqlite3.connect('committee.db')
cursor = conn.cursor()

# टेबल बनाना
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    person_name TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

# टेस्टिंग के लिए एक-दो एंट्री डालना
cursor.execute("INSERT INTO transactions (type, amount, description, person_name, date) VALUES ('Income', 5000.0, 'Masjid Chanda', 'अहमद भाई', '2026-06-01')")
cursor.execute("INSERT INTO transactions (type, amount, description, person_name, date) VALUES ('Expense', 1200.0, 'Tent House', 'शर्मा टेंट', '2026-06-06')")

conn.commit()
conn.close()
print("Database and table created successfully!")