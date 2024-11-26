from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe_search")
def home():
    return render_template("recipe_search.html")


@app.route("/nutrition_tracker")
def home():
    return render_template("nutrition_tracker.html")


@app.route("/saved_recipes")
def home():
    return render_template("saved_recipes.html")