import json
import math

# Mesafe hesaplama fonksiyonu (Haversine formülü)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Dünya'nın yarıçapı (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# IATA.json dosyasını yükleme
def load_airport_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# En yakın havalimanını bulma
def find_nearest_airport(user_lat, user_lon, airports_data):
    nearest_airport = None
    min_distance = float("inf")

    for country, airports in airports_data.items():
        for airport in airports:
            airport_lat = airport.get("latitude")
            airport_lon = airport.get("longitude")
            if airport_lat is not None and airport_lon is not None:
                distance = haversine(user_lat, user_lon, airport_lat, airport_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_airport = {
                        "iata_code": airport.get("iata_code"),
                        "airport_name": airport.get("airport_name"),
                        "distance_km": min_distance,
                    }

    return nearest_airport

# Örnek kullanım
if __name__ == "__main__":
    user_lat, user_lon = 41.0082, 28.9784  # İstanbul'un koordinatları (örnek)
    file_path = "IATA.json"
    
    try:
        airport_data = load_airport_data(file_path)
        nearest_airport = find_nearest_airport(user_lat, user_lon, airport_data)
        if nearest_airport:
            print(f"En yakın havalimanı: {nearest_airport['airport_name']} ({nearest_airport['iata_code']})")
            print(f"Uzaklık: {nearest_airport['distance_km']:.2f} km")
        else:
            print("Havalimanı bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")
