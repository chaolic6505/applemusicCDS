
import darklyrics
import lyricwikia

def track_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    try:
        result = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&track={TRACK_TITLE}&format=json").json()
    except IndexError:
        genre = "Not Specified"
        print('genre not found')
    except KeyError:
        genre = "Not Found"
        # return genre

def album_cover_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    try:
        result = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&album={TRACK_TITLE}&format=json").json()
        album_Cover = "Single" if not result['album']['image'][ALBUM_COVER_SIZE][
            '#text'] else result['album']['image'][ALBUM_COVER_SIZE]['#text']
    except KeyError:
        album_Cover = '../static/dc.png'
    except IndexError:
        album_Cover = '../static/dc.png'
    return album_Cover

def get_song_lyric(ARTIST_NAME,TRACK_NAME):
    try:
        lyrics = lyricwikia.get_lyrics(f'{ARTIST_NAME}', f'{TRACK_NAME}')
        return lyrics
    except KeyError:
        return 'No lyrics found'
    except IndexError:
        return 'No lyrics found'
    except SyntaxError:
        return 'No lyrics found'
