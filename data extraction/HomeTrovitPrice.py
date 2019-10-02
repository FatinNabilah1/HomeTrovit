# -*- coding: utf-8 -*-
"""
Created on Sun Sept 29 2019
Author: WQD190011

Home Trovit
Aparment Only
price 400k to 500k
2 bedrooms only
Cheras Only

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
source_info1 = []
source_date1 = []
price1       = []
nofbedroom1  = []
floorsize1   = []

num         = 0
page        = 0
total_page  = 0

r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/sug.0/isUserSearch.1/origin.2/order_by.relevance/city.Cheras/price_min.400000/price_max.500000/rooms_min.2/property_type.Apartment/')
soup = bs4.BeautifulSoup(r.text,'xml')

##retrieve the total page number        
total_page = soup.find('div',{'class':'results-counter js-results-counter'}).find('span').text
total_page = int(total_page.replace(',',''))

#start loop

for page in range(0,total_page):
        r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.2/price_min.400000/price_max.500000/rooms_min.2/bathrooms_min.0/property_type.Apartment/city.Cheras/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.'+str(math.ceil((page+1)/25)))
        
        soup = bs4.BeautifulSoup(r.text,'xml')
        
        #checking 25 item per page
        if num < 25:
           num
           
        else:
            num = 0
            
        
        ## retrieving of the data
        
        # Title
        try:
            title = soup.find_all('a',{'class':'js-item-title'})[num].text
        except IndexError:
            title = "#NA"
        title1.append(title)
        
        # Address or Zone
        address     = soup.find_all('div',{'class':'details'})[num].find('span').text
        address1.append(address)
        
        # Property Details
        detail      = soup.find_all('div',{'class':'description'})[num].find('p').text
        detail1.append(detail)
        
        # URL
        url = soup.find_all('a',{'class':'js-item-title'})[num].get('href')
        url1.append(url)
        
        # Source Info
        source_info = soup.find_all('small',{'class':'source'})[num].text
        source_info1.append(source_info)
        
        # Source Date or Published Date
        source_date = soup.find_all('small',{'class':'date'})[num].text
        source_date1.append(source_date)
        
        # Price
        price       = soup.find_all('div',{'class':'price'})[num].find('span').text
        price1.append(price)
        
        # No of Bedroom Available
        if soup.find_all('div',{'class':'property'})[num].find('span') is not None:
            nofbedroom  = soup.find_all('div',{'class':'property'})[num].find('span').text
        else:
            nofbedroom = "#NA"
        nofbedroom1.append(nofbedroom)
        
        # Floor Size or Property Size
       
        try:
            floorsize   = soup.find_all(itemprop="floorSize")[num].get("content")
        except IndexError:
            floorsize = "#NA"
        floorsize1.append(floorsize)    
        
        num += 1
       
        # Saving all the data into Cheras_HomeTrovit_raw.xls file
        
        cols = ['Title', 
                'Address or Zone', 
                'Property Details',
                'Url', 
                'Source Info', 
                'Source Date or Published Date', 
                'Price',
                'No of Bedroom Available', 
                'Floor Size or Property Size']

        dataframe = pd.DataFrame({'Title': title1,
                                  'Address or Zone': address1,
                                  'Property Details': detail1,
                                  'Url': url1,
                                  'Source Info': source_info1,
                                  'Source Date or Published Date': source_date1,
                                  'Price': price1,
                                  'No of Bedroom Available': nofbedroom1,
                                  'Floor Size or Property Size': floorsize1})[cols]

        dataframe.to_excel('Cheras_HomeTrovit_raw.xls')