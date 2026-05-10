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

# API .............................................................................................

@app.route('/api/weather/post', methods=['POST']) # to jest dodawanie danych
def api_post_wheather():
    data = request.json #BEDZIE PRZYJMOWAĆ NOWE DATA W JSON

    if not data or 'temp' not in data or 'hum' not in data:
        return jsonify({"error": "Brak danych"}), 400
    new_entry = {
    "temp": data['temp'],
    "hum": data['hum'],
    "press": data['press'],
    }

    db = get_db()
    db.execute("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [new_entry['temp'], new_entry['hum'], new_entry['press']])
    db.commit()

    # Zapisz dane do bazy danych
    return jsonify({"message": "dane zapisane"}), 201

@app.route("/api/weather/get", methods=["GET"])
def api_measure_list():
    db = get_db()
    rows = db.execute("SELECT id, temp, hum, press, created_at FROM measurements ORDER BY created_at DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/weather/get/<int:measure_id>", methods=["GET"])
def api_measure_get(measure_id):
    db = get_db()
    row = db.execute("SELECT id, temp, hum, created_at FROM measurements WHERE id = ?", [measure_id]).fetchone()
    if row is None:
        abort(404, description="measure not found")
    return jsonify(dict(row))

@app.route("/api/weather/delete/<int:measure_id>", methods=["POST"])
def delete_measurement(measure_id):
    db = get_db()
    db.execute("DELETE FROM measurements WHERE id = ?", [measure_id])
    db.commit()
    return redirect(url_for("database"))

# Strony HTML .............................................................................................

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    db = get_db()
    measurements = db.execute("SELECT * FROM measurements").fetchall()
    return render_template('weather.html', measurements=measurements)

@app.route('/database')
def database():
    db = get_db()
    measurements = db.execute("SELECT * FROM measurements").fetchall()
    return render_template('database.html', measurements=measurements)

if __name__ == '__main__':    app.run(host='0.0.0.0', port=5001, debug=True) # uruchamia serwer Flask na porcie 5001, dostępny dla wszystkich interfejsów sieciowych.