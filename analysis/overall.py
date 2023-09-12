import pandas as pd
from dataset import startup

class Overall:

    def __init__(self):
        self.startup = startup

    def total_invested_amount(self):
        return round(self.startup['amount'].sum())

    def max_amount_infused(self):
        result = self.startup.groupby('startup')['amount'].max()
        sorted_result = result.sort_values(ascending=False)
        max_value = sorted_result.head(1).values[0]
        return max_value


    def avg_ticket_size(self):
        return self.startup.groupby('startup')['amount'].sum().mean()

    def total_funded_startup(self):
        return self.startup['startup'].nunique()

    def total_funding_mom(self):
        temp_df = startup.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['MM-YYYY'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        temp_df.rename(columns={
            'amount': 'Total Funding (In Crore Rs.)'
        }, inplace=True)

        return temp_df

    def total_funded_startup_mom(self):
        temp_df = startup.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['MM-YYYY'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        temp_df.rename(columns={
            'amount': 'Total Funded Startups'
        }, inplace=True)

        return temp_df

    def most_funded_sector(self):
        temp_df = startup.groupby('vertical')['amount'].sum().reset_index()
        most_funded_sectors = temp_df[temp_df['amount'] != 0.0].sort_values(
            by='amount',
            ascending=False
        ).head(10)

        most_funded_sectors['amount'] = round(most_funded_sectors['amount'], 2)

        return most_funded_sectors

    def most_funded_round(self):
        temp_df = startup.groupby('round')['amount'].sum().reset_index()
        most_funded_type = temp_df[temp_df['amount'] != 0.0].sort_values(
            by='amount',
            ascending=False
        ).head(10)

        return most_funded_type

    def most_funded_cities(self):
        temp_df = startup.groupby('city')['amount'].sum().sort_values(ascending=False)
        most_funded_city = temp_df.head(10).reset_index()
        return most_funded_city

    def most_funded_startups_yoy(self):
        most_funded_startup_yoy = startup.groupby(['year', 'startup'])['amount'].sum() \
            .sort_values(ascending=False).reset_index().drop_duplicates(
            'year',
            keep='first'
        ).sort_values(by='year')

        most_funded_startup_yoy.rename(columns={
            'year': 'Year',
            'startup': 'StartUp Name',
            'amount': 'Amount (In Crore Rs)'
        }, inplace=True)

        return most_funded_startup_yoy

    def top_investors(self):
        # New dataframe with separate rows for each investor
        investor_list = []

        for _, row in self.startup.iterrows():
            investors = row['investors'].split(',')
            investors = [investor.strip() for investor in investors]
            data = {
                'date': row['date'],
                'startup': row['startup'],
                'vertical': row['vertical'],
                'subvertical': row['subvertical'],
                'city': row['city'],
                'amount': row['amount'],
                'year': row['year'],
                'month': row['month']
            }
            
            for investor in investors:
                data['investors'] = investor
                investor_list.append(data.copy())

        new_df = pd.DataFrame(investor_list)

        # Top investors
        top_investors = new_df.groupby('investors')['amount'].sum().sort_values(ascending=False).reset_index()

        # Sum investment amounts for both 'SoftBank Group' and 'Softbank'
        softbank_group_amount = top_investors.loc[
            top_investors['investors'].isin(['Softbank Group', 'Softbank']), 'amount'
        ].sum()

        # Update the investment amount for 'SoftBank Group'
        top_investors.loc[
            top_investors['investors'] == 'Softbank Group', 'amount'
        ] = softbank_group_amount

        # Drop the rows corresponding to 'Softbank'
        top_investors = top_investors[top_investors['investors'] != 'Softbank']

        top_investors = top_investors.sort_values(by='amount', ascending=False).head(10)
        return top_investors

    def funding_amount_year_month(self):
        # Aggregate funding amount by year and month
        df_agg = startup.groupby(['year', 'month'])['amount'].sum().reset_index()

        # Create pivot table
        pivot_table = df_agg.pivot(index='year', columns='month', values='amount')

        return pivot_table