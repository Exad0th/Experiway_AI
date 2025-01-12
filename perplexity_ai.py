import os
from openai import OpenAI
from booking_scraper import create_booking_url  # Booking fonksiyonunu içe aktar
import re

# Perplexity API'sini kullanarak AI yanıtı alma fonksiyonu
def get_ai_response(user_prompt):
    # API anahtarını çevre değişkenine ekle
    os.environ["PERPLEXITY_API_KEY"] = "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"

    # OpenAI istemcisini yapılandır
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
                "Always respond in the following format and do not provide any additional information:\n\n"
                "Tatil yeriniz: [Konum], Tarihler: [YYYY-AA-GG] - [YYYY-AA-GG]\n\n"
                "For example:\n"
                "Tatil yeriniz: Paris, Tarihler: 2025-01-10 - 2025-01-17"
            ),
        },
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=300
)




    # Yanıtı döndür
    return response.choices[0].message.content



def handle_react_prompt(react_text):
    try:
        # Yapay zekadan tatil önerisini al
        ai_response = get_ai_response(react_text)

        # Konum ve tarih bilgilerini düzenli ifadelerle ayıkla
        location_match = re.search(r"Tatil yeriniz: (.*?),", ai_response)
        date_match = re.search(r"Tarihler: (\d{4}-\d{2}-\d{2}) - (\d{4}-\d{2}-\d{2})", ai_response)

        if location_match and date_match:
            konum = location_match.group(1).strip()
            giris_tarihi = date_match.group(1)
            cikis_tarihi = date_match.group(2)

            # Booking.com URL'si oluştur
            booking_url = create_booking_url(konum, giris_tarihi, cikis_tarihi)
            return {"booking_url": booking_url}
        else:
            # Eğer bilgiler eksikse hata mesajı döndür
            missing_info = []
            if not location_match:
                missing_info.append("Tatil yeri bilgisi eksik.")
            if not date_match:
                missing_info.append("Tarih bilgisi eksik.")
            return {"error": " ".join(missing_info) or "Yanıt formatı eksik."}
    except Exception as e:
        # Hata durumunda hata mesajı döndür
        return {"error": str(e)}
