# -*- coding: utf-8 -*-
"""
Created on Sat Nov 2 2019
Author: WQD190011

transformation and cleaning process

"""

import pandas as pd

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
dataframe_clean['Floor Size or Property Size sq. feet'] = pd.to_numeric(dataframe_clean['Floor Size or Property Size sq. feet'], errors='coerce')
#remove a row or a column from a dataframe which has a NaN or no values in it
dataframe_clean.dropna(subset=['Floor Size or Property Size sq. feet'], inplace=True)

#drop unneccessary attributes ; 'Url', 'Image', 'Source Info'
dataframe_clean.drop(['Url', 'Image', 'Source Info'], axis=1, inplace=True)
dataframe_clean.drop(dataframe_clean.columns[0], axis=1, inplace=True)

#get the Price per sq. feet
dataframe_clean['Price/sq. feet'] = dataframe_clean['Price'] / dataframe_clean['Floor Size or Property Size sq. feet']

##Save clean data to csv file
dataframe_clean.to_csv('Cheras_HomeTrovit_clean.csv')