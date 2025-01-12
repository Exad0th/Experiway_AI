from datetime import datetime

def create_flypgs_url(departure_port, arrival_port, departure_date, return_date, adult_count=1):
    """
    Flypgs.com uçak bileti arama URL'si oluşturur.
    """
    base_url = "https://web.flypgs.com/booking"
    
    # Pegasus'un uçuş arama sayfası için uygun parametreler
    params = {
        "adultCount": adult_count,  # Yetişkin sayısı
        "arrivalPort": arrival_port,  # Varış havalimanı
        "currency": "TL",  # Para birimi
        "dateOption": "1",  # Tek yön veya gidiş-dönüş seçeneği
        "departureDate": departure_date,  # Gidiş tarihi
        "departurePort": departure_port,  # Kalkış havalimanı
        "language": "tr",  # Dil seçeneği
        "returnDate": return_date  # Dönüş tarihi
    }

    # Parametreleri URL'ye ekle
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    full_url = f"{base_url}?{query_string}"
    
    return full_url

# Örnek veriler
departure_port = "AYT"  # Antalya Havalimanı (IATA kodu)
arrival_port = "TGD"    # Podgorica Havalimanı (IATA kodu)
departure_date = "2025-01-10"  # Gidiş tarihi
return_date = "2025-01-17"     # Dönüş tarihi

# Flypgs.com için uçak bileti arama bağlantısı oluştur
flypgs_url = create_flypgs_url(departure_port, arrival_port, departure_date, return_date)

# Sonuçları yazdır
print("Flypgs.com Uçak Bileti Arama Linki:")
print(flypgs_url)
