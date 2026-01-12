import sqlite3
from flask import Flask, render_template, g, request, redirect

app = Flask(__name__)

#Database Creation
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
    return render_template("home.html")


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
    return render_template("run_sessions.html")

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