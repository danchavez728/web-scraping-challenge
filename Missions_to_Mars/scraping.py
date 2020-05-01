# Dependencies
from selenium import webdriver
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
browser = Browser('chrome')


def init_browser():
    executable_path = {
        "executable_path": "/usr/local/Caskroom/chromedriver/81.0.4044.69/chromedriver"}
    browser = Browser("chrome", headless=False, **executable_path)
    return browser


mars_code = {}


def scrape_info():
    browser = init_browser()
    executable_path = {
        "executable_path": "/usr/local/Caskroom/chromedriver/81.0.4044.69/chromedriver"}
    browser = Browser("chrome", headless=False, **executable_path)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    nasaTitle = soup.find("div", class_="content_title").text
    news_title = "Mars Helicopter Attached to NASA's Perseverance Rover"
    nasaBody = soup.find("div", class_="rollover_description").text
    news_p = "The team also fueled the rover's sky crane to get ready for this summer's history-making launch."

    mars_code["News_Title"] = news_title
    mars_code["News_Paragraoh"] = news_p
    return mars_code


def scrape_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    marsIm = browser.find_by_id("full_image")
    marsIm.click()
    browser.is_element_present_by_text("more info")
    marsIm2 = browser.find_link_by_partial_text("more info")
    marsIm2.click()
    html = browser.html
    soup = bs(html, "html.parser")
    pic = soup.select_one("figure.lede a img").get("src")
    baseurl = "https://www.jpl.nasa.gov"
    featuredImage = baseurl + pic

    mars_code["featured_image"] = featuredImage
    return mars_code


def scrape_weather():
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    mars_weather = [p.text for p in soup.find_all("p", class_="tweet-text")][0]

    mars_code["mars_temperature"] = mars_weather
    return mars_code


def scrape_table():
    facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    facts_df
    htable = facts_df.to_html()
    mars_code["mars_table"] = htable
    return mars_code
    browser.quit()
