from flask import Flask, jsonify, request
from flask_cors import CORS
from perplexity_ai import handle_react_prompt  # Yapay zeka fonksiyonunu içe aktar
from booking_scraper import create_booking_url  # Booking URL oluşturma fonksiyonunu içe aktar

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing'i etkinleştir

@app.route('/api/data', methods=['POST'])
def handle_data():
    try:
        # React'ten gelen JSON veriyi al
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid data"}), 400

        # Prompt'u al ve yapay zeka fonksiyonuna ilet
        prompt_text = data['prompt']
        result = handle_react_prompt(prompt_text)

        # Eğer yapay zeka yanıtından konum ve tarihler çıkarılabiliyorsa Booking URL'si oluştur
        if "ai_response" in result and "Tatil yeriniz" in result["ai_response"]:
            konum = result["ai_response"].split("Tatil yeriniz: ")[1].split(",")[0].strip()
            tarihler = result["ai_response"].split("Tarihler: ")[1].strip()
            giris_tarihi, cikis_tarihi = tarihler.split(" - ")
            
            # Booking.com URL'sini oluştur
            booking_url = create_booking_url(konum, giris_tarihi, cikis_tarihi)
            result["booking_url"] = booking_url

        # Yapay zeka yanıtı ve Booking linkini döndür
        return jsonify(result)
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
