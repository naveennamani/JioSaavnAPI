## JioSaavnAPI
![GitHub stars](https://img.shields.io/github/stars/naveennamani/JioSaavnAPI?style=social)
![GitHub forks](https://img.shields.io/github/forks/naveennamani/JioSaavnAPI?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/naveennamani/JioSaavnAPI?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/naveennamani/JioSaavnAPI?style=social)
![GitHub issues](https://img.shields.io/github/issues/naveennamani/JioSaavnAPI?style=social)
![GitHub pull requests](https://img.shields.io/github/issues-pr/naveennamani/JioSaavnAPI?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/naveennamani/JioSaavnAPI?style=social)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

---
#### An opensource (unofficial) API for jiosaavn website build with python and [FastAPI](https://fastapi.tiangolo.com/)

#### Feaures:
* Search songs using any query
* Get song details from the jiosaavn song url
* Get all songs from the jiosaavn album/playlist url
* Song details include many useful fields such as **image_url, album_id, artists details, lyrics (only if supported), jiotune preview link etc.**
```json
{
  "id": "Grohf5-o",
  "title": "Something Just Like This",
  "perma_url": "https://www.jiosaavn.com/song/something-just-like-this/NxoEWRIFGlw",
  "image": "https://c.saavncdn.com/168/Something-Just-Like-This-English-2017-500x500.jpg",
  "language": "english",
  "play_count": 50077552,
  "music": "Andrew Taggart, Christopher Martin, Will Champion, Guy Berryman, Jonny Buckland",
  "album": "Something Just Like This",
  "album_id": "10290258",
  "album_url": "https://www.jiosaavn.com/album/something-just-like-this/TMJs0WfIbJI_",
  "label": "Disruptor Records/Columbia",
  "origin": "none",
  "is_320kbps": true,
  "media_url": "https://aac.saavncdn.com/168/c3ff67fbe7ab6cac1e90d8e3499c51d5_320.mp3",
  "duration": 247,
  "has_lyrics": false,
  "starred": false,
  "copyright_text": "(P) 2017 Disruptor Records/Columbia Records",
  "artistMap": {
    "primary_artists": [
      {
        "id": 615629,
        "name": "The Chainsmokers",
        "role": "primary_artists",
        "image": "https://c.saavncdn.com/artists/The_Chainsmokers_500x500.jpg",
        "type": "artist",
        "perma_url": ""
      },
      ...
    ],
    "featured_artists": [],
    "artists": [
      {
        "id": 698794,
        "name": "Andrew Taggart",
        "role": "music",
        "image": "",
        "type": "artist",
        "perma_url": ""
      },
      ...
    ]
  },
  "release_date": "2017-02-22",
  "year": 2017,
  "vlink": "https://jiotunepreview.jio.com/content/Converted/010910140558508.mp3"
}
```

 ---
 
#### Installation:

Clone this repository using
```sh
$ git clone https://github.com/naveennamani/JioSaavnAPI
```
Install all the requirements using
```sh
$ cd JioSaavnAPI
$ pip3 install -r requirements.txt
```
And run the app using
```sh
$ python3 app.py
or 
$ uvicorn app:app --reload
```
Navigate to http://127.0.0.1:5000/docs to see the interactive documentation made with OpenAPI
and check out the API endpoints.

#### API endpoints available:
```/search?query=<any query>``` : Pass any query as the query parameter and get the details for all the songs matching the query
###### Note: song/album/playlist links shared from the jiosaavn website/app can also be passed as the query

```/song/{song_id}``` : Pass song_id obtained from `/search` results
```/album/{album_id}``` : Pass album_id obtained from `/search` results
```/playlist/{playlist_id}``` : Pass playlist_id obtained from `/search` results

### Fork the repo and deploy on Heroku now!
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/naveennamani/JioSaavnAPI/tree/master)

---
###### This project is heavily inspired by the [JioSaavnAPI](https://github.com/cyberboysumanjay/JioSaavnAPI/tree/master) project by [@cyberboysumanjay](https://github.com/cyberboysumanjay/).
# © [Naveen Namani](https://github.com/naveennamani)
