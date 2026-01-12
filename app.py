import sqlite3
from flask import Flask, render_template, g

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

#Database functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Nav functions
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/view")
def view():
    return render_template("view_sessions.html")

@app.route("/run")
def run():
    return render_template("run_sessions.html")

if __name__ == "__main__":
    app.run(debug=True)