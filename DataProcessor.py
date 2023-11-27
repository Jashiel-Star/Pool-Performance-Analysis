import pandas as pd
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self, df):
        # Initialize DataProcessor with a DataFrame
        self.df = df
        self.grouped_dfs = {}  # Dictionary to store grouped DataFrames
        self.sorted_addresses = []  # List to store sorted addresses

    def process_data(self):
        self.df['address'] = self.df['address'].astype(str)

        # Grouping DataFrame by 'address' and then by 'range_label'
        grouped = self.df.groupby(['address', 'range_label'])

        # Storing each sub-group in the dictionary
        for (address, range_label), group in grouped:
            if address not in self.grouped_dfs.keys():
                self.grouped_dfs[address] = {}
            self.grouped_dfs[address][range_label] = group

        self._calculate_metrics()

        # Sorting addresses based on the calculated metric, in descending order
        self.sorted_addresses = sorted(self.grouped_dfs.keys(), reverse=True)

    def _calculate_metrics(self):
        net_apr_threshold = 20
        lookback_days = 7
        for address, range_groups in self.grouped_dfs.items():
            for range_label, df in range_groups.items():
                # Convert 'timestamp' to datetime and adjust timezone
                df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True).dt.tz_convert(None)
                now_utc_naive = datetime.utcnow()
                recent_df = df[df['timestamp'] > (now_utc_naive - timedelta(days=lookback_days))]
                above_threshold_count = (recent_df['net_apr'] > net_apr_threshold).sum()
                self.grouped_dfs[address][range_label] = df.assign(above_threshold_recent=above_threshold_count)

        # Sorting logic will need to be updated based on the new data structure

    def get_processed_data(self):
        return self.grouped_dfs, self.sorted_addresses
