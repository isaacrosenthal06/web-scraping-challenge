import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find('section', class_='image_and_description_container')

    title_div = news.find('div', class_ ="content_title")

    news_title = title_div.text.strip()

    teaser_div = news.find('div', class_ ="article_teaser_body")

    news_p = teaser_div.text.strip()

    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('img', class_ = "headerimage fade-in")

    featured_image_url = url2 + image['src']

    browser.quit()

    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    mars_df = tables[0]

    html_mars_table = mars_df.to_html()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='collapsible results')
    hemisphere_items = soup.find_all('div', class_ = 'item')

    hemisphere_images = []
    hemisphere_image_urls = {}

    for x in range(len(hemisphere_items)):
        description = hemisphere_items[x].find('div', class_ = 'description').find('h3').text
        url = url4 + hemisphere_items[x].a['href']
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('div', class_='container').find('div', class_='wide-image-wrapper').find('img', class_='wide-image')
        image = url4 + image['src']
        hemisphere_image_urls['title' + str(x)] = description
        hemisphere_image_urls['img_url' + str(x)] = image


    hemisphere_images.append(hemisphere_image_urls)
    print(hemisphere_images)
    
    browser.quit()

    mars = {}
    mars['title'] = news_title
    mars['paragraph'] = news_p
    mars['featured_image'] = featured_image_url
    mars['table'] = html_mars_table.strip()
    mars['hemisphere'] = hemisphere_images

    return mars