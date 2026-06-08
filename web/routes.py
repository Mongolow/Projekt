from flask import request, render_template, redirect, url_for, Blueprint
from db import get_db
from render_chart import render_chart
from outside_weather import outside_weather
import math
from datetime import datetime, timezone

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/weather',methods=["GET","POST"])
def weather():
    db = get_db()
    measurements = db.execute("SELECT * FROM measurements").fetchall()
    city= "Krakow" #Domyślne miasto

    user_city= None

    if request.method == "POST":
        try:
            user_city = request.form.get("city")
        except Exception as e:
            print(f"Błąd podczas pobierania danych z formularza: {e}")
            user_city = None

    if user_city:
        try:
            city = user_city
        except Exception as e:
            print(f"Błąd podczas ustawiania miasta: {e}")
            city = "Krakow" # Fallback do domyślnego miasta w przypadku błędu
    try:
        outside_data= outside_weather(city)
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return render_template('weather.html', measurements=measurements, outside=outside_data, current_city=city, current_time=current_time)
    except Exception as e:
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return render_template('weather.html', measurements=measurements, outside=None, current_city=city, current_time=current_time)

@web.route('/database')
def database():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    db = get_db()
    offset = (page - 1) * per_page
    cursor = db.cursor()

    cursor.execute("""SELECT * FROM measurements ORDER BY created_at DESC LIMIT ? OFFSET ? """, (per_page, offset))
    measurements = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM measurements")
    total_records = cursor.fetchone()[0]
    total_pages = math.ceil(total_records / per_page)
    
    return render_template(
        'database.html', 
        measurements=measurements, 
        current_page=page, 
        total_pages=total_pages
    )

@web.route("/delete_measurement/<int:measure_id>", methods=["POST"])
def delete_measurement(measure_id):
    db = get_db()
    db.execute("DELETE FROM measurements WHERE id = ?", [measure_id])
    db.commit()
    return redirect(url_for("web.database"))

@web.route("/charts", methods=['POST', 'GET'])
def chart():

    render_chart('temp')
    render_chart('hum')
    render_chart('press')

    return render_template('charts.html')
