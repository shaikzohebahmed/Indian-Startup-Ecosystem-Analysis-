import random
import itertools
import pandas as pd
from dataset import startup

class Investor:
    """
    Investor class for analyzing startup investments.

    This class provides methods to analyze investments made by investors in startup companies.
    It loads a startup dataset and offers various functionalities to retrieve investment-related information.

    Attributes:
        INVESTOR_COLUMN (str): The name of the column containing investor names.
        AMOUNT_COLUMN (str): The name of the column containing investment amounts.
        VERTICAL_COLUMN (str): The name of the column containing startup vertical (sector).
        SUBVERTICAL_COLUMN (str): The name of the column containing startup subvertical.
        CITY_COLUMN (str): The name of the column containing the city of the startup.
        ROUND_COLUMN (str): The name of the column containing funding round information.
        YEAR_COLUMN (str): The name of the column containing the investment year.

    Methods:
        __init__(): Initialize the Investor class and load the startup dataset.
        investor_list(): Get a sorted list of unique investors.
        recent_five_investments(investor_name): Get information about the five most recent investments by an investor.
        group_and_reset(data, group_column): Helper method to group data and reset the index.
        biggest_investments(investor_name): Get information about the top investments by an investor.
        invested_sector(investor_name): Get total investments by sector for an investor.
        invested_subsector(investor_name): Get total investments by subsector for an investor.
        invested_city(investor_name): Get total investments by city for an investor.
        invested_round(investor_name): Get total investments by funding round for an investor.
        yoy_investment(investor_name): Get yearly investments by an investor.
        get_similar_investors(investor_name): Get similar investors in the same sector as an investor.
    """

    INVESTOR_COLUMN = 'investors'
    AMOUNT_COLUMN = 'amount'
    VERTICAL_COLUMN = 'vertical'
    SUBVERTICAL_COLUMN = 'subvertical'
    CITY_COLUMN = 'city'
    ROUND_COLUMN = 'round'
    YEAR_COLUMN = 'year'

    def __init__(self):
        """
        Initialize the Investor class.

        Loads the startup dataset, which is assumed to be defined in an external module (e.g., 'dataset').
        """
        self.startup = startup

    def investor_list(self):
        """
        Get a sorted list of unique investors.

        Returns:
            list: A sorted list of unique investors, excluding the first two.
        """
        investors = self.startup[self.INVESTOR_COLUMN].str.split(',').sum()
        unique_investors = sorted(set(investors))[2:]
        return unique_investors

    def recent_five_investments(self, investor_name):
        """
        Get information about the five most recent investments made by a specific investor.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame containing information about the recent investments.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)].head()
        columns = {
            'date': 'Date of Investment',
            'name': 'Startup Name',
            'vertical': 'Vertical',
            'city': 'City',
            'round': 'Type',
            self.AMOUNT_COLUMN: 'Amount (In crore ₹)'
        }
        recent_investments = investor_data.rename(columns=columns)
        return recent_investments

    def group_and_reset(self, data, group_column):
        """
        Group data by a specified column and sum the 'amount' column, then reset the index.

        Args:
            data (pandas.DataFrame): The DataFrame to be grouped.
            group_column (str): The column by which to group the data.

        Returns:
            pandas.DataFrame: A DataFrame with the 'amount' column summed and index reset.
        """
        grouped_data = data.groupby(group_column)[self.AMOUNT_COLUMN].sum()
        return grouped_data.reset_index()

    def biggest_investments(self, investor_name):
        """
        Get information about the top five investments made by a specific investor.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame containing information about the top investments.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, 'startup').nlargest(5, self.AMOUNT_COLUMN)

    def invested_sector(self, investor_name):
        """
        Get the total amount invested by a specific investor in each startup sector (vertical).

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame with the total investments by sector.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, self.VERTICAL_COLUMN)

    def invested_subsector(self, investor_name):
        """
        Get the total amount invested by a specific investor in each startup subsector (subvertical).

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame with the total investments by subsector.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, self.SUBVERTICAL_COLUMN)

    def invested_city(self, investor_name):
        """
        Get the total amount invested by a specific investor in each city.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame with the total investments by city.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, self.CITY_COLUMN)

    def invested_round(self, investor_name):
        """
        Get the total amount invested by a specific investor in each funding round type.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame with the total investments by funding round type.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, self.ROUND_COLUMN)

    def yoy_investment(self, investor_name):
        """
        Get the total yearly investments made by a specific investor.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            pandas.DataFrame: A DataFrame with the total investments by year.
        """
        investor_data = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]
        return self.group_and_reset(investor_data, self.YEAR_COLUMN)

    def get_similar_investors(self, investor_name):
        """
        Get a list of similar investors who have invested in the same sector as a specific investor.

        Args:
            investor_name (str): The name of the investor.

        Returns:
            list: A list of similar investors.
        """
        investor_df = self.startup[self.startup[self.INVESTOR_COLUMN].str.contains(investor_name)]

        if investor_df.empty:
            return pd.Series()

        investor_vertical = investor_df[self.VERTICAL_COLUMN].iloc[0]

        similar_investors_df = self.startup[
            (self.startup[self.VERTICAL_COLUMN] == investor_vertical) &
            (~self.startup[self.INVESTOR_COLUMN].str.contains('Undisclosed Investors', case=False)) &
            (self.startup[self.INVESTOR_COLUMN] != investor_name)
        ]

        similar_investors = list(
            itertools.chain.from_iterable(
                similar_investors_df[self.INVESTOR_COLUMN].str.split(',')
            )
        )

        try:
            return random.sample(similar_investors, min(4, len(similar_investors)))
        except ValueError:
            return similar_investors
