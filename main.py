from bs4 import BeautifulSoup
from my_functions import *
import requests
import pandas as pd

# IMPORTANT - Before use check these, or expect problems!
# Ensure proxies are up to date {my_function.py/get_with_proxy/proxyList} - 'https://free-proxy-list.net/'
# Ensure API functionality, my free account has a LIMIT of 50 requests {route to api key} - 'https://unsplash.com/'
# Font is freeware, acquired from - 'https://www.fontspace.com/ora-urus-font-f119179'

# Initialise necessary html data for quotes website
url = "https://quotes.toscrape.com/"
result = get_with_proxy(url)
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
# # Display quote data
# print("Quote = ", randomQuote['Quote'], "Tags = ", randomQuote['Tag'])

# # Generate an image using quote data
# imageTag = randomQuote['Tag']
# imageURL = generate_image_url(imageTag)
# print(imageURL)

# Test quote placed on image
image = get_image_with_text(randomQuote['Quote'], randomQuote['Tag'])
image.show()  # only shows and not save, so screenshot if needed