# House Searcher

This script searches for new houses on Funda and sends the data to a specified Notion database. It utilizes the FundaScraper library for scraping house listings and integrates with the Google Maps API for additional data processing.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/houssearcher.git
    cd houssearcher
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up environment variables**:
    Create a `.env` file in the root directory of your project and add the following environment variables:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    NOTION_SECRET=your_notion_secret
    NOTION_DATABASE_ID=your_notion_database_id
    ```

2. **Create `scores.csv` file**:
    Ensure you have a `scores.csv` file in the same directory as the script. This file should contain `PC4` and `afw` columns.
