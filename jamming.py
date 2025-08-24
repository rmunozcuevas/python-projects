import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
 
import warnings
warnings.filterwarnings('ignore')

def Recommendation():
    print("reccomending music is the goal")



def Music_choice(user):
    print("choose your music")
    while True:
        if user == "stop":
            print("exiting the decision process")
            break
        Recommendation()






try:
    # Read CSV with default settings
    tracks = pd.read_csv("rage_songs_ray.csv", index_col=False)

    # If the DataFrame is still empty, try with different delimiters
    if tracks.empty:
        print("Warning: Empty DataFrame. Retrying with different delimiter...")
        tracks = pd.read_csv("rage_songs_ray.csv", delimiter=";", index_col=False)

    print(tracks.head())

except FileNotFoundError:
    print("Error: 'rage_songs_ray.csv' file not found.")
