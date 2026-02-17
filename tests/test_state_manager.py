"""Tests for state manager."""

import unittest
import tempfile
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    """Tests for StateManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = Path(self.temp_dir) / "test_state.json"
    
    def test_new_state_manager(self):
        """Test creating a new state manager."""
        manager = StateManager(str(self.state_file))
        self.assertEqual(len(manager.processed_items), 0)
        self.assertFalse(manager.is_processed("item-1"))
    
    def test_mark_processed(self):
        """Test marking items as processed."""
        manager = StateManager(str(self.state_file))
        manager.mark_processed("item-1")
        self.assertTrue(manager.is_processed("item-1"))
        self.assertFalse(manager.is_processed("item-2"))
    
    def test_state_persistence(self):
        """Test that state persists across instances."""
        manager1 = StateManager(str(self.state_file))
        manager1.mark_processed("item-1")
        manager1.mark_processed("item-2")
        
        # Create new instance - should load previous state
        manager2 = StateManager(str(self.state_file))
        self.assertTrue(manager2.is_processed("item-1"))
        self.assertTrue(manager2.is_processed("item-2"))
    
    def test_get_unprocessed_items(self):
        """Test filtering unprocessed items."""
        manager = StateManager(str(self.state_file))
        
        # Create mock items
        class MockItem:
            def __init__(self, id_val):
                self.id = id_val
        
        items = [MockItem("item-1"), MockItem("item-2"), MockItem("item-3")]
        
        # Mark one as processed
        manager.mark_processed("item-2")
        
        # Get unprocessed
        unprocessed = manager.get_unprocessed_items(items)
        self.assertEqual(len(unprocessed), 2)
        self.assertEqual(unprocessed[0].id, "item-1")
        self.assertEqual(unprocessed[1].id, "item-3")


if __name__ == '__main__':
    unittest.main()
