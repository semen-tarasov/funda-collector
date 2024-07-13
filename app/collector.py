"""
This script searches for new houses on Funda and sends the data to Notion.

It utilizes the FundaScraper library for scraping house listings and integrates
with the Google Maps API for additional data processing. Results are then sent
to a specified Notion database.

FundaScraper documentation:
https://pypi.org/project/funda-scraper/
"""

import os
import re
import dataclasses
from datetime import datetime, timedelta

import requests
import pandas as pd
import googlemaps

from funda_scraper import FundaScraper

CITIES = [
    "Alphen aan den Rijn",
    "Amstelveen",
    "Bussum",
    "Den Haag",
    "Hilversum",
    "Huizen",
    "Leiden",
    "Muiden",
    "Naarden",
    "Zaandam",
    "Weesp",
    "Gemeente Almere",
    "Regio Utrecht",
]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

NOTION_SECRET = os.getenv("NOTION_SECRET")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

OFFICE_S = "Gustav Mahlerlaan 308, Amsterdam, Netherlands"
OFFICE_V = "Croeselaan 18, Utrecht, Netherlands"


def slug_to_title(slug: str) -> str:
    """
    Converts a slug string to a title string.

    Args:
        slug (str): The slug string to convert.

    Returns:
        str: The converted title string with each word capitalized.
    """
    return " ".join(word.capitalize() for word in slug.split("-"))


def create_scores_dict_from_csv() -> dict:
    """
    Reads 'scores.csv' located in the data directory relative to the script
    and constructs a dictionary from its contents, focusing on the latest year's data.

    Returns:
        dict: A dictionary with 'PC4' as keys and 'afw' as float values for the latest year.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    file_path = os.path.join(data_dir, "scores.csv")

    df = pd.read_csv(file_path)

    latest_year = df["year"].max()
    latest_year_data = df[df["year"] == latest_year]

    result_dict = {}
    for _, row in latest_year_data.iterrows():
        pc4 = int(row["PC4"])
        result_dict[pc4] = float(row["afw"])

    return result_dict


def get_departure_time() -> datetime:
    """
    Creates a datetime object for departure at 8 AM the next day.

    Returns:
        datetime: Tomorrow at 8 AM as a datetime object.
    """
    today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    return today + timedelta(days=1)


def search_funda(search_city) -> dict:
    """
    Search houses on Funda.

    Args:
        search_city (str): City of Search.

    Returns:
        dict: Dict with houses from Funda in city.
    """
    scraper = FundaScraper(
        area=search_city,
        want_to="buy",
        page_start=1,
        n_pages=100,
        min_price=350000,
        max_price=450000,
        days_since=5,
        find_past=False,
        property_type="house",
    )

    search_results_dict = {}
    search_results = scraper.run(raw_data=True)
    search_results_raw_data = search_results.to_dict()

    i = 0
    if not search_results.empty:
        while True:
            url = search_results_raw_data["url"][i]
            price_str = search_results_raw_data["date_list"][i]

            patterns = {
                "id": r"huis-(\d+)-",
                "city": r"koop/([^/]+)/",
                "price": r"€\s*([\d.]+)",
                "address": r"huis-\d+-(.+?)/",
            }

            matches = {
                "id": re.search(patterns["id"], url),
                "city": re.search(patterns["city"], url),
                "address": re.search(patterns["address"], url),
                "price": re.search(patterns["price"], price_str),
            }

            if matches["id"] and matches["price"] and matches["address"]:
                house_id = matches["id"].group(1)
                house_dict = {
                    "url": url,
                    "city": slug_to_title(matches["city"].group(1)),
                    "address": slug_to_title(matches["address"].group(1)),
                    "price": int(matches["price"].group(1).replace(".", "")),
                }

                search_results_dict.setdefault(house_id, house_dict)

            else:
                raise ValueError(
                    f"Can't get house ID, address, or price from link {url}."
                )

            i += 1
            if i == len(search_results_raw_data["url"]):
                return search_results_dict


def add_houses_to_notion(found_houses: list) -> None:
    """
    Adding found houses from Funda to Notion DataBase.

    Args:
        found_houses (list): List with found houses on Funda.
    """

    headers = {
        "Authorization": f"Bearer {NOTION_SECRET}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

    for house in found_houses:
        house: House
        query_payload = {
            "filter": {"property": "House ID", "title": {"equals": house.id}}
        }

        response = requests.post(
            query_url, headers=headers, json=query_payload, timeout=60
        )

        response.raise_for_status()
        results = response.json()["results"]

        if results:
            print(f"House ID {house.id} already exists in the database.")
            continue

        create_url = "https://api.notion.com/v1/pages"

        create_payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "House ID": {"title": [{"text": {"content": house.id}}]},
                "URL": {"url": house.url},
                "Post Address": {
                    "rich_text": [{"text": {"content": house.address["full"]}}]
                },
                "City": {"rich_text": [{"text": {"content": house.address["city"]}}]},
                "Price": {"number": house.price},
                "ZIP Code": {
                    "rich_text": [{"text": {"content": house.address["zip"]}}]
                },
                "Time to office S.": {
                    "rich_text": [{"text": {"content": house.s_office_travel_time}}]
                },
                "Time to office V.": {
                    "rich_text": [{"text": {"content": house.v_office_travel_time}}]
                },
                "Life Level Score": {"number": house.life_level_score},
            },
        }

        response = requests.post(
            create_url, headers=headers, json=create_payload, timeout=60
        )

        try:
            response.raise_for_status()
            print(f"New house with ID {house.id} added to the database.")
        except requests.exceptions.HTTPError as e:
            print(f"Error creating entry for House ID {house.id}: {e.response.text}")


class GoogleMaps:
    """
    A class to interact with the Google Maps API for various geographical and travel-related
    functionalities.

    Methods:
        get_departure_time() -> datetime:
            Creates a datetime object for departure at 8 AM the next day.

        get_travel_time(origin: str, destination: str, mode="transit"):
            Calculates travel time from origin to destination using the Google Maps API.

        get_zip_code(address: str) -> str:
            Gets the zip code for a given address.
    """

    def __init__(self):
        """
        Initializes the GoogleMaps object with a Google Maps API key.

        Args:
            api_key (str): The API key for accessing Google Maps services.
        """
        self.gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    def get_travel_time(self, origin: str, destination: str, mode="transit") -> str:
        """
        Calculates travel time from origin to destination using the Google Maps API.

        Args:
            origin (str): The starting point for travel.
            destination (str): The endpoint for travel.
            mode (str, optional): The mode of travel. Defaults to "transit".

        Returns:
            dict: Duration of travel time if found, otherwise "TRAVEL TIME NOT FOUND".
        """
        distance_matrix = self.gmaps.distance_matrix(
            origin, destination, mode=mode, departure_time=departure_time
        )

        if distance_matrix["status"] == "OK":
            return distance_matrix["rows"][0]["elements"][0]["duration"]["text"]
        return "TRAVEL TIME NOT FOUND"

    def get_zip_code(self, address: str) -> str:
        """
        Gets the zip code for a given address.

        Args:
            address (str): The full address to geocode.

        Returns:
            str: The zip code as a string if found, otherwise "ZIP CODE NOT FOUND".
        """
        geocode_result = self.gmaps.geocode(address)
        if geocode_result:
            for component in geocode_result[0]["address_components"]:
                if "postal_code" in component["types"]:
                    return component["long_name"]
        return "ZIP CODE NOT FOUND"


@dataclasses.dataclass
class House:
    """
    House data class representing the details of a house.

    Attributes:
        id (int): The unique identifier for the house.
        url (str): The URL of the house listing.
        price (int): The price of the house.
        address (dict): A dictionary containing the address details of the house.
        s_office_travel_time (str): Travel time from the house to the S office.
        v_office_travel_time (str): Travel time from the house to the V office.
        life_level_score (float): The life level score based on the house's postal code.
    """

    id: int
    url: str
    price: int
    address: dict
    s_office_travel_time: str
    v_office_travel_time: str
    life_level_score: float

    def __init__(self, house_id: int, **house_dict):
        """
        Initializes the House object with the provided house details.

        Args:
            house_id (int): The unique identifier for the house.
            **house_dict: Additional house details, including URL, price, address, and city.

        The house_dict is expected to contain:
            - url (str): The URL of the house listing.
            - price (int): The price of the house.
            - address (dict): Dict with short and full versions of address and with city.
            - city (str): The city where the house is located.
        """
        self.id: int = house_id
        self.url: str = house_dict["url"]
        self.price: int = house_dict["price"]

        self.address: dict = {
            "short": house_dict["address"],
            "full": f"{house_dict['address']}, {house_dict['city']}, Netherlands",
            "city": house_dict["city"],
        }

        self.s_office_travel_time: str = gmaps.get_travel_time(
            self.address["full"], OFFICE_S
        )
        self.v_office_travel_time: str = gmaps.get_travel_time(
            self.address["full"], OFFICE_V
        )

        self.address.setdefault("zip", gmaps.get_zip_code(self.address["full"]))

        if self.address["zip"][:4] != "ZIP CODE NOT FOUND":
            self.life_level_score: float = life_level_scores[
                int(self.address["zip"][:4])
            ]
        else:
            self.life_level_score: float = 0


life_level_scores = create_scores_dict_from_csv()
departure_time = get_departure_time()
gmaps = GoogleMaps()

if __name__ == "__main__":
    funda_houses = []

    for city in CITIES:
        funda_listings = search_funda(city)

        if funda_listings:
            for listing_id, listing_dict in funda_listings.items():
                funda_houses.append(House(listing_id, **listing_dict))

    add_houses_to_notion(funda_houses)
