from charset_normalizer import api
from flask import Flask, g
from db import get_db
from api.routes import api
from web.routes import web
import secrets


app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(web)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS measurements(
id INTEGER PRIMARY KEY AUTOINCREMENT,
temp FLOAT,
hum FLOAT,
press FLOAT,
created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

"""


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Function initializing the database
def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()


# Command initializing the database
@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Database initialized")

# Command adding sample measurements to the database
@app.cli.command("seed-db")
def seed_db_command():
    db = get_db()
    howManyMeasurements = db.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
    if howManyMeasurements == 0:
        db.executemany("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [[36, 82, 38], [76, 64, 23], [23, 54, 24]])
        db.commit()
        print("✔ Sample data has been added to the measurements table")
    else:
        print("Table already contains data")

# Command adding a random measurement to the database
@app.cli.command("add-measure")
def add_measure_command():
    me_1 = round(secrets.SystemRandom().uniform(21, 36), 2)
    me_2 = round(secrets.SystemRandom().uniform(30, 40), 2)
    me_3 = round(secrets.SystemRandom().uniform(990, 1000), 2)
    db = get_db()
    db.execute("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [me_1, me_2, me_3])
    db.commit()
    print("Measurement added")




if __name__ == '__main__':    app.run(host='0.0.0.0', port=5001, debug=True) # Runs Flask server on port 5001, available for all network interfaces.
