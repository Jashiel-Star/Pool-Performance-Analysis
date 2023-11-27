# Importing necessary classes from their respective modules
from ConfigManager import *
from DatabaseConnection import *
from DataProcessor import *
from Plotter import *
import pandas as pd

class Application:
    def __init__(self, config_path):
        # Initialize the Application class with a configuration file path
        self.config_manager = ConfigManager(config_path)
        # Retrieve database configuration settings from the config manager
        self.db_config = self.config_manager.get_database_config()
        # Establish a database connection using the retrieved configuration
        self.database = DatabaseConnection(self.db_config)

    def run(self):
        # SQL query to fetch required data from the database
        query = """
        SELECT x.* 
        FROM prm.aggregated_data x
        WHERE (range_label IN ('0.50σ','1.00σ','1.50σ'))
        ORDER BY x."timestamp" DESC
        """
        # Execute the query and store the result in a DataFrame
        df = self.database.query(query)
        # Close the database connection after the query execution
        self.database.close()

        # Initialize the DataProcessor with the fetched data
        processor = DataProcessor(df)
        # Process the data (grouping, calculating metrics, etc.)
        processor.process_data()

        # Get the processed DataFrames and sorted addresses from the DataProcessor
        grouped_dfs, _ = processor.get_processed_data()

        # Create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter('processed_data.xlsx', engine='xlsxwriter') as writer:
            # Iterate through the nested dictionary and save each DataFrame as a separate sheet
            for address, range_groups in grouped_dfs.items():
                for range_label, df in range_groups.items():
                    # Replace invalid characters and construct a sheet name
                    name = df['name'].iloc[0].replace('/', '-')  # Replace '/' with '-'
                    fee = f"{df['fee'].iloc[0]*100:.0f}%"  # Convert fee to percentage format
                    sheet_name = f"{name}_{fee}_{range_label}"  # Create a sheet name
                    # Truncate sheet name to avoid exceeding Excel's limit
                    sheet_name = sheet_name[:31]
                    # Save the DataFrame as a sheet with the constructed sheet name
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Initialize the Plotter with the processed data
        plotter = Plotter(processor)
        # Create and save the plots into a PDF file
        plotter.plot('sorted_grouped_plots.pdf')