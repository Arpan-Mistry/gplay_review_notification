'''
No need to run this api.......(this is just for Referance)
I have Deployed this API on My Heroku,Live link of same api: https://gplay-rev-api.herokuapp.com/key    plz enter pkg_name in place of key
examples of package names : com.twitter.android OR com.facebook.katana OR com.whatsapp OR  com.phonepe.app ETC.......
'''

from google_play_scraper import Sort, reviews
from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def info():
    return f"<h2>please add Package_name at the end of url with /<br>Ex: http://127.0.0.1:5000/com.facebook.katana</h2>"

@app.route('/<string:input>')
def index(input):
    pkg_name=input
    result = reviews(
        pkg_name,
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count=50, # defaults to 100
        filter_score_with=None # defaults to None(means all score)
        )
    return jsonify(result[0])
if __name__ =="__main__":
    app.run(debug=True)





