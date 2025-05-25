import csv
from tabulate import tabulate

def find_replicas_main():
    all_songs = []

    with open('Personal Song Library.csv', newline='', encoding='utf-8') as library_csv:
        reader = csv.DictReader(library_csv) # returns each row as a dict while keeping the headers as the keys
        all_songs = list(reader) # pusts each dictonary into a list of dictionaries

    def find_dupes(): # finds dupes
        unique = set()
        dupes = []

        for song_dict in all_songs: # goes trhough every dictionary in all_songs list
            title = song_dict['Song Title']
            artist = song_dict['Artist']
            if (title, artist) in unique: # checks for dupes based on title
                dupes.append(song_dict) # adds full dict not just title
            else:
                unique.add((title, artist)) # adds just title, since that's what we're checking against

        return dupes # returns a list of dictionaries

    duplicates = find_dupes()
    for dict in duplicates: # I just want the song and artist
        del dict['Popularity']
        del dict['Genres']
        del dict['Album Title']
    duplicates =  sorted(duplicates, key=lambda song_dict: song_dict['Artist'])

    sorted_table = tabulate(duplicates, headers='keys', tablefmt='fancy_grid')
    with open('songs to check.txt', 'w', encoding='utf-8') as file:
        
        file.write(sorted_table)

    if len(duplicates) > 0: # TODO
        print("Song duplicates have been recorded!")
    else:
        print("No duplicates found!")

    return duplicates
