from flask import Flask, render_template

app = Flask(__name__)

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