# Importing necessary classes from their respective modules
from ConfigManager import *
from DatabaseConnection import *
from DataProcessor import *
from Plotter import *

class Application:
    def __init__(self, config_path):
        # Initializing the ConfigManager with the path to the configuration file
        self.config_manager = ConfigManager(config_path)
        
        # Retrieving database configuration settings from the config manager
        self.db_config = self.config_manager.get_database_config()

        # Establishing a database connection using the retrieved configuration
        self.database = DatabaseConnection(self.db_config)

    def run(self):
        # SQL query to fetch required data from the database
        query = """
        SELECT x.* 
        FROM prm.aggregated_data x
        WHERE (range_label IN ('0.50σ','1.00σ','1.50σ'))
        ORDER BY x."timestamp" DESC
        """
        
        # Executing the query and storing the result in a DataFrame
        df = self.database.query(query)

        # Closing the database connection after the query execution
        self.database.close()

        # Initializing the DataProcessor with the fetched data
        processor = DataProcessor(df)
        # Processing the data (grouping, calculating metrics, etc.)
        processor.process_data()

        # Initializing the Plotter with the processed data
        plotter = Plotter(processor)
        # Creating and saving the plots into a PDF file
        plotter.plot('sorted_grouped_plots.pdf')