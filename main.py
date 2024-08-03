from bs4 import BeautifulSoup
from my_functions import *
import requests
import pandas as pd

# Initialise necessary html data for quotes website
url = "https://quotes.toscrape.com/"
result = get_with_proxy(url)  # REMINDER - update proxy list when using
doc = BeautifulSoup(result.text, "html.parser")

# # Collect relevant quote information
# quotesText = get_quote_text(doc)
# quotesTags = get_quote_tags(doc)
# nearlyAll = get_specific_quote_data(url, get_quote_tags)
# print(quotesText)
# print(quotesTags)
# print(nearlyAll)

# # Convert list data into a dictionary
# dataDict = get_all_quote_data(url)
# df = pd.DataFrame(dataDict)  # make into a data frame
# df.to_csv('quote.csv', index=None)  # create a new quote.csv to save dataframe into
# pd.read_csv('quote.csv')  # output csv
# print(df)

# Get all quote data
allQuotes = get_all_quote_data(url)
# Get a random quote
randomQuote = select_random_row(allQuotes)
# Display quote data
print("Quote = ", randomQuote['Quote'], "Tags = ", randomQuote['Tag'])