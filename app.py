import sqlite3
import time
from flask import Flask, render_template, g, request, redirect, jsonify
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mpld3


app = Flask(__name__, static_folder="static", template_folder="templates")



# Database Creation
connect = sqlite3.connect('database.db') #Connects to the database (will create it if it doesn't exits)
c = connect.cursor() #creates cursor which executes SQL
c.execute(''' 
CREATE TABLE IF NOT EXISTS planned_session (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date TEXT NOT NULL,
          topic TEXT NOT NULL) ''')

c.execute('''
CREATE TABLE IF NOT EXISTS completed_session (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date TEXT NOT NULL,
          start_time TEXT NOT NULL,
          end_time TEXT NOT NULL,
          duration TEXT NOT NULL,
          topic TEXT) ''')
connect.commit()
connect.close()


#Nav functions
@app.route("/")
def home():
    chart = plot_graph()
    return render_template("home.html", chart=chart)

@app.route("/graph")
def plot_graph():
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('SELECT date, SUM(duration) as total_duration FROM completed_session GROUP BY date ORDER BY date')
    result = c.fetchall()
    dates = []
    duration = []

    for i in result:
        dates.append(i[0])
        duration.append(i[1])
    
    fig, ax = plt.subplots()
    
    ax.bar(dates, duration)
    ax.set_title('Duration per Date')
    ax.set_xlabel('Date')
    ax.set_ylabel('Hours of study')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    figure = mpld3.fig_to_html(fig)
    connect.close()
    return render_template("home.html", chart=figure)


    




@app.route("/view")
def view():
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('SELECT * FROM completed_session')
    view_sessions = c.fetchall()

    c.execute('SELECT * FROM planned_session')
    planned_sessions = c.fetchall()
    connect.close()
    return render_template("view_sessions.html", view_sessions=view_sessions, planned_sessions = planned_sessions)

@app.route("/run")
def run():
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('SELECT start_time FROM completed_session WHERE end_time = "TBD"')
    row = c.fetchone()
    connect.close()

    start_time = row[0] if row else None
    return render_template("run_sessions.html")

@app.route("/start_session", methods=["POST"])
def start_session():
    start_time = datetime.now().strftime("%H:%M:%S")
    session_date = datetime.now().strftime("%d/%m/%Y")
    topic = request.form.get("topic")
    duration = request.form.get("duration")
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('INSERT INTO completed_session (date, start_time, end_time, duration) VALUES (?, ?, ?, ?)', (session_date, start_time, "TBD", duration))
    connect.commit()
    if topic != "":
        c.execute('UPDATE completed_session SET (topic) = (?) WHERE end_time = "TBD"', (topic,))
        connect.commit()
    connect.close()
    return redirect("/run")

@app.route("/end_session", methods=["POST"])
def end_session():
    end_time = datetime.now().strftime("%H:%M:%S")
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('SELECT start_time FROM completed_session WHERE end_time = "TBD"')
    start_time = c.fetchone()       
    if start_time is None:
        connect.close()
        return "No active session found", 400
    
    start_time_str = start_time[0]
    
    start_time_dt = datetime.strptime(start_time_str, "%H:%M:%S")
    end_time_dt = datetime.strptime(end_time, "%H:%M:%S")
    delta = end_time_dt - start_time_dt

    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    duration = f"{hours:02}:{minutes:02}:{seconds:02}"

    c.execute('UPDATE completed_session SET (end_time, duration) = (?, ?) WHERE end_time = "TBD"', (end_time, duration,))
    connect.commit()
    connect.close()
    return redirect("/view")

@app.route("/calculate_current_duration")
def current_duration():
    connect = sqlite3.connect('database.db')
    c = connect.cursor()
    c.execute('SELECT start_time, duration FROM completed_session WHERE end_time = "TBD"')
    record_results = c.fetchone()

    if record_results:
        start_time_str, planned_minutes = record_results
        planned_minutes = int(planned_minutes)
        start_time_dt = datetime.strptime(start_time_str, "%H:%M:%S")
        now = datetime.now().time() 
        now_in_seconds = (now.hour * 3600) + (now.minute * 60) + now.second
        st = datetime.strptime(start_time_str, "%H:%M:%S").time()
        start_in_seconds = (st.hour * 3600) + (st.minute * 60) + st.second
        elapsed_seconds = now_in_seconds - start_in_seconds
        total_planned_seconds = planned_minutes * 60
        progress = (elapsed_seconds / total_planned_seconds) * 100
        progress = max(0, min(round(progress, 2), 100))
        elapsed_minutes = int(elapsed_seconds // 60)
    else:
        elapsed_minutes = 0
        planned_minutes = 1
        progress = 0
    return jsonify({"elapsed":elapsed_minutes, "planned": planned_minutes, "progress": progress})


@app.route("/view", methods=["POST", "GET"])
def saveDetails():
    if request.method == "POST":
        try:
            topic = request.form.get("topic")
            date = request.form.get("date")
            with sqlite3.connect("database.db") as connect:
                c = connect.cursor()
                c.execute("INSERT INTO planned_session (date, topic) VALUES (?, ?)", (date,topic))
                connect.commit()
            return redirect("/view")
        except Exception as e:
            return f"Databse error: {e}"
    return render_template("view_sessions.html")

@app.route("/delete", methods=["POST", "GET"])
def delete_record():
    if request.method == "POST":
        record = request.form['record_id']
        table = request.form['table_name']
        with sqlite3.connect("database.db") as connect:
            c = connect.cursor()
            if table == "planned_session":
                c.execute("DELETE FROM planned_session WHERE id = ?", (record,))
            else: 
                c.execute("DELETE FROM completed_session WHERE id = ?", (record,))
            connect.commit()
        return redirect("/view")



if __name__ == "__main__":
    app.run(debug=True)