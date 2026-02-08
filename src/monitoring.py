"""
System Monitoring & Metrics Collection Module
Handles logging of predictions, performance metrics, and system health for the dashboard.
"""
import time
import psutil
import pandas as pd
import os
from datetime import datetime
import json
import threading

LOG_FILE = "logs/prediction_log.jsonl"
METRICS_FILE = "logs/system_metrics.jsonl"

os.makedirs("logs", exist_ok=True)

class SystemMonitor:
    def __init__(self):
        self.ensure_logs_exist()
        
    def ensure_logs_exist(self):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f: pass
        if not os.path.exists(METRICS_FILE):
            with open(METRICS_FILE, 'w') as f: pass

    def log_prediction(self, input_data, result, latency_ms):
        """Log a single prediction event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "animal": input_data.get("Animal", "Unknown"),
            "category": result.get("predicted_category"),
            "disease": result.get("predicted_disease"),
            "category_confidence": result.get("category_confidence"),
            "disease_confidence": result.get("disease_confidence"),
            "latency_ms": latency_ms,
            "status": "success" if result.get("success") else "error",
            "error_msg": result.get("error", None)
        }
        
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def log_system_health(self):
        """Log system resource usage (CPU, Memory)"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
        
        with open(METRICS_FILE, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def get_recent_predictions(self, limit=100):
        """Get most recent logs"""
        logs = []
        try:
            with open(LOG_FILE, 'r') as f:
                # Read last N lines (inefficient for huge files, fine for demo)
                lines = f.readlines()[-limit:]
                for line in lines:
                    if line.strip():
                        logs.append(json.loads(line))
        except Exception:
            return []
        return pd.DataFrame(logs)

    def get_system_metrics(self, limit=50):
        """Get recent system metrics"""
        metrics = []
        try:
            with open(METRICS_FILE, 'r') as f:
                lines = f.readlines()[-limit:]
                for line in lines:
                    if line.strip():
                        metrics.append(json.loads(line))
        except Exception:
            return []
        return pd.DataFrame(metrics)

# Background Metrics Collector
def start_background_monitoring(interval=10):
    monitor = SystemMonitor()
    def run():
        while True:
            monitor.log_system_health()
            time.sleep(interval)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

# Global Instance
monitor = SystemMonitor()
