import re
import pandas as pd
from flask import json
import numpy as np
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import faiss

def gender_features(word):
    if len(word) > 0:
        return {'last_letter': word[-1]}
    else:
        # Return a default feature if the name is empty
        return {'last_letter': 'unknown'}


def preprocessing(df):

    
    df['Name'] = df['Information'].str.extract(r'^(.*?)(?: has \d+ years of experience)')
    df['Experience'] = df['Information'].str.extract(r'(\d+) years of experience')
    df['Experience In'] = df['Information'].str.extract(r'experience in (.+?)\.')
    df['Client Rating'] = df['Information'].str.extract(r'Client Feedback of ([\d.]+) out of 5.0')
    df['Jurisdiction'] = df['Information'].str.extract(r'Jurisdiction is ([\w\s]+)\.')
    df['Pay'] = df['Information'].str.extract(r'charges (\d+\.\d+) USD per hour')
    df['Disposal Days'] = df['Information'].str.extract(r'takes (\d+\.\d+) Avg Days for Disposal')
    df['Languages'] = df['Information'].str.extract(r'speaks: ([\w\s,]+)\.')
    df['Place'] = df['Information'].str.extract(r'practices at ([\w\s\-]+)\,')
    df['City'] = df['Information'].str.extract(r'based in (\w+)')
    df['Pro Bono'] = (~df['Information'].str.contains('not')).astype(int)
    df['Client Demographics'] = df['Information'].str.extract(r'Client Demographics is (.+)')

    # Drop the original column
    df = df.drop(columns=['Information'])
    
    df['Experience In'] = df['Experience In'].str.replace(', and', ',')
    df['Languages'] = df['Languages'].str.replace(' and', ',')
    df[['Field 1', 'Field 2', 'Field 3']] = df['Experience In'].str.split(', ', expand=True)
    df[['Language 1', 'Language 2', 'Language 3']] = df['Languages'].str.split(', ', expand=True)
    
    df.drop(columns = ['Name', 'Experience In', 'Languages'], inplace = True)
    
    df['Client Demographics'] = df['Client Demographics'].str.replace('.', '')

    column_to_round = 'Disposal Days'
    decimal_places = 0  # Set the number of decimal places you want

    df[column_to_round] = pd.to_numeric(df[column_to_round], errors='coerce')  # Convert to numeric
    df[column_to_round] = df[column_to_round].round(decimal_places)
    
    column_to_round_1 = 'Pay'
    decimal_places = 2  # Set the number of decimal places you want

    df[column_to_round_1] = pd.to_numeric(df[column_to_round_1], errors='coerce')  # Convert to numeric
    df[column_to_round_1] = df[column_to_round_1].round(decimal_places)
    

    df['Client Rating'] = pd.to_numeric(df['Client Rating'], errors='coerce')
    if df['Client Rating'].isnull().sum() > 0:
        df = df.fillna(round(df['Client Rating'].mean()))
    
    columns_to_fill = [
        'Jurisdiction',
        'Place',
        'City',
        'Pro Bono',
        'Client Demographics',
        'Field 1',
        'Field 2',
        'Field 3',
        'Language 1',
        'Language 2',
        'Language 3',
    ]

    for column in columns_to_fill:
        if df[column].isnull().sum() > 0:
            df[column].fillna(df[column].mode().iloc[0], inplace=True)

    # Handle 'Experience', 'Pay', and 'Disposal Days'
    columns_to_fill_mean = ['Experience', 'Pay', 'Disposal Days']
    for column in columns_to_fill_mean:
        if df[column].isnull().sum() > 0:
            df[column].fillna(round(df[column].mean()), inplace=True)

    # Drop rows with missing values in 'Lawyer Names'
    df.dropna(subset=['Lawyer Names'], inplace=True)


    # Read custom 'male.txt' and 'female.txt' files
    with open('me.txt', 'r') as male_file:
        male_names = male_file.read().splitlines()

    with open('fme.txt', 'r') as female_file:
        female_names = female_file.read().splitlines()

    # preparing a list of examples and corresponding class labels.
    labeled_names = ([(name, 'male') for name in male_names] +
                    [(name, 'female') for name in female_names])

    random.shuffle(labeled_names)

    # We use the feature extractor to process the names data.
    featuresets = [(gender_features(n), gender)
                  for (n, gender) in labeled_names]

    # Divide the resulting list of feature sets into a training set and a test set.
    train_set, test_set = featuresets[500:], featuresets[:500]

    # The training set is used to train a new "naive Bayes" classifier.
    classifier = nltk.NaiveBayesClassifier.train(train_set)


    lst=[]

    # Iterate through the first column values
    for index, row in df.iterrows():
        first_column_value = row[0]
        x=first_column_value.split(sep=" ")
        y=classifier.classify(gender_features(x[0]))
        lst.append(y)
        
    df['Gender'] = lst
    print(df)
    df.to_csv(file_path,index=False)

    return df

file_path = 'LawYantra.csv'
df = pd.read_csv(file_path)
df = preprocessing(df)

def merge_columns_to_csv(df):
    # Initialize an empty list to store the merged values
    merged_values = []

    # Isolate the first column
    first_column = df.iloc[:, 0]

    # Iterate through rows and merge the data with column names
    for index, row in df.iloc[:, 1:].iterrows():
        merged_row = ', '.join([f'{col}: {value}' for col, value in row.items()])
        merged_values.append(merged_row)

    # Create a new DataFrame with both the first column and the merged values
    merged_df = pd.DataFrame({'Name': first_column[:len(merged_values)], 'Info': merged_values})
    
    return merged_df

merged_data=merge_columns_to_csv(df)


def find_nearest_lawyers(csv_file, query_text, n_neighbors=5):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Access the "Name" and "Info" columns
    lawyer_names = df['Name']
    lawyer_info = df['Info']

    # Preprocess and vectorize the lawyer data
    tfidf_vectorizer = TfidfVectorizer()
    lawyer_vectors = tfidf_vectorizer.fit_transform(lawyer_info)

    # Prepare Faiss Index
    dimension = lawyer_vectors.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)  # Using L2 (Euclidean) distance

    # Insert Vectors into Faiss
    for i in range(len(lawyer_names)):
        vector = lawyer_vectors[i].toarray()
        faiss_index.add(vector)

    # Train a KNN model
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(lawyer_vectors)

    # Preprocess and vectorize the query text
    query_vector = tfidf_vectorizer.transform([query_text]).toarray()

    # Query Faiss Index
    _, faiss_indices = faiss_index.search(query_vector, k=n_neighbors)

    knn_indices = knn.kneighbors(query_vector, n_neighbors=n_neighbors)

    knn_neighbors = []
    
    for i, knn_neighbor_index in enumerate(zip(faiss_indices[0], knn_indices[0])):
        knn_neighbor_name = lawyer_names.iloc[knn_neighbor_index]

        knn_neighbors.append({"Match (KNN)": i + 1, "Name (KNN)": knn_neighbor_name})

    data = knn_neighbors

    json_data = []

    for item in data:
        match_dict = {}
        fields = re.findall(r"(\w+): (.*?)(?:, |$)", item) + re.findall(r"(\w+ \d+): (.*?)(?:, |$)", item)
        for field in fields:
            match_dict[field[0]] = field[1]
        json_data.append(match_dict)


    # Convert the list of match dictionaries to JSON
    json_output = json.dumps(json_data, indent=4)

    # Print or save the JSON data
    return print(json_output)



csv_file = merged_data
query_text = "My brother ditched me for money, I am a simple man from Chennai, need a Tamil lawyer only, and his disposal days should be around 120"
knn_results = find_nearest_lawyers(csv_file, query_text, n_neighbors=5)

