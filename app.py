from fastapi import FastAPI, Query
from chatbot.chatbot import recommend_song, load_model, load_data
from fastapi.responses import JSONResponse

app = FastAPI()

df = load_data()
model = load_model()


@app.get("/")
def home():
    return {"message": "Welcome to the Music Recommendation API!"}


@app.get("/recommend/")
def recommend(artist_name: str = Query(None, description="Enter an artist's name")):
    if not artist_name:
        return JSONResponse(content={"error": "Artist name is required. Please provide an artist name."},
                            status_code=400)

    recommended_song = recommend_song(artist_name, model, df)
    return {"artist": artist_name, "recommended_song": recommended_song}