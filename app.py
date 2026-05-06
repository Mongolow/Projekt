from flask import request, jsonify, Flask, render_template, g, redirect, url_for, flash, abort
import secrets
import sqlite3


app = Flask(__name__)

DATABASE = "Station_database.db"
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS measurements(
id INTEGER PRIMARY KEY AUTOINCREMENT,
temp FLOAT,
hum FLOAT,
press FLOAT,
created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

"""

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Funkcja inicjująca baze danych
def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()


# Komenda inicjująca baze danych
@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Zainicjowano bazę danych")

# Komenda dodająca do bazy danych przykładowe pomiary
@app.cli.command("seed-db")
def seed_db_command():
    db = get_db()
    howManyMeasurements = db.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
    if howManyMeasurements == 0:
        db.executemany("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [[36, 82, 38], [76, 64, 23], [23, 54, 24]])
        db.commit()
        print("✔ dane przykladowe zostaly dodane do tabeli measurements")
    else:
        print("tabela zawiera juz dane")

# Komenda dodająca do bazy danych losowy jeden pomiar
@app.cli.command("add-measure")
def add_measure_command():
    me_1 = round(secrets.SystemRandom().uniform(2.5, 100), 2)
    me_2 = round(secrets.SystemRandom().uniform(2.5, 100), 2)
    me_3 = round(secrets.SystemRandom().uniform(2.5, 100), 2)
    db = get_db()
    db.execute("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [me_1, me_2, me_3])
    db.commit()
    print("Dodano pomiar")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    db = get_db()
    measurements = db.execute("SELECT * FROM measurements").fetchall()
    return render_template('weather.html', measurements=measurements)

if __name__ == '__main__':    app.run(host='0.0.0.0', port=5001, debug=True) # uruchamia serwer Flask na porcie 5001, dostępny dla wszystkich interfejsów sieciowych.