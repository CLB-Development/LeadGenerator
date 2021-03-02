from flask import Flask, render_template, request, jsonify
import FlaskProject
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    category = 'computers'
    listings = FlaskProject.getListingsFrom('https://www.nzdirectory.co.nz/{}.html'.format(category), 'https://www.nzdirectory.co.nz/')
    return render_template("index.html", listings=listings)