import requests
import json
from datetime import datetime


#tarvitaan pysäkki numero, jonka avulla parsetaan vehicle activitystä vain ko. pysäkille seuraavaksi tulevat  
#tarvitaan myös tämän hetken aika samassa formaatissa kuin pysäkkidatassa, löytyy responsesta

r = requests.get("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")

expectedArrival = ""
busNumber = ""

stopPoint = 'http://178.217.134.14/journeys/api/1/stop-points/5116'

parsed = r.json()

currentTime = parsed['body'][0]['recordedAtTime']

dictio = {}
dictio = parsed['body']



for data in dictio:
    onwardCalls = data['monitoredVehicleJourney']['onwardCalls']
    for call in onwardCalls:
        if call['stopPointRef'] == stopPoint:
            busNumber = data['monitoredVehicleJourney']['lineRef']
            expectedArrival = call['expectedArrivalTime']
            print("Bussinumero ", busNumber, " on pysäkillä ", expectedArrival, ".\n")


 
      








   
    #currentTime = data["recordedAtTime"]
    #if data["monitoredVehicleJourney"]:
     #   busNumber = data_by_bus[dat["lineRef"]]
      #  if dat["onwardCalls"]:
            







