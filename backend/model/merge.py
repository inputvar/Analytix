import re
import pandas as pd
from flask import json
import numpy as np
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import faiss


pf = pd.read_csv('preprosdata.csv')
def merge_columns_to_csv(pf):
    # Initialize an empty list to store the merged values
    merged_values = []

    # Isolate the first column
    first_column = pf.iloc[:, 0]

    # Iterate through rows and merge the data with column names
    for index, row in pf.iloc[:, 1:].iterrows():
        merged_row = ', '.join([f'{col}: {value}' for col, value in row.items()])
        merged_values.append(merged_row)

    # Create a new DataFrame with both the first column and the merged values
    merged_df = pd.DataFrame({'Name': first_column[:len(merged_values)], 'Info': merged_values})

    merged_df.to_csv('finaldata.csv', index=False)

pf = pd.read_csv('preprosdata.csv')
merge_columns_to_csv(pf)
