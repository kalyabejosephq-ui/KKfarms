from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "kkfarm_secret_key"

# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = sqlite3.connect("farm.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- HOME ----------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

    # ---------- VIEW CATTLE ----------
@app.route("/cattle")
def cattle():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cattle")
    rows = cur.fetchall()

    return render_template("cattle.html", cattle=rows)


# ---------- ADD CATTLE ----------
@app.route("/add_cattle", methods=["POST"])
def add_cattle():
    if "user_id" not in session:
        return redirect("/login")

    tag = request.form["tag"]
    breed = request.form["breed"]
    age = request.form["age"]
    pregnant = request.form["pregnant"]
    expected_date = request.form["expected_date"]
    insemination_type = request.form["insemination_type"]
    last_insemination = request.form["last_insemination"]
    milk_per_day = request.form["milk_per_day"]
    notes = request.form["notes"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cattle (tag, breed, age, pregnant, expected_date, insemination_type, last_insemination, milk_per_day, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tag, breed, age, pregnant, expected_date, insemination_type, last_insemination, milk_per_day, notes))

    conn.commit()
    return redirect("/cattle")


# ---------- DELETE CATTLE ----------
@app.route("/delete_cattle/<int:id>")
def delete_cattle(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cattle WHERE id = ?", (id,))
    conn.commit()

    return redirect("/cattle")

# ---------- VIEW GOATS ----------
@app.route("/goats")
def goats():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM goats")
    rows = cur.fetchall()

    return render_template("goats.html", goats=rows)


# ---------- ADD GOAT ----------
@app.route("/add_goat", methods=["POST"])
def add_goat():
    if "user_id" not in session:
        return redirect("/login")

    tag = request.form["tag"]
    breed = request.form["breed"]
    age = request.form["age"]
    pregnant = request.form["pregnant"]
    expected_kidding = request.form["expected_kidding"]
    milk_per_day = request.form["milk_per_day"]
    notes = request.form["notes"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO goats (tag, breed, age, pregnant, expected_kidding, milk_per_day, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tag, breed, age, pregnant, expected_kidding, milk_per_day, notes))

    conn.commit()
    return redirect("/goats")


# ---------- DELETE GOAT ----------
@app.route("/delete_goat/<int:id>")
def delete_goat(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM goats WHERE id = ?", (id,))
    conn.commit()

    return redirect("/goats")

# ---------- VIEW MILK ----------
@app.route("/milk")
def milk():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM milk")
    rows = cur.fetchall()

    return render_template("milk.html", milk_records=rows)


# ---------- ADD MILK ----------
@app.route("/add_milk", methods=["POST"])
def add_milk():
    if "user_id" not in session:
        return redirect("/login")

    date = request.form["date"]
    morning = float(request.form["morning"])
    evening = float(request.form["evening"])
    sold = float(request.form["sold"])
    used_home = float(request.form["used_home"])

    total = morning + evening

    # Get milk price from settings table
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT milk_price FROM settings WHERE id = 1")
    milk_price = cur.fetchone()["milk_price"]

    income = sold * milk_price

    cur.execute("""
        INSERT INTO milk (date, morning, evening, total, sold, used_home, price, income)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, morning, evening, total, sold, used_home, milk_price, income))

    conn.commit()
    return redirect("/milk")


# ---------- DELETE MILK ----------
@app.route("/delete_milk/<int:id>")
def delete_milk(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM milk WHERE id = ?", (id,))
    conn.commit()

    return redirect("/milk")

# ---------- VIEW WORKERS ----------
@app.route("/workers")
def workers():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM workers")
    rows = cur.fetchall()

    return render_template("workers.html", workers=rows)


# ---------- ADD WORKER ----------
@app.route("/add_worker", methods=["POST"])
def add_worker():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    role = request.form["role"]
    phone = request.form["phone"]
    notes = request.form["notes"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workers (name, role, phone, notes)
        VALUES (?, ?, ?, ?)
    """, (name, role, phone, notes))

    conn.commit()
    return redirect("/workers")


# ---------- DELETE WORKER ----------
@app.route("/delete_worker/<int:id>")
def delete_worker(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM workers WHERE id = ?", (id,))
    conn.commit()

    return redirect("/workers")

# ---------- VIEW SETTINGS ----------
@app.route("/settings")
def settings():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # Get settings
    cur.execute("SELECT milk_price, theme FROM settings WHERE id = 1")
    settings_data = cur.fetchone()

    # Get users
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    return render_template("settings.html", 
                           milk_price=settings_data["milk_price"], 
                           theme=settings_data["theme"],
                           users=users)


# ---------- UPDATE SETTINGS ----------
@app.route("/update_settings", methods=["POST"])
def update_settings():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    milk_price = request.form["milk_price"]
    theme = request.form["theme"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE settings SET milk_price = ?, theme = ? WHERE id = 1", (milk_price, theme))
    conn.commit()

    return redirect("/settings")


# ---------- ADD USER ----------
@app.route("/add_user", methods=["POST"])
def add_user():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()

    return redirect("/settings")


# ---------- DELETE USER ----------
@app.route("/delete_user/<int:id>")
def delete_user(id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()

    return redirect("/settings")

# ---------- VIEW REPORTS ----------
@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # Total cattle and goats
    cur.execute("SELECT COUNT(*) as total FROM cattle")
    total_cattle = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) as total FROM goats")
    total_goats = cur.fetchone()["total"]

    # Milk summary
    cur.execute("SELECT SUM(total) as total_milk, SUM(sold) as total_sold, SUM(used_home) as total_used_home, SUM(income) as total_income FROM milk")
    milk_summary = cur.fetchone()

    total_milk = milk_summary["total_milk"] if milk_summary["total_milk"] else 0
    total_sold = milk_summary["total_sold"] if milk_summary["total_sold"] else 0
    total_used_home = milk_summary["total_used_home"] if milk_summary["total_used_home"] else 0
    total_income = milk_summary["total_income"] if milk_summary["total_income"] else 0

    # All milk records
    cur.execute("SELECT * FROM milk ORDER BY date DESC")
    milk_records = cur.fetchall()

    return render_template("reports.html",
                           total_cattle=total_cattle,
                           total_goats=total_goats,
                           total_milk=total_milk,
                           total_sold=total_sold,
                           total_used_home=total_used_home,
                           total_income=total_income,
                           milk_records=milk_records)


# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(debug=True, port=8000)

