import requests
import json


oldWantedStop = "" #initialisoidaan vanha haku loopin ulkopuolella

while True:         #koska ohjelma, eikä pelkkä script
    r = requests.get("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")   #haetaan bussien data
    restop = requests.get("http://data.itsfactory.fi/journeys/api/1/stop-points")   #haetaan pysäkkien data


    parsed_stop = restop.json()     #parsitaan pysäkkien dataa

    expectedArrival = ""    #init odotettu saapumisaika
    busNumber = ""          #init bussinumero
    stopPoint = ""          #init haettu pysäkki, url
    stopName = ""           #init haettu pysäkki nimi
    stopNumber = ""         #init haetun pysäkin numero

    stopDictio = {}         #init pysäkkidictionary
    stopDictio.clear()      #clearataan
    stopDictio = parsed_stop['body']        #dictionary parsitusta pysäkki-datasta

    wantedStop = input("Enterillä päivität vanhan haun. \nSyötä pysäkin nimi tai numero. Poistuaksesi syötä 'poistu': ")      #input 
    if wantedStop.upper() == "POISTU":
        print("Näkemiin!")
        break
    if wantedStop == "":                        #jos uusi haku tyhjä
        if oldWantedStop != "":                 #jos vanha haku ei ole tyhjä
            wantedStop = oldWantedStop          #vanha hausta uusi haku
    

    oldWantedStop = wantedStop              #uusi haku tallennetaan vanha haku muuttujaan

    for stop in stopDictio:                 #käydään läpi pysäkki-data
        if (stop['name'].upper() == wantedStop.upper() or stop['shortName'] == wantedStop):      #jos pysäkin nimi (caps) tai numero on sama kuin haluttu pysäkki (caps)
            stopPoint = stop['url']                         #stopPointiin tallennetaan löydetyn pysäkin url
            stopName = stop['name']                         #haetaan stopNameen ko. pysäkin nimi
            stopNumber = stop['shortName']                  #haetaan stopNumberiin pysäkin numero

    if stopPoint == "":                                                             #jos stopPoint on tyhjä (eli hakua ei löytynyt)
        #for stop in stopDictio:                                                 #käy läpi koko pysäkkidatan
            #print("{} ({})".format(stop['name'], stop['shortName']))            #printtaa koko pysäkkidatan, tarvitsee hakutoiminnon koska lista on IHAN LIIAN PITKÄ >:(
        print("Antamaasi pysäkkiä ei löytynyt. Tarkista oikeinkirjoitus listasta.")

    parsed = r.json()                                   #parsitaan bussidataa

    currentTime = parsed['body'][0]['recordedAtTime']       #haetaan bussidatasta kellonaika

    busDictio = {}                         #init dictionary bussidatalle
    busDictio.clear()
    busDictio = parsed['body']             #parsitaan bussidata dictionaryyn

    found = []                          #init lista löydetyille hakutuloksille
    found.clear()                       #alustetaan lista uutta hakua varten
    foundOne = ""                       #yksittäisen hakutuloksen muuttuja

    currentTime = currentTime[11:16]        #otetaan bussidatasta kellonaika päiväyksestä
    print("Kello on: ", currentTime)
    minTime = int(currentTime[0:2]) * 60 + int(currentTime[3:6])    #muutetaan kellonaika minuuteiksi vertailua varten
    for data in busDictio:                                                      #käydään läpi bussidataa dictionaryssa
        onwardCalls = data['monitoredVehicleJourney']['onwardCalls']            #haetaan bussien pysäkkikohtaiset ennusteet 
        for call in onwardCalls:                                               #käydään pysäkkikohtaisia ennusteita läpi
            if call['stopPointRef'][-4:-1] == stopPoint[-4:-1]:                 #jos oikea pysäkki löytyy bussin reitiltä
                busNumber = data['monitoredVehicleJourney']['lineRef']          #otetaan talteen bussin numero
                expectedArrival = call['expectedArrivalTime']                   #otetaan talteen ennustettu saapumisaika (päiväys)
                expectedArrival = expectedArrival[11:16]                        #muokataan saapumisaika päiväyksestä pelkäksi kellonajaksi
                minArrival = int(expectedArrival[0:2]) * 60 + int(expectedArrival[3:5])     #muutetaan saapumisaika (kellonaika) minuuteiksi vertailua varten
                minErotus = (minArrival - minTime)                                          #erotetaan nykyinen kellonaika (minuutit) ennustetusta saapumisajasta (minuutit)
                foundOne = "{:5} bussi numero {:2} on pysäkillä {} ({}) eli {:3} minuutin kuluttua.".format(str(expectedArrival), str(busNumber), stopName, stopNumber, str(minErotus))     #tehdään printattava string löydetystä datasta
                found.append(foundOne)                                          #lisätään löydetty ja muotoiltu string listaan
    
    found.sort()    #järjestetään lista saapumisjärjestykseen

    for e in found: #käydään löydettyjen lista läpi ja printataan
        print(e)
