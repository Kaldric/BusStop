import requests
import json


def getDatatoDictionary(url):  
    return requests.get(url).json()


#busDictio = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")

#stopDictio = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/stop-points")

busDictio = getDatatoDictionary("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")

print(busDictio)

