"""Configuration management for RSS to NotebookLM."""

import yaml
from pathlib import Path
from typing import List, Dict, Optional


class FeedConfig:
    """Configuration for a single RSS feed."""
    
    def __init__(self, url: str, filter_text: Optional[str] = None):
        self.url = url
        self.filter_text = filter_text
    
    def matches_filter(self, text: str) -> bool:
        """Check if text matches the filter (case-insensitive)."""
        if not self.filter_text:
            return True
        return self.filter_text.lower() in text.lower()


class AppConfig:
    """Application configuration."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}. "
                "Please copy config.yaml.example to config.yaml and configure it."
            )
        
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Google Drive settings
        google_drive = config_data.get('google_drive', {})
        self.credentials_file = google_drive.get('credentials_file', 'credentials.json')
        self.document_id = google_drive.get('document_id')
        
        if not self.document_id:
            raise ValueError("google_drive.document_id must be specified in config.yaml")
        
        # Feed configurations
        feeds_data = config_data.get('feeds', [])
        self.feeds: List[FeedConfig] = []
        for feed_data in feeds_data:
            url = feed_data.get('url')
            if not url:
                raise ValueError("Each feed must have a 'url' field")
            filter_text = feed_data.get('filter')
            self.feeds.append(FeedConfig(url, filter_text))
        
        if not self.feeds:
            raise ValueError("At least one feed must be configured")
        
        # Application settings
        settings = config_data.get('settings', {})
        self.check_interval = settings.get('check_interval', 3600)
        self.state_file = Path(settings.get('state_file', '.rss_state.json'))
        self.max_articles_per_run = settings.get('max_articles_per_run', 0)
