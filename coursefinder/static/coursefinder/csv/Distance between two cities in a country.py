#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''Code to get distance to major cities in a country'''

import googlemaps
import pandas as pd

#Major cities in a counrty
major_cities = {'canada' : ['Montreal','Vancouver','Toronto','Ottawa','Quebec City'],                
            'uk' : ['London', 'Edinburgh','Manchester', 'Birmingham', 'Glasgow']}
#List of cities in a country
cities_list = {'canada' : [], 'uk' : [], }

country = 'canada'

df = pd.DataFrame(columns = major_cities[country], index = cities_list[country])

for i in cities_list[country]:
    destination = i + ', ' + country
    for j in major_cities[country]:
        origin = j+ ', ' + country
        
        gmaps = googlemaps.Client(key='AIzaSyBFR5BVrw04B-KdOBNNnBdpH5zWjsrVjK4')
        my_dist = gmaps.distance_matrix(origin,destination)['rows'][0]['elements'][0]
        
        if my_dist['status'] != 'OK':
            distance = 'N/A'
        
        distance = my_dist['distance']['value']/1000
        
        df[j][i] = distance
        
        
df.to_excel('DistanceDataFinal.xlsx')
      


# In[ ]:




