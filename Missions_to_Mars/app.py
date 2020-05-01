
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_code")


@app.route("/")
def index():
    mars_code = mongo.db.mars_code.find_one()
    return render_template("index.html", mars_code=mars_code)


@app.route("/scrape")
def scrape():
    mars_facts = scraping.scrape_info()
    mars_facts = scraping.scrape_image()
    mars_facts = scraping.scrape_weather()
    mars_facts = scraping.scrape_table()

    mongo.db.collection.update({}, mars_facts, upsert=True)

    return redirect("/")

    if __name__ == '__main__':
        app.run(debug=True)
