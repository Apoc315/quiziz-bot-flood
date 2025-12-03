import os
import json
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log_success(self, message):
        """Log success message"""
        self._log("SUCCESS", message)
        print(message)
    
    def log_error(self, message):
        """Log error message"""
        self._log("ERROR", message)
        print(message)
    
    def log_info(self, message):
        """Log info message"""
        self._log("INFO", message)
        print(message)
    
    def _log(self, level, message):
        """Save log to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        log_file = os.path.join(self.log_dir, f"quizizz_{datetime.now().strftime('%Y%m%d')}.log")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def save_stats(self, stats):
        """Save statistics to file"""
        stats_file = os.path.join(self.log_dir, "stats.json")
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    all_stats = json.load(f)
            else:
                all_stats = []
            
            stats['timestamp'] = datetime.now().isoformat()
            all_stats.append(stats)
            
            with open(stats_file, 'w') as f:
                json.dump(all_stats, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not save stats: {e}")
