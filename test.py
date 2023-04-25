
def request_example():
    url = "https://localhost:3000/api/tasks"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data = {
        "module":"calidad_agua",
        "name":"tds_agua",
        "description":"sensor que mide la cantidad de solidos totales del agua",
        "min":0,
        "max":1000,
        "pin":"A2",
        "status":"encendido"
    }
    data1 = {
        "module":"calidad_aire",
        "name":"luminosidad",
        "description":"sensor que mide la cantidad de luz en el ambiente",
        "min":0,
        "max":1000,
        "pin":"5",
        "status":"encendido"
    }
    data2 = {
        "module":"calidad_aire",
        "name":"cantidad_co2",
        "description":"sensor que mide la cantidad de co2 en el ambiente",
        "min":0,
        "max":1000,
        "pin":"A0",
        "status":"encendido"
    }
    while (continues):
        resp = requests.post(url, headers=headers, data=data)        
        print(resp.status_code)
