"""RSS feed parsing and filtering."""

import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from dateutil import parser as date_parser


class RSSItem:
    """Represents a single RSS feed item."""
    
    def __init__(self, entry: Dict):
        self.title = entry.get('title', 'Untitled')
        self.link = entry.get('link', '')
        self.published = self._parse_date(entry.get('published'))
        self.summary = entry.get('summary', '')
        self.description = entry.get('description', '')
        self.id = entry.get('id', self.link)
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str:
            return None
        try:
            return date_parser.parse(date_str)
        except (ValueError, TypeError):
            return None
    
    def matches_filter(self, filter_text: Optional[str]) -> bool:
        """Check if this item matches the filter text."""
        if not filter_text:
            return True
        
        search_text = f"{self.title} {self.summary} {self.description}".lower()
        return filter_text.lower() in search_text
    
    def __repr__(self):
        return f"RSSItem(title='{self.title}', link='{self.link}')"


class RSSParser:
    """Parser for RSS feeds."""
    
    @staticmethod
    def parse_feed(url: str) -> List[RSSItem]:
        """
        Parse an RSS feed from a URL.
        
        Args:
            url: URL of the RSS feed
            
        Returns:
            List of RSSItem objects
            
        Raises:
            Exception: If feed cannot be parsed or retrieved
        """
        feed = feedparser.parse(url)
        
        if feed.bozo and feed.bozo_exception:
            raise Exception(f"Error parsing RSS feed {url}: {feed.bozo_exception}")
        
        items = []
        for entry in feed.entries:
            items.append(RSSItem(entry))
        
        return items
    
    @staticmethod
    def filter_items(items: List[RSSItem], filter_text: Optional[str]) -> List[RSSItem]:
        """
        Filter RSS items by text.
        
        Args:
            items: List of RSSItem objects
            filter_text: Optional filter text (case-insensitive)
            
        Returns:
            Filtered list of RSSItem objects
        """
        if not filter_text:
            return items
        
        return [item for item in items if item.matches_filter(filter_text)]
