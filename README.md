# House Searcher

This script searches for new houses on Funda and sends the data to a specified Notion database. It utilizes the FundaScraper library for scraping house listings and integrates with the Google Maps API for additional data processing.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/house-searcher.git
    cd house-searcher
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

## Usage

1. **Run the script**:
    ```sh
    python searcher.py
    ```

2. **Example usage in code**:
    ```python
    from searcher import GoogleMaps, House, create_scores_dict_from_csv

    # Initialize GoogleMaps
    gmaps = GoogleMaps(api_key=os.getenv("GOOGLE_API_KEY"))

    # Example house data
    house_dict = {
        "url": "https://www.funda.nl/koop/leusden/huis-43669755-rondeel-79/?old_ldp=true",
        "price": 350000,
        "address": "Rondeel 79",
        "city": "Leusden"
    }

    # Create a House object
    house = House(house_id=43669755, **house_dict)

    # Print house details
    print(house)
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. **Commit your changes**:
    ```sh
    git commit -m "Add some feature"
    ```
4. **Push to the branch**:
    ```sh
    git push origin feature/your-feature-name
    ```
5. **Open a pull request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.