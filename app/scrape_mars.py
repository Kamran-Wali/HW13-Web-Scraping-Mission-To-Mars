# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time

# Define scrape function
def scrape():
    # Initialize a library to collect the scraped mars data
    mars_library = {}

    #Use splinter and chrome extension
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    # NASA URL to be scraped
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #Visit the page using the browser
    browser.visit(url1)

    # assign html content
    html = browser.html

    # Create a Beautiful Soup object of the NASA site
    soup1 = bs(html, 'html.parser')

    # Extract the text of the title and Clean up the text
    soup1.title.text.strip()

    # Extract the text using strip functionality
    news_title = soup1.find_all('div', class_='content_title')[0].find('a').text.strip()

    # Extract the paragraph from the class="rollover_description_inner" and clean up the text use strip
    news_p = soup1.find_all('div', class_='rollover_description_inner')[0].text.strip()

    # add title and paragraph to the dictionary
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p

    # JPL Mars Space Images - Featured Image

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    # Create a soup object of the JPL website
    html = browser.html
    soup2 = bs(html, 'html.parser')

    partial_address = soup2.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()

    #combine root url with the full address
    featured_image_url = "https://www.jpl.nasa.gov"+partial_address

    # add featured_image_url to the dictionary
    mars_library['featured_image_url'] = featured_image_url

    #browse to check url
    browser.visit(featured_image_url)

    # Mars Weather

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html = browser.html

    soup3 = bs(html, 'html.parser')

    #scrap latest Mars weather tweet and print
    mars_weather = soup3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    # Add mars_weather into Library
    mars_library['mars_weather'] = mars_weather

    # Mars Facts
    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)

    # Convert list of table into pandas dataframe
    df = tables[0]
    df.columns=['description','value']

    # reset index on the description column
    df.set_index('description', inplace=True)

    # converrt to html and and assign to variable
    mars_facts=df.to_html(justify='left')

    # Put Mars facts into Library
    mars_library['mars_facts'] = mars_facts

    # Mars Hemisperes
    # MARS website to be scraped
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    # Create a beautiful soup object of the MArs html
    html = browser.html
    soup5 = bs(html,'html.parser')

    # initialize the list variable
    hemisphere_image_urls = []

    # initialize a dictonary 
    dict = {}

    # get all the title
    results = soup5.find_all('h3')

    # Loop through each result of the h3 heading tag collected by beautiful soup object 
    for result in results:
    
        itema = result.text
        time.sleep(1)    
        browser.click_link_by_partial_text(itema)
        time.sleep(1)
    
        htmla = browser.html
    
        soupa = bs(htmla,'html.parser')
        time.sleep(1)
    
        # Grab the image link
        linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
    
        # Pass title to Dict
    
        time.sleep(1)
        dict["title"]=itema
        # Pass url to Dict
        dict["img_url"]=linka
        # Append Dict to the list 
        hemisphere_image_urls.append(dict)
        # Clean Up Dict
        dict = {}
        browser.click_link_by_partial_text('Back')
        time.sleep(1)

    # Put facts into Library
    mars_library['hemisphere_image_urls']=hemisphere_image_urls

    browser.quit()
    
    # Return Library Dictionary
    return mars_library





















