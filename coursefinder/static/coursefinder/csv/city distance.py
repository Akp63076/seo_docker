
#Distance calculated using Google API
import googlemaps
import pandas as pd

# df = pd.read_excel('C:/Users/Lenovo/Downloads/study_abroad_colleges.xlsx') #loading the file
# df1 = df.drop_duplicates(subset = ["City"])  #dropping duplicates
df1 = pd.read_csv('E:/flask_project/seoTool/coursefinder/static/coursefinder/csv/city_list.csv')
cities_list = ['Montreal','Vancouver','Toronto','Ottawa','Quebec City']  #The destination cities list
df3 = pd.DataFrame(columns=['City' , 'Montreal', 'Toronto', 'Vancouver','Ottawa', 'Quebec City']) #Final Dataframe


for i in df1.index:  
    city = df1['City'][i]
    origin = df1['City'][i] + ', canada'
    for j in cities_list:
        destination = j + ', canada'

        gmaps = googlemaps.Client(key='AIzaSyBFR5BVrw04B-KdOBNNnBdpH5zWjsrVjK4')
        my_dist = gmaps.distance_matrix(origin,destination)['rows'][0]['elements'][0]
        
        #If the googlemaps api couldnt calculate the distance. 
        if my_dist['status'] != 'OK':
            print('Distance not available between ',origin,' and ',destination)
            continue
        
        
        if j == 'Montreal':
            mon = my_dist['distance']['value']/1000
        elif j == 'Toronto':
            tor = my_dist['distance']['value']/1000
        elif j == 'Vancouver':
            van = my_dist['distance']['value']/1000
        elif j == 'Ottawa':
            ott = my_dist['distance']['value']/1000
        elif j == 'Quebec City':
            que = my_dist['distance']['value']/1000
            
    df3 = df3.append({'City' : city, 'Montreal' : mon, 'Toronto' : tor, 'Vancouver' : van, 'Ottawa': ott, 'Quebec City' : que}, ignore_index = True)

df3.to_csv('e:/flask_project/seoTool/coursefinder/static/coursefinder/csv/DistanceDataFinal_new.csv')

