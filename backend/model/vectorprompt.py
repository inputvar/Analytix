import re
import pandas as pd
from flask import json
import numpy as np
import random
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import faiss


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

    # Print the nearest neighbors from Faiss
    for i, faiss_neighbor_index in enumerate(faiss_indices[0]):
        faiss_neighbor_name = lawyer_names.iloc[faiss_neighbor_index]
        faiss_output_string = f"Match (Faiss): {i + 1}, Name: {faiss_neighbor_name}"
     

    # Find the k-nearest neighbors using KNN
    distances, indices = knn.kneighbors(query_vector)


    # Initialize an empty list to store the neighbor data
    neighbor_data = []

    # Print the nearest neighbors from KNN
    for i in range(len(indices[0])):
        neighbor_index = indices[0][i]
        neighbor_name = lawyer_names.iloc[neighbor_index]
        neighbor_info = lawyer_info.iloc[neighbor_index]

        # Create a dictionary for the neighbor
        neighbor_dict = {
            "Match": i + 1,
            "Name": neighbor_name,
            "Info": neighbor_info
        }
        neighbor_data.append(neighbor_dict)

    # Convert the list of dictionaries to a JSON format
    json_output = json.dumps(neighbor_data, indent=4)

    print(json_output)
    
# Example usage
csv_file = 'finaldata.csv'
query_text = "My brother ditched me for money, I am a simple man from Chennai, need a Tamil lawyer only, and his disposal days should be around 120"
find_nearest_lawyers(csv_file, query_text, 5)
