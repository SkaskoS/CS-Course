
import argparse
import collections
import csv
import json
import glob
import math
import os
import pandas
import re
import requests
import string
import sys
import time
import xml

class Bike():
    def __init__(self, baseURL, station_info, station_status):
        # initialize the instance
        pass
    
        self.baseURL = baseURL
        self.info = baseURL+'/station_information.json'
        self.status = baseURL+'/station_status.json'
        

    #WORKS  
    def total_bikes(self):
        # return the total number of bikes available
        
        station_stat = requests.get(self.status).json()


        total_bikes = 0
        
        for data in station_stat['data']['stations']:
            total_bikes += data.get('num_bikes_available')
        
        return total_bikes
        
    #WORKS
    def total_docks(self):
        # return the total number of docks available
        
        station_stat = requests.get(self.status).json()

        total_docks = 0
        
        #gets list of data from info
        for data in station_stat['data']['stations']:
            total_docks += data.get('num_docks_available')
        
        return total_docks
    
    #WORKS
    def percent_avail(self, station_id):
        # return the percentage of available docks
        station_stat = requests.get(self.status).json()
        
        #gets list of data from info
        for data in station_stat['data']['stations']:
            #get data  to check if equal to id where we convert to a string
            if data['station_id'] == str(station_id):
      
        
   
                stat_docks = data['num_docks_available']
                stat_bikes = data['num_bikes_available']
         
                
            
                percent = ( stat_docks / (stat_docks + stat_bikes) ) * 100              
                
                return str(int(percent)) + "%"
            
        return ''
        
    #WORKS
    def closest_stations(self, latitude, longitude):
        # return the stations closest to the given coordinates
        station_info = requests.get(self.info).json()
        
        #store info on distances from location
        empty_dis = []
        #store info on distances
        closest = {}

        #gets list of data from info
        for data in station_info['data']['stations']:
            
 
            #call from distance method
            distance = self.distance(latitude, longitude, data['lat'], data['lon'])
            
            #add distance + info
            empty_dis.append((data['station_id'], data['name'], distance))
            
        #sorting info based on distance from location by getting elements
        empty_dis.sort(key = lambda x: x[2])
            
        #three closest
        for data in empty_dis[:3]:
            
            #Data closest we will take into the empty data, 
            #[#] = first element in statation_id, name
            #took from one library of data and put it in another to output the data we want
            closest[data[0]] = data[1]
            
        return closest

    
    #WORKS
    def closest_bike(self, latitude, longitude):
         # return the station with available bikes closest to the given coordinates
         station_info = requests.get(self.info).json()
         
         empty_dis = []
         
         #gets list of data from info
         for data in station_info['data']['stations']:
             
  
             #call from distance method
             distance = self.distance(latitude, longitude, data['lat'], data['lon'])
             
             #add distance + info
             empty_dis.append((data, distance))
             
         #sorting info based on distance from location by getting elements
         empty_dis.sort(key = lambda x: x[1])
             
         #return closest and getting data for first 0,0
         closest = empty_dis[0][0]

         return {closest['station_id']: closest['name']}

    #WORKS     
    def station_bike_avail(self, latitude, longitude):
        # return the station id and available bikes that correspond to the station with the given coordinates
        stat_info = requests.get(self.info).json()
        stat_stat = requests.get(self.status).json()

        #gets list of data from info
        for data in stat_info['data']['stations']:
            #checking if data coods match with latitude and longitude
            if latitude == data['lat'] and longitude == data['lon']:
                #get the num_bikes_available data to result
                for result in stat_stat['data']['stations']:
                    #get the corresponding data
                    if data['station_id'] == result['station_id']:
                        
                        
                        return {data['station_id']: result['num_bikes_available']}
        
        return {}

    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
        return 12742 * math.asin(math.sqrt(a))


# testing and debugging the Bike class

if __name__ == '__main__':
    instance = Bike('https://db.cs.pitt.edu/courses/cs1656/data', '/station_information.json', '/station_status.json')
    print('------------------total_bikes()-------------------')
    t_bikes = instance.total_bikes()
    print(type(t_bikes))
    print(t_bikes)
    print()

    print('------------------total_docks()-------------------')
    t_docks = instance.total_docks()
    print(type(t_docks))
    print(t_docks)
    print()

    print('-----------------percent_avail()------------------')
    p_avail = instance.percent_avail(342885) # replace with station ID
    print(type(p_avail))
    print(p_avail)
    print()

    print('----------------closest_stations()----------------')
    c_stations = instance.closest_stations(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_stations))
    print(c_stations)
    print()

    print('-----------------closest_bike()-------------------')
    c_bike = instance.closest_bike(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_bike))
    print(c_bike)
    print()

    print('---------------station_bike_avail()---------------')
    s_bike_avail = instance.station_bike_avail(40.445834, -79.954707) # replace with exact latitude and longitude of station
    print(type(s_bike_avail))
    print(s_bike_avail)
