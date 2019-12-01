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
newprice1       = []
oldprice1       = []
nofbedroom1  = []
nofbathroom1 = []
floorsize1   = []
typeProperty1 = []

num         = 0
num1        = 1
page        = 1
total_page  = 0
total_item  = 0
no_propertylist = 1

propertyType = ["Apartment","Bungalow","Condo","House","Plex"]

#start loop
#loop per propertyhouse
while no_propertylist <= len(propertyType):
    r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/sug.0/isUserSearch.1/origin.2/order_by.source_date/price_min.100000/rooms_min.1/bathrooms_min.1/area_min.500/property_type.'+propertyType[no_propertylist-1]+'/decrease_price.true/')
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
            r    = requests.get('https://homes.trovit.my/index.php/cod.search_homes/type.1/what_d.kuala%20lumpur/origin.2/price_min.100000/rooms_min.1/bathrooms_min.1/property_type.'+propertyType[no_propertylist-1]+'/decrease_price.1/area_min.500/order_by.source_date/resultsPerPage.25/isUserSearch.1/page.'+str(page))
            soup = bs4.BeautifulSoup(r.text,'xml')
            
            if total_page > 1:
                nofitem = 25
            else:
                nofitem = total_item
            
            #second loop
            #loop per item number     
            while num < nofitem:
                
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
                    newprice = soup.find_all('span', {'class' : 'amount'})[num].text
                    newprice = newprice.replace(',','')
                except IndexError:
                    newprice = "#NA"
                newprice1.append(newprice)
                
                # Price
                try:
                    oldprice = soup.find_all('span', {'class' : 'price-old'})[num].text
                    oldprice = oldprice.replace(',','')
                except IndexError:
                    oldprice = "#NA"
                oldprice1.append(oldprice)
                
                # No of Bedroom Available
                try:
                    nofbedroom  = soup.find_all(itemprop="numberOfRooms")[num].text
                    nofbedroom = nofbedroom.replace(',','')
                except IndexError:
                    nofbedroom = "#NA"
                nofbedroom1.append(nofbedroom)
                
                
                # No of Bathroom Available
                try:
                    if(num1 == 1):
                        num1 = 1
                    else:
                        num1 = num1 + 2
                    nofbathroom  = soup.find_all('div',{'class':'property'})[num1].find('span').text
                    nofbathroom = nofbathroom.replace(',','')
                    nofbathroom = nofbathroom.replace(' br','')
                except IndexError:
                    nofbathroom = "#NA"
                nofbathroom1.append(nofbathroom)
                
                # Floor Size or Property Size
                try:
                    floorsize   = soup.find_all(itemprop="floorSize")[num].get("content")
                    floorsize = floorsize.replace(',','')
                except IndexError:
                    floorsize   = "#NA"
                floorsize1.append(floorsize)    
                
                typeProperty = propertyType[no_propertylist-1]
                typeProperty1.append(typeProperty)  
                
                num += 1
                num1 += 1
                
            num   = 0
            num1  = 1
            page += 1
    num   = 0
    num1  = 1
    page  = 1        
    no_propertylist += 1
    
    # Saving all the data into Cheras_HomeTrovit_raw.xls file
        
cols = ['title', 
            'location', 
            'property_details',
            'url', 
            'image', 
            'source_info', 
            'published_days', 
            'newprice',
            'oldprice',
            'no_of_bedroom', 
            'no_of_bathroom', 
            'property_size', 
            'property_type']

dataframe = pd.DataFrame({'title': title1,
                              'location': address1,
                              'property_details': detail1,
                              'url': url1,
                              'image': image1,
                              'source_info': source_info1,
                              'published_days': source_date1,
                              'newprice': newprice1,
                              'oldprice': oldprice1,
                              'no_of_bedroom': nofbedroom1,
                              'no_of_bathroom': nofbathroom1,
                              'property_size': floorsize1,
                              'property_type': typeProperty1})[cols]

dataframe.to_csv('HomeTrovit_pricechange_raw.csv', index=False)
        