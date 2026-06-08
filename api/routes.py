from flask import request, jsonify, abort, Blueprint
from db import get_db

api = Blueprint('api', __name__)


@api.route('/api/weather/post', methods=['POST']) # this is adding data
def api_post_wheather():
    data = request.json # WILL RECEIVE NEW DATA IN JSON

    if not data or 'temp' not in data or 'hum' not in data:
        return jsonify({"error": "Missing data"}), 400
    new_entry = {
    "temp": data['temp'],
    "hum": data['hum'],
    "press": data['press'],
    }

    db = get_db()
    db.execute("INSERT INTO measurements(temp, hum, press) VALUES (?, ?, ?)", [new_entry['temp'], new_entry['hum'], new_entry['press']])
    db.commit()

    # Save data to the database
    return jsonify({"message": "data saved"}), 201

@api.route("/api/weather/get", methods=["GET"])
def api_measure_list():
    db = get_db()
    rows = db.execute("SELECT id, temp, hum, press, created_at FROM measurements ORDER BY created_at DESC").fetchall()
    return jsonify([dict(row) for row in rows])

@api.route("/api/weather/get/<int:measure_id>", methods=["GET"])
def api_measure_get(measure_id):
    db = get_db()
    row = db.execute("SELECT id, temp, hum, created_at FROM measurements WHERE id = ?", [measure_id]).fetchone()
    if row is None:
        abort(404, description="measure not found")
    return jsonify(dict(row))

@api.route("/api/weather/delete/<int:measure_id>", methods=["DELETE", "POST"])
def api_delete_measurement(measure_id):
    db = get_db()
    cur = db.execute("DELETE FROM measurements WHERE id = ?", [measure_id])
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "measurement not found"}), 404
    return jsonify({"message": "measurement deleted"}), 200
