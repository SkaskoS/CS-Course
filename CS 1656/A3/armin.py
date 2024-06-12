from collections import defaultdict
from pandas import Series, DataFrame
import itertools as it
import pandas as pd
import math
import csv
import sys
import argparse
import collections
import glob
import os
import re
import requests
import string
import sys

class Armin():
    
    def apriori(self, input_filename, output_filename, min_support_percentage, min_confidence):
        """
        Implement the Apriori algorithm, and write the result to an output file

        PARAMS
        ------
        input_filename: String, the name of the input file
        output_filename: String, the name of the output file
        min_support_percentage: float, minimum support percentage for an itemset
        min_confidence: float, minimum confidence for an association rule to be significant

        """
        # Read data from the input file
        transactions, distinct_items = self.read_file(input_filename)
        
        # Find frequent itemsets and their support values
        frequent_itemsets, support = self.frequent_itemsets(transactions, distinct_items, min_support_percentage)
        
        # Write the obtained results to the output file
        self.write_output(output_filename, frequent_itemsets, support, min_confidence)

    def read_file(self, input_filename):
       
        # Create data list and unique items set
        data = []
        unique_items = set()
        
        # Input file
        with open(input_filename, newline='') as csvfile:
            for row in csv.reader(csvfile):
                
                # Convert the row into a set of itmes and append to a list
                items = set(row[1:])
                data.append(items)
                
                # Update the unique_items set with the items 
                unique_items.update(items)
                
        # Return the collected data and sorted unique items
        return data, sorted(unique_items)
    
    def frequent_itemsets(self, transactions, unique_items, min_support_percentage):
        
        # Empty list to store frequent itemsets
        frequent_itemsets = []
        
        # Create an empty dictionary to store support values
        support_dict = {}
    
        for i in range(len(unique_items) + 1):
            
            # Generate combinations of unique items
            for j in it.combinations(unique_items, i + 1):
                
                item_combination = set(j)
                
                # Counter for the number of occurrences
                count = 0
                
                for transaction in transactions:
                    
                    # Check if the item combination is a subset of the transaction
                    if item_combination.issubset(transaction):
                        
                        # Count if the item combination is found
                        count += 1
                        
                # Calculate the support for the itemset
                support = count / len(transactions)
                
                
                
                # If support is greater than or equal to the min support percentage
                if support >= min_support_percentage:
                    
                    # Append itemset to the frequent itemsets list
                    frequent_itemsets.append(sorted(item_combination))
                    
                    # Store the support values for the itemset into the dictionary 
                    support_dict[frozenset(item_combination)] = support
    
        # Returning the list of frequent itemsets and the support values
        return frequent_itemsets, list(support_dict.values())
    
    def association_rules(self, itemset, frequent_itemsets, support, min_confidence):
       
            rules = []
            support_dict = {}
        
        

            # Create a dictionary for the frequent itemsets
            for i, item in enumerate(frequent_itemsets):
                
                support_dict[frozenset(item)] = i
        
            # Applying association rules
            for item in frequent_itemsets:
                
                itemset_index = support_dict[frozenset(item)]
        
                for i in range(1, len(item)):
                    for antecedent in it.combinations(item, i):
                        
                        antecedent_set = set(antecedent)
                        consequent_set = frozenset(item) - antecedent_set
        
                        # Calculate support and confidence
                        antecedent_set_support = support[support_dict[frozenset(antecedent_set)]]
                        itemset_support = support[itemset_index]
        
                        confidence = itemset_support / antecedent_set_support
        
                        # Check if the confidence meets the requirements            
                        if confidence >= min_confidence:
                            
                            antecedent_list = ', '.join(sorted(map(str, antecedent_set)))
                            consequent_list = ', '.join(sorted(map(str, consequent_set)))

                            # Construct the rule as a list
                            rule_output = ['R',f"{itemset_support:.4f}",f"{confidence:.4f}",''.join(antecedent_list),"'=>'",''.join(consequent_list)]

                            # Append the rule to the list of rules
                            rules.append((rule_output))

                            
            return rules

   
    def write_output(self, output_filename, frequent_itemsets, support, min_confidence):
      
      with open(output_filename, "w", newline="") as csvfile:
          
            writer = csv.writer(csvfile)


            # Writing frequent itemsets to the file
            for i in range(len(frequent_itemsets)):
                
                itemset = frequent_itemsets[i]
                support_items = support[i]
                row = ['S'] + [f'{support_items:.4f}'] + sorted(itemset)
                writer.writerow(row)

                
            # Writing association rules to the file            
            rules = self.association_rules(itemset, frequent_itemsets, support, min_confidence)
           
            for rule in rules:
                
                writer.writerow(rule)

                    
if __name__ == "__main__":
    armin = Armin()
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.7.csv', 0.5, 0.7)
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.8.csv', 0.5, 0.8)
    armin.apriori('input.csv', 'output.sup=0.6,conf=0.8.csv', 0.6, 0.8)
