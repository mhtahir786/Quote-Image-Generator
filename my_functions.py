# All functions to be used in main program, placed here for better readability
from bs4 import BeautifulSoup
import requests
import random

# Uses a proxy to redirect data from site request
def get_with_proxy(url):
    # Proxies attained from 'https://free-proxy-list.net/'
    # Remember to update proxies (ensure they work)
    proxyList = [
        'http://194.5.25.34:443',        # Singapore
        'http://20.111.54.16:8123',      # Canada
        'http://160.86.242.23:8080',     # Japan
        'http://8.223.31.16:1080',       # Singapore
        'http://135.148.171.194:18080'   # USA
        ]
    
    # Loop through all proxies till one works
    for i in range(len(proxyList)):
        proxy = random.choice(proxyList)

        try:  # attempt to use the proxy's available
            result = requests.get(url, proxies={'http': proxy, 'https': proxy})
            if result.status_code == 200:
                return result
            else:
                print(f"This proxy failed - {proxy}, status code: {result.status_code}")
        except requests.exceptions.RequestException as error:  # handle proxy errors and continue
            print(f"Proxy {proxy} failed. Error: {error}")
    
    return None


# Return all quote text within a set of quotes as a list
def get_quote_text(doc):
    allQuotes = []
    divQuotes = doc.find_all('div', class_='quote')

    # Find all quote text within quote div
    for content in divQuotes:
        quote = content.find('span', class_="text").text
        allQuotes.append(quote)

    return allQuotes

# Return all tags associated within a set of quotes as a list
def get_quote_tags(doc):
    allTags = []
    divQuotes = doc.find_all('div', class_='quote')

    # Find all quote tags within quote div
    for content in divQuotes:
        tag = content.find('div', class_="tags").meta['content']
        allTags.append(tag)

    return allTags


# Returns a dictionary format of data acquired from lists
def list_to_dict(quoteList, tagList):
    # Ensure lists are same length
    if (len(quoteList) != len(tagList)):
        raise ValueError("List to Dict Function - different length of lists")

    newDict = {}

    # Initialise column names
    columns = ['Key', 'Quote', 'Tag']

    # Using i like a key to map quote information in a dictionary
    for i in range(len(quoteList)):
        newDict[i] = {
            columns[0]: i,               # Key
            columns[1]: quoteList[i],    # Quote Text
            columns[2]: tagList[i]       # Tag
        }
    
    return newDict

# Return specific quote data from main site, traversing through all pages
# mainURL = url without changes, typeFunc = function name for type i.e. get_quote_text
def get_specific_quote_data(mainURL, typeFunc):
    allData = []
    pageNum = 1

    # Get all quotes whilst pages contain them (should be 10 pages)
    while True:

        # Setup new page to get quote div's from
        newURL = f"{mainURL}/page/{pageNum}"  # update url to access
        result = requests.get(newURL)
        doc = BeautifulSoup(result.text, "html.parser")

        if result.status_code != 200:  # 200 illustrates success
            break
        data = typeFunc(doc)

        # Break loop when list is empty (couldn't get more quotes)
        if not data:
            break
        
        # Add quotes to allData list
        allData.extend(data)
        pageNum += 1
    
    return allData

# Return a dictionary containing all required quote content from main site's pages
def get_all_quote_data(mainURL):
    allQuotes = []
    allTags = []
    pageNum = 1

    # Get all quotes, of all types - whilst pages contain them
    while True:

        # Setup new page to get quote div's from
        newURL = f"{mainURL}/page/{pageNum}"  # update url to access
        result = requests.get(newURL)
        doc = BeautifulSoup(result.text, "html.parser")

        if result.status_code != 200:  # 200 illustrates success
            break

        # Get required data for this page and store in list
        dataQuotes = get_quote_text(doc)
        dataTags = get_quote_tags(doc)

        # Break loop when any list is empty (couldn't get more quotes)
        if (not dataQuotes) or (not dataTags):
            break
        
        # Add quotes to allData list
        allQuotes.extend(dataQuotes)
        allTags.extend(dataTags)
        pageNum += 1
    
    # Convert lists into dict format to return
    allData = list_to_dict(allQuotes, allTags)
    return allData

# Returns a random row selected within dictionary presented
def select_random_row(quoteDict):
    keys = list(quoteDict.keys())  # convert dictionary keys to a list
    randomKey = random.choice(keys) # get a random key
    return quoteDict[randomKey]  # return row associated with that key