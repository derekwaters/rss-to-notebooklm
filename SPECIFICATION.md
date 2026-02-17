# RSS to NotebookLM
## Specification
### Purpose

This application will periodically check a set of configured RSS feeds for any new articles matching defined filters. The contents of those articles will be retrieved and added to a Google Doc for inclusion as a NotebookLM source.

### Requirements

1. The application will be written in Python
2. The application will have a configuration file defined in YAML
3. The configuration file will list one or more RSS feed URLs
4. Each RSS URL may also specify an optional filter text string
5. The application will retrieve the RSS feed from each URL, and filter the items in the feed by the defined filter
6. The URL link for each matching feed item will be retrieved
7. The content of the retrieved page will be added to a configured Google Document using the Google Drive API
8. The application may be a long-running process that retrieves updates periodically, or the application itself may just be run periodically.

### Implementation

1. The application will be written in Python
2. The application will include unit tests
3. The application unit tests will include dummy RSS feed files
4. The application will include documentation for the formatting of its configuration file
5. The application will include documentation on how to use it
6. The application will include definitions to build and run as a containerized microservice