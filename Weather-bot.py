import json
import os
from flask import Flask
from flask import request
from flask import make_response
import requests

app = Flask(__name__)
@app('/webhook',methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    #force will convert the incoming data to json and it will use that data accordingly
    #silent will returns none if the incoming data is not in proper format without througing an exception 
    print(json.dumps(req,indent=4))
    res = makerespone(req)
    res = json.dumps(res, indent =4)
    r = make_response(res)
    # this flask function will setup the response in the right format
    r.headers['Content-Type']= 'application/json'

def makeresponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r = request.get('api.openweathermap.org/data/2.5/forecast?q='+city+'api=0f083506be5607c1c5314158c0b683b9')
    json_object = r.json()
    weather = json_object('list')
    for i in len(weather):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
    
    #The dialogflow expect the response from the webhook as
    #{"speech":"","display_text":"","source":""}   
    speech = 'The weather forecast for'+city+'for'+date+'is:'+condition
    return {
        "speech":speech,
        "display_text": speech,
        "source":"apiai-weather-webhook"
    }
if '__name__'=='__main__':
    port = int(os.getenv('PORT',5000))
    app.run(debug=False,port=port,host='0.0.0.0')
