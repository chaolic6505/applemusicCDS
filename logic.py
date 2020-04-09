
import darklyrics

def track_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    try:
        result = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&track={TRACK_TITLE}&format=json").json()
        print(result['track']['toptags'])
        genre = "Not Specified" if not result['track']['toptags']['tag'][1]['name'] else result['track']['toptags']['tag'][1]['name']
    except IndexError:
        genre = "Not Specified"
        print('genre not found')
    return genre

def album_cover_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    try:
        result = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&album={TRACK_TITLE}&format=json").json()
        album_Cover = "Single" if not result['album']['image'][ALBUM_COVER_SIZE]['#text'] else result['album']['image'][ALBUM_COVER_SIZE]['#text']
    except KeyError:
        print('No album cover found')
        album_Cover = '../static/dc.png'
    return album_Cover

def get_song_lyric(ARTIST_NAME,TRACK_NAME):
    try:
        print(darklyrics.get_lyrics(TRACK_NAME,ARTIST_NAME))
        return darklyrics.get_lyrics(TRACK_NAME,ARTIST_NAME)
    except darklyrics.LyricsNotFound:
        return 'No lyrics found'
