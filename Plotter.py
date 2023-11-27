import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from DataProcessor import *


class Plotter:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def plot(self, pdf_path):
        grouped_dfs, sorted_addresses = self.data_processor.get_processed_data()
        window_size = 7
        apr_threshold = 20

        with PdfPages(pdf_path) as pdf:
            for address in sorted_addresses:
                address_group = grouped_dfs[address]
                for range_label, df in address_group.items():
                    # Convert APR values to percentages for readability
                    df['net_apr'] = df['net_apr'] * 100
                    df['il_hedge_apr'] = df['il_hedge_apr'] * 100
                    df['adj_apr'] = df['adj_apr'] * 100

                    # Calculate rolling averages for APR values
                    df['net_apr_smooth'] = df['net_apr'].rolling(window=window_size).mean()
                    df['il_hedge_apr_smooth'] = df['il_hedge_apr'].rolling(window=window_size).mean()
                    df['adj_apr_smooth'] = df['adj_apr'].rolling(window=window_size).mean()

                    # Skip plot creation if DataFrame is empty or if rolling averages are all NaN
                    if df.empty or df[['net_apr_smooth', 'il_hedge_apr_smooth', 'adj_apr_smooth']].notna().sum().sum() == 0:
                        continue
                                
                    # Create a new figure with specified dimensions
                    plt.figure(figsize=(10, 6))

                    # Plot a horizontal line at the 20% APR threshold
                    plt.axhline(y=apr_threshold, color='gray', linestyle='--', label='20% APR Threshold')

                    # Plot each APR type with a smooth line (rolling average)
                    plt.plot(df['timestamp'], df['net_apr_smooth'], label='Net APR')
                    plt.plot(df['timestamp'], df['il_hedge_apr_smooth'], label='IL Hedge APR')
                    plt.plot(df['timestamp'], df['adj_apr_smooth'], label='Adj APR', linestyle='--')

                    # Fill the area under the net_apr_smooth curve
                    plt.fill_between(df['timestamp'], df['net_apr_smooth'], apr_threshold, 
                                     where=(df['net_apr_smooth'] > apr_threshold), facecolor='green', alpha=0.3)
                    # Fill the area above the net_apr_smooth curve
                    plt.fill_between(df['timestamp'], df['net_apr_smooth'], apr_threshold, 
                                     where=(df['net_apr_smooth'] < apr_threshold), facecolor='red', alpha=0.3)

                    # Set the title of the plot using data from the DataFrame
                    title = f"{df['blockchain'].iloc[0]}: {df['name'].iloc[0]} - {range_label} - {df['fee'].iloc[0]*100}%"
                    plt.title(title)
                    plt.xlabel('Timestamp')
                    plt.ylabel('APR (%)')
                    plt.legend()  # Add a legend to the plot
                    #plt.show()
                    pdf.savefig()  # Save the current plot to the PDF
                    plt.close()  # Close the plot to free memory
                    
