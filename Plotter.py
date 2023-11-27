# Importing matplotlib for plotting
import matplotlib.pyplot as plt
# Importing PdfPages for saving plots into a PDF file
from matplotlib.backends.backend_pdf import PdfPages

class Plotter:
    def __init__(self, data_processor):
        # Initializing the Plotter with a DataProcessor instance
        # The DataProcessor instance is used to get processed data for plotting
        self.data_processor = data_processor


    def plot(self, pdf_path):
        # Retrieving processed data from the DataProcessor instance
        grouped_dfs, sorted_addresses = self.data_processor.get_processed_data()
        # Setting the window size for calculating rolling averages
        window_size = 7
        #Setting the position at which the horizontal divisor will be placed
        apr_threshold = 20 

        # Creating a PDF file at the specified path to save plots
        with PdfPages(pdf_path) as pdf:
            # Iterating through each address in the sorted list
            for address in sorted_addresses:
                # Retrieving the DataFrame corresponding to the current address
                df = grouped_dfs[address]

                # Converting APR values to percentages for better readability in the plot
                df['net_apr'] = df['net_apr'] * 100
                df['il_hedge_apr'] = df['il_hedge_apr'] * 100
                df['adj_apr'] = df['adj_apr'] * 100

                # Calculating rolling averages for APR values
                df['net_apr_smooth'] = df['net_apr'].rolling(window=window_size).mean()
                df['il_hedge_apr_smooth'] = df['il_hedge_apr'].rolling(window=window_size).mean()
                df['adj_apr_smooth'] = df['adj_apr'].rolling(window=window_size).mean()

                # Skipping plot creation if DataFrame is empty or if rolling averages are all NaN
                if df.empty or df[['net_apr_smooth', 'il_hedge_apr_smooth', 'adj_apr_smooth']].notna().sum().sum() == 0:
                    continue

                # Setting up the plot with specified dimensions
                plt.figure(figsize=(10, 6))

                # Plot the 20% APR threshold line
                plt.axhline(y=apr_threshold, color='gray', linestyle='--', label='20% APR Threshold')

                # Plotting each APR type with a smooth line (rolling average)
                plt.plot(df['timestamp'], df['net_apr_smooth'], label='Net APR')
                plt.plot(df['timestamp'], df['il_hedge_apr_smooth'], label='IL Hedge APR')
                plt.plot(df['timestamp'], df['adj_apr_smooth'], label='Adj APR', linestyle='--')

                # Fill the area under the net_apr_smooth curve
                plt.fill_between(df['timestamp'], df['net_apr_smooth'], apr_threshold, 
                                 where=(df['net_apr_smooth'] > apr_threshold), facecolor='green', alpha=0.3)
                plt.fill_between(df['timestamp'], df['net_apr_smooth'], apr_threshold, 
                                 where=(df['net_apr_smooth'] < apr_threshold), facecolor='red', alpha=0.3)
                                 
                # Setting the title of the plot using data from the DataFrame
                title = f"{df['blockchain'].iloc[0]}: {df['name'].iloc[0]} - {df['range_label'].iloc[0]}"
                plt.title(title)
                # Setting labels for axes
                plt.xlabel('Timestamp')
                plt.ylabel('APR (%)')
                # Adding a legend to the plot
                plt.legend()
                # Saving the current plot to the PDF
                pdf.savefig()
                # Closing the plot to free memory
                plt.close()