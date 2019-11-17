# -*- coding: utf-8 -*-
"""
Created on Sun Sept 29 2019
Author: WQD190011

Home Trovit
Cheras
min 100k
floor size > 500 sq

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

r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/sug.0/isUserSearch.1/origin.2/order_by.relevance/city.Cheras/price_min.100000/rooms_min.1/area_min.500/property_type.Apartment/')
soup = bs4.BeautifulSoup(r.text,'html.parser')

##retrieve and set the total page number        
total_item = soup.find('div',{'class':'results-counter js-results-counter'}).find('span').text
total_item = int(total_item.replace(',',''))
total_page = math.ceil(total_item/25)

if total_page > 100:
   total_page = 100

#start loop
#loop per page number
while page <= total_page:
        r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.2/price_min.100000/rooms_min.1/bathrooms_min.0/property_type.Apartment/city.Cheras/area_min.500/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.'+str(page))
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
                title = title.replace(',','')
            except IndexError:
                title = "#NA"
            title1.append(title)
            
            # Address or Zone
            try:
                address = soup.find_all('div',{'class':'details'})[num].find('span').text
                address = address.replace(',','')    
            except IndexError:
                address = "#NA"
            address1.append(address)
            
            # Property Details
            try:
                detail = soup.find_all('div',{'class':'description'})[num].find('p').text
                detail = detail.replace(',','')
            except IndexError:
                detail = "#NA"
            detail1.append(detail)
            
            # URL
            try:
                url = soup.find_all('a',{'class':'js-item-title'})[num].get('href')
                url = url.replace(',','')
            except IndexError:
                url = "#NA"
            url1.append(url)
            
            # Image
            try:
                image   = soup.find_all(itemprop="image")[num].get("src")
                image = image.replace(',','')
            except IndexError:
                image   = "#NA"
            image1.append(image)
            
            # Source Info
            try:
                source_info = soup.find_all('small',{'class':'source'})[num].text
                source_info = source_info.replace(',','')
            except IndexError:
                source_info = "#NA"
            source_info1.append(source_info)
            
            # Source Date or Published Date
            try:
                source_date = soup.find_all('small',{'class':'date'})[num].text
                source_date = source_date.replace(',','')
                source_date = source_date.replace('+','')
                source_date = source_date.replace('days ago','')  
                source_date = source_date.replace(' ','') 
            except IndexError:
                source_date = "#NA"
            source_date1.append(source_date)
            
            # Price
            try:
                price = soup.find_all('div',{'class':'price'})[num].find('span').text
                price = price.replace(',','')
            except IndexError:
                price = "#NA"
            price1.append(price)
            
            # No of Bedroom Available
            try:
                nofbedroom  = soup.find_all(itemprop="numberOfRooms")[num].text
                nofbedroom = nofbedroom.replace(',','')
            except IndexError:
                nofbedroom = "#NA"
            nofbedroom1.append(nofbedroom)
            
            # Floor Size or Property Size
            try:
                floorsize   = soup.find_all(itemprop="floorSize")[num].get("content")
                floorsize = floorsize.replace(',','')
            except IndexError:
                floorsize   = "#NA"
            
            floorsize1.append(floorsize)    
           
            num += 1
            
        num   = 0
        page += 1
        
        # Saving all the data into Cheras_HomeTrovit_raw.xls file
        
        cols = ['title', 
                'location', 
                'property_details',
                'url', 
                'image', 
                'source_info', 
                'published_days', 
                'price',
                'no_of_bedroom', 
                'property_size']

        dataframe = pd.DataFrame({'title': title1,
                                  'location': address1,
                                  'property_details': detail1,
                                  'url': url1,
                                  'image': image1,
                                  'source_info': source_info1,
                                  'published_days': source_date1,
                                  'price': price1,
                                  'no_of_bedroom': nofbedroom1,
                                  'property_size': floorsize1})[cols]

        dataframe.to_csv('Cheras_HomeTrovit_raw.csv', index=False)
        