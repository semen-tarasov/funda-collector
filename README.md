# Funda Collector

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
    git clone git@github.com:semen-tarasov/Funda-Collector.git
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
Create a `.env` file in the root directory of your project and add the following environment variables.

### Google API

This script uses the Google API for collecting ZIP codes from addresses and calculating travel times to selected addresses (OFFICE_S and OFFICE_V variables). 
Follow these steps to set up the Google API:

1. **Create a Google Cloud Project**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Click on the project drop-down and select "New Project".
    - Enter a name for your project and click "Create".

2. **Enable the Necessary APIs**:
    - In the Google Cloud Console, go to the **API & Services** > **Library**.
    - Enable the following APIs:
        - **Geocoding API**
        - **Distance Matrix API**

3. **Create API Key**:
    - In the Google Cloud Console, go to **API & Services** > **Credentials**.
    - Click on **Create Credentials** and select **API Key**.
    - Copy the API key and add it to your `.env` file as `GOOGLE_API_KEY`.

### Notion Database

This script interacts with a Notion database to store and manage information about houses. To enable this functionality, you'll need to configure environment variables and set up the database in Notion.

1. **Create a Notion Database**:
    To create a Notion database that matches the expected schema, follow these steps:

    1. **Open Notion**: Open your Notion workspace and navigate to the page where you want to create the database.

    2. **Create a New Database**:
        - Click on the `+` button or type `/database` to create a new database.
        - Select "Table" to create a table-based database.

    3. **Add the Following Fields**:
    
    <details>
      <summary>Click to expand the list of fields</summary>
      
        - **House ID**:
          - Type: Title
          - This is the primary field for the house ID.

        - **URL**:
          - Type: URL
          - Store the URL of the house listing.

        - **Post Address**:
          - Type: Rich Text
          - The full postal address of the house.

        - **City**:
          - Type: Rich Text
          - The city where the house is located.

        - **ZIP Code**:
          - Type: Rich Text
          - The ZIP code of the house.

        - **Price**:
          - Type: Number
          - Set the number format to Euro.

        - **Time to office S.**:
          - Type: Rich Text
          - Travel time from the house to office S.

        - **Time to office V.**:
          - Type: Rich Text
          - Travel time from the house to office V.

        - **Life Level Score**:
          - Type: Number
          - Set the number format to "Number with commas".

        - **Status**:
          - Type: Status
          - Use default status options or customize as needed:
            - New
            - Not sure
            - Thinking
            - Viewing Scheduled
            - Waiting List
            - Need to Call
            - Declined
            - Sold
            - Bought

        - **Comment**:
          - Type: Rich Text
          - Any additional comments or notes about the house.

        - **View**:
          - Type: Date
          - The date when the house was viewed.

        - **9292 S. Link**:
          - Type: Formula
          - Formula: `concat("https://9292.nl/en/journeyadvice/", replaceAll(lower(prop("City")), " ", "-"), "_", replaceAll(lower(prop("ZIP Code")), " ", ""), "/amsterdam_1082me/")`
          - Note: Replace `amsterdam_1082me` with the relevant city and ZIP code of office S.

        - **9292 V. Link**:
          - Type: Formula
          - Formula: `concat("https://9292.nl/en/journeyadvice/", replaceAll(lower(prop("City")), " ", "-"), "_", replaceAll(lower(prop("ZIP Code")), " ", ""), "/utrecht_3521cb/")`
          - Note: Replace `utrecht_3521cb` with the relevant city and ZIP code of office V.
    </details>

    4. **Customize and Save**:
        - Customize the database view and properties as needed.
        - Save the database and copy its ID to use in your `.env` file.

2. **Get information from Notion**:
    - **Notion Secret**: You can obtain your Notion Integration token (secret) by creating an integration in Notion:
      1. Go to [Notion Integrations](https://www.notion.so/my-integrations).
      2. Click on "New Integration" and follow the instructions to create a new integration.
      3. Copy the "Internal Integration Token" and add it to your `.env` file as `NOTION_SECRET`.

    - **Notion Database ID**: You can find your database ID by opening the database in Notion and copying the part of the URL that comes after `notion.so/` and before the `?` (if present). For example, in the URL `https://www.notion.so/8c3b832c81884c67966db9098ac188d7`, the database ID is `8c3b832c81884c67966db9098ac188d7`. Add this to your `.env` file as `NOTION_DATABASE_ID`.

3. **Set up environment variables**:
    Add the following environment variables to your `.env` file:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    NOTION_SECRET=your_notion_secret
    NOTION_DATABASE_ID=your_notion_database_id
    ```

### Life Level Scores

As the source of information for the current life level score, the script uses data from the Dutch government. You can download the CSV with information about scores for different addresses from this link: [Leefbaarometer Opendata](https://www.leefbaarometer.nl/page/Opendata#scores).

In the downloaded archive, you need the file `Leefbaarometer-scores PC4 {years}.csv`. This file should contain `PC4` and `afw` columns. 
Rename this file to `scores.csv` and place it in the `data` folder.

## Usage

**Run the script**:
    ```sh
    python searcher.py
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
