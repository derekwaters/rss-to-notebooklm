"""Tests for configuration management."""

import unittest
import tempfile
import yaml
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import AppConfig, FeedConfig


class TestFeedConfig(unittest.TestCase):
    """Tests for FeedConfig class."""
    
    def test_feed_config_without_filter(self):
        """Test FeedConfig without filter."""
        config = FeedConfig("https://example.com/feed.xml")
        self.assertEqual(config.url, "https://example.com/feed.xml")
        self.assertIsNone(config.filter_text)
        self.assertTrue(config.matches_filter("any text"))
    
    def test_feed_config_with_filter(self):
        """Test FeedConfig with filter."""
        config = FeedConfig("https://example.com/feed.xml", "Python")
        self.assertEqual(config.url, "https://example.com/feed.xml")
        self.assertEqual(config.filter_text, "Python")
        self.assertTrue(config.matches_filter("Python is great"))
        self.assertTrue(config.matches_filter("python is great"))  # Case insensitive
        self.assertFalse(config.matches_filter("JavaScript is great"))


class TestAppConfig(unittest.TestCase):
    """Tests for AppConfig class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.yaml"
    
    def create_config_file(self, config_data):
        """Helper to create a config file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(config_data, f)
    
    def test_valid_config(self):
        """Test loading valid configuration."""
        config_data = {
            'google_drive': {
                'credentials_file': 'creds.json',
                'document_id': 'doc123'
            },
            'feeds': [
                {'url': 'https://example.com/feed.xml'},
                {'url': 'https://example.com/feed2.xml', 'filter': 'Python'}
            ],
            'settings': {
                'check_interval': 1800,
                'state_file': '.state.json',
                'max_articles_per_run': 10
            }
        }
        self.create_config_file(config_data)
        
        config = AppConfig(str(self.config_path))
        self.assertEqual(config.credentials_file, 'creds.json')
        self.assertEqual(config.document_id, 'doc123')
        self.assertEqual(len(config.feeds), 2)
        self.assertEqual(config.feeds[0].url, 'https://example.com/feed.xml')
        self.assertIsNone(config.feeds[0].filter_text)
        self.assertEqual(config.feeds[1].url, 'https://example.com/feed2.xml')
        self.assertEqual(config.feeds[1].filter_text, 'Python')
        self.assertEqual(config.check_interval, 1800)
        self.assertEqual(config.max_articles_per_run, 10)
    
    def test_missing_document_id(self):
        """Test that missing document_id raises error."""
        config_data = {
            'google_drive': {
                'credentials_file': 'creds.json'
            },
            'feeds': [
                {'url': 'https://example.com/feed.xml'}
            ]
        }
        self.create_config_file(config_data)
        
        with self.assertRaises(ValueError):
            AppConfig(str(self.config_path))
    
    def test_no_feeds(self):
        """Test that missing feeds raises error."""
        config_data = {
            'google_drive': {
                'credentials_file': 'creds.json',
                'document_id': 'doc123'
            },
            'feeds': []
        }
        self.create_config_file(config_data)
        
        with self.assertRaises(ValueError):
            AppConfig(str(self.config_path))
    
    def test_default_settings(self):
        """Test default settings are applied."""
        config_data = {
            'google_drive': {
                'credentials_file': 'creds.json',
                'document_id': 'doc123'
            },
            'feeds': [
                {'url': 'https://example.com/feed.xml'}
            ]
        }
        self.create_config_file(config_data)
        
        config = AppConfig(str(self.config_path))
        self.assertEqual(config.check_interval, 3600)  # Default
        self.assertEqual(config.max_articles_per_run, 0)  # Default


if __name__ == '__main__':
    unittest.main()
