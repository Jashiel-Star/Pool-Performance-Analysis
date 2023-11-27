# Importing psycopg2 for PostgreSQL database connection
import psycopg2 
# Importing pandas for data manipulation and analysis
import pandas as pd

class DatabaseConnection:
    def __init__(self, config):
        # Establishing a database connection using the provided configuration.
        # The configuration is expected to be a dictionary containing
        # database connection parameters like host, user, password, and database name.
        self.connection = psycopg2.connect(**config)

    def query(self, sql):
        # Executing a SQL query and returning the result as a pandas DataFrame.
        # This method is useful for retrieving data from the database.
        return pd.read_sql_query(sql, self.connection)

    def close(self):
        # Closing the database connection.
        # It's important to close connections to free up database resources.
        self.connection.close()