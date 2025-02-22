import pandas as pd
import tensorflow as tf
import random
from fuzzywuzzy import process

DATA_FILE = "/Users/rajath/pythonProject/data/songs.parquet"
CF_MODEL_PATH = "/Users/rajath/pythonProject/models/models/cf_model.keras"

def load_data():
    """Load song dataset."""
    return pd.read_parquet(DATA_FILE)

def load_model():
    """Load the trained collaborative filtering model."""
    return tf.keras.models.load_model(CF_MODEL_PATH)

def recommend_song(artist_name, model, df):
    """Recommend one song from the given artist, changing every time."""
    artist_names = df["artist_name"].unique()
    best_match, score = process.extractOne(artist_name, artist_names)

    if score < 60:  # If confidence score is low, suggest similar artists
        similar_artists = [match[0] for match in process.extract(artist_name, artist_names, limit=3)]
        return f"No exact match found. Did you mean: {', '.join(similar_artists)}?"

    # Filter songs by the matched artist
    artist_songs = df[df["artist_name"] == best_match]

    if artist_songs.empty:
        return "No recommendations found."

    # Pick a completely random song each time
    random_song = artist_songs.sample(n=1, random_state=random.randint(1, 10000))["track_name"].values[0]

    return f"🎶 Recommended Song by {best_match}: {random_song}"

    return message + "\n" + "\n".join(top_songs["track_name"].tolist())
if __name__ == "__main__":
    df = load_data()
    model = load_model()

    while True:
        user_input = input("Enter an artist name (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        recommendation = recommend_song(user_input, model, df)
        print(f"Recommended Songs: {recommendation}")