# Importing the configparser module for reading configuration files
import configparser

class ConfigManager:
    def __init__(self, config_path):
        # Initialize the ConfigParser
        self.config = configparser.ConfigParser()
        # Read the configuration file specified by the config_path
        self.config.read(config_path)

    def get_database_config(self):
        # Extract and return database configuration as a dictionary
        # This includes the host, user, password, and database name
        # as specified in the configuration file under the 'database' section
        return {
            'host': self.config['database']['host'],
            'user': self.config['database']['user'],
            'password': self.config['database']['password'],
            'database': self.config['database']['db']
        }
