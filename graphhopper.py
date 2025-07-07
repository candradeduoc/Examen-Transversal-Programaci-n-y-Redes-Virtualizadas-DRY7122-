import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "51781e7d-dc73-4f31-9926-52b49e33636d"  

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif country:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de transporte disponibles en Graphhopper:")
    print("1. Automóvil (car)")
    print("2. Bicicleta (bike)")
    print("3. A pie (foot)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    # Traducción de opciones al formato válido de Graphhopper
    vehiculos_disponibles = {
        "1": "car", "automovil": "car", "auto": "car", "car": "car",
        "2": "bike", "bicicleta": "bike", "bike": "bike",
        "3": "foot", "pie": "foot", "a pie": "foot", "foot": "foot"
    }

    vehicle_input = input("Ingrese un tipo de transporte (número o nombre en español): ").lower()

    if vehicle_input in ["quit", "q", "s"]:
        break
    elif vehicle_input in vehiculos_disponibles:
        vehicle = vehiculos_disponibles[vehicle_input]
    else:
        vehicle = "car"
        print("Entrada no válida. Se utilizará 'automóvil' por defecto.")

    loc1 = input("Ciudad de origen: ")
    if loc1.lower() in ["quit", "q", "s"]:
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ciudad de destino: ")
    if loc2.lower() in ["quit", "q", "s"]:
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        response = requests.get(paths_url)
        paths_status = response.status_code
        paths_data = response.json()

        print("Estado de la API de rutas: " + str(paths_status))
        print("URL de la API:\n" + paths_url)
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in paths_data["paths"][0]["instructions"]:
                path = each["text"]
                distance = each["distance"]
                print("{0} ({1:.1f} km / {2:.1f} millas)".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=============================================")
        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")
