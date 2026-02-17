"""Extract content from web pages."""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import time


class ContentExtractor:
    """Extract main content from web pages."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize content extractor.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_content(self, url: str) -> Optional[str]:
        """
        Extract main content from a web page.
        
        Args:
            url: URL of the web page
            
        Returns:
            Extracted content as plain text, or None if extraction fails
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find main content areas
            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower() or 'post' in x.lower())) or
                soup.find('body')
            )
            
            if main_content:
                # Get text and clean it up
                text = main_content.get_text(separator='\n', strip=True)
                # Remove excessive whitespace
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                return '\n\n'.join(lines)
            else:
                # Fallback to body text
                text = soup.get_text(separator='\n', strip=True)
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                return '\n\n'.join(lines)
        
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None
    
    def extract_with_metadata(self, url: str, title: str) -> Optional[str]:
        """
        Extract content and format it with metadata.
        
        Args:
            url: URL of the web page
            title: Title of the article
            
        Returns:
            Formatted content with title and URL, or None if extraction fails
        """
        content = self.extract_content(url)
        if not content:
            return None
        
        # Format with metadata
        formatted = f"# {title}\n\n"
        formatted += f"Source: {url}\n\n"
        formatted += "---\n\n"
        formatted += content
        formatted += "\n\n---\n\n"
        
        return formatted
