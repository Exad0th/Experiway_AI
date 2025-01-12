import os
from openai import OpenAI
from booking_scraper import create_booking_url  # Booking fonksiyonunu içe aktar
import re
from datetime import datetime, timedelta

# Kullanıcı profilleri
PROFILLER = [
    {
        "environment": "Nature (rivers, forests, mountains)",
        "vacation_type": "Exciting and adventurous",
        "stress_level": "Low (1-3)",
        "passport": "Germany",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Alps", "Nepal"],
    },
    {
        "environment": "Beach and sunny weathers",
        "vacation_type": "Relaxing and peaceful",
        "stress_level": "Moderate (4-6)",
        "passport": "Turkey",
        "visa_preference": "Yes (Visa-free destinations)",
        "suggestions": ["Maldives", "Seychelles", "Kaş in Turkey"],
    },
    {
        "environment": "Winter, snow, and cold climates",
        "vacation_type": "Fun and lively",
        "stress_level": "Low (1-3)",
        "passport": "Sweden",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Swiss Alps", "Banff National Park in Canada", "Norwegian fjords"],
    },
    {
        "environment": "Nature (rivers, forests, mountains)",
        "vacation_type": "A custom mix (adventure and peace)",
        "stress_level": "High (7-9)",
        "passport": "Turkey",
        "visa_preference": "Yes (Visa-free destinations)",
        "suggestions": ["Cappadocia", "Kazbegi in Georgia", "Bali forest retreats"],
    },
    {
        "environment": "Beach and sunny weathers",
        "vacation_type": "Exciting and adventurous",
        "stress_level": "Moderate (4-6)",
        "passport": "United Kingdom",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Maldives", "Phuket", "Gold Coast in Australia"],
    },
    {
        "environment": "Winter, snow, and cold climates",
        "vacation_type": "Relaxing and peaceful",
        "stress_level": "High (7-9)",
        "passport": "Turkey",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Uludağ", "Swiss Alps", "Igloo hotels in Finland"],
    },
    {
        "environment": "Nature (rivers, forests, mountains)",
        "vacation_type": "Fun and lively",
        "stress_level": "Low (1-3)",
        "passport": "Canada",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Burning Man", "Camping activities in Canadian Rockies"],
    },
    {
        "environment": "Beach and sunny weathers",
        "vacation_type": "A custom mix (relaxation and social activities)",
        "stress_level": "High (7-9)",
        "passport": "Italy",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Ibiza", "Mykonos", "Dubai beach hotels"],
    },
    {
        "environment": "Winter, snow, and cold climates",
        "vacation_type": "Exciting and adventurous",
        "stress_level": "Moderate (4-6)",
        "passport": "United States",
        "visa_preference": "No (No visa issues)",
        "suggestions": ["Aspen", "Whistler in Canada", "Austrian Alps"],
    },
    {
        "environment": "Nature (rivers, forests, mountains)",
        "vacation_type": "Relaxing and peaceful",
        "stress_level": "Moderate (4-6)",
        "passport": "Turkey",
        "visa_preference": "Yes (Visa-free destinations)",
        "suggestions": ["Artvin highlands", "Nature tours in Black Sea region"],
    },
]



# Tarihleri stres seviyesine göre hesapla
def tarih_hesapla(stres_seviyesi):
    bugun = datetime.now()
    if stres_seviyesi == "Az stresli (1-3)":
        baslangic = bugun + timedelta(days=90)  # 3 ay sonrası
        bitis = baslangic + timedelta(days=7)  # 1 hafta tatil
    elif stres_seviyesi == "Orta derecede stresli (4-6)":
        baslangic = bugun + timedelta(days=30)  # 1 ay sonrası
        bitis = baslangic + timedelta(days=7)
    elif stres_seviyesi == "Yüksek stresli (7-9)":
        baslangic = bugun + timedelta(days=7)  # 1 hafta sonrası
        bitis = baslangic + timedelta(days=7)
    else:
        baslangic = bugun + timedelta(days=60)  # Varsayılan
        bitis = baslangic + timedelta(days=7)
    return baslangic.strftime("%Y-%m-%d"), bitis.strftime("%Y-%m-%d")

# Prompt'u ayrıştır
def parse_responses(responses_str):
    responses = {}
    match_patterns = {
        "comfort": r"Where do you feel most comfortable\?: (.+)",
        "dream_vacation": r"What is your dream vacation like\?: (.+)",
        "stress": r"How would you rate your stress level over the past 9 months\?: (.+)",
        "passport": r"Which country's passport do you hold\?: (.+)",
        "visa_requirement": r"Is visa requirement important for you\?: (.+)",
    }

    for key, pattern in match_patterns.items():
        match = re.search(pattern, responses_str)
        if match:
            responses[key] = match.group(1).strip()

    return responses

# React prompt'u işleyip uygun tatil önerisi oluştur
def handle_react_prompt(responses_str):
    try:
        # Parse the responses string into a dictionary
        responses = parse_responses(responses_str)

        # Debug prints to check the type and content of responses
        print(f"Type of responses: {type(responses)}")
        print(f"Content of responses: {responses}")

        # Profili belirle
        profil = next(
            (p for p in PROFILLER if 
             responses.get("comfort") == p["environment"] and 
             responses.get("stress") == p["stress_level"]), 
            None
        )

        if profil:
            # Eğer uygun bir profil bulunursa, profil üzerinden tahmin yap
            konum = profil["suggestions"][0]  # İlk öneriyi seç
            giris_tarihi, cikis_tarihi = tarih_hesapla(responses.get("stress"))

            # Booking.com URL'si oluştur
            booking_url = create_booking_url(konum, giris_tarihi, cikis_tarihi)

            return {
                "ai_response": f"Your vacation destination: {konum}, Dates: {giris_tarihi} - {cikis_tarihi}",
                "booking_url": booking_url,
            }
        else:
            # Eğer uygun bir profil bulunamazsa, tahmin yürüt
            return tahmin_yurut(responses)

    except Exception as e:
        return {"error": str(e)}

# Profil dışı tahmin yürütme
def tahmin_yurut(responses):
    try:
        # Kullanıcının verdiği cevaplara göre öneri üret
        comfort = responses.get("comfort", "a peaceful environment")
        stress = responses.get("stress", "moderate stress")
        vacation_type = responses.get("dream_vacation", "relaxing vacation")

        # Tarih hesapla
        giris_tarihi, cikis_tarihi = tarih_hesapla(stress)

        # Yapay zeka yorumları
        comment = f"Based on your preferences for {comfort} and a {vacation_type}, we recommend a destination that offers tranquility and excitement."
        
        # Önerilen konum (örnek bir tahmin için basit bir kural)
        if "beach" in comfort.lower():
            konum = "Bali"
        elif "snow" in comfort.lower():
            konum = "Swiss Alps"
        else:
            konum = "Kyoto"

        # Booking.com URL'si oluştur
        booking_url = create_booking_url(konum, giris_tarihi, cikis_tarihi)

        return {
            "ai_response": f"{comment} Suggested destination: {konum}, Dates: {giris_tarihi} - {cikis_tarihi}",
            "booking_url": booking_url,
        }
    except Exception as e:
        return {"error": str(e)}


# OpenAI kullanımı
def get_ai_response(user_prompt):
    os.environ["PERPLEXITY_API_KEY"] = "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"
    client = OpenAI(
        api_key=os.environ["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai"
    )

    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a travel planning assistant. "
                    "Generate a vacation suggestion with a location and valid date range based on the user's profile. "
                    "Always ensure the response includes both the location and date range."
                ),
            },
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
