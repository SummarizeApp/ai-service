from flask import Flask, request, jsonify
from src.utils.summarize import summarize_with_model
from src.logger import setup_logger

from prometheus_client import Gauge, start_http_server
import psutil
import pynvml

app = Flask(__name__)

logger = setup_logger("flask-app", "logs/app.log")

cpu_usage_gauge = Gauge('ai_cpu_usage', 'CPU usage by AI service')
gpu_usage_gauge = Gauge('ai_gpu_usage', 'GPU usage by AI service')

start_http_server(8000)
pynvml.nvmlInit()

@app.before_request
def track_usage():
    cpu_usage = psutil.cpu_percent(interval=0.1)
    cpu_usage_gauge.set(cpu_usage)

    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        gpu_usage_gauge.set(gpu_utilization)
    except pynvml.NVMLError as e:
        logger.warning(f"GPU kullanım bilgisi alınamadı: {e}")

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
        
        initial_cpu = psutil.cpu_percent(interval=None)
        initial_gpu = pynvml.nvmlDeviceGetUtilizationRates(pynvml.nvmlDeviceGetHandleByIndex(0)).gpu

        try:
            summary = summarize_with_model(text)
        except Exception as e:
            logger.error(f'Summary generation error: {e}', exc_info=True)
            return jsonify({'status': 'error', 'message': f'Özetleme sırasında hata oluştu: {e}'}), 500
        
        
        final_cpu = psutil.cpu_percent(interval=None)
        final_gpu = pynvml.nvmlDeviceGetUtilizationRates(pynvml.nvmlDeviceGetHandleByIndex(0)).gpu

        cpu_used = final_cpu - initial_cpu
        gpu_used = final_gpu - initial_gpu

        logger.info(f"CPU Kullanımı: {cpu_used}%, GPU Kullanımı: {gpu_used}%")
                
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