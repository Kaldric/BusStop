import json
import requests

CHARSET = 'UTF-8'

listOfStops = ["0003","0036","0035","0015","0014","0010","0011","0012","0042","0002","0001","0008","0007","0005","0041","5102","5103","4998","5008","5007","0522","0523"]

def busStopTre(event, context):
    searchTerm = event.get('body').split("=")[1]
    searchTerm = str(searchTerm).replace("+", " ")
    parsedBus = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
    parsedStop = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/stop-points")
    stopList = matchingWithStop(searchTerm, parsedStop)   
    
    if len(stopList) == 3:
        successbody = "<html> <body> <p>" + sortAndReturnList(busesForStop(stopList, parsedBus, getCurrentTime(parsedBus))) + "<p> </body> </html>"
        return  str(successbody)
            
    
    else: 
        failurebody = "<html> <body> <p>" + notMatchingWithStop(searchTerm, parsedStop) + "</p> </body> </html>"
        return str(failurebody)
        
      
def getDatatoDictionary(url):  
    return requests.get(url).json()


def matchingWithStop(searchTerm, parsedStop):                                                                                   #funktio(ottaa sisään nimen tai numeron) joka etsii searchTerm => stopDatasta, tuloksena oikea pysäkki ja sen data listana
    foundStop = []
    foundStop.clear()
    for stop in parsedStop['body']:
        if (stop['name'].upper() == searchTerm.upper() or stop['shortName'] == searchTerm):
            foundStop.append(stop['url']) 
            foundStop.append(stop['name']) 
            foundStop.append(stop['shortName'])                                                           #0 = url, 1 =  nimi, 2 = numero
    
    return foundStop


def notMatchingWithStop(searchTerm, parsedStop):
    notFounds = []                                                                                 #funktio(0-3 merkit searchTermistä): jos ei löydy palauttaa haun ensimmäisiin 3 merkkiin sopivat vaihtoehdot                                                                           
    for stop in parsedStop['body']:                                                
            if (searchTerm[0:3].upper() == stop['name'][0:3].upper() or searchTerm[0:3] == stop['shortName'][0:3]):
                notFounds.append("<p>{} ({})".format(stop['name'], stop['shortName'],"<br></p>"))
    return sortAndReturnList(notFounds) + "<p>The stop you provided was not found or there are multiple stops with the same name. Please check the spelling from the list above or use the bus stop number.</p>"
    


def getCurrentTime(parsedBus):
    return parsedBus['body'][0]['recordedAtTime'][11:16]


def busesForStop(foundStop, parsedBus, currentTime):                                                                            #kun oikea pysäkki löytyy funktio(pysäkki): hakee bussit, jotka pysähtyvät ko. pysäkillä
    notFoundlist = []
    notFoundlist.clear()
    notFoundlist.append("Unfortunately there are no buses stopping at this stop in the near future.")
    foundBuses = []
    foundBuses.clear()
    busNumber = ""
    expectedArrival = ""
    arrivalInMin = ""
    minDifference = ""
    timeInMin = int(currentTime[0:2]) * 60 + int(currentTime[3:5])
    for bus in parsedBus['body']:
        onwardCalls = bus['monitoredVehicleJourney']['onwardCalls']
        stopsAtKtori = False                                                                                                        #0-14
        orderKtori = 0
        stopsAtTAYS = False                                                                                                         #15-19
        orderTAYS = 0
        stopsAtBusStation = False                                                                                                   #20-21
        orderBusStation = 0
        for call in onwardCalls:
            if call['stopPointRef'][-4:] in listOfStops:
                    if call['stopPointRef'][-4:] in listOfStops[0:15]:
                        stopsAtKtori = True
                        orderKtori = call['order']
                    if call['stopPointRef'][-4:] in listOfStops[15:20]:
                        stopsAtTAYS = True
                        orderTAYS = call['order']
                    if call['stopPointRef'][-4:] in listOfStops[20:22]:
                        stopsAtBusStation = True
                        orderBusStation = call['order']
        for call in onwardCalls:
            if call['stopPointRef'][-4:] == foundStop[0][-4:]:
                busNumber = bus['monitoredVehicleJourney']['lineRef']
                expectedArrival = call['expectedArrivalTime']
                callOrder = int(call['order'])
                if callOrder > int(orderKtori):
                    stopsAtKtori = False
                if callOrder > int(orderTAYS):
                    stopsAtKtori = False
                if callOrder > int(orderBusStation):
                    stopsAtKtori = False
                expectedArrival = expectedArrival[11:16] 
                arrivalInMin = int(expectedArrival[0:2]) * 60 + int(expectedArrival[3:5])
                minDifference = arrivalInMin - timeInMin
                foundOne = "<p>At {:5} bus number {:2} will be at the stop {} ({}) in {:3} minutes. Stops at: Town square {}, TAYS (hospital) {}, Bus station {}.<br></p>".format(str(expectedArrival), str(busNumber), foundStop[1], foundStop[2], str(minDifference), stopsAtKtori, stopsAtTAYS, stopsAtBusStation)
                foundBuses.append(foundOne)
           
    if len(foundBuses) > 0:
        if foundStop[0][-4:] == ("0522"):
            foundBuses.append("Note that this stop is on the bus station's side of the road. For the one on the other side look up bus stop number 0523.")
        elif foundStop[0][-4:] == ("0523"):
            foundBuses.append("Note that this stop is on the opposite side of the road from the bus station. For the one on the bus station's side look up bus stop number 0522.")
        return foundBuses  
    else: 
        return notFoundlist
  
   
def sortAndReturnList(busesForStop):
    stringlist = "<table>"
    busesForStop.sort()
    for bus in busesForStop:
        stringlist = stringlist + "<tr>" + bus + "</tr>"
    stringlist = stringlist + "</table>"
    return stringlist