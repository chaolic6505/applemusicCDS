
import darklyrics

def track_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    
    # print(result['track']['toptags']['tag'][1]['name'])

    
    

    
    try:
        result = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&track={TRACK_TITLE}&format=json").json()
        print(result['track']['toptags'])
        GENRE = "Not Specified" if not result['track']['toptags']['tag'][1]['name'] else result['track']['toptags']['tag'][1]['name']
        # print(GENRE)

    except IndexError:
        GENRE = "Not Specified"
       
        print('genre not found')
    
    return GENRE

def album_cover_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):

    try:
        result = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&album={TRACK_TITLE}&format=json").json()
        Album_Cover = "Single" if not result['album']['image'][ALBUM_COVER_SIZE]['#text'] else result['album']['image'][ALBUM_COVER_SIZE]['#text']
        #print(result)
        #print(Album_Cover)

    except KeyError:
        #print(result)
        print('No album cover found')
        Album_Cover = '../static/dc.png'

    return Album_Cover


def get_song_lyric(ARTIST_NAME,TRACK_NAME):
    #  try:
    #     LYRICS_FROM_API = lyricwikia.get_lyrics(f'{ARTIST_NAME}', f'{TRACK_NAME}')
    #     print(LYRICS_FROM_API)

    #  except KeyError:
    #      LYRICS_FROM_API ='None'
    
    #  print(LYRICS_FROM_API)
    try:
        print(darklyrics.get_lyrics(TRACK_NAME,ARTIST_NAME))
        return darklyrics.get_lyrics(TRACK_NAME,ARTIST_NAME)
        # print(darklyrics.get_lyrics(song))
        # print(darklyrics.get_songs(artist))
        # print(darklyrics.get_albums(artist))
        # print(darklyrics.get_all_lyrics(artist))
    except darklyrics.LyricsNotFound:
        return 'No lyrics found'
