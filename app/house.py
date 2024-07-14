"""
Module for representing addresses and house details using data classes.

Dependencies:
    dataclasses

Classes:
    Address: Dataclass which represents an address with short and full forms, city, and ZIP code.
    House: Dataclass which represents the details of a house, including its ID, URL, price, address,
   travel times to offices, and life level score.
"""

from dataclasses import dataclass


@dataclass
class Address:
    """
    A dataclass representing an address.

    Attributes:
        short (str): The short form of the address.
        full (str): The full form of the address, including city and country.
        city (str): The city where the address is located.
        zip_code (str): The ZIP code of the address.
    """

    short: str
    full: str
    city: str
    zip_code: str


@dataclass
class House:
    """
    A dataclass representing the details of a house.

    Attributes:
        id (int): The unique identifier for the house.
        url (str): The URL of the house listing.
        price (int): The price of the house.
        address (Address): An Address object containing the details of the house's address.
        s_office_travel_time (str): Travel time from the house to the S office.
        v_office_travel_time (str): Travel time from the house to the V office.
        life_level_score (float): The life level score based on the house's postal code.
    """

    id: int
    url: str
    price: int
    address: Address
    s_office_travel_time: str
    v_office_travel_time: str
    life_level_score: float
