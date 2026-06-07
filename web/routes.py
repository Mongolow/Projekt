from flask import request, render_template, redirect, url_for, Blueprint
from db import get_db
from city_coordinates import city_coordinates
from outside_weather import outside_weather
import pygal 
import math

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
        return render_template('weather.html', measurements=measurements, outside=outside_data, current_city=city)
    except Exception as e:
        return render_template('weather.html', measurements=measurements, outside=None, current_city=city)

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

# Usuwanie pomiaru z bazy danych
@web.route("/delete_measurement/<int:measure_id>", methods=["POST"])
def delete_measurement(measure_id):
    db = get_db()
    db.execute("DELETE FROM measurements WHERE id = ?", [measure_id])
    db.commit()
    return redirect(url_for("web.database"))

@web.route("/charts", methods=['POST', 'GET'])
def chart():
    # TEMPERATURE

    chart  = pygal.Line(fill=True)
    chart.title = 'Temperature'
    db = get_db()
    rows = db.execute("SELECT temp FROM measurements").fetchall()
    dates = db.execute("SELECT created_at FROM measurements").fetchall()
    if len(dates) > 15 and len(dates) <= 50:
        dates = dates[::3]
        rows = rows[::3]
    elif len(dates) > 50 and len(dates) <= 100:
        dates = dates[::5]
        rows = rows[::5]
    elif len(dates) > 100 and len(dates) <= 200:
        dates = dates[::12]
        rows = rows[::12]
    elif len(dates) > 200:
        dates =dates[-150::12]
        rows = rows[-150::12]
    dates_hours = []
    for date in dates:
        date = date[0][11:16]
        dates_hours.append(date)
    chart.x_labels = dates_hours
    temps = [row['temp'] for row in rows]
    chart.add('Temperature', temps)
    chart.render_to_png('static/temp_plot.png')
    # HUM

    chart2 = pygal.Line(fill=True)
    chart2.title = 'Humidity'
    db = get_db()
    rows = db.execute("SELECT hum FROM measurements").fetchall()
    dates = db.execute("SELECT created_at FROM measurements").fetchall()
    if len(dates) > 15 and len(dates) <= 50:
        dates = dates[::3]
        rows = rows[::3]
    elif len(dates) > 50 and len(dates) <= 100:
        dates = dates[::5]
        rows = rows[::5]
    elif len(dates) > 100 and len(dates) <= 200:
        dates = dates[::12]
        rows = rows[::12]
    elif len(dates) > 200:
        dates =dates[-150::12]
        rows = rows[-150::12]
    dates_hours = []
    for date in dates:
        date = date[0][11:16]
        dates_hours.append(date)
    chart2.x_labels = dates_hours
    hums = [row['hum'] for row in rows]
    chart2.add('Humidity', hums)
    chart2.render_to_png('static/hum_plot.png')
    # PRESSURE
    
    chart3  = pygal.Line(fill=True)
    chart3.title = 'Pressure'
    db = get_db()
    rows = db.execute("SELECT press FROM measurements").fetchall()
    dates = db.execute("SELECT created_at FROM measurements").fetchall()
    if len(dates) > 15 and len(dates) <= 50:
        dates = dates[::3]
        rows = rows[::3]
    elif len(dates) > 50 and len(dates) <= 100:
        dates = dates[::5]
        rows = rows[::5]
    elif len(dates) > 100 and len(dates) <= 200:
        dates = dates[::12]
        rows = rows[::12]
    elif len(dates) > 200:
        dates =dates[-150::12]
        rows = rows[-150::12]
    dates_hours = []
    for date in dates:
        date = date[0][11:16]
        dates_hours.append(date)
    chart3.x_labels = dates_hours
    presses = [row['press'] for row in rows]
    chart3.add('Pressure', presses)
    chart3.render_to_png('static/press_plot.png')
    # RENDER TEMPLATE

    return render_template('charts.html')
