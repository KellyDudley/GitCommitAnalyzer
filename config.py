"""
Configuration module for GitCommitAnalyzer
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self, config_file="analyzer_config.json"):
        self.config_file = config_file
        self.default_config = {
            "output": {
                "default_format": "text",
                "plots_directory": "plots",
                "reports_directory": "reports",
                "csv_directory": "csv_exports"
            },
            "analysis": {
                "include_merges": False,
                "max_commits": None,
                "date_format": "%Y-%m-%d %H:%M:%S"
            },
            "visualization": {
                "chart_style": "seaborn",
                "figure_size": [12, 6],
                "dpi": 300
            },
            "filtering": {
                "exclude_authors": [],
                "include_only_authors": [],
                "since_date": None,
                "until_date": None
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return self.default_config.copy()
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path, default=None):
        """Get config value using dot notation (e.g., 'output.default_format')."""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, key_path, value):
        """Set config value using dot notation."""
        keys = key_path.split('.')
        config_ref = self.config
        
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = value
    
    def ensure_directories(self):
        """Create output directories if they don't exist."""
        dirs = [
            self.get('output.plots_directory'),
            self.get('output.reports_directory'),
            self.get('output.csv_directory')
        ]
        
        for directory in dirs:
            if directory:
                Path(directory).mkdir(parents=True, exist_ok=True)