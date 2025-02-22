import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Embedding, Input, Dot, Flatten
from sklearn.model_selection import train_test_split

DATA_FILE = "/Users/rajath/pythonProject/data/songs.parquet"


def load_data():
    """Load preprocessed song data."""
    return pd.read_parquet(DATA_FILE)


def prepare_training_data(df):
    """Convert song data into training data for collaborative filtering."""
    df["song_id"] = df["track_uri"].astype("category").cat.codes
    df["artist_id"] = df["artist_name"].astype("category").cat.codes
    df["interaction"] = 1  # Implicit feedback (since user listened)
    return df[["artist_id", "song_id"]], df["interaction"]


def build_model(num_artists, num_songs, embedding_dim=50):
    """Build a simple Neural Collaborative Filtering model."""
    artist_input = Input(shape=(1,))
    song_input = Input(shape=(1,))

    artist_embedding = Embedding(num_artists, embedding_dim)(artist_input)
    song_embedding = Embedding(num_songs, embedding_dim)(song_input)

    dot_product = Dot(axes=1, normalize=True)([Flatten()(artist_embedding), Flatten()(song_embedding)])
    output = dot_product  # Directly output dot product

    model = keras.Model(inputs=[artist_input, song_input], outputs=output)
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


if __name__ == "__main__":
    df = load_data()
    X, y = prepare_training_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model(num_artists=df["artist_id"].nunique(), num_songs=df["song_id"].nunique())
    model.fit([X_train["artist_id"], X_train["song_id"]], y_train, epochs=10, batch_size=32,
              validation_data=([X_test["artist_id"], X_test["song_id"]], y_test))
    model.save("models/cf_model.keras")