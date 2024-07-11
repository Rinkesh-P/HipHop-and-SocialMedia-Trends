from dotenv import load_dotenv 
from requests import post, get
import os 
import base64
import json
import asyncio
from shazamio import Shazam, Serialize, GenreMusic


load_dotenv() #loading client id and client secret from the .env file 

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

async def fetch_shazam_top_200():
    shazam = Shazam()
    top_hiphop = await shazam.top_world_genre_tracks(genre=GenreMusic.HIP_HOP_RAP, limit=200)
    return top_hiphop['data']

async def get_spotify_track(token, track, artist):
    url = "https://api.spotify.com/v1/search" 
    headers = get_auth_header(token)
    query = f"?q=track:{track} artist:{artist}&type=track&limit=1"
    query_url = url+query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['tracks']['items']
    for i in json_result:
        popularity = i['popularity'] #popularity
        release_date = i['album']['release_date'] #release date
        return({"track_name": track, "artist_name": artist, "popularity_sore":popularity, "release_date":release_date}) 

async def main():
    token = get_token() #token will need to be passed onto all api calls 
    
    shazam_top_200 = await fetch_shazam_top_200()
    
    data = [] 
    for i in shazam_top_200:
        song_name = i['attributes']['name']
        artist_name = i['attributes']['artistName']
        spotify_track = await get_spotify_track(token, song_name, artist_name)
        data.append(spotify_track)
    
    print(data)
        
if __name__ == "__main__":
    asyncio.run(main())