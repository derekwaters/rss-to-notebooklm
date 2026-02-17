"""Main application logic."""

import time
from typing import List
from .config import AppConfig, FeedConfig
from .rss_parser import RSSParser, RSSItem
from .content_extractor import ContentExtractor
from .google_drive_client import GoogleDriveClient
from .state_manager import StateManager


class RSSToNotebookLMApp:
    """Main application class."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the application.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = AppConfig(config_path)
        self.rss_parser = RSSParser()
        self.content_extractor = ContentExtractor()
        self.drive_client = GoogleDriveClient(
            self.config.credentials_file,
            self.config.document_id
        )
        self.state_manager = StateManager(str(self.config.state_file))
    
    def process_feed(self, feed_config: FeedConfig) -> List[RSSItem]:
        """
        Process a single RSS feed.
        
        Args:
            feed_config: Feed configuration
            
        Returns:
            List of matching RSS items
        """
        print(f"Processing feed: {feed_config.url}")
        
        try:
            # Parse RSS feed
            items = self.rss_parser.parse_feed(feed_config.url)
            print(f"  Found {len(items)} items in feed")
            
            # Filter items
            if feed_config.filter_text:
                items = self.rss_parser.filter_items(items, feed_config.filter_text)
                print(f"  {len(items)} items match filter: '{feed_config.filter_text}'")
            
            # Filter out already processed items
            unprocessed = self.state_manager.get_unprocessed_items(items)
            print(f"  {len(unprocessed)} new items to process")
            
            return unprocessed
        
        except Exception as e:
            print(f"Error processing feed {feed_config.url}: {e}")
            return []
    
    def process_item(self, item: RSSItem) -> bool:
        """
        Process a single RSS item: extract content and add to Google Doc.
        
        Args:
            item: RSS item to process
            
        Returns:
            True if successful, False otherwise
        """
        print(f"  Processing: {item.title}")
        
        # Extract content from article URL
        content = self.content_extractor.extract_with_metadata(
            item.link,
            item.title
        )
        
        if not content:
            print(f"    Failed to extract content from {item.link}")
            return False
        
        # Append to Google Doc
        success = self.drive_client.append_content(content)
        
        if success:
            # Mark as processed
            self.state_manager.mark_processed(item.id)
            print(f"    Successfully added to Google Doc")
            return True
        else:
            print(f"    Failed to add to Google Doc")
            return False
    
    def run_once(self) -> int:
        """
        Run the application once (process all feeds).
        
        Returns:
            Number of articles processed
        """
        print("=" * 60)
        print("RSS to NotebookLM - Processing feeds")
        print("=" * 60)
        
        # Get document info
        doc_info = self.drive_client.get_document_info()
        if doc_info:
            print(f"Target document: {doc_info['title']}")
        print()
        
        all_items = []
        
        # Process each feed
        for feed_config in self.config.feeds:
            items = self.process_feed(feed_config)
            all_items.extend(items)
            print()
        
        # Process items
        processed_count = 0
        max_items = self.config.max_articles_per_run
        
        for item in all_items:
            if max_items > 0 and processed_count >= max_items:
                print(f"Reached maximum articles per run ({max_items})")
                break
            
            if self.process_item(item):
                processed_count += 1
                # Small delay to avoid rate limiting
                time.sleep(1)
        
        print()
        print("=" * 60)
        print(f"Processing complete. {processed_count} articles processed.")
        print("=" * 60)
        
        return processed_count
    
    def run_continuous(self):
        """Run the application continuously, checking feeds periodically."""
        print("Running in continuous mode...")
        print(f"Check interval: {self.config.check_interval} seconds")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                self.run_once()
                print(f"\nWaiting {self.config.check_interval} seconds until next check...\n")
                time.sleep(self.config.check_interval)
        except KeyboardInterrupt:
            print("\nStopping application...")
