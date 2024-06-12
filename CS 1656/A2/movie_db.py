import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml


class Movie_db(object):
    def __init__(self, db_name):
        #db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()
    
    #q0 is an example 
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #WORKS
    def q1(self):
        query = '''
        
        SELECT act.fname, act.lname
        FROM Actors AS act, Cast AS cas, Cast AS cas1, Movies AS mov, Movies AS mov1
        
        -- Filtering for movies after or on 2000 
        WHERE mov.year >= 2000
        
        -- Joining tables
        AND act.aid = cas.aid
        AND cas.mid = mov.mid
        
        -- Comparing actors to the cast then from cast of movies after or on 2000 year
        AND act.aid = cas1.aid
        AND cas1.mid = mov1.mid
        
        -- Filtering for movies between the dates of 1980 and 1990
        AND mov1.year BETWEEN 1980 AND 1990
        ORDER BY act.lname, act.fname
                    
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        
    #WORKS
    def q2(self):
        query = '''
        
    
        SELECT mov1.title, mov1.year
        
        -- mov is of the movies table and mov1 is comparing movies in table to other movies in table with name Rogue One: A Star Wars Story 
        FROM Movies AS mov, Movies AS mov1
        
        -- Filtering for movies that are Rogue One: A Star Wars Story
        WHERE mov.title = 'Rogue One: A Star Wars Story'
        
        -- Selecting moives released in same year as Rogue One: A Star Wars Story 
        AND mov.year = mov1.year
        
        -- Filtering movies with higher rank than Rogue One: A Star Wars Story 
        AND mov.rank < mov1.rank
        
        -- Getting order of the movies from filtered result
        ORDER BY mov1.title
    
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #WORKS
    def q3(self):
        query = '''
        
        SELECT act.fname, act.lname, COUNT(*) as number_of_movies
        FROM Actors AS act,  Cast AS cas, Movies AS mov
        
        -- Filtering for movies only containing the key words Star Wars
        WHERE mov.title LIKE '%Star Wars%'
        
        -- Joining tables
        AND act.aid = cas.aid
        AND cas.mid = mov.mid
        GROUP BY act.lname, act.fname
        ORDER BY number_of_movies DESC, act.lname, act.fname
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #WORKS
    def q4(self):
        query = '''
        
        
        -- DISTINCT is getting one set of all things named the same or are the same
        SELECT DISTINCT act.fname, act.lname
        FROM Actors AS act, Cast AS cas, Movies AS mov
        
        -- Joining tables
        WHERE act.aid = cas.aid
        AND cas.mid = mov.mid 
        
        -- Filtering/Selecting from actors and not in movies
        AND act.aid NOT IN (
            SELECT cas.aid
            FROM Actors AS act, Cast AS cas, Movies AS mov
            WHERE cas.mid = mov.mid
            AND mov.year >= 1990
        )
        ORDER BY act.lname ASC, act.fname ASC
         
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    
    #WORKS
    def q5(self):
        query = '''
        
        SELECT dir.fname, dir.lname, COUNT(*) as number_of_films_directed
        FROM Directors AS dir, Movie_Director as mdir 
        
        -- Joining rows
        WHERE dir.did = mdir.did
        GROUP BY dir.lname, dir.fname
        ORDER BY number_of_films_directed DESC, dir.lname, dir.fname
        
        -- Filtering for ten rows
        LIMIT 10
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #WORKS
    def q6(self):
        query = '''
        
        SELECT mov.title, COUNT(*) as number_of_movies
        FROM Cast AS cas, Movies mov
        
        -- Joining table
        WHERE mov.mid = cas.mid
        GROUP BY mov.title
        ORDER BY number_of_movies DESC, mov.title
        
        -- Filtering for ten rows
        LIMIT 11
    
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    
    #WORKS
    def q7(self):
        query = '''
        
        -- SUM is to add up the actors 
        SELECT mov.title, SUM(act.gender = 'Male') as male, SUM(act.gender = 'Female') AS female
        FROM Actors AS act, Movies mov, Cast AS cas
        
        -- Joining tables together
        WHERE mov.mid = cas.mid
        AND cas.aid = act.aid
        GROUP BY mov.title
        
        -- Filtering for number of males are greater than females in a movie
        HAVING  male > female 
        ORDER BY mov.title
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    
    #WORKS
    def q8(self):
        query = '''
        
        SELECT act.fname, act.lname, COUNT(DISTINCT dir.did) AS number_of_directors
        FROM Directors AS dir, Movie_Director AS mdir, Cast AS cas, Actors AS act 
        
        -- Joining tables 
        WHERE mdir.did = dir.did
        AND act.aid = cas.aid
        AND cas.mid = mdir.mid
        AND mdir.did = dir.did
        
        -- Get rid of actors who are directors
        AND act.aid != dir.did
        GROUP BY act.fname, act.lname
        
        -- Filtering for actors who work with 7 or greater diractors
        HAVING number_of_directors >= 7 
        ORDER BY number_of_directors DESC
    

       
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    #WORKS
    def q9(self):
        query = '''
        
        
        SELECT act.fname, act.lname, COUNT(*) as number_of_actors
        FROM Actors AS act,  Cast AS cas, Movies AS mov
        
        -- Filtering to actors with first names starting with B
        WHERE act.fname LIKE 'B%'
        
        -- Joining tables together with actor id and cast for movies table  
        AND act.aid = cas.aid
        AND cas.mid = mov.mid
        
        -- Selecting the debut year based on actors instead of movie
        AND mov.year IN (
            SELECT MIN(mov.year)
            FROM Movies AS mov, Cast AS cas
            WHERE mov.mid = cas.mid
            AND cas.aid = act.aid
            )
        GROUP BY act.fname, act.lname
        ORDER BY number_of_actors DESC, act.fname, act.lname 
       
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #WORKS 
    def q10(self):
        query = '''
        
        SELECT act.lname, mov.title
        FROM Actors AS act,  Cast AS cas, Movies AS mov, Directors as dir, Movie_Director AS mdir
        
        -- Joining tables 
        WHERE act.lname = dir.lname
        AND act.aid = cas.aid
        AND cas.mid = mov.mid
        AND mdir.did = dir.did
        AND mov.mid = mdir.mid
        
        -- Grouping by the last name of actor and the movie title they played
        GROUP BY act.lname, mov.title
        ORDER BY act.lname ASC, mov.title ASC
        
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q11(self):
        
        # Level one: Selecting bacon himself
        query = '''
        
        DROP VIEW IF EXISTS one
        
        '''
        self.cur.execute(query)
        
        query = '''
        
        CREATE VIEW one AS
        SELECT DISTINCT act.fname, act.lname
        FROM Actors as act, Cast as cas, Movies AS mov
        WHERE act.aid = cas.aid
        AND cas.mid = mov.mid
        AND act.fname = 'Kevin'
        AND act.lname = 'Bacon'
        
        '''
        self.cur.execute(query)
        
        # Level two: Selecting bacons co-actors and who worked alongside him
        query = '''
        
        DROP VIEW IF EXISTS two
        
        '''
        self.cur.execute(query)
        
        query = '''
        
        CREATE VIEW two AS
        SELECT DISTINCT act.fname, act.lname
        FROM Actors as act, Cast as cas, Movies AS mov
        WHERE act.aid = cas.aid
        AND cas.mid = mov.mid
        AND act.aid NOT IN (
           SELECT act.aid 
           FROM one
        )
        
        '''
        self.cur.execute(query)
        
        # Level three: Excluding co-actors of the co-actors 
        query = '''
        
        DROP VIEW IF EXISTS three
        
        '''
        self.cur.execute(query)
        
        query = '''
        
        CREATE VIEW three AS
        SELECT DISTINCT act.fname, act.lname 
        FROM Actors as act, Cast as cas, Movies AS mov
        WHERE act.aid = cas.aid
        AND cas.mid = mov.mid
        AND act.aid NOT IN (
            SELECT act.aid 
            FROM two
        )
        
        '''
        self.cur.execute(query)
        
        # Select actors 
        query = '''
        
        SELECT fname, lname 
        FROM three
        
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
         
    
    #WORKS
    def q12(self):
        query = '''
        
        SELECT act.fname, act.lname, COUNT(*) AS movies, AVG(mov.rank) AS ranking
        FROM Actors AS act, Cast as cas, Movies as mov
        
        -- Joining tables
        WHERE act.aid = cas.aid
        AND cas.mid = mov.mid
        GROUP BY act.fname, act.lname
        ORDER BY ranking DESC
        
        -- Filtering for 20 rows 
        LIMIT 20
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()
