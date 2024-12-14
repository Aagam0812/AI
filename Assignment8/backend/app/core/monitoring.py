import psutil
import logging
from datetime import datetime
from typing import Dict, List
import json
import os
from prometheus_client import Counter, Histogram, Gauge

logger = logging.getLogger(__name__)

# Define Prometheus metrics
REQUESTS_COUNTER = Counter('model_requests_total', 'Total model inference requests')
INFERENCE_TIME = Histogram('model_inference_seconds', 'Time spent processing inference requests')
ERROR_COUNTER = Counter('model_errors_total', 'Total number of model errors')
MEMORY_GAUGE = Gauge('system_memory_usage_bytes', 'System memory usage in bytes')
CPU_GAUGE = Gauge('system_cpu_usage_percent', 'System CPU usage percentage')

class MonitoringService:
    def __init__(self, log_dir: str = "monitoring/logs"):
        self.log_dir = log_dir
        self.metrics_history = []
        self.max_history_size = 1000
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Create log directory if it doesn't exist"""
        os.makedirs(self.log_dir, exist_ok=True)

    def log_inference_request(self, request_data: Dict):
        """
        Log model inference request
        """
        try:
            REQUESTS_COUNTER.inc()
            
            timestamp = datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "request_type": "inference",
                "input_length": len(str(request_data)),
                "system_metrics": self.get_system_metrics()
            }
            
            self._save_log_entry(log_entry)
            logger.info(f"Logged inference request: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging inference request: {str(e)}")
            ERROR_COUNTER.inc()

    def log_error(self, error: Exception, context: Dict = None):
        """
        Log error with context
        """
        try:
            ERROR_COUNTER.inc()
            
            timestamp = datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context or {},
                "system_metrics": self.get_system_metrics()
            }
            
            self._save_log_entry(log_entry, error=True)
            logger.error(f"Logged error: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging error: {str(e)}")

    def log_metric(self, metric_name: str, value: float, labels: Dict = None):
        """
        Log custom metric
        """
        try:
            timestamp = datetime.now().isoformat()
            metric_entry = {
                "timestamp": timestamp,
                "metric_name": metric_name,
                "value": value,
                "labels": labels or {}
            }
            
            self.metrics_history.append(metric_entry)
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history.pop(0)
                
            logger.info(f"Logged metric: {json.dumps(metric_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging metric: {str(e)}")
            ERROR_COUNTER.inc()

    def get_system_metrics(self) -> Dict:
        """
        Get current system metrics
        """
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            CPU_GAUGE.set(cpu_percent)
            MEMORY_GAUGE.set(memory.used)
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used": memory.used,
                "memory_available": memory.available,
                "disk_usage": psutil.disk_usage('/').percent
            }
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {str(e)}")
            return {}

    def _save_log_entry(self, entry: Dict, error: bool = False):
        """
        Save log entry to file
        """
        try:
            filename = f"error_log_{datetime.now().strftime('%Y%m%d')}.json" if error else \
                      f"request_log_{datetime.now().strftime('%Y%m%d')}.json"
            
            filepath = os.path.join(self.log_dir, filename)
            
            # Read existing logs
            existing_logs = []
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    existing_logs = json.load(f)
            
            # Append new entry
            existing_logs.append(entry)
            
            # Write back to file
            with open(filepath, 'w') as f:
                json.dump(existing_logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving log entry: {str(e)}")

    def get_metrics_summary(self, time_range: str = "1h") -> Dict:
        """
        Get summary of metrics for specified time range
        """
        try:
            now = datetime.now()
            
            # Filter metrics based on time range
            filtered_metrics = [
                m for m in self.metrics_history
                if (now - datetime.fromisoformat(m["timestamp"])).total_seconds() <= 
                self._parse_time_range(time_range)
            ]
            
            # Calculate summary statistics
            metrics_by_name = {}
            for metric in filtered_metrics:
                name = metric["metric_name"]
                if name not in metrics_by_name:
                    metrics_by_name[name] = []
                metrics_by_name[name].append(metric["value"])
            
            summary = {}
            for name, values in metrics_by_name.items():
                summary[name] = {
                    "count": len(values),
                    "mean": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0
                }
            
            return {
                "time_range": time_range,
                "metrics_summary": summary,
                "system_metrics": self.get_system_metrics()
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics summary: {str(e)}")
            return {}

    def _parse_time_range(self, time_range: str) -> int:
        """
        Parse time range string to seconds
        """
        unit = time_range[-1]
        value = int(time_range[:-1])
        
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        elif unit == 'd':
            return value * 86400
        else:
            raise ValueError(f"Invalid time range format: {time_range}")
