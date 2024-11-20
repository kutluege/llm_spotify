import requests
import os


#client_id = os.getenv("CLIENT_ID")  # Replace with your Client ID in .env
#client_secret = os.getenv("CLIENT_SECRET")  # Replace with your Client Secret in .env
#redirect_uri = os.getenv("REDIRECT_URI")  # Replace with your Redirect URI in .env

client_id = "f29ee281b7664d65ad23ecc58965e61d"
client_secret ="55f57bd1a7c14c3ba3e05657f9f19294"
redirect_uri = "https://llmspotify.streamlit.app/"

code = "AQC71aKQQ2AwkNd9G7mIQP7BSKVCgjHW_L-J6U9SJqzBiCDcDcFDjNf71Kg8zdsr7bhMJYDELaNkNCiSTX_B8UzI1R4C430h9Z83Xr5NCH2qXc0ERr9Ea4wYf7KZzewGM4Nycu2Mu1jpdfKovFP27us3YUiZYZ_j46COOxskXknzYystYVv8N8Gx5tm2G5-RNoicCvtBNBDYQ1Y3"

def get_access_token(code):
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]

        # Access token'ı access_token.txt dosyasına kaydediyoruz
        with open("access_token.txt", "w") as f:
            f.write(access_token)
        print("Access token başarıyla kaydedildi.")
    else:
        print("Access token alınamadı:", response.json())

get_access_token(code)
