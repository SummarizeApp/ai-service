from flask import Flask, request, jsonify
from src.utils.summarize import summarize_with_model

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'status': 'error', 'message': 'Geçersiz giriş: "text" anahtarı eksik'}), 400
        
        text = data.get('text', '')
        if not text:
            return jsonify({'status': 'error', 'message': 'Geçersiz giriş: "text" değeri boş'}), 400
        
        try:
            summary = summarize_with_model(text)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Özetleme sırasında hata oluştu: {e}'}), 500
        
        return jsonify({'status': 'success', 'summary': summary}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Beklenmeyen bir hata oluştu: {e}'}), 500

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f'Sunucu başlatılırken hata oluştu: {e}')