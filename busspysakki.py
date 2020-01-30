import requests
import json


oldWantedStop = "" #initialisoidaan vanha haku loopin ulkopuolella

while True:
    r = requests.get("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")   #haetaan bussien data
    restop = requests.get("http://data.itsfactory.fi/journeys/api/1/stop-points")   #haetaan pysäkkien data


    parsed_stop = restop.json()     #parsitaan pysäkkien dataa

    expectedArrival = ""    #init odotettu saapumisaika
    busNumber = ""          #init bussinumero
    stopPoint = ""          #init haettu pysäkki, url
    stopName = ""           #init haettu pysäkki nimi

    

    wantedStop = input("Pelkällä enterillä päivität vanhan haun. \nSyötä pysäkin nimi tai 'poistu': ")      #input 
    if wantedStop.upper() == "POISTU":
        print("Näkemiin!")
        break
    elif wantedStop.upper() == "":              #jos uusi haku tyhjä
        if oldWantedStop != "":                 #jos vanha haku ei ole tyhjä
            wantedStop = oldWantedStop          #vanha hausta uusi haku
        else:
            print("Et voi päivittää edeltävää hakua ilman edeltävää hakua.") 
    
    stopDictio = parsed_stop['body']        #dictionary parsitusta pysäkki-datasta
    oldWantedStop = wantedStop              #uusi haku tallennetaan vanha haku muuttujaan

    for stop in stopDictio:                 #käydään läpi pysäkki-data
        if stop['name'].upper() == wantedStop.upper():      #jos pysäkin nimi (caps) on sama kuin haluttu pysäkki (caps)
            stopPoint = stop['url']                         #stopPointiin tallennetaan löydetyn pysäkin url
            stopName = stop['name']                         #haetaan stopNameen ko. pysäkin nimi

    if stopPoint == "":                                                             #jos stopPoint on tyhjä (eli hakua ei löytynyt)
        print("Antamaasi pysäkkiä ei löytynyt. Tarkista oikeinkirjoitus.")

    parsed = r.json()                                   #parsitaan bussidataa

    currentTime = parsed['body'][0]['recordedAtTime']       #haetaan bussidatasta kellonaika

    dictio = {}                         #init dictionary bussidatalle
    dictio = parsed['body']             #parsitaan bussidata dictionaryyn

    found = []                          #init lista löydetyille hakutuloksille
    found.clear()                       #alustetaan lista uutta haua varten

    currentTime = currentTime[11:16]        #otetaan bussidatasta kellonaika päiväyksestä
    print("Kello on: ", currentTime)
    minTime = int(currentTime[0:2]) * 60 + int(currentTime[3:6])    # muutetaan kellonaika minuuteiksi vertailua varten
    for data in dictio:                                                 #käydään läpi bussidataa dictionaryssa
        onwardCalls = data['monitoredVehicleJourney']['onwardCalls']     #haetaan bussien pysäkkikohtaiset ennusteet   
        for call in onwardCalls:                                        #käydään pysäkkikohtaisia ennusteita läpi
            if call['stopPointRef'] == stopPoint:                       #jos oikea pysäkki löytyy bussin reitiltä
                busNumber = data['monitoredVehicleJourney']['lineRef']  #otetaan talteen bussin numero
                expectedArrival = call['expectedArrivalTime']           #otetaan talteen ennustettu saapumisaika (päiväys)
                expectedArrival = expectedArrival[11:16]                   #muokataan saapumisaika päiväyksestä pelkäksi kellonajaksi
                minArrival = int(expectedArrival[0:2]) * 60 + int(expectedArrival[3:5]) #muutetaan saapumisaika (kellonaika) minuuteiksi vertailua varten
                minErotus = (minArrival - minTime)                                      #erotetaan nykyinen kellonaika (minuutit) ennustetusta saapumisajasta (minuutit)
                foundOne =   "{:5} bussi numero {:2} on pysäkillä {}. {:3} minuuttia jäljellä.".format(str(expectedArrival), str(busNumber), stopName, str(minErotus)) #tehdään printattava string löydetystä datasta
                foundOne = str(foundOne)  #todnäk turha ylimääräinen ja muutenkin extra rivi
                found.append(foundOne) #lisätään löydetty ja muotoiltu string listaan

    found.sort()    #järjestetään lista saapumisjärjestykseen

    for e in found: #käydään löydettyjen lista läpi ja printataan
        print(e)