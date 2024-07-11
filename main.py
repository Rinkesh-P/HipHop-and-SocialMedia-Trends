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

# def get_current_top_tracks(token):
#     url = "https://api.spotify.com/v1/"
#     headers = get_auth_header(token)
#     playlist_id = "37i9dQZEVXbNG2KDcFcKOF" #playlist ID of the Top Songs Global Playlist
#     query = f"playlists/{playlist_id}"
#     #print(query)
#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)
    
#     # with open('top_tracks.json', 'w') as f: #looking at the output of the JSON file to know what i need
#     #     json.dump(json_result, f)
        
#     return json_result['tracks']['items']

# def get_artist_information(token, link):
#     url = f"https://api.spotify.com/v1/artists/{link}"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     # with open('artist_information.json', 'w') as f: #looking at the output of the JSON file to know what i need
#     #     json.dump(json_result, f)
#     #print(f"name {json_result['name']}, genres = {json_result['genres']}, type = {type(json_result['genres'])}")
    
#     result_set = set(json_result['genres'])
#     if "hip hop" in result_set or "rap" in result_set:
#         return(True)

async def fetch_shazam_top_200():
    shazam = Shazam()
    top_hiphop = await shazam.top_world_genre_tracks(genre=GenreMusic.HIP_HOP_RAP)
    return top_hiphop['data']


async def get_spotify_track(token, track, artist):
    url = "" 
    headers = get_auth_header(token)
    query = f""
    query_url = url+query
    
    pass 

async def main():
    token = get_token() #token will need to be passed onto all api calls 
    
    shazam_top_200 = await fetch_shazam_top_200()
    
    for i in shazam_top_200:
        song_name = i['attributes']['name']
        artist_name = i['attributes']['artistName']
        spotify_track = await get_spotify_track(token, song_name, artist_name)
        
    # result = get("https://api.spotify.com/v1/search?q=kendrick+lamar+%26+type%3Dartist+not+like+us+%26type+%3Dtrack&type=artist%2Ctrack&limit=1", headers=get_auth_header(token))
    # json_result = json.loads(result.content)['tracks']['items']
    # print(json_result[0]['name']) #song name
    # print(json_result[0]['artists'][0]['name']) #artist name
    # print(json_result[0]['popularity']) #popularity 
    # print(json_result[0]['album']['release_date']) #release date
    
    
    
    #print(top_tracks['tracks']['items'][0]['track']['name']) #Song name
    
    # filtered_tracks = [] 
    
    # for i in top_tracks:
    #     artist_name = i['track']['artists'][0]['name']
    #     song_name = i['track']['name']
    #     popularity = i['track']['popularity']
    #     added_date = i['added_at'] 
    #     artist_link_id = i['track']['artists'][0]['id']
    #     release_date = i['track']['album']['release_date']
    #     if get_artist_information(token, artist_link_id):
    #         filtered_tracks.append({'name':song_name, 
    #                                 'artist':artist_name,
    #                                 'popularity': popularity,
    #                                 'release_date': release_date,
    #                                 'added_date': added_date
    #                                 })
        #print(f"Artist Name = {artist_name}, Song Name = {song_name}, Popularity = {popularity}, Date Added = {added_date}, Artist Link = {artist_link_id},  Release Date = {release_date} \n")
        
    #print(filtered_tracks)

    
    
if __name__ == "__main__":
    asyncio.run(main())