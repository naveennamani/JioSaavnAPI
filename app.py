from typing import List
from typing import Optional
from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from saavn_nn import AlbumDetails
from saavn_nn import PlaylistDetails
from saavn_nn import SongDetails
from saavn_nn import check_media_url
from saavn_nn import get_album_details
from saavn_nn import get_album_details_from_url
from saavn_nn import get_playlist_details
from saavn_nn import get_playlist_details_from_url
from saavn_nn import get_song_details
from saavn_nn import get_song_details_from_url
from saavn_nn import search_query

app = FastAPI()


@app.get('/')
def home():
    return RedirectResponse(url = '/docs')


@app.get('/search')
def search_jiosaavn(query: str, lyrics: Optional[bool] = False) -> Union[
    SongDetails, AlbumDetails, PlaylistDetails, JSONResponse, List[
        SongDetails]]:
    """
    Submit your query here.
    Valid query options are - song/album/playlist link of from https://www.jiosaavn.com/
    or text query
    """
    if 'jiosaavn' in query:
        token = query.split('/')[-1]
        if '/song' in query:
            return get_song_details_from_url(token)
        elif '/album' in query:
            return get_album_details_from_url(token)
        elif '/playlist' in query or '/featured' in query:
            return get_playlist_details_from_url(token, 1)
        else:
            return JSONResponse(status_code = 404, content = {
                "error": "Unknown URL",
                "error code": 1001,
                "url": query,
                "message": "Please send links from https://www.jiosaavn.com only"
            })
    return search_query(query)


@app.get('/song/{song_id}')
def song_details(song_id: str):
    """Get song details using song id,
    which may be obtained from previous query results"""
    return get_song_details(song_id)


@app.get('/album/{album_id}')
def album_details(album_id: str):
    """Get album details including details of all songs in the album by using
    album id, which may be obtained from previous query results"""
    return get_album_details(album_id)


@app.get('/playlist/{playlist_id}')
def playlist_details(playlist_id: str, page_no: Optional[int] = 1):
    """Get playlist details with top 5 songs in the playlist by using
    album id, which may be obtained from previous query results"""
    return get_playlist_details(playlist_id, page_no)


@app.get('/media_url/{song_id}')
def download_link(song_id: str):
    """Get verified download link of the song using song_id"""
    return check_media_url(get_song_details(song_id).media_url)


if __name__ == '__main__':
    from os import environ
    from uvicorn import run

    run("app:app", host = "0.0.0.0", port = int(environ.get("PORT", 5000)))
