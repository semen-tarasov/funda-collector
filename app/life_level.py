"""
This module provides a service class to manage and retrieve life level scores based on ZIP codes.

The LifeLevelScoreService class reads life level scores from a CSV file and provides a method
to get the score for a given ZIP code. It focuses on using the latest year's data.

Dependencies:
    os
    pandas
    dataclasses

Classes:
    LifeLevelScoreService: A service class to handle life level scores based on ZIP codes.

Attributes in LifeLevelScoreService:
    life_level_scores (dict): A dictionary with 'PC4' as keys and 'afw' as float values.

Methods in LifeLevelScoreService:
    get_score(zip_code: str) -> float: Retrieves the life level score for a given ZIP code.
    create_scores_dict_from_csv() -> dict: Reads 'scores.csv' and constructs a dictionary from 
      its contents, focusing on the latest year's data.
"""

import os
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class LifeLevelScoreService:
    """
    A service class to manage and retrieve life level scores based on ZIP codes.

    This class reads life level scores from a CSV file and provides a method
    to get the score for a given ZIP code. It focuses on using the latest year's data.

    Attributes:
        life_level_scores (dict): A dictionary with 'PC4' as keys and 'afw' as float values.
    """

    life_level_scores: dict = field(init=False)

    def __post_init__(self):
        """
        Initializes the life level scores dictionary after the instance is created.
        """
        self.life_level_scores = self.create_scores_dict_from_csv()

    def get_score(self, zip_code: str) -> float:
        """
        Retrieves the life level score for a given ZIP code.

        Args:
            zip_code (str): The ZIP code for which to retrieve the life level score.

        Returns:
            float: The life level score associated with the given ZIP code.

        Raises:
            KeyError: If the ZIP code is not found in the life level scores dictionary.
        """
        if zip_code != "ZIP CODE NOT FOUND":
            return self.life_level_scores[int(zip_code[:4])]
        return 0

    @staticmethod
    def create_scores_dict_from_csv() -> dict:
        """
        Reads 'scores.csv' located in the data directory near the app folder
        and constructs a dictionary from its contents, focusing on the latest year's data.

        Returns:
            dict: A dictionary with 'PC4' as keys and 'afw' as float values for the latest year.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))

        app_dir = os.path.dirname(script_dir)
        data_dir = os.path.join(app_dir, "data")
        file_path = os.path.join(data_dir, "scores.csv")

        df = pd.read_csv(file_path)

        latest_year = df["jaar"].max()
        latest_year_data = df[df["jaar"] == latest_year]

        result_dict = {
            int(row["PC4"]): float(row["afw"]) for _, row in latest_year_data.iterrows()
        }

        return result_dict
