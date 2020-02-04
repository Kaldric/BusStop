import requests
import json




#POST-function
def doesitwork(searchTerm):
    parsedBus = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")        
    parsedStop = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/stop-points")   
    stopList = matchingWithStop(searchTerm, parsedStop)
    if len(stopList) > 0:
        return sortAndReturnList(busesForStop(stopList, parsedBus, getCurrentTime(parsedBus)))
    else: 
        notMatchingWithStop(searchTerm, parsedStop)


def getDatatoDictionary(url):  
    return requests.get(url).json()


def matchingWithStop(searchTerm, parsedStop):                                                                                   #funktio(ottaa sisään nimen tai numeron) joka etsii searchTerm => stopDatasta, tuloksena oikea pysäkki ja sen data listana
    foundStop = []
    foundStop.clear()
    for stop in parsedStop['body']:
        if (stop['name'].upper() == searchTerm.upper() or stop['shortName'] == searchTerm):
            foundStop = [stop['url'], stop['name'], stop['shortName']]                                                          #0 = url, 1 =  nimi, 2 = numero
    return foundStop


def notMatchingWithStop(searchTerm, parsedStop):
    searchTerm = searchTerm                                                                                 #funktio(0-3 merkit searchTermistä): jos ei löydy palauttaa haun ensimmäisiin 3 merkkiin sopivat vaihtoehdot                                                                           
    for stop in parsedStop:                                                
            if (searchTerm[0:3].upper() == stop['name'][0:3].upper() or searchTerm[0:3] == stop['shortName'][0:3]):
                return ("{} ({})".format(stop['name'], stop['shortName']))
    return "The stop you provided was not found. Please check the spelling from the list above."


def getCurrentTime(parsedBus):
    return parsedBus['body'][0]['recordedAtTime'][11:16]


def busesForStop(foundStop, parsedBus, currentTime):                                                                            #kun oikea pysäkki löytyy funktio(pysäkki): hakee bussit, jotka pysähtyvät ko. pysäkillä
    foundBuses = []
    foundBuses.clear()
    busNumber = ""
    expectedArrival = ""
    arrivalInMin = ""
    minDifference = ""
    timeInMin = int(currentTime[0:2]) * 60 + int(currentTime[3:5])
    for bus in parsedBus['body']:
        onwardCalls = bus['monitoredVehicleJourney']['onwardCalls']
        for call in onwardCalls:
            if call['stopPointRef'][-4:] == foundStop[0][-4:]:
                busNumber = bus['monitoredVehicleJourney']['lineRef']
                expectedArrival = call['expectedArrivalTime'] 
                expectedArrival = expectedArrival[11:16] 
                arrivalInMin = int(expectedArrival[0:2]) * 60 + int(expectedArrival[3:5])
                minDifference = arrivalInMin - timeInMin
                foundOne = "At {:5} bus number {:2} will be at the stop {} ({}) in {:2} minutes.".format(str(expectedArrival), str(busNumber), foundStop[1], foundStop[2], str(minDifference))
                foundBuses.append(foundOne)
    return foundBuses
  
   
def sortAndReturnList(busesForStop):
    busesForStop.sort()
    for bus in busesForStop:
        print(bus)
    











