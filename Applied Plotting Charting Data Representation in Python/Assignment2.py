
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Fairfax, Virginia, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

#leaflet_plot_stations(400,'921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47')


# In[2]:

binsize = 400
hashid = '921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47'


# In[13]:

df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(400))
station_locations_by_hash = df[df['hash'] == hashid]

lons = station_locations_by_hash['LONGITUDE'].tolist()
lats = station_locations_by_hash['LATITUDE'].tolist()

station_locations_by_hash.shape


# In[4]:

data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/921a697d63e17c1cb86364faf0d309c7fe078fabf6f3e24be2cefa47.csv')
#data['Data_Value'] = data['Data_Value']/10.0
data.head()


# In[95]:

data['year'] = data['Date'].apply(lambda x: x[:4])
data['dayinyear'] = data['Date'].apply(lambda x: x[5:])
dates = data['dayinyear'].unique()
dates.sort()
data = data.sort(['dayinyear', 'year'])
data = data[data['dayinyear'] != '02-29']
data.head()


# In[96]:

data_14 = data[data['year']!= '2015']
data_15 = data[data['year'] == '2015']


# In[97]:

min_df = data_14[data_14['Element'] == 'TMIN']
max_df = data_14[data_14['Element'] == 'TMAX']


# In[126]:

min_14 = min_df.groupby('dayinyear')['Data_Value'].min()/10
max_14 = max_df.groupby('dayinyear')['Data_Value'].max()/10


# In[99]:

min_15_df = data_15[data_15['Element'] == 'TMIN']
max_15_df = data_15[data_15['Element'] == 'TMAX']


# In[127]:

min_15 = min_15_df.groupby('dayinyear')['Data_Value'].min()/10
max_15 = max_15_df.groupby('dayinyear')['Data_Value'].max()/10


# In[157]:

min_broken = min_15 < min_14
max_broken = max_15 > max_14


# In[166]:

min_broken_ind = np.where(min_broken)[0]
max_broken_ind = np.where(max_broken)[0]


# In[206]:

plt.figure(figsize=(20,10))
plt.plot(min_14.values, c='steelblue', label='daily minimum temperature from 2005-2014')
plt.plot(max_14.values, c='darkorange', label='daily maximum temperature from 2005-2014')
plt.scatter(list(min_broken_ind), min_15[min_broken_ind], c='darkblue', s=15, label='break record low temperature in 2015')
plt.scatter(list(max_broken_ind), max_15[max_broken_ind], c='red', s=15, label='break record high temperature in 2015')
plt.gca().fill_between(range(len(min_14)), min_14.values, max_14.values, facecolor='green', alpha=0.4)
plt.xticks(range(0, len(min_14), 10), min_14.index[range(0, len(min_14), 10)], rotation=45)
plt.yticks(range(-25, 45, 5))
plt.xlabel('Day in years')
plt.ylabel('Temperature (Celcius)')
plt.title('Temperature summary over 10 years near Fairfax, Virginia')
plt.legend(loc=2, bbox_to_anchor=(0.01, 0.95))
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().tick_params('y', length=0)
for y in range(-25, 45, 5):
    plt.axhline(y=y, c='purple', alpha=0.2)
plt.savefig('assignment2-fig.jpg')

