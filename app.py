from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

@app.route("/")
def root():
    query = """
    SELECT url
    FROM urls
    """

    urls = db.engine.execute(query)

    return render_template("main.html", urls=urls)

@app.route("/register-client")
def new_post():
    return render_template("newclient.html")

@app.route("/insert_client", methods = ["POST"])
def insert_client():
    query = """
    INSERT INTO urls (url)
    VALUES ('{}')
    """ 

    url = request.form["title"]

    db.engine.execute(query.format(url))

    return render_template("confirmation.html")


@app.route("/dashboard")
def get_dashboard():
    query = """
    SELECT count(*), url
    FROM counts
    GROUP BY url
    ORDER BY count(*) DESC
    LIMIT(10)
    """

    urls = db.engine.execute(query)

    return render_template("dashboard.html", urls=urls)

@app.route("/url/<url>")
def insert_count(url):
    query = """
    INSERT INTO counts (url)
    VALUES ('{}')
    """


    db.engine.execute(query.format(url))

    return render_template("confirmationcount.html")


db.init_app(app)
app.run()