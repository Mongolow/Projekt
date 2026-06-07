from db import get_db
import pygal 

def render_chart(chart_type):
    if chart_type == 'temp':

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
    elif chart_type == 'hum':

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
    elif chart_type == 'press':

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