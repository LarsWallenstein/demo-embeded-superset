from crypt import methods
from distutils.debug import DEBUG
from urllib import request, response
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests;
import json;
import time;

#configuration
DEBUG = True

# instantiate
app = Flask(__name__)
app.config.from_object(__name__)

#enable CORS
CORS(app, resources={r'/*': {'Origins': '*'}})

#By default access token expires in 300 seconds, can be changed in Superset config
GUEST_TOKEN_JWT_EXP_SECONDS = 295 # 5 seconds prefetch to expire

PROTOCOL = "http"
SUPERSET_DOMAIN = "192.168.39.188:30034"

API_GUEST_TOKEN   = "/api/v1/security/guest_token/"
API_REFRESH_TOKEN = "/api/v1/security/refresh"
API_ACCESS_TOKEN = "/api/v1/security/login"

ADMIN = {
      "password": "admin",
      "provider": "db",
      "refresh": True,
      "username": "admin"
}

# user info from superset databse (registered) with enough privileges (GAMMA) at the moment
USER = {
    "username" : "alex",
    "first_name" : "App",
    "last_name" : "Vue"
}

# Dashboard filtering clause, 
# Dashboard shows contents of some table as a result of a SQL query
# CLAUSE is passed into the WHERE part of query
CLAUSE = "score>2"

TOKENS = {
    "ACCESS_TOKEN":"",
    "REFRESH_TOKEN":"",
    "ACCESS_TOKEN_FETCHED":"",
    "GUEST_TOKEN":""
}

# First request to get tokens
def get_tokens():
    '''
        First we fetch access_token along with refresh_token
    '''
    url = f"{PROTOCOL}://{SUPERSET_DOMAIN}{API_ACCESS_TOKEN}"

    payload = json.dumps(ADMIN)

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)

    TOKENS["ACCESS_TOKEN_FETCHED"] = time.time()    
    TOKENS["ACCESS_TOKEN"] = response_dict["access_token"]
    TOKENS["REFRESH_TOKEN"] = response_dict["refresh_token"]

get_tokens()

def refresh_access_token():
    url = f"{PROTOCOL}://{SUPERSET_DOMAIN}{API_REFRESH_TOKEN}"
    headers = {
      'Authorization': f'Bearer {TOKENS["REFRESH_TOKEN"]}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers)
    response_dict = json.loads(response.text)
    
    TOKENS["ACCESS_TOKEN_FETCHED"] = time.time()
    TOKENS["ACCESS_TOKEN"] = response_dict["access_token"]
    
def get_guest_token(dashboard_id = 'f93f686e-5672-4917-b0ef-675f8ee8f683'):
    # Such request for each seperate dashboard... Needs further examination
    url = f"{PROTOCOL}://{SUPERSET_DOMAIN}{API_GUEST_TOKEN}"

    if time.time()-TOKENS["ACCESS_TOKEN_FETCHED"]>GUEST_TOKEN_JWT_EXP_SECONDS:
        refresh_access_token()

    payload = json.dumps({
      "user": USER,
      "resources": [
        {
          "type": "dashboard",
          "id": f"{dashboard_id}"
        }
      ],
      "rls": [
        {
          "clause": CLAUSE 
        }
      ]
    })

    headers = {
      'Authorization': f'Bearer {TOKENS["ACCESS_TOKEN"]}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)

    TOKENS["GUEST_TOKEN"] = response_dict.get("token")
      

@app.route('/guest_token', methods=['GET'])
def guest_token():

    dashboard_id = request.args.get('id')
    get_guest_token(dashboard_id=dashboard_id)

    response_object = {
        'status': 'success',
        'guest_token': TOKENS["GUEST_TOKEN"]
        }
    return jsonify(response_object)



if __name__ == '__main__':
    app.run()