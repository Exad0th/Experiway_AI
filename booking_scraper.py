def create_booking_url(konum, giris_tarihi, cikis_tarihi):
    """
    Kullanıcıdan alınan bilgilerle Booking.com arama URL'si oluşturur.
    """
    base_url = "https://www.booking.com/searchresults.tr.html"
    params = {
        "ss": konum,
        "ssne": konum,
        "ssne_untouched": konum,
        "checkin": giris_tarihi,
        "checkout": cikis_tarihi,
        "group_adults": 2,
        "group_children": 0,
        "no_rooms": 1,
        "aid": 304142,  # Sabit bir aid (örnek)
        "lang": "tr",   # Dil parametresi
        "src": "index", # Kaynak bilgisi
    }

    # Parametreleri URL'ye ekle
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    full_url = f"{base_url}?{query_string}"
    
    return full_url
