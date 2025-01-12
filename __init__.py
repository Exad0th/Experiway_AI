from flask import Flask, jsonify, request
from flask_cors import CORS
from booking_scraper import create_booking_url
from flying_gps_scraper import create_flypgs_url
from perplexity_ai import get_perplexity_response

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Booking.com URL oluşturucu fonksiyon
    @app.route('/api/booking', methods=['POST'])
    def booking():
        data = request.json
        url = create_booking_url(
            data['konum'],
            data['giris_tarihi'],
            data['cikis_tarihi']
        )
        return jsonify({"url": url})

    # Pegasus uçuş URL oluşturucu fonksiyon
    @app.route('/api/flight', methods=['POST'])
    def flight():
        data = request.json
        url = create_flypgs_url(
            data['departure_port'],
            data['arrival_port'],
            data['departure_date'],
            data['return_date'],
            data.get('adult_count', 1)
        )
        return jsonify({"url": url})

    # Perplexity AI çağrısı yapan fonksiyon
    @app.route('/api/chat', methods=['POST'])
    def chat():
        prompt = request.json['prompt']
        response = get_perplexity_response(prompt)
        return jsonify({"response": response})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
