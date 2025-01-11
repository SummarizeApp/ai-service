import psutil
import pynvml
from prometheus_client import Gauge, start_http_server
from ..logger import setup_logger

logger = setup_logger("metrics", "logs/metrics.log")

class MetricsCollector:
    def __init__(self, port=8000):
        self.cpu_usage_gauge = Gauge('ai_cpu_usage', 'CPU usage by AI service')
        self.gpu_usage_gauge = Gauge('ai_gpu_usage', 'GPU usage by AI service')
        
        try:
            pynvml.nvmlInit()
            self.gpu_available = True
        except Exception as e:
            logger.warning(f"GPU metrics will not be available: {e}")
            self.gpu_available = False
            
        start_http_server(port)
        
    def track_usage(self):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        self.cpu_usage_gauge.set(cpu_usage)

        if self.gpu_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
                self.gpu_usage_gauge.set(gpu_utilization)
            except pynvml.NVMLError as e:
                logger.warning(f"Failed to get GPU usage: {e}")
                
    def get_resource_usage(self):
        initial_cpu = psutil.cpu_percent(interval=None)
        initial_gpu = 0
        
        if self.gpu_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                initial_gpu = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            except pynvml.NVMLError as e:
                logger.warning(f"Failed to get initial GPU usage: {e}")
                
        return initial_cpu, initial_gpu 