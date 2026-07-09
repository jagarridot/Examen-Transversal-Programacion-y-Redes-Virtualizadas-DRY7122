import requests

API_KEY = "15d755de-4dc5-459e-8792-e5176aed4237"  # reemplaza con tu API key de GraphHopper

def geocodificar(ciudad, api_key):
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "locale": "es", "limit": 1, "key": api_key}
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    if datos.get("hits"):
        punto = datos["hits"][0]["point"]
        nombre = datos["hits"][0].get("name", ciudad)
        return punto["lat"], punto["lng"], nombre
    return None, None, None


def calcular_ruta(lat1, lon1, lat2, lon2, vehiculo, api_key):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{lat1},{lon1}", f"{lat2},{lon2}"],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "key": api_key
    }
    respuesta = requests.get(url, params=params)
    return respuesta.json()


def main():
    print("=== Calculadora de Distancia Chile - Perú ===")
    print("(Escribe 's' en cualquier momento para salir)\n")

    while True:
        origen = input("Ingrese Ciudad de Origen: ")
        if origen.lower() == "s":
            print("Saliendo del programa...")
            break

        destino = input("Ingrese Ciudad de Destino: ")
        if destino.lower() == "s":
            print("Saliendo del programa...")
            break

        print("\nMedios de transporte disponibles:")
        print("1. Auto (car)")
        print("2. Bicicleta (bike)")
        print("3. A pie (foot)")
        opcion = input("Elija el medio de transporte (1/2/3) o 's' para salir: ")

        if opcion.lower() == "s":
            print("Saliendo del programa...")
            break

        vehiculos = {"1": "car", "2": "bike", "3": "foot"}
        vehiculo = vehiculos.get(opcion, "car")

        lat1, lon1, nombre_origen = geocodificar(origen, API_KEY)
        lat2, lon2, nombre_destino = geocodificar(destino, API_KEY)

        if lat1 is None or lat2 is None:
            print("No se pudo encontrar una de las ciudades. Intente nuevamente.\n")
            continue

        resultado = calcular_ruta(lat1, lon1, lat2, lon2, vehiculo, API_KEY)

        if "paths" in resultado and len(resultado["paths"]) > 0:
            ruta = resultado["paths"][0]
            distancia_km = ruta["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            tiempo_min = ruta["time"] / 1000 / 60
            horas = int(tiempo_min // 60)
            minutos = int(tiempo_min % 60)

            print("\n--- Resultado del Viaje ---")
            print(f"Origen: {nombre_origen}")
            print(f"Destino: {nombre_destino}")
            print(f"Medio de transporte: {vehiculo}")
            print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
            print(f"Duración estimada: {horas}h {minutos}min")

            print("\n--- Narrativa del Viaje ---")
            if "instructions" in ruta:
                for instruccion in ruta["instructions"]:
                    print(f"- {instruccion['text']}")
            print()
        else:
            print("No se pudo calcular la ruta entre esas ciudades.\n")


if __name__ == "__main__":
    main()
