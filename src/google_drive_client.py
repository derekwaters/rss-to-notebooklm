"""Google Drive API client for appending content to Google Docs."""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
from typing import Optional
from pathlib import Path


# Scopes required for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']


class GoogleDriveClient:
    """Client for interacting with Google Docs API."""
    
    def __init__(self, credentials_file: str, document_id: str):
        """
        Initialize Google Drive client.
        
        Args:
            credentials_file: Path to Google API credentials JSON file
            document_id: ID of the Google Doc to append to
        """
        self.credentials_file = Path(credentials_file)
        self.document_id = document_id
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google API and build service."""
        creds = None
        token_file = Path('.token.pickle')
        
        # Load existing token if available
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_file.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}. "
                        "Please download your OAuth 2.0 credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('docs', 'v1', credentials=creds)
    
    def append_content(self, content: str) -> bool:
        """
        Append content to the Google Doc.
        
        Args:
            content: Text content to append
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the current document to find the end index
            doc = self.service.documents().get(documentId=self.document_id).execute()
            end_index = doc['body']['content'][-1]['endIndex'] - 1
            
            # Prepare the request to insert text
            requests = [{
                'insertText': {
                    'location': {
                        'index': end_index,
                    },
                    'text': content + '\n\n'
                }
            }]
            
            # Execute the request
            self.service.documents().batchUpdate(
                documentId=self.document_id,
                body={'requests': requests}
            ).execute()
            
            return True
        
        except HttpError as e:
            print(f"Error appending to Google Doc: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def get_document_info(self) -> Optional[dict]:
        """
        Get information about the document.
        
        Returns:
            Document metadata or None if error
        """
        try:
            doc = self.service.documents().get(documentId=self.document_id).execute()
            return {
                'title': doc.get('title', 'Unknown'),
                'document_id': self.document_id
            }
        except Exception as e:
            print(f"Error getting document info: {e}")
            return None
