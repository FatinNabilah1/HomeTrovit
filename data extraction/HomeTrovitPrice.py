# -*- coding: utf-8 -*-
"""
Created on Sun Sept 29 2019
Author: WQD190011

Home Trovit
Kuala Lumpur

"""
import bs4
from bs4 import BeautifulSoup
import requests
import math
import pandas as pd

## define or initialise all the attributes
title1       = []
address1     = []
detail1      = []
url1         = []
image1       = []
source_info1 = []
source_date1 = []
price1       = []
nofbedroom1  = []
floorsize1   = []

num         = 0
page        = 1
total_page  = 0
total_item  = 0

#r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/sug.0/isUserSearch.1/origin.2/order_by.relevance/city.Cheras/price_min.400000/price_max.500000/rooms_min.2/property_type.Apartment/')
r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.11/rooms_min.0/bathrooms_min.0/order_by.source_date/resultsPerPage.25/tracking.%7B%22acc%22%3A2404%2C%22c%22%3A920185567%2C%22a%22%3A46360633192%2C%22k%22%3A297024398149%2C%22d%22%3A%22c%22%2C%22gclid%22%3A%22EAIaIQobChMIrc-uv4f95AIVg5KPCh0F-QJSEAAYAyAAEgIEtPD_BwE%22%7D/isUserSearch.1/page.1')
soup = bs4.BeautifulSoup(r.text,'xml')

##retrieve and set the total page number        
total_item = soup.find('div',{'class':'results-counter js-results-counter'}).find('span').text
total_item = int(total_item.replace(',',''))
total_page = math.ceil(total_item/25)

if total_page > 100:
   total_page = 100

#start loop
#loop per page number
while page <= total_page:
        #r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.2/price_min.400000/price_max.500000/rooms_min.2/bathrooms_min.0/property_type.Apartment/city.Cheras/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.'+str(page))
        r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.11/rooms_min.0/bathrooms_min.0/order_by.source_date/resultsPerPage.25/tracking.%7B%22acc%22%3A2404%2C%22c%22%3A920185567%2C%22a%22%3A46360633192%2C%22k%22%3A297024398149%2C%22d%22%3A%22c%22%2C%22gclid%22%3A%22EAIaIQobChMIrc-uv4f95AIVg5KPCh0F-QJSEAAYAyAAEgIEtPD_BwE%22%7D/isUserSearch.1/page.'+str(page))
        soup = bs4.BeautifulSoup(r.text,'xml')
        
        #check and set the item number
        if page == total_page:
               no_item = total_item - ((page - 1) * 25)
        else:
               no_item = 25
        
        #second loop
        #loop per item number     
        while num < no_item:
            
            ## retrieving of the data
            
            # Title
            try:
                title = soup.find_all('a',{'class':'js-item-title'})[num].text
            except IndexError:
                title = "#NA"
            title1.append(title)
            
            # Address or Zone
            try:
                address = soup.find_all('div',{'class':'details'})[num].find('span').text
            except IndexError:
                address = "#NA"
            address1.append(address)
            
            # Property Details
            try:
                detail = soup.find_all('div',{'class':'description'})[num].find('p').text
            except IndexError:
                detail = "#NA"
            detail1.append(detail)
            
            # URL
            try:
                url = soup.find_all('a',{'class':'js-item-title'})[num].get('href')
            except IndexError:
                url = "#NA"
            url1.append(url)
            
            # Image
            try:
                image   = soup.find_all(itemprop="image")[num].get("src")
            except IndexError:
                image   = "#NA"
            image1.append(image)
            
            # Source Info
            try:
                source_info = soup.find_all('small',{'class':'source'})[num].text
            except IndexError:
                source_info = "#NA"
            source_info1.append(source_info)
            
            # Source Date or Published Date
            try:
                source_date = soup.find_all('small',{'class':'date'})[num].text
            except IndexError:
                source_date = "#NA"
            source_date1.append(source_date)
            
            # Price
            try:
                price = soup.find_all('div',{'class':'price'})[num].find('span').text
            except IndexError:
                price = "#NA"
            price1.append(price)
            
            # No of Bedroom Available
            try:
                if soup.find_all('div',{'class':'property'})[num].find('span') is not None:
                    nofbedroom  = soup.find_all('div',{'class':'property'})[num].find('span').text
                else:
                    nofbedroom = "#NA"
            except IndexError:
                nofbedroom = "#NA"
            nofbedroom1.append(nofbedroom)
            
            # Floor Size or Property Size
            try:
                floorsize   = soup.find_all(itemprop="floorSize")[num].get("content")
            except IndexError:
                floorsize   = "#NA"
            
            floorsize1.append(floorsize)    
           
            num += 1
            
        num = 0
        page += 1
        
        # Saving all the data into Cheras_HomeTrovit_raw.xls file
        
        cols = ['Title', 
                'Address or Zone', 
                'Property Details',
                'Url', 
                'Image', 
                'Source Info', 
                'Source Date or Published Date (Days)', 
                'Price',
                'No of Bedroom Available', 
                'Floor Size or Property Size sq. feet']

        dataframe = pd.DataFrame({'Title': title1,
                                  'Address or Zone': address1,
                                  'Property Details': detail1,
                                  'Url': url1,
                                  'Image': image1,
                                  'Source Info': source_info1,
                                  'Source Date or Published Date (Days)': source_date1,
                                  'Price': price1,
                                  'No of Bedroom Available': nofbedroom1,
                                  'Floor Size or Property Size sq. feet': floorsize1})[cols]

        dataframe.to_excel('Cheras_HomeTrovit_raw.xls')
        