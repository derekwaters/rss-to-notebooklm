# Usage Guide

This document explains how to use the RSS to NotebookLM application.

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up configuration:**
   - Copy `config.yaml.example` to `config.yaml`
   - Edit `config.yaml` with your settings (see [CONFIGURATION.md](CONFIGURATION.md))

3. **Set up Google API credentials:**
   - Download OAuth 2.0 credentials from Google Cloud Console
   - Save as `credentials.json` in the project directory
   - See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions

## Running the Application

### Single Run Mode

Process all feeds once and exit:

```bash
python main.py
```

Or with a custom config file:

```bash
python main.py --config my_config.yaml
```

### Continuous Mode

Run continuously, checking feeds periodically:

```bash
python main.py --continuous
```

The application will check feeds at the interval specified in `config.yaml` (default: 1 hour).

Press `Ctrl+C` to stop the application.

## How It Works

1. **Feed Processing**: The application retrieves each configured RSS feed
2. **Filtering**: Items are filtered by the optional filter text (if specified)
3. **Deduplication**: Already processed items (tracked in the state file) are skipped
4. **Content Extraction**: For each new item, the full article content is extracted from the URL
5. **Document Update**: The extracted content is appended to your Google Doc

## Output Format

Each article is added to the Google Doc in the following format:

```
# Article Title

Source: https://example.com/article-url

---

[Article content extracted from the web page]

---
```

## State Management

The application maintains a state file (default: `.rss_state.json`) that tracks which articles have been processed. This prevents duplicate entries even if you run the application multiple times.

If you want to reprocess all articles, you can delete the state file:

```bash
rm .rss_state.json
```

## Troubleshooting

### Authentication Issues

- Make sure `credentials.json` is in the correct location
- On first run, a browser window should open for authorization
- If authorization fails, delete `token.pickle` and try again

### Feed Parsing Errors

- Verify that the RSS feed URLs are correct and accessible
- Some feeds may require authentication or have rate limiting

### Content Extraction Issues

- Some websites may block automated content extraction
- The application will skip articles where content extraction fails
- Check the console output for error messages

### Google Doc Access

- Ensure the Google Doc ID in your config is correct
- Make sure the authenticated account has write access to the document

## Running Tests

Run the unit tests:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests
```

## Docker Usage

See [README.md](README.md) for Docker usage instructions.
