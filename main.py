#!/usr/bin/env python3
"""Main entry point for RSS to NotebookLM application."""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.app import RSSToNotebookLMApp


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='RSS to NotebookLM - Feed articles to Google Docs for NotebookLM'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run continuously, checking feeds periodically'
    )
    
    args = parser.parse_args()
    
    try:
        app = RSSToNotebookLMApp(args.config)
        
        if args.continuous:
            app.run_continuous()
        else:
            app.run_once()
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
