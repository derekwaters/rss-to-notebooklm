"""Tests for RSS parser."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rss_parser import RSSParser, RSSItem


class TestRSSItem(unittest.TestCase):
    """Tests for RSSItem class."""
    
    def test_rss_item_creation(self):
        """Test RSSItem creation."""
        entry = {
            'title': 'Test Article',
            'link': 'https://example.com/article',
            'published': 'Mon, 01 Jan 2024 12:00:00 GMT',
            'summary': 'This is a test article',
            'id': 'article-123'
        }
        item = RSSItem(entry)
        self.assertEqual(item.title, 'Test Article')
        self.assertEqual(item.link, 'https://example.com/article')
        self.assertEqual(item.id, 'article-123')
        self.assertEqual(item.summary, 'This is a test article')
    
    def test_rss_item_matches_filter(self):
        """Test RSSItem filter matching."""
        entry = {
            'title': 'Python Programming Guide',
            'link': 'https://example.com/python',
            'summary': 'Learn Python programming',
            'description': 'A comprehensive guide to Python'
        }
        item = RSSItem(entry)
        
        # Should match when filter is in title
        self.assertTrue(item.matches_filter('Python'))
        # Should match when filter is in summary
        self.assertTrue(item.matches_filter('Learn'))
        # Should match when filter is in description
        self.assertTrue(item.matches_filter('comprehensive'))
        # Should not match
        self.assertFalse(item.matches_filter('JavaScript'))
        # Should match everything when no filter
        self.assertTrue(item.matches_filter(None))


class TestRSSParser(unittest.TestCase):
    """Tests for RSSParser class."""
    
    def test_parse_local_feed(self):
        """Test parsing a local RSS feed file."""
        feed_path = Path(__file__).parent / 'test_data' / 'sample_feed.xml'
        items = RSSParser.parse_feed(str(feed_path))
        
        self.assertGreater(len(items), 0)
        self.assertEqual(len(items), 4)
        self.assertEqual(items[0].title, 'Introduction to Python Programming')
        self.assertEqual(items[0].link, 'https://example.com/python-intro')
    
    def test_filter_items(self):
        """Test filtering RSS items."""
        feed_path = Path(__file__).parent / 'test_data' / 'sample_feed.xml'
        items = RSSParser.parse_feed(str(feed_path))
        
        # Filter for Python items
        python_items = RSSParser.filter_items(items, 'Python')
        self.assertEqual(len(python_items), 2)
        self.assertTrue(all('Python' in item.title for item in python_items))
        
        # Filter for JavaScript items
        js_items = RSSParser.filter_items(items, 'JavaScript')
        self.assertEqual(len(js_items), 1)
        self.assertEqual(js_items[0].title, 'Advanced JavaScript Techniques')
        
        # No filter should return all items
        all_items = RSSParser.filter_items(items, None)
        self.assertEqual(len(all_items), len(items))
    
    def test_filter_case_insensitive(self):
        """Test that filtering is case-insensitive."""
        feed_path = Path(__file__).parent / 'test_data' / 'sample_feed.xml'
        items = RSSParser.parse_feed(str(feed_path))
        
        # Should match regardless of case
        python_items_lower = RSSParser.filter_items(items, 'python')
        python_items_upper = RSSParser.filter_items(items, 'PYTHON')
        python_items_mixed = RSSParser.filter_items(items, 'Python')
        
        self.assertEqual(len(python_items_lower), len(python_items_upper))
        self.assertEqual(len(python_items_upper), len(python_items_mixed))


if __name__ == '__main__':
    unittest.main()
