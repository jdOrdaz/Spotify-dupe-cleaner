# Spotify-dupe-cleaner 🎵

A Python tool that extracts your full liked songs library from Spotify, enriches it with genre information, and helps you find and remove duplicate tracks.

## 🚀 Features

- ✅ Pulls your entire liked songs library using the Spotify Web API
- ✅ Retrieves genre metadata for each artist
- ✅ Outputs a clean CSV with:
  - Song title
  - Artist
  - Album name
  - Popularity score
  - Artist genres
  - Artist link
- ✅ Detects duplicate songs (even across albums like deluxe or explicit editions)
- ✅ Creates a readable `.txt` report of duplicates
- ✅ Optional: removes duplicates from your Spotify account automatically

---

## 📁 Files

- `main.py` – main script that collects liked songs, artist info, and outputs CSV
- `find_replicas.py` – helper script that finds and lists duplicate tracks
- `requirements.txt` – list of dependencies to run the project

---

## 🛠 Installation & Setup

1. **Create a Spotify Developer App**  
   - Go to [developer.spotify.com](https://developer.spotify.com)
   - Create a new app to get your `Client ID`, `Client Secret`, and `Redirect URI`

2. **Clone this repo**

   ```bash
   git clone https://github.com/jdOrdaz/Spotify-dupe-cleaner.git
   cd Spotify-dupe-cleaner
