import logging

import azure.functions as func
import os
import requests
import json

COULD_NOT_PARSE = "Couldn't get the air pollution there"

QUALITY_INDEX = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

def getAQI(lat, lon):
    api_key = os.environ["API_key"]
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    resp = requests.get(url)
    if resp.status_code == 200:
        body = json.loads(resp.text)
        aqi = body['list'][0]['main']['aqi']
        return aqi
    return COULD_NOT_PARSE

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = None;
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    
    lattitude = req.params.get('lattitude')
    if not lattitude and req_body:
        lattitude = req_body.get('lattitude')
    longitude = req.params.get('longitude')
    if not longitude and req_body:
        longitude = req_body.get('longitude')

    if lattitude and longitude:
        air_pollution = getAQI(lattitude, longitude)
        if air_pollution != COULD_NOT_PARSE:
            return func.HttpResponse(f"The AQI at that area is {QUALITY_INDEX[air_pollution]}.", status_code=200)
        else:
            return func.HttpResponse(air_pollution, status_code=200)
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass lattitude and longitude in the query string or request body to get the AQI at that location.\n\nExample:\n{\n\t\"lattitude\": \"47.60357\"\n\t\"longitude\": \"-122.32945\"\n}",
            status_code=200
        )
