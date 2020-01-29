import requests
import json


oldWantedStop = ""

while True:
    r = requests.get("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
    restop = requests.get("http://data.itsfactory.fi/journeys/api/1/stop-points")


    parsed_stop = restop.json()

    expectedArrival = ""
    busNumber = ""
    stopPoint = ""
    stopName = ""

    

    wantedStop = input("Pelkällä enterillä päivität vanhan haun. \nSyötä pysäkin nimi tai 'poistu': ")
    if wantedStop.upper() == "KESKUSTORI":
        wantedStop = input("Tarvitaan tarkennus, syötä Keskustorin lisäksi pysäkin kirjain esim. 'Keskustori M': ")
    elif wantedStop.upper() == "POISTU":
        print("Näkemiin!")
        break
    elif wantedStop.upper() == "":
        if oldWantedStop != "":
            wantedStop = oldWantedStop
        else:
            print("Et voi päivittää vanhaa hakua ilman vanhaa hakua.")
    
    stopDictio = parsed_stop['body']
    oldWantedStop = wantedStop

    for stop in stopDictio:
        if stop['name'].upper() == wantedStop.upper():
            stopPoint = stop['url']
            stopName = stop['name']

    if stopPoint == "":    
        print("Antamaasi pysäkkiä ei löytynyt. Tarkista oikeinkirjoitus.")

    parsed = r.json()

    currentTime = parsed['body'][0]['recordedAtTime']

    dictio = {}
    dictio = parsed['body']

    found = []
    found.clear()

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
                foundOne =   "{:5} bussi numero {:2} on pysäkillä {}. {:3} minuuttia jäljellä.".format(str(expectedArrival), str(busNumber), stopName, str(minErotus)) 
                foundOne = str(foundOne)
                found.append(foundOne)

    found.sort()

    for e in found:
        print(e)