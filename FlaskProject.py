from flask import Flask 
import requests
from bs4 import BeautifulSoup

def getUrlsFrom(page, directory):
    urls = []
    page_html = requests.get(page)
    html_soup = BeautifulSoup(page_html.text, 'html.parser')
    nav = html_soup.find('div', id='page_cat')
    if nav is None:
        return []
    links = nav.findChildren('a')
    for link in links:
        urls.append(directory + link.get('href'))
    return urls

def findAllUrls(homepage, directory):
    allUrls = []
    page_html = requests.get(homepage)
    html_soup = BeautifulSoup(page_html.text, 'html.parser')
    table = html_soup.find('table', id='categories')
    links = table.findChildren('a')
    mainUrls = []
    for link in links:
        mainUrls.append(directory + link.get('href'))
    mainUrls.append(homepage)
    for url in mainUrls:
        allUrls.extend(getUrlsFrom(url, directory))
    allUrls.extend(mainUrls)
    return allUrls

def scrapeUrl(url):
    search_list = []    
    page_html = requests.get(url)
    html_soup = BeautifulSoup(page_html.text, 'html.parser')
    ul = html_soup.find(id='directory_listings')
    lis = ul.findChildren('li')

    for li in lis:
        if li.find('div', class_='listing_content') is not None:
            company = li.find('a').get_text()
            details = li.find('p', class_='address')
            if details is None:
                continue
            details = details.get_text()
            if details.find('+') == -1:
                continue
            address, phone = details.split('+', 1)
            for word in company.split(' '):
                address = address.replace(word, '')
            address = address.lstrip(', ')
            phone = '+' + phone
            search_list.append({'company': company, 'address': address, 'phone': phone})
        return search_list

def getListingsFrom(directoryPage, directory):
    listings = []
    webpages = findAllUrls(directoryPage, directory)
    for page in webpages:
        listings.extend(scrapeUrl(page))
    print(len(listings))
    return listings

getListingsFrom('https://www.nzdirectory.co.nz/computers.html', 'https://www.nzdirectory.co.nz/')