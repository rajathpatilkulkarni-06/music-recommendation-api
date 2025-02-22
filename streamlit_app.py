import os
import streamlit as st
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


class MusicRecommender:
    def __init__(self):
        self._init_spotify_client()
        self.api_url = os.getenv("API_URL", "http://127.0.0.1:8000/recommend/")
        self._configure_ui()

    def _init_spotify_client(self):
        """Initialize Spotify client with environment variables"""
        try:
            client_id = st.secrets["SPOTIPY_CLIENT_ID"]
            client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]

            self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            ))
        except Exception as e:
            st.error(f"Failed to initialize Spotify client: {str(e)}")
            st.stop()

    def _configure_ui(self):
        """Configure all UI elements and styles"""
        self._set_background()
        self._set_title()
        self._set_input_style()
        self._set_main_layout()

    def _set_background(self):
        """Set background image with overlay"""
        bg_image = "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg"
        st.markdown(f"""
            <style>
            .stApp {{
                background: url({bg_image}) no-repeat center center fixed;
                background-size: cover;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                z-index: -1;
            }}
            </style>
            """, unsafe_allow_html=True)

    def _set_title(self):
        """Set custom styled title with enforced color"""
        st.markdown("""
           <link href="https://fonts.googleapis.com/css2?family=Metamorphous&display=swap" rel="stylesheet">
            <style>
            .title-container {
                width: 100%;
                display: flex !important;
                justify-content: center !important;
            }
            .main-title {
                font-size: 4rem !important;
                font-family: 'Metamorphous', serif !important;
                color: #2A0101 !important;  <!-- Forced color -->
                text-align: center !important;
                margin: 3rem 0 !important;
                font-weight: 900 !important;
                text-shadow: 
                    0 2px 4px rgba(0, 0, 0, 0.3) !important;
                background: linear-gradient(
                    to bottom right,
                    rgba(255, 255, 255, 0.15),
                    rgba(255, 255, 255, 0.05)
                ) !important;
                padding: 12px 24px !important;
                border-radius: 6px !important;
                border: 1px solid rgba(42, 1, 1, 0.2) !important;
            }
            </style>
            <div class="title-container">
                <h1 class="main-title">Harmony Guide</h1>
            </div>
            """, unsafe_allow_html=True)

    def _set_input_style(self):
        """Style input elements"""
        st.markdown("""
            <style>
            .stTextInput > div > div > input {
                font-size: 18px;
                padding: 12px;
                border-radius: 6px;
                border: 2px solid #FF6666; /* Soft red border */
                background: rgba(50, 50, 50, 0.7); /* Dark semi-transparent background */
                color: #FFFFFF; /* White text */
            }
            .stTextInput > div > div > input::placeholder {
                color: rgba(255, 200, 200, 0.6); /* Light reddish placeholder */
                font-style: italic;
            }.stTextInput input {{
                background: rgba(255, 204, 204, 0.15) !important;
                border: 2px solid #32CD32 !important;
                color: white !important;
                border-radius: 6px;
                border: 1.5px solid #32CD32;
                padding: 12px;
            }}
            div.stButton > button {
            display: block;
            margin: 0 auto;
            }
            .stButton>button {{
                background: #32CD32 !important;
                color: black !important;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            .stButton>button:hover {{
                transform: scale(1.05);
                box-shadow: 0 0 15px #32CD32;
            }}
            </style>
            """, unsafe_allow_html=True)

    def _set_main_layout(self):
        """Set main content layout"""
        st.markdown("""
            <style>
            .main {{
                max-width: 800px;
                margin: 0 auto;
            }}
            </style>
            """, unsafe_allow_html=True)

    def get_song_info(self, song_name, artist_name):
        """Fetch track metadata from Spotify"""
        try:
            results = self.sp.search(q=f"{song_name} {artist_name}", limit=1)
            if not results["tracks"]["items"]:
                return None

            track = results["tracks"]["items"][0]
            return track["album"]["images"][0]["url"]  # Return only album cover

        except Exception as e:
            st.error(f"Error fetching track info: {str(e)}")
            return None

    def display_recommendation(self, song_name, artist_name):
        """Display recommendation with album art"""
        with st.spinner("🎵 Searching for track details..."):
            album_cover = self.get_song_info(song_name, artist_name)

        col1, col2 = st.columns([1, 2])
        with col1:
            if album_cover:
                st.image(album_cover, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/400x400.png?text=No+Album+Cover",
                         use_container_width=True)

        with col2:
            st.markdown(f"""
                <div style='padding: 20px; border-radius: 10px; background: rgba(0, 0, 0, 0.4);'>
                    <h3 style='color: #FEBCAE; margin-bottom: 15px; font-size: 28px; font-size: 32px; font-weight: bold; 
                    text-shadow: 1px 1px 10px rgba(255, 200, 200, 0.8);'>{song_name}</h3>
                    <p style='font-size: 1.1rem;'>by {artist_name}</p>
                </div>
                """, unsafe_allow_html=True)

    def run(self):
        """Main application flow"""
        st.markdown(
            "<h3 style='text-align: center; color: #ffffff; margin-bottom: 2rem; "
            "text-shadow: 2px 2px 20px rgba(50, 50, 50, 0.8)'>"
            "Discover your next favorite track</h3>",
            unsafe_allow_html=True)

        artist_name = st.text_input("Enter artist name:", key="artist_input")

        if st.button("Get Recommendation", type="primary"):
            if not artist_name.strip():
                st.warning("Please enter an artist name")
                return

            try:
                response = requests.get(f"{self.api_url}?artist_name={artist_name}")
                response.raise_for_status()
                result = response.json()
                recommended_song = result['recommended_song'].split(": ")[-1]
                self.display_recommendation(recommended_song, artist_name)

            except requests.exceptions.RequestException as e:
                st.error(f"Recommendation service unavailable: {str(e)}")
            except KeyError:
                st.error("Unexpected response format from API")


if __name__ == "__main__":
    recommender = MusicRecommender()
    recommender.run()
