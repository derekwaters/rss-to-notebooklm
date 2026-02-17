# RSS to NotebookLM

A Python application that periodically checks RSS feeds for new articles matching defined filters, extracts their content, and adds them to a Google Doc for use as a NotebookLM source.

## Features

- ✅ Configure multiple RSS feeds with optional text filters
- ✅ Automatic content extraction from article URLs
- ✅ Appends formatted content to Google Docs
- ✅ State tracking to avoid duplicate entries
- ✅ Run once or continuously with periodic checks
- ✅ Fully containerized with Docker support
- ✅ Comprehensive unit tests

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the application:**
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml with your settings
   ```

3. **Set up Google API credentials:**
   - Download OAuth 2.0 credentials from [Google Cloud Console](https://console.cloud.google.com/)
   - Save as `credentials.json` in the project directory
   - See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions

4. **Run the application:**
   ```bash
   python main.py
   ```

## Documentation

- **[CONFIGURATION.md](CONFIGURATION.md)** - Configuration file format and setup
- **[USAGE.md](USAGE.md)** - Usage instructions and troubleshooting
- **[SPECIFICATION.md](SPECIFICATION.md)** - Application specification

## Docker Usage

### Build and run with Docker Compose:

```bash
docker-compose up -d
```

### Build Docker image:

```bash
docker build -t rss-to-notebooklm .
```

### Run container:

```bash
docker run -v $(pwd)/config.yaml:/app/config.yaml:ro \
           -v $(pwd)/credentials.json:/app/credentials.json:ro \
           -v $(pwd)/data:/app/data \
           rss-to-notebooklm
```

## Running Tests

```bash
python -m pytest tests/
```

Or:

```bash
python -m unittest discover tests
```

## Project Structure

```
rss-to-notebooklm/
├── src/                    # Application source code
│   ├── __init__.py
│   ├── app.py             # Main application logic
│   ├── config.py          # Configuration management
│   ├── rss_parser.py      # RSS feed parsing
│   ├── content_extractor.py  # Web content extraction
│   ├── google_drive_client.py # Google Docs API client
│   └── state_manager.py   # State tracking
├── tests/                  # Unit tests
│   ├── test_data/         # Test RSS feed files
│   └── test_*.py          # Test modules
├── main.py                # Application entry point
├── config.yaml.example    # Example configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
└── README.md            # This file
```

## License

This project is provided as-is for personal use.
