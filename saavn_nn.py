import base64
import json
from traceback import print_exc
from typing import Any
from typing import List

import requests
from fastapi.applications import FastAPI
from pyDes import ECB
from pyDes import PAD_PKCS5
from pyDes import des
from pydantic import BaseModel
from pydantic import validator

app = FastAPI()

base_url = "https://www.jiosaavn.com/api.php"

des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad = None,
                 padmode = PAD_PKCS5)


################################################################################
# pydantic models
################################################################################
class Artist(BaseModel):
    id: int
    name: str
    role: str
    image: str
    type: str
    perma_url: str

    @validator('image', allow_reuse = True)
    def fix_artist_image(cls, v):
        return fix_image_url(v)


class ArtistsMap(BaseModel):
    primary_artists: List[Artist]
    featured_artists: List[Artist]
    artists: List[Artist]


class SongDetails(BaseModel):
    id: str
    title: str
    subtitle: str
    type: str = "song"
    perma_url: str
    image: str
    language: str
    play_count: int = None
    explicit_content: bool = None
    list_count: int = None
    list_type: str = None
    list: Any = None
    music: str
    album: str
    album_id: str
    album_url: str
    label: str
    origin: str
    is_320kbps: bool
    encrypted_media_url: str
    media_url: str
    media_url_default: str
    duration: int
    has_lyrics: bool
    lyrics_snippet: str
    lyrics_id: str = None
    starred: bool
    copyright_text: str
    artistMap: ArtistsMap
    release_date: str
    year: int
    vlink: str = None

    @validator('title', 'subtitle', 'album', allow_reuse = True)
    def fix_title_(cls, v):
        return fix_title(v)

    @validator('image', allow_reuse = True)
    def fix_image(cls, v):
        return fix_image_url(v)


class AlbumDetails(BaseModel):
    id: int
    title: str
    subtitle: str
    type: str
    perma_url: str
    image: str
    language: str
    year: int
    play_count: str
    explicit_content: bool
    list_count: int
    list_type: str
    songs: List[SongDetails]

    # @validator('title', 'subtitle')
    # def fix_title_(cls, v):
    #     return fix_title(v)

    @validator('image', allow_reuse = True)
    def fix_image(cls, v):
        return fix_image_url(v)


class PlaylistDetails(AlbumDetails):
    # more_info
    uid: str
    last_updated: str
    username: str
    firstname: str
    lastname: str
    follower_count: int
    fan_count: int


################################################################################
# jiosaavn_api functions
################################################################################
def jiosaavn_request(search_params, resp_only = False):
    search_params = {'api_version': 4, '_format': 'json', '_marker': 0,
                     **search_params}
    resp = requests.get(base_url, params = search_params, headers = {
        "Host": "c.saavncdn.com",
        "Referer": "https://www.jiosaavn.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.89 Safari/537.36 "
                      "Edg/84.0.522.40"
    })
    if resp_only:
        return resp
    try:
        return resp.json()
    except:
        print_exc()
        print(resp.text)
        try:
            return json.loads(resp.text.strip())
        except:
            print_exc()
            return None


def search_query(query: str) -> List[SongDetails]:
    query_results = jiosaavn_request({
        '__call': "autocomplete.get",
        'ctx': "wap6dot0",
        'query': query
    })
    if query_results is None:
        return None
    return [
        get_song_details(song['id'])
        for song in query_results["songs"]['data']
    ]


def get_song_details(song_id: str) -> SongDetails:
    resp = jiosaavn_request({
        '__call': "song.getDetails",
        'pids': song_id,
        # 'ctx': "wap6dot0",
    })
    if resp is None:
        return None
    return fix_song_details(resp[song_id])


def get_song_details_from_url(song_url: str) -> SongDetails:
    resp = jiosaavn_request({
        "__call": "webapi.get",
        "token": song_url,
        "type": "song"
    })
    if resp is None:
        return None
    if type(resp) == dict and len(resp) == 1:
        return fix_song_details(resp.popitem()[1])
    else:
        print("Error", resp)
        return None


def fix_song_details(song_details) -> SongDetails:
    song_more_details = song_details["more_info"]
    default_media_url, media_url = decrypt_url(
        song_more_details["encrypted_media_url"])
    song_details["media_url"] = media_url
    song_details["media_url_default"] = default_media_url
    # song_details["media_url"] = check_media_url(decrypt_url(
    #     song_more_details['encrypted_media_url']))
    # song_details["image"] = fix_image_url(song_details["image"])
    # song_details["title"] = fix_title(song_details["title"])
    # song_more_details["album"] = fix_title(song_more_details["album"])
    return SongDetails(
        **song_details,
        **song_more_details,
        is_320kbps = song_more_details["320kbps"]
    )  # .dict(exclude_none = True)


def get_album_details(album_id: str) -> AlbumDetails:
    album_results = jiosaavn_request({
        "__call": "content.getAlbumDetails",
        "albumid": album_id
    })
    if album_results is None:
        return None
    return AlbumDetails(**album_results, songs = list(
        map(fix_song_details, album_results["list"])))


def get_album_details_from_url(album_url: str) -> AlbumDetails:
    album_results = jiosaavn_request({
        "__call": "webapi.get",
        "token": album_url,
        "type": "album"
    })
    if album_results is None:
        return None
    return AlbumDetails(**album_results, songs = list(
        map(fix_song_details, album_results["list"])))


def get_playlist_details(playlist_id: str, page_no: int) -> PlaylistDetails:
    playlist_details = jiosaavn_request({
        "__call": "playlist.getDetails",
        "listid": playlist_id,
        "p": page_no
    })
    if playlist_details is None:
        return None
    return PlaylistDetails(
        **playlist_details, **playlist_details["more_info"], songs = list(
            map(fix_song_details, playlist_details["list"])))


def get_playlist_details_from_url(
        playlist_url: str, page_no: int) -> PlaylistDetails:
    playlist_details = jiosaavn_request({
        "__call": "webapi.get",
        "token": playlist_url,
        "type": "playlist",
        "p": page_no
    })
    if playlist_details is None:
        return None
    return PlaylistDetails(
        **playlist_details, **playlist_details["more_info"], songs = list(
            map(fix_song_details, playlist_details["list"])))


def get_lyrics(song_id: str):
    pass


################################################################################
# utility functions
################################################################################
def decrypt_url(url):
    enc_url = base64.b64decode(url.strip())
    default_dec_url = des_cipher.decrypt(enc_url, padmode = PAD_PKCS5).decode(
        'utf-8')
    dec_url = default_dec_url.replace("_96.mp4", "_320.mp3")
    return default_dec_url, dec_url


def fix_image_url(url):
    url = str(url)
    if 'http://' in url:
        url = url.replace("http://", "https://")
    url = url.replace('150x150', '500x500')
    return url


def fix_title(title):
    title = title.replace('&quot;', '')
    return title


def get_lyrics(link):
    try:
        if '/song/' in link:
            link = link.replace("/song/", '/lyrics/')
            link_ = link.split('/')
            link_[-2] = link_[-2] + '-lyrics'
            link = '/'.join(link_)
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            res = soup.find(class_ = 'u-disable-select')
            lyrics = str(res).replace("<span>", "")
            lyrics = lyrics.replace("</span>", "")
            lyrics = lyrics.replace("<br/>", "\n")
            lyrics = lyrics.replace('<p class="lyrics"> ', '')
            lyrics = lyrics.replace("</p>", '')
            lyrics = lyrics.split("<p>")[1]
            return (lyrics)
    except Exception:
        print_exc()
        return None


def expand_url(url):
    try:
        session = requests.Session()
        resp = session.head(url, allow_redirects = True)
        return (resp.url)
    except Exception as e:
        print("URL Redirect Error: ", e)
        return url


def check_media_url(dec_url):
    ex_dec_url = expand_url(dec_url)
    r = requests.head(ex_dec_url)
    if r.status_code != 200:
        fixed_dec_url = dec_url.replace(".mp3", '.mp4')
        fixed_dec_url = expand_url(fixed_dec_url)
        return fixed_dec_url
    return ex_dec_url
