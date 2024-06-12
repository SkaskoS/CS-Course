
import os
import pandas as pd
import datetime
import numpy as np



class Calculations:
    def __init__(self, files):
        self.trips = self.produce_trips_table(files)
        self.daily_counts = self.calculate_daily_counts(self.get_trips())
        self.monthly_counts = self.calculate_monthly_counts(self.get_trips())
    
    def get_trips(self):
        
        return self.trips

    def get_daily_counts(self):
        return self.daily_counts

    def get_monthly_counts(self):
        return self.monthly_counts
    

    def produce_trips_table(self, files):
        # DataFrame must have at least the 'Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id' columns
        
        trips = pd.concat([pd.read_csv(file) for file in files], ignore_index = True)
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        return trips[['Bikeid', 'Starttime', 'From station id', 'To station id']]
     
    
    
    
    def calculate_daily_counts(self, trips):
        # DataFrame must have "month", "station_id", "fromCNT", "toCNT" and "rebalCNT" columns
        
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')

        # Calculate counts for trips from each station on each day
        from_CNT = trips.groupby(['day', 'From station id'], as_index = False)['Bikeid'].count()
        from_CNT.columns = ['day', 'station_id', 'fromCNT']

        # Calculate counts for trips to each station on each day
        to_CNT = trips.groupby(['day', 'To station id'], as_index = False)['Bikeid'].count()
        to_CNT.columns = ['day', 'station_id', 'toCNT']

        # Merge the DataFrames
        from_to = from_CNT.merge(to_CNT, how = 'outer', on = ['day', 'station_id'])
        from_to = from_to.fillna(0).sort_values(by=['day', 'station_id'])

        # Calculate rebalancing 
        from_to['rebalCNT'] = abs(from_to['fromCNT'] - from_to['toCNT'])

        # Convert counts to integers
        from_to[['station_id', 'fromCNT', 'toCNT', 'rebalCNT']] = from_to[['station_id', 'fromCNT', 'toCNT', 'rebalCNT']].astype(int)

        # Return the DataFrame 
        return from_to[['day', 'station_id', 'fromCNT', 'toCNT', 'rebalCNT']]
          
        
        


        
    def calculate_monthly_counts(self, trips):
        # DataFrame must have "month", "station_id", "fromCNT", "toCNT" and "rebalCNT" columns
        
        trips['Starttime'] = pd.to_datetime(trips['Starttime'])
        trips['month'] = trips['Starttime'].dt.strftime('%m/%Y')
    
        # Calculate counts for trips from each station in each month
        from_CNT = trips.groupby(['month', 'From station id'], as_index = False)['Bikeid'].count()
        from_CNT.columns = ['month', 'station_id', 'fromCNT']
    
        # Calculate counts for trips to each station in each month
        to_CNT = trips.groupby(['month', 'To station id'], as_index = False)['Bikeid'].count()
        to_CNT.columns = ['month', 'station_id', 'toCNT']
    
        # Merge the DataFrames
        from_to = from_CNT.merge(to_CNT, how = 'outer', on = ['month', 'station_id'])
        from_to = from_to.fillna(0).sort_values(by = ['month', 'station_id'])
    
        # Calculate rebalancing counts
        from_to['rebalCNT'] = abs(from_to['fromCNT'] - from_to['toCNT'])
    
        # Convert counts to integers
        from_to[['station_id', 'fromCNT', 'toCNT', 'rebalCNT']] = from_to[['station_id', 'fromCNT', 'toCNT', 'rebalCNT']].astype(int)
    
        # Return the DataFrame
        return from_to[['month', 'station_id', 'fromCNT', 'toCNT', 'rebalCNT']] 





if __name__ == "__main__":
    calculations = Calculations(['HealthyRideRentals2021-Q1.csv', 'HealthyRideRentals2021-Q2.csv', 'HealthyRideRentals2021-Q3.csv'])
    print("-------------- Trips Table ---------------")
    print(calculations.get_trips().head(10))
    print()
    print("-------------- Daily Counts ---------------")
    print(calculations.get_daily_counts().head(10))
    print()
    print("------------- Monthly Counts---------------")
    print(calculations.get_monthly_counts().head(10))
    print()