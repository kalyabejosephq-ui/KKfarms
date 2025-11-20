import sqlite3

conn = sqlite3.connect("farm.db")
cur = conn.cursor()

# ---------- USERS ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin','user'))
)
""")

# Insert default admin
cur.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', 'admin123', 'admin')")

# ---------- CATTLE ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS cattle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT,
    breed TEXT,
    age INTEGER,
    status TEXT,
    pregnant INTEGER DEFAULT 0,
    expected_date TEXT,
    last_insemination TEXT,
    insemination_type TEXT,
    milk_per_day REAL DEFAULT 0,
    notes TEXT
)
""")

# ---------- GOATS ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS goats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT,
    breed TEXT,
    age INTEGER,
    pregnant INTEGER DEFAULT 0,
    expected_kidding TEXT,
    milk_per_day REAL DEFAULT 0,
    notes TEXT
)
""")

# ---------- MILK ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS milk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    morning REAL DEFAULT 0,
    evening REAL DEFAULT 0,
    total REAL DEFAULT 0,
    sold REAL DEFAULT 0,
    used_home REAL DEFAULT 0,
    price REAL DEFAULT 0,
    income REAL DEFAULT 0
)
""")

# ---------- WORKERS ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    phone TEXT,
    notes TEXT
)
""")

# ---------- SETTINGS ----------
cur.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    milk_price REAL DEFAULT 1000,
    theme TEXT DEFAULT 'light'
)
""")

# Insert default settings row
cur.execute("INSERT OR IGNORE INTO settings (id, milk_price, theme) VALUES (1, 1000, 'light')")

conn.commit()
conn.close()

print("Database created successfully.")
