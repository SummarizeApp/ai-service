from flask import Flask, request, jsonify
from src.utils.summarize import summarize_with_model
from src.utils.summarizer import TextSummarizer
from src.utils.metrics import MetricsCollector
from src.logger import setup_logger

app = Flask(__name__)
logger = setup_logger("flask-app", "logs/app.log")

metrics_collector = MetricsCollector(port=8000)
text_summarizer = TextSummarizer()

@app.before_request
def track_usage():
    metrics_collector.track_usage()

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

        initial_cpu, initial_gpu = metrics_collector.get_resource_usage()

        try:
            if len(text) > 400:
                summary = text_summarizer.summarize_with_tfidf(text)
                method = "tf-idf + graph"
            else:
                summary = summarize_with_model(text)
                method = "transformer"
        except Exception as e:
            logger.error(f'Summary generation error: {e}', exc_info=True)
            return jsonify({'status': 'error', 'message': f'Özetleme sırasında hata oluştu: {e}'}), 500

        final_cpu, final_gpu = metrics_collector.get_resource_usage()
        cpu_used = final_cpu - initial_cpu
        gpu_used = final_gpu - initial_gpu

        logger.info(f"CPU Kullanımı: {cpu_used}%, GPU Kullanımı: {gpu_used}%")
        logger.info(f'Summary generated successfully using {method} method')

        return jsonify({
            'status': 'success', 
            'summary': summary,
            'method': method
        }), 200
    
    except Exception as e:
        logger.critical(f'Unexpected error: {e}', exc_info=True)
        return jsonify({'status': 'error', 'message': f'Beklenmeyen bir hata oluştu: {e}'}), 500

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f'Server failed to start: {e}', exc_info=True)
