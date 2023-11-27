# Importing pandas for data manipulation
import pandas as pd
# Importing datetime for working with date and time
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self, df):
        # Initializing the DataProcessor with a DataFrame
        self.df = df
        # Dictionary to hold grouped DataFrames
        self.grouped_dfs = {}
        # List to store addresses sorted based on a calculated metric
        self.sorted_addresses = []

    def process_data(self):
        # Converting the 'address' column to string type for consistency
        self.df['address'] = self.df['address'].astype(str)
        # Grouping the DataFrame by 'address' and storing each group in the dictionary
        self.grouped_dfs = {address: group for address, group in self.df.groupby('address')}
        # Internal method to calculate additional metrics
        self._calculate_metrics()

    def _calculate_metrics(self):
        # Setting a threshold for 'net_apr' and a lookback period
        net_apr_threshold = 20
        lookback_days = 7
        # Iterating over each grouped DataFrame to calculate metrics
        for address, df in self.grouped_dfs.items():
            # Converting 'timestamp' to datetime and adjusting timezone
            df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True).dt.tz_convert(None)
            # Getting the current time in UTC for the lookback calculation
            now_utc_naive = datetime.utcnow()
            # Filtering DataFrame for entries in the last 'lookback_days'
            recent_df = df[df['timestamp'] > (now_utc_naive - timedelta(days=lookback_days))]
            # Counting occurrences where 'net_apr' is above the threshold
            above_threshold_count = (recent_df['net_apr'] > net_apr_threshold).sum()
            # Assigning the count back to the DataFrame
            self.grouped_dfs[address] = df.assign(above_threshold_recent=above_threshold_count)
        
        # Sorting addresses based on the calculated metric, in descending order
        self.sorted_addresses = sorted(self.grouped_dfs, key=lambda x: self.grouped_dfs[x]['above_threshold_recent'].iloc[0], reverse=True)

    def get_processed_data(self):
        # Method to retrieve processed DataFrames and sorted addresses
        return self.grouped_dfs, self.sorted_addresses
