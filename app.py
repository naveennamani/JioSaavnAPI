from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from file_downloader import TaskManager
from saavn_nn import AlbumDetails
from saavn_nn import PlaylistDetails
from saavn_nn import SongDetails
from saavn_nn import check_media_url
from saavn_nn import get_album_details
from saavn_nn import get_album_details_from_url
from saavn_nn import get_lyrics
from saavn_nn import get_playlist_details
from saavn_nn import get_playlist_details_from_url
from saavn_nn import get_song_details
from saavn_nn import get_song_details_from_url
from saavn_nn import search_query

app = FastAPI()
task_manager = TaskManager()


@app.get('/')
def home():
    return RedirectResponse(url = '/docs')


@app.get('/search')
def search_jiosaavn(query: str, lyrics: Optional[bool] = False) -> Union[
    Dict[str, Union[str, Union[SongDetails, AlbumDetails, PlaylistDetails, List[
        SongDetails]]]], JSONResponse]:
    """
    Submit your query here.
    Valid query options are - song/album/playlist link of from https://www.jiosaavn.com/
    or text query
    """
    if 'saavn' in query:
        token = query.split('/')[-1]
        if '/song' in query:
            return {"type": "song", "result": get_song_details_from_url(token)}
        elif '/album' in query:
            return {
                "type": "album",
                "result": get_album_details_from_url(token)
            }
        elif '/playlist' in query or '/featured' in query:
            return {
                "type": "playlist",
                "result": get_playlist_details_from_url(token, 1)
            }
        else:
            return JSONResponse(status_code = 404, content = {
                "error": "Unknown URL",
                "error code": 1001,
                "url": query,
                "message": "Please send links from https://www.jiosaavn.com only"
            })
    return {"type": "query", "result": search_query(query)}


@app.get('/song/{song_id}')
def song_details(song_id: str) -> SongDetails:
    """Get song details using song id,
    which may be obtained from previous query results"""
    return get_song_details(song_id)


@app.get('/lyrics/{song_id}')
def get_song_lyrics_(song_id: str):
    """Get song lyrics"""
    return get_lyrics(song_id)


@app.get('/album/{album_id}')
def album_details(album_id: str) -> AlbumDetails:
    """Get album details including details of all songs in the album by using
    album id, which may be obtained from previous query results"""
    return get_album_details(album_id)


@app.get('/playlist/{playlist_id}')
def playlist_details(playlist_id: str,
                     page_no: Optional[int] = 1) -> PlaylistDetails:
    """Get playlist details with top 5 songs in the playlist by using
    album id, which may be obtained from previous query results"""
    return get_playlist_details(playlist_id, page_no)


@app.get('/media_url/{song_id}')
def download_link(song_id: str) -> str:
    """Get verified download link of the song using song_id"""
    return check_media_url(get_song_details(song_id).media_url)


@app.get('/download_song/{song_id}')
def download_song(song_id: str):
    song_details = get_song_details(song_id)
    media_url = song_details.media_url
    return {"task_id": task_manager.add_task(media_url)}


@app.get('/get_task_status/{task_id}')
def get_task_status(task_id: int):
    print("getting task status", task_id)
    return {"task_finished": task_manager.get_task_status(task_id)}


@app.get('/del_task/{task_id}')
def del_task(task_id: int):
    print("deleting task status", task_id)
    task_manager.del_task(task_id)
    return {"task_finished": True}


if __name__ == '__main__':
    from os import environ
    from uvicorn import run

    run("app:app", host = "0.0.0.0", port = int(environ.get("PORT", 5000)))
