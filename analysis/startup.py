import pandas as pd

from dataset import startup


class Startup:

    def __init__(self):
        self.startup = startup

    def list_of_startups(self):
        return list(startup['startup'].sort_values().unique())

    def sector(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['vertical'].values[0]

    def subsector(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['subvertical'].values[0]

    def location(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['city'].values[0]

    def stage(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['round'].values[0]

    def investors(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['investors'].values[0]

    def investment_date(self, startup_name):
        return self.startup[self.startup['startup'] == startup_name]['date'].values[0]

    def funding(self, startup_name):
        company = self.startup[self.startup['startup'] == startup_name]
        return company.groupby('startup')['amount'].sum().values[0]

    def similar_startups(self, startup_name):
        vertical = startup.loc[startup['startup'] == startup_name, 'vertical'].values[0]

        temp_startups = startup.loc[startup['vertical'] == vertical, 'startup'].unique()

        similar_startups = []
        for company in temp_startups:
            if company != startup_name:
                similar_startups.append(company)

        return similar_startups