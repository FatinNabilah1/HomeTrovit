# -*- coding: utf-8 -*-
"""
Created on Sat Nov 2 2019
Author: WQD190011

transformation and cleaning process

"""

import pandas as pd
import numpy as np

num = 0

dataframe = pd.read_csv(r'D:\GitHub\WXD7005\HomeTrovit\data extraction\Cheras_HomeTrovit_raw.csv')
dataframe_clean = dataframe

#Replace "MYR" in the "Price" column value
dataframe_clean['price'] = dataframe_clean['price'].str.replace('MYR', '')
#Convert “Price” to numeric values
dataframe_clean['price'] = pd.to_numeric(dataframe_clean['price'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['price'], inplace=True)

#Convert “No of Bedroom Available” to numeric values
dataframe_clean['no_of_bedroom'] = pd.to_numeric(dataframe_clean['no_of_bedroom'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['no_of_bedroom'], inplace=True)

#Convert “Floor Size or Property Size sq. feet” to numeric values
dataframe_clean['property_size'] = pd.to_numeric(dataframe_clean['property_size'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['property_size'], inplace=True)

#Reassign the Zone
a = dataframe_clean['location']
cheras = a.str.contains('Cheras')
kuala_lumpur = a.str.contains('Kuala Lumpur')
selangor = a.str.contains('Selangor')
dataframe_clean['location'] = pd.np.where(cheras, 'Cheras',
                                               pd.np.where(kuala_lumpur, 'Kuala Lumpur',
                                                        pd.np.where(selangor, 'Selangor','')))

#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean['location'].replace('', np.nan, inplace=True)
dataframe_clean.dropna(subset=['location'], inplace=True)
 
#get the Price per sq. feet
dataframe_clean['price_per_square'] = dataframe_clean['price'] / dataframe_clean['property_size']


#drop unneccessary attributes ; 'Url', 'Image', 'Source Info'
dataframe_clean.drop(['url', 'image', 'source_info'], axis=1, inplace=True)

#filter for data property size < 3000 sq feet and price < 2000000
#other remove from dataframe
#other data is irrelevant and lack of data for size > 3000 sq feet and price > 2000000
dataframe_clean = dataframe_clean[dataframe_clean['property_size'] < 3000]
dataframe_clean = dataframe_clean[dataframe_clean['price'] < 2000000]
dataframe_clean.reset_index(inplace=True, drop=True)

#drop duplicate data
dataframe_clean.drop_duplicates(keep=False, inplace=True)

##Save clean data to csv file
dataframe_clean.to_csv('Cheras_HomeTrovit_clean.csv', index=False)