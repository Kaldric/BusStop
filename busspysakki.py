import requests
import json


#tarvitaan pysäkki numero, jonka avulla parsetaan vehicle activitystä vain ko. pysäkille seuraavaksi tulevat 
#tarvitaan myös tämän hetken aika samassa formaatissa kuin pysäkkidatassa, löytyy responsesta

response = requests.get("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")



dictio = response.json()

print(dictio)    




