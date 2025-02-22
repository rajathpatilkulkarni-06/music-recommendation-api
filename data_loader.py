import os
import json
import pandas as pd

DATA_DIR = "../data/"
OUTPUT_FILE = "../data/songs.parquet"

def load_json_files():
    """Load multiple JSON files from the dataset directory."""
    playlists = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                playlists.extend(data["playlists"])
    return playlists

def extract_songs(playlists):
    """Extract song data from playlists and store in a DataFrame."""
    songs = []
    for playlist in playlists:
        for track in playlist["tracks"]:
            songs.append({
                "track_name": track["track_name"],
                "artist_name": track["artist_name"],
                "track_uri": track["track_uri"],
                "album_name": track["album_name"],
                "duration_ms": track["duration_ms"],
            })
    return pd.DataFrame(songs).drop_duplicates()

def save_to_parquet(df):
    """Save processed data as a Parquet file for efficiency."""
    df.to_parquet(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    playlists = load_json_files()
    df_songs = extract_songs(playlists)
    save_to_parquet(df_songs)
    print(f"Processed {len(df_songs)} unique songs saved to {OUTPUT_FILE}")