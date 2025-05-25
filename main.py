"""
Made this program because I hated how spotify doesn't fully let you see what your songs genres are.
This program gives you a full list of every liked song, with it's genre, artist, and other additional info, into a neat csv file.
I could've added more info, like dates on when I added, but I decided this was best for my liking.

Also, I noticed that when I shuffled my music, some songs would come up more than once, and I realized
that I liked the same song multiple times. Sometimes the artist would release different versions of an album, and this would occur (like a deluxe album).
To fix this, I made a seperate file program that allows me to find replicas of a liked song based on the csv file info.
I then added a feature that allows you to view what songs are replicas within the csv file.
The program then makes a txt file, and saves your duplicate songs for you to review, along with the artist link so that you can see for yourself.
If you agree that the duplicates are unnecessary, there's a feature that give the user the option to remove the duplicates from your liked songs.

By the end, I had over 150 songs that were just duplicates. How annoying, but now much better! :)
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

from find_replicas import find_replicas_main

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( # empty so I won't expose myself lol 
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET", 
    redirect_uri="http://localhost:8888/callback", 
    scope="user-library-read"
    ))

songs_limit = 50
my_liked_data = sp.current_user_saved_tracks(limit=songs_limit) # data from saved tracks
total_songs = my_liked_data['total'] # total tracks
songs_offset = 0

song_data = [] # list of dictionaries, each holding song info
artist_cache = {}
while(total_songs > songs_offset): # Spotify can only handle up to 50 at a time O_O
    my_liked_data = sp.current_user_saved_tracks(limit=songs_limit, offset=songs_offset)

    for item in my_liked_data['items']:
        track = item['track'] # This accesses the track within every item within my_liked_data
        artist_id = track['artists'][0]['id']
        artist_name = track['artists'][0]['name']

        if artist_id in artist_cache: # More effiecient if I already have the artist_id stored
            artist_info = artist_cache[artist_id]
        else:
            artist_info = sp.artist(artist_id)
            artist_cache[artist_id] = artist_info
            time.sleep(0.1)  # avoid hitting rate limits


        song_data.append({
            'Song Title' : track['name'],
            'Artist' : artist_name,
            'Album Title' : track['album']['name'],
            'Popularity' : track['popularity'],
            'Genres': ", ".join(artist_info.get('genres', [])) if artist_info.get('genres') else 'Unknown', # some songs have multiple genres
            'Artist Link': artist_info['external_urls']['spotify'],
            'Track ID': track['id']
        })
        
    songs_offset += songs_limit


liked_songs_df = pd.DataFrame(song_data)
liked_songs_df.to_csv('Personal Song Library.csv', mode='w', header=True, index= False)

print("Liked songs have been recorded!")

def delete_duplicates_from_spotify(duplicates_list, sp):
    track_ids = [song['Track ID'] for song in duplicates_list if 'Track ID' in song] # lists track IDs from the duplicates... duplicates have unique id from the original so it's ok (;
    
    if not track_ids:
        print("No valid track IDs found for deletion.")
        return
    
    # Spotify only allows up to 50 songs at once
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50] # iterates 50 at a time
        sp.current_user_saved_tracks_delete(batch) # actual deleting happens

    print("All duplicates have been removed from your liked songs.")

duplicates = find_replicas_main()

if len(duplicates) > 0 and input("Would you like to delete duplicates?(y or n): ").lower().strip() == 'y':
    delete_duplicates_from_spotify(duplicates_list=duplicates, sp=sp)
