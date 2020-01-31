import json
import requests

CHARSET = 'UTF-8'

def busStopTre(event, context):
    searchTerm = event['searchTerm']
    parsedBus = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")        
    parsedStop = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/stop-points")   
    stopList = matchingWithStop(searchTerm, parsedStop)
    
    
    if len(stopList) > 0:
        successbody = sortAndReturnList(busesForStop(stopList, parsedBus, getCurrentTime(parsedBus)))
        return {
            "statusCode": 200,
            "body": json.dumps(str(successbody)),
            "headers": {
                'Content-Type': 'text/html'
            }
            
        }
    
    else: 
        failurebody = notMatchingWithStop(searchTerm, parsedStop)
        return {
            "statusCode": 200,
            'body': json.dumps(str(failurebody)),
            "headers": {
                'Content-Type': 'text/html'
            }
            
        }
    
        
def getDatatoDictionary(url):  
    return requests.get(url).json()


def matchingWithStop(searchTerm, parsedStop):                                                                                   #funktio(ottaa sisään nimen tai numeron) joka etsii searchTerm => stopDatasta, tuloksena oikea pysäkki ja sen data listana
    foundStop = []
    foundStop.clear()
    for stop in parsedStop['body']:
        if (stop['name'].upper() == searchTerm.upper() or stop['shortName'] == searchTerm):
            foundStop = [stop['url'], stop['name'], stop['shortName']]                                                          #0 = url, 1 =  nimi, 2 = numero
    return foundStop


def notMatchingWithStop(searchTerm, parsedStop):                                                                                 #funktio(0-3 merkit searchTermistä): jos ei löydy palauttaa haun ensimmäisiin 3 merkkiin sopivat vaihtoehdot                                                                           
    for stop in parsedStop:                                                
            if (searchTerm[0:3].upper() == stop['name'][0:3].upper() or searchTerm[0:3] == stop['shortName'][0:3]):
                return ("<p>{} ({})".format(stop['name'], stop['shortName'],"<br></p>"))
    return "<p>The stop you provided was not found. Please check the spelling from the list above.</p>"


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
                foundOne = "<p>At {:5} bus number {:2} will be at the stop {} ({}) in {:3} minutes.<br></p>".format(str(expectedArrival), str(busNumber), foundStop[1], foundStop[2], str(minDifference))
                foundBuses.append(foundOne)
    return foundBuses
  
   
def sortAndReturnList(busesForStop):
    stringlist = "<html><body>"
    busesForStop.sort()
    for bus in busesForStop:
        stringlist = stringlist + bus
    stringlist = stringlist + "</body></html>"
    return stringlist