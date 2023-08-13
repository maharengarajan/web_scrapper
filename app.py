from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq

app = Flask(__name__)

#route to display home page
@app.route('/', methods=['GET'])
def home_page():
    return render_template()

# route to show the review comments in a web UI
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            uClient = ureq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()

        
        
        
        
        
        
        except:
            pass



