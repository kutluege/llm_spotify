import streamlit as st
import requests
from llm import generate_api_call

# Access token'ı dosyadan okuma işlevi
def read_access_token():
    try:
        with open("access_token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        st.error("Access token bulunamadı. Lütfen get_access_token.py'yi çalıştırarak token'ı alın.")
        return None

st.title("Spotify Playlist Viewer")

playlist_id = st.text_input("Enter Spotify Playlist ID:", "")

# Access token'ı dosyadan okuyorum
access_token = read_access_token()

if playlist_id and access_token:
    url, headers = generate_api_call(playlist_id, access_token)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        playlist_data = response.json()
        st.subheader("Playlist Details")
        st.write(f"**Name:** {playlist_data['name']}")
        st.write(f"**Description:** {playlist_data['description']}")
        st.write(f"**Total Tracks:** {playlist_data['tracks']['total']}")
        
        st.subheader("Tracks")
        for track in playlist_data['tracks']['items']:
            track_info = track['track']
            st.write(f"- **{track_info['name']}** by {', '.join(artist['name'] for artist in track_info['artists'])}")
            if track_info['album']['images']:
                st.image(track_info['album']['images'][0]['url'], width=100)
    else:
        st.error(f"Failed to fetch playlist. Status Code: {response.status_code}")
else:
    if not access_token:
        st.error("Lütfen access token'ı almak için get_access_token.py'yi çalıştırın.")