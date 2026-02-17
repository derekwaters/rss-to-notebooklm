"""State management to track processed articles."""

import json
from pathlib import Path
from typing import Set, Optional
from datetime import datetime


class StateManager:
    """Manages state of processed RSS items to avoid duplicates."""
    
    def __init__(self, state_file: str = ".rss_state.json"):
        """
        Initialize state manager.
        
        Args:
            state_file: Path to state file
        """
        self.state_file = Path(state_file)
        self.processed_items: Set[str] = set()
        self._load_state()
    
    def _load_state(self):
        """Load state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.processed_items = set(data.get('processed_items', []))
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state file: {e}")
                self.processed_items = set()
        else:
            self.processed_items = set()
    
    def _save_state(self):
        """Save state to file."""
        try:
            data = {
                'processed_items': list(self.processed_items),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state file: {e}")
    
    def is_processed(self, item_id: str) -> bool:
        """
        Check if an item has been processed.
        
        Args:
            item_id: Unique identifier for the RSS item
            
        Returns:
            True if item has been processed, False otherwise
        """
        return item_id in self.processed_items
    
    def mark_processed(self, item_id: str):
        """
        Mark an item as processed.
        
        Args:
            item_id: Unique identifier for the RSS item
        """
        self.processed_items.add(item_id)
        self._save_state()
    
    def get_unprocessed_items(self, items, id_key: str = 'id') -> list:
        """
        Filter out already processed items.
        
        Args:
            items: List of items (must have an 'id' attribute or key)
            id_key: Key to use for item ID (default: 'id')
            
        Returns:
            List of unprocessed items
        """
        unprocessed = []
        for item in items:
            # Try to get ID as attribute first, then as dict key
            if hasattr(item, id_key):
                item_id = getattr(item, id_key, None)
            elif isinstance(item, dict):
                item_id = item.get(id_key)
            else:
                item_id = None
            
            if item_id and not self.is_processed(item_id):
                unprocessed.append(item)
        return unprocessed
