import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 🔹 CONFIGURA TUS CREDENCIALES
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8888/callback/"

# 🔹 AUTENTICACIÓN EN SPOTIFY
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public"))

# 🔹 STREAMLIT UI
st.title("🎵 Playlist Automática por Artista y Género 🎶")
st.write("Selecciona un artista y un género para generar tu playlist.")

# 📌 Input para seleccionar el artista
artist_name = st.text_input("🎤 Nombre del Artista", "Chris Brown")

# 📌 Opciones de género musical
genres = ["Pop", "Hip-Hop", "R&B", "Dance", "Latino", "Rock", "Electrónica"]
selected_genre = st.selectbox("🎼 Selecciona un Género", genres)

# 📌 Nombre de la Playlist
playlist_name = f"{artist_name} - {selected_genre} Essentials"

if st.button("🎧 Crear Playlist"):
    with st.spinner("Buscando canciones... ⏳"):

        # 🔹 BUSCAR EL ID DEL ARTISTA
        artist_result = sp.search(q=artist_name, type="artist", limit=1)
        if not artist_result["artists"]["items"]:
            st.error("❌ No se encontró el artista. Intenta con otro nombre.")
        else:
            artist_id = artist_result["artists"]["items"][0]["id"]

            # 🔹 OBTENER CANCIONES POPULARES DEL ARTISTA
            top_tracks = sp.artist_top_tracks(artist_id, country="US")["tracks"]

            # 🔹 EXTRAER LOS URIs DE LAS CANCIONES
            track_uris = [track["uri"] for track in top_tracks[:10]]

            # 🔹 OBTENER EL ID DEL USUARIO
            user_id = sp.me()["id"]

            # 🔹 CREAR UNA PLAYLIST
            playlist = sp.user_playlist_create(user=user_id, name=playlist_name,
                                               public=True, description=f"Playlist de {artist_name} con lo mejor de {selected_genre}.")
            
            # 🔹 AGREGAR CANCIONES A LA PLAYLIST
            sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

            # 🔹 MOSTRAR EL LINK DE LA PLAYLIST
            playlist_link = playlist["external_urls"]["spotify"]
            st.success(f"✅ Playlist creada exitosamente: [Abrir en Spotify]({playlist_link})")
