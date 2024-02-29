import requests
import json
import time

def search_adress(adress):
    base_url = 'https://nominatim.openstreetmap.org/search'
    #q for free search
    params = {
        'q': adress,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


# open json file
with open('updated_journal_batch_only_phil_cleaned.json', 'r', encoding='utf-8') as file:
    json_string = json.load(file)

x=0
#957:
while x!=957:
    try:
        name = json_string[x]['bibjson']['institution']['name']
        address_to_search = name
        try:
            result = search_adress(address_to_search)

            # Check if the result is empty or doesn't contain the expected values
            # if not result or 'lon' not in result[0] or 'lat' not in result[0]:
            # raise Exception("API did not return the expected result")

            long = result[0]['lon']
            lat = result[0]['lat']
            print(f"Longitude: {long}, Latitude: {lat}")

            # Update the 'location' field in the JSON with retrieved 'long' and 'lat' values
            json_string[x]['bibjson']['location'] = {
                'long': long,
                'lat': lat
            }


        except Exception as e:
            print(f"Error processing API response for {address_to_search}: {e}")
    except (KeyError):
        print("KeyError")

    x += 1

#update the json
with open('updated_journal_batch_InstitutionLoc.json', 'w') as outfile:
    json.dump(json_string, outfile)