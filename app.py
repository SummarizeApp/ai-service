from flask import Flask, request, jsonify
from src.utils.summarize import summarize_with_model
from src.logger import setup_logger

app = Flask(__name__)

logger = setup_logger("flask-app", "logs/app.log")

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logger.warning('Invalid input: Missing "text" key')
            return jsonify({'status': 'error', 'message': 'Geçersiz giriş: "text" anahtarı eksik'}), 400
        
        text = data.get('text', '')
        if not text:
            logger.warning('Invalid input: Empty "text" value')
            return jsonify({'status': 'error', 'message': 'Geçersiz giriş: "text" değeri boş'}), 400
        
        try:
            summary = summarize_with_model(text)

        except Exception as e:
            logger.error(f'Summary generation error: {e}', exc_info=True)
            return jsonify({'status': 'error', 'message': f'Özetleme sırasında hata oluştu: {e}'}), 500
        
        logger.info('Summary generated successfully')
        return jsonify({'status': 'success', 'summary': summary}), 200
    
    except Exception as e:
        logger.critical(f'Unexpected error: {e}', exc_info=True)
        return jsonify({'status': 'error', 'message': f'Beklenmeyen bir hata oluştu: {e}'}), 500

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f'Server failed to start: {e}', exc_info=True)