# Boards API Client

Python client for the IntoBridge Boards API with command-line interface.

## Installation

```bash
pip install boards-api-client
```

## Usage

### Python API

```python
from boards_api_client import BoardsApiClient
from datetime import datetime

client = BoardsApiClient("http://localhost:8080", api_key="your-key")

# Search boards
boards = client.search_boards(
    nickname="player1",
    board_type="ranked",
    created_from=datetime(2024, 1, 1),
    page=1,
    page_size=10
)

# Download all boards for a user
total_files = client.download_all_boards(
    nickname="player1",
    output_dir="./boards",
    board_type="ranked"
)
```

### Command Line

```bash
# Search boards
boards-api search-boards --nickname player1 --board-type ranked --page 1

# With date filters
boards-api search-boards --created-from 2024-01-01T00:00:00 --created-to 2024-12-31T23:59:59

# Download all boards for a user
boards-api download-all-boards --nickname player1

# Download with custom output directory
boards-api download-all-boards --nickname player1 --output-dir ./boards

# Download with filters
boards-api download-all-boards --nickname player1 --board-type ranked --output-dir ./ranked_boards
```