Financial Data Analysis and Visualization Tool
Overview
This tool is designed to process financial data from a PostgreSQL database, specifically focusing on aggregated data related to financial metrics like Net APR, IL Hedge APR, and Adjusted APR. The tool fetches data, performs specific calculations, and visualizes the results in a series of plots, which are then saved to a PDF file.

How it Works
The program is structured in an object-oriented manner, with each major functionality encapsulated in its class. It reads configuration data from a file, connects to a PostgreSQL database to retrieve data, processes this data, and then generates visualizations.

Classes and Their Functions
ConfigManager
File: config_manager.py
Functionality: Handles the reading and parsing of the configuration file (config.ini). It specifically extracts and provides database connection parameters.
DatabaseConnection
File: database_connection.py
Functionality: Manages the database connection. It establishes a connection to the PostgreSQL database using parameters provided by ConfigManager and executes SQL queries. It's also responsible for closing the database connection.
DataProcessor
File: data_processor.py
Functionality: Processes the data fetched from the database. This includes converting data types, grouping data by specific criteria, and calculating essential metrics for analysis. The processed data is then prepared for visualization.
Plotter
File: plotter.py
Functionality: Responsible for creating visualizations based on the processed data. It generates line plots for different financial metrics and saves them into a single PDF file. This class handles all aspects of plotting, including formatting and layout.
Application
File: application.py
Functionality: Serves as the main entry point of the program. It orchestrates the process flow by utilizing the other classes. It initializes the configuration, database connection, data processing, and plotting sequences.
Setup and Execution
Configuration File: Ensure config.ini is correctly set up with the necessary database credentials.
Dependencies: Install required Python packages listed in requirements.txt.
Run the Program: Execute the main script (usually main.py) to start the application.
Requirements
Python 3.x
pandas
matplotlib
psycopg2
configparser
Note: For detailed package versions and dependencies, refer to requirements.txt.

Additional Information
Ensure that the PostgreSQL database is accessible with the credentials provided in config.ini.
The SQL query used for data extraction can be modified based on the specific data requirements.
The visualizations and data processing logic can be adjusted in their respective classes to cater to different analysis needs.