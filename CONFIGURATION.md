# Configuration Guide

This document describes the configuration file format for RSS to NotebookLM.

## Configuration File Format

The application uses a YAML configuration file (default: `config.yaml`). You can copy `config.yaml.example` to `config.yaml` and modify it according to your needs.

## Configuration Structure

### Google Drive Settings

```yaml
google_drive:
  credentials_file: "credentials.json"
  document_id: "YOUR_GOOGLE_DOC_ID"
```

- **credentials_file**: Path to your Google API OAuth 2.0 credentials JSON file. This file is downloaded from the Google Cloud Console when you set up OAuth 2.0 credentials.
- **document_id**: The ID of the Google Doc where content will be appended. You can find this in the URL of your Google Doc: `https://docs.google.com/document/d/DOCUMENT_ID/edit`

### RSS Feeds Configuration

```yaml
feeds:
  - url: "https://example.com/feed.xml"
  - url: "https://example.com/tech-feed.xml"
    filter: "Python"
  - url: "https://example.com/news-feed.xml"
    filter: "AI"
```

Each feed entry can have:
- **url** (required): The URL of the RSS feed
- **filter** (optional): A text string to filter feed items. Only items containing this text (case-insensitive) in their title, summary, or description will be processed. If omitted, all items from the feed will be processed.

### Application Settings

```yaml
settings:
  check_interval: 3600
  state_file: ".rss_state.json"
  max_articles_per_run: 0
```

- **check_interval**: How often to check feeds when running in continuous mode (in seconds). Default: 3600 (1 hour)
- **state_file**: Path to the state file that tracks processed articles to avoid duplicates. Default: `.rss_state.json`
- **max_articles_per_run**: Maximum number of articles to process per run. Set to 0 for unlimited. Default: 0

## Example Configuration

```yaml
google_drive:
  credentials_file: "credentials.json"
  document_id: "1a2b3c4d5e6f7g8h9i0j"

feeds:
  - url: "https://rss.example.com/tech.xml"
    filter: "Python"
  - url: "https://rss.example.com/news.xml"
  - url: "https://blog.example.com/feed.xml"
    filter: "Machine Learning"

settings:
  check_interval: 7200
  state_file: ".rss_state.json"
  max_articles_per_run: 10
```

## Setting Up Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API for your project
4. Go to "Credentials" and create OAuth 2.0 Client ID credentials
5. Choose "Desktop app" as the application type
6. Download the credentials JSON file and save it as `credentials.json` in your project directory
7. The first time you run the application, it will open a browser window for you to authorize the application
8. After authorization, a `token.pickle` file will be created for future runs

## Getting Your Google Doc ID

1. Open your Google Doc in a web browser
2. Look at the URL: `https://docs.google.com/document/d/DOCUMENT_ID/edit`
3. Copy the `DOCUMENT_ID` part and use it as the `document_id` in your configuration
