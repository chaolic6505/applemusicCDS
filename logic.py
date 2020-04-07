
def track_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):
    result = requests.get(
        f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&track={TRACK_TITLE}&format=json").json()

    # print(result['track']['toptags']['tag'][1]['name'])

    GENRE = "Not Specified" if not result['track']['toptags']['tag'][
        1]['name'] else result['track']['toptags']['tag'][1]['name']
    #print(GENRE)

    return GENRE


def album_cover_get_info(LAST_FM_API_key, ARTIST_NAME_COVER_SIZE, TRACK_TITLE, requests, ALBUM_COVER_SIZE):

    try:
        result = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={ARTIST_NAME_COVER_SIZE}&album={TRACK_TITLE}&format=json").json()
        Album_Cover = "Single" if not result['album']['image'][ALBUM_COVER_SIZE]['#text'] else result['album']['image'][ALBUM_COVER_SIZE]['#text']
        #print(result)

    except KeyError:
        print('No album cover found')
        Album_Cover = 'notfound'

    return Album_Cover
