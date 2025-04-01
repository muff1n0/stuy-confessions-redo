from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def num_rows():
    con = sqlite3.connect("confessions.db")
    cur = con.cursor()
    cur.execute("select count(*) from post")
    return cur.fetchone()[0]

@app.route("/submit")
def subpage():
    return render_template("submit.html")

@app.route("/submits", methods=["POST", "GET"])
def submit():
    con = sqlite3.connect("confessions.db")
    cur = con.cursor()
    cur.execute("create table if not exists post(id, title, confession, upvotes)")
    if request.method == "POST":
        conf_id = num_rows()
        title = request.form.get("title")
        conf = request.form.get("confession")
        cur.execute("insert into post (id, title, confession, upvotes) values (?, ?, ?, ?)", (conf_id, title, conf, 0))
        con.commit()
        return redirect(url_for("fetch"))
    return render_template("submit.html")

@app.route("/", methods=["GET"])
def fetch():
    con = sqlite3.connect("confessions.db")
    cur = con.cursor()
    cur.execute("create table if not exists post(id, title, confession, upvotes)")
    res = cur.execute("select * from post")
    confessions = res.fetchall()
    return render_template("submissions.html", confessions=confessions)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)