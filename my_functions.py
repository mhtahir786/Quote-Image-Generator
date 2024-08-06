# All functions to be used in main program, placed here for better readability
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont  # PythonImageLibrary
from io import BytesIO
import requests
import random
import logging
import textwrap
import os


# - - Setup for functions
# Log's configuration, to track and debug in development
logging.basicConfig(
    filename='test.log',
    filemode='a',  # append to log file
    level=logging.DEBUG,  # set logging level (debugging, info, warning, error, critical)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' # time, name, level, message
)

# Load environment variables from file path specified
load_dotenv(dotenv_path='store.env')

# - - All functions
# Uses a proxy to redirect data from site request
def get_with_proxy(url):
    # Proxies attained from 'https://free-proxy-list.net/'
    # Remember to update proxies (ensure they work)
    proxyList = [
        'http://128.199.136.56:3128',    # Singapore
        'http://172.183.241.1:8090',     # USA
        'http://189.240.60.166:9090',    # Mexico
        'http://103.152.232.162:8199',     # Columbia
        'http://223.135.156.183:8080'    # Japan
        ]
    
    # Loop through all proxies till one works
    for i in range(len(proxyList)):
        proxy = random.choice(proxyList)

        try:  # attempt to use the proxy's available
            result = requests.get(url, proxies={'http': proxy, 'https': proxy})
            if result.status_code == 200:
                logging.debug(f"Proxy used - {proxy}")
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


# Returns an image URL generated using the Unsplash API given a string of tags
def generate_image_url(tags):
    # Grab API key from .env file, report issue when not found
    apiKey = os.getenv('UNSPLASH_ACCESS_KEY')
    if not apiKey:
        logging.debug("Unable to get UNSPLASH_ACCESS_KEY from file")
        raise ValueError("Unable to retrieve UNSPLASH_ACCESS_KEY")
    
    # Ensure tag parameter contains content
    if tags:
        logging.debug("Parameters contain content in function; generate_image_url")
    else:
        logging.debug("Error - No content in parameters for function; generate_image_url")
        raise ValueError("Error - No content in parameters for function; generate_image_url")
    
    # Initiate a get request using tags given as parameter
    apiURL = "https://api.unsplash.com/photos/random"
    headers = {
        'Authorization': f'Client-ID {apiKey}'
    }
    params = {
        'query': tags,
        'count': 1  # only one result required
    }
    result = requests.get(apiURL, headers=headers, params=params)

    # Check process was successful and return image url
    imageURL = "No image found"  # default issue
    if result.status_code == 200:
        data = result.json()
        # Ensure data was returned and is not empty
        if data:
            imageURL = data[0]['urls']['regular']  # check API documentation for parsing details
            logging.debug(f"Successfully obtained image url {data[0]['urls']['regular']}")
        else:
            logging.debug("Data returned from API was empty.")
    else:
        logging.debug(f"Error with API request statsus code {result.status_code} - {result.text}")
    
    return imageURL

# Returns an image which has been downlaoded from url provided as parameter
def download_image_from_url(url):
    # Issue a get request for the image and check it's success
    result = requests.get(url)
    if result.status_code == 200:
        # Return as an image in memory without saving it (for temporary use)
        image = Image.open(BytesIO(result.content))
        logging.debug("Successfully downlaoded image in function; download_image_from_url")
        return image
    else:
        logging.debug(f"Couldn't downlaod image in function; download_image_from_url), Status code - {result.status_code}")
        raise Exception(f"Couldn't downlaod image in function; download_image_from_url), Status code - {result.status_code}")
    

# Returns font size adjusted to fit a bounding box for the quote
def draw_text_on_image(quoteText, image):
    # Initialise font size & type ideally
    FONT_NAME = "fonts/OraUrus-BLjPx.ttf"
    FONT_SIZE = 120  # also max font size
    FONT_COLOUR = (255,255,255)  # white
    BOX_WIDTH = 900  # using static pixels over percentage sizes makes text appear different
    BOX_HEIGHT = 600 # .. size with different image dimensions, this is an artistic choice

    # Setup pillow library to draw on to image
    fontSize = FONT_SIZE
    draw = ImageDraw.Draw(image)

    # Adjust font size dynamically till it fits bounding box
    while True:
        # Wrap text within bounding box by trying with current font size
        font = ImageFont.truetype(FONT_NAME, fontSize)  # load font
        wrapText = textwrap.fill(quoteText, width=BOX_WIDTH  // font.getbbox(' ')[1])  # returns as (left, top, right, bottom)

        # Recalculate text with and height
        left, top, right, bottom = draw.multiline_textbbox((0,0), wrapText, font=font)  # get bounding box, positions can be 0
        textWidth = right - left
        textHeight = bottom - top
        logging.debug(f"Font Size - {fontSize}, Text Width - {textWidth}, Text Height - {textHeight}")

        # Check text fits in bounding box and use that font, otherwise decrement and continue loop
        if (textWidth <= BOX_WIDTH) and (textHeight <= BOX_HEIGHT):
            break
        fontSize -= 1
    
    # Use image and text dimensions to find the correct positions for text placement in CENTRE
    imageWidth, imageHeight = image.size
    posX = ((imageWidth - textWidth) / 2)
    posY = ((imageHeight - textHeight) / 2)
    logging.debug(f"Pos x - {posX}, Pos y - {posY}")
    draw.multiline_text((posX, posY), wrapText, fill=FONT_COLOUR, font=font, align="center")

    return image

# Returns an image with quote text inserted on it
def get_image_with_text(quoteText, quoteTags):    
    # Obtain an image from API & download into memory for use
    imageURL = generate_image_url(quoteTags) 
    
    # Download image temporarily into memory to draw on
    image = download_image_from_url(imageURL)

    # Draw text on to image using dynamic sizing and center placement onto image
    image = draw_text_on_image(quoteText, image)   

    return image