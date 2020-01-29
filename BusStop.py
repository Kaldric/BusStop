import requests

response = requests.get('http://data.itsfactory.fi/journeys/api/1/vehicle-activity')

stopPoint = "http://data.itsfactory.fi/journeys/api/1/stop-points/5116"

json_data = response.json() if response and response.status_code == 200 else None

found = []

for f in json_data['monitoredVehicleJourney']['onwardCalls']:
    found.append(f)        

print(f)
           # for call in json_data['monitoredVehicleJourney']['onwardCalls']:
           # host_name = hoststatus.get('name')
           # status_text = hoststatus.get('status_text')