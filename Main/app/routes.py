import urllib.parse
from app import app
from app.model import dataBase as db
from flask import request, jsonify
from config import Config
import requests

ALLOWED_DAYS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30, 31]
ALLOWED_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


# POST /dates
@app.route('/dates', methods=['POST'])
def postDate():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonInput = request.json
        if dataValidation(jsonInput):
            return jsonify(db.findDate(prepJsonData(jsonInput))[0]), 201
        else:
            return 'Wrong date format', 400
    else:
        return 'Content-Type not supported', 400


# DELETE /dates/{id}
@app.route('/dates/<int:id>', methods=['DELETE'])
def delDate(id):
    if request.headers.get('X-API-KEY') == Config.SECRET_API_KEY:
        if db.delete(id) > 0:
            return '', 204
        else:
            return "File not found", 404
    else:
        return "Wrong X-API-KEY", 405


# GET /dates
@app.route('/dates')
def allDates():
    return jsonify(db.fetchAll([])), 200


# GET /popular
@app.route('/popular')
def popularMonths():
    return jsonify(db.aggregateByMonth()), 200


# Validation of received date, as described in task, but not the best should check for amount of days in received month
# I weren't sure if it's right so write the better one at the end just additionally, not actually used in this api
def dataValidation(json):
    if json['day'] in ALLOWED_DAYS and json['month'] in ALLOWED_MONTHS:
        return True
    else:
        return False


# Build an URL to request an event from numbersapi.com in json format
def buildURL(json):
    path = f"/{json['month']}/{json['day']}/date?json"
    base = 'http://numbersapi.com/'
    URL = urllib.parse.urljoin(base, path)
    return URL


# Send request and return event for given URL
def checkEvent(json):
    URL = buildURL(json)  # Build Url
    return requests.get(URL).json()['text']


# Prepare file to save in db and return to the user
def prepJsonData(json):
    eventText = checkEvent(json)
    jsonData = {
        "_id": db.countDocs(),
        "month": eventText.split()[0],
        "day": json['day'],
        "text": eventText
    }
    return jsonData

# Example for better date validation for this api

# THIRTY_DAYS_MONTHS = [4, 6, 9, 11]
# THIRTY_ONE_DAYS_MONTHS = [1, 3, 5, 7, 8, 10, 12]
#
#
# def betterDataValidation(json):
#     if json['month'] in THIRTY_DAYS_MONTHS:
#         if json['day'] in ALLOWED_DAYS[:30]:
#             return True
#     elif json['month'] in THIRTY_ONE_DAYS_MONTHS:
#         if json['day'] in ALLOWED_DAYS:
#             return True
#     elif json['month'] == 2:
#         if json['day'] in ALLOWED_DAYS[:29]:
#             return True
#     else:
#         return False
