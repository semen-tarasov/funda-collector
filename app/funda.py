"""
This module provides a service to search for houses on Funda.

It includes a function to convert slugs to titles and a service class to search for houses in a 
specified city on Funda, retrieving the search results as a dictionary.

Environment Variables:
    FUNDA_SEARCH_TYPE: The type of search (e.g., "buy" or "rent").
    FUNDA_SEARCH_MIN_PRICE: The minimum price for the search.
    FUNDA_SEARCH_MAX_PRICE: The maximum price for the search.
    FUNDA_SEARCH_DAYS_SINCE: The number of days since the houses were listed.
    FUNDA_SEARCH_PROPERTY_TYPE: The type of property to search for (e.g., "house", "apartment").

Dependencies:
    re
    os
    funda_scraper (for the FundaScraper class)

Functions:
    slug_to_title(slug: str) -> str: Converts a slug string to a title string.

Classes:
    FundaService: A service class to search for houses on Funda.

Methods in FundaService:
    search(search_city: str) -> dict: Searches for houses on Funda in the specified city and 
      returns the results as a dictionary.
"""

import re
import os

from dataclasses import dataclass

from dotenv import load_dotenv
from funda_scraper import FundaScraper

load_dotenv()

FUNDA_SEARCH_TYPE = os.getenv("FUNDA_SEARCH_TYPE")
FUNDA_SEARCH_MIN_PRICE = os.getenv("FUNDA_SEARCH_MIN_PRICE")
FUNDA_SEARCH_MAX_PRICE = os.getenv("FUNDA_SEARCH_MAX_PRICE")
FUNDA_SEARCH_DAYS_SINCE = os.getenv("FUNDA_SEARCH_DAYS_SINCE")
FUNDA_SEARCH_PROPERTY_TYPE = os.getenv("FUNDA_SEARCH_PROPERTY_TYPE")


def slug_to_title(slug: str) -> str:
    """
    Converts a slug string to a title string.

    Args:
        slug (str): The slug string to convert.

    Returns:
        str: The converted title string with each word capitalized.
    """
    return " ".join(word.capitalize() for word in slug.split("-"))


@dataclass
class FundaService:
    """
    A service class to search for houses on Funda.

    This class provides functionality to search for houses in a specified city on Funda
    and retrieve the search results as a dictionary.

    Methods:
        search(search_city: str) -> dict:
            Searches for houses on Funda in the specified city and returns the results as a
            dictionary.
    """

    @staticmethod
    def search(search_city: str) -> dict:
        """
        Searches for houses on Funda in the specified city.

        Args:
            search_city (str): The city to search for houses.

        Returns:
            dict: A dictionary with house information from Funda in the specified city.

        Raises:
            ValueError: If house ID, address, or price cannot be extracted from the search results.
        """
        scraper = FundaScraper(
            area=search_city,
            want_to=str(FUNDA_SEARCH_TYPE),
            page_start=1,
            n_pages=100,
            min_price=int(FUNDA_SEARCH_MIN_PRICE),
            max_price=int(FUNDA_SEARCH_MAX_PRICE),
            days_since=int(FUNDA_SEARCH_DAYS_SINCE),
            find_past=False,
            property_type=str(FUNDA_SEARCH_PROPERTY_TYPE),
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

        return None
