# %% Imports
import pandas as pd

# %% GETTING DATA FROM nasdaq_100.csv file
nasdaq_100 = pd.read_csv('./csv_files/nasdaq_100.csv')
nasdaq_100['Ticker']
# %%

# %% GETTING DATA FROM s&p500.csv file
s_p500 = pd.read_csv('./csv_files/s&p500.csv')
s_p500["Symbol"]
# %%
list_codes = set([(code, "Stock") for code in nasdaq_100['Ticker'].to_list() + s_p500["Symbol"].to_list()])