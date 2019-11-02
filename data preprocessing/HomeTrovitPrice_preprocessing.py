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
dataframe_clean['Price'] = dataframe_clean['Price'].str.replace('MYR', '')
#Convert “Price” to numeric values
dataframe_clean['Price'] = pd.to_numeric(dataframe_clean['Price'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['Price'], inplace=True)

#Convert “No of Bedroom Available” to numeric values
dataframe_clean['No of Bedroom Available'] = pd.to_numeric(dataframe_clean['No of Bedroom Available'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['No of Bedroom Available'], inplace=True)

#Convert “Floor Size or Property Size sq. feet” to numeric values
dataframe_clean['Size sq. feet'] = pd.to_numeric(dataframe_clean['Floor Size or Property Size sq. feet'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['Floor Size or Property Size sq. feet'], inplace=True)

#Reassign the Zone
a = dataframe_clean['Address or Zone']
cheras = a.str.contains('Cheras')
kuala_lumpur = a.str.contains('Kuala Lumpur')
selangor = a.str.contains('Selangor')
dataframe_clean['Address or Zone'] = pd.np.where(cheras, 'Cheras',
                                               pd.np.where(kuala_lumpur, 'Kuala Lumpur',
                                                        'Selangor'))

#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['Address or Zone'], inplace=True)

#get the Price per sq. feet
dataframe_clean['Price/sq. feet'] = dataframe_clean['Price'] / dataframe_clean['Floor Size or Property Size sq. feet']


#drop unneccessary attributes ; 'Url', 'Image', 'Source Info'
dataframe_clean.drop(['Url', 'Image', 'Source Info'], axis=1, inplace=True)
dataframe_clean.drop(dataframe_clean.columns[0], axis=1, inplace=True)

#filter for data property size < 3000 sq feet and price < 2000000
#other remove from dataframe
dataframe_clean = dataframe_clean[dataframe_clean['Floor Size or Property Size sq. feet'] < 3000]
dataframe_clean = dataframe_clean[dataframe_clean['Price'] < 2000000]
dataframe_clean.reset_index(inplace=True, drop=True)

#drop duplicate data
dataframe_clean.drop_duplicates(keep=False, inplace=True)

##Save clean data to csv file
dataframe_clean.to_csv('Cheras_HomeTrovit_clean.csv')