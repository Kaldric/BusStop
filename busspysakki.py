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

found = []

currentTime = currentTime[11:16]
print("Kello on: ", currentTime)
minTime = int(currentTime[0:2]) * 60 + int(currentTime[3:6])
for data in dictio:
    onwardCalls = data['monitoredVehicleJourney']['onwardCalls']
    for call in onwardCalls:
        if call['stopPointRef'] == stopPoint:
            busNumber = data['monitoredVehicleJourney']['lineRef']
            expectedArrival = call['expectedArrivalTime']
            expectedArrival = expectedArrival[11:16]
            minArrival = int(expectedArrival[0:2]) * 60 + int(expectedArrival[3:5])
            minErotus = (minArrival - minTime)
            print(minArrival, minTime)
            foundOne = str("{:02}".format(minErotus)) + " minuutin päästä bussi (" + str(busNumber) + ") on pysäkillä kello: " + str(expectedArrival)
            foundOne = str(foundOne)
            found.append(foundOne)

found.sort()

for e in found:
    print(e)

 
      








   
    #currentTime = data["recordedAtTime"]
    #if data["monitoredVehicleJourney"]:
     #   busNumber = data_by_bus[dat["lineRef"]]
      #  if dat["onwardCalls"]:
            







