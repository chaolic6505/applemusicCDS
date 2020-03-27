class Song:
    __tablename__ = 'songs'

    def __init__(self, year, title, artist, language, genre, album, duration=0, count=0, lyrics=None):
        self.title = title
        self.year = year
        self.artist = artist
        self.duration = duration
        self.lyrics = lyrics
        self.language = language
        self.genre = genre
        self.count = genre
        self.album = album

    def get_artist(self):
        return self.artist

    def get_duration(self):
        return self.duration

    def get_title(self):
        return self.title

    def get_lyrics(self):
        return self.lyrics

    def get_language(self):
        return self.language

    def get_play_count(self):
        return self.count

    def get_genre(self):
        return self.genre

    def get_album(self):
        return self.album

    def __str__(self):
        return {'year': self.year, 'title': self.title, 'artist': self.artist, 'language': self.language, 'genre': self.genre, 'duration': self.duration, "Album": self.album}


class Album:
    __tablename__ = 'albums'

    def __init__(self, album_name, year, cover_photo, artist):
        self.album_name = album_name
        self.year = year
        self.cover_photo = cover_photo
        if artist is None:
            self.artists = Artist("Various Artists")
        else:
            self.artists = [artist]
        self.tracks = []

    def add_song(self, song, position=None):
        if position is None:
            self.tracks.append(song)
        else:
            self.tracks.insert(position, song)

    def get_year(self):
        return self.year

    def get_cover_photo(self):
        return self.cover_photo

    # def get_song_position(self, song_postion):
    #     return self.song_postion

    def get_artists_names(self):
        return self.artists.name


class Artist:
    __tablename__ = 'artists'

    def __init__(self, name, artist_photo=None, country=None, genre=None):
        self.name = name
        self.country = country
        self.genre = genre
        self.artist_photo = artist_photo
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)

    def get_artist_name(self):
        return self.name

    def get_artist_photo(self):
        return self.artist_photo

    def get_artist_country(self):
        return self.country

    def get_artist_genre(self):
        return self.genre


class Playlist:
    def __init__(self, name, playlist_photo):
        self.name = name
        self.playlist_photo = playlist_photo
        self.playlist = []

    def add_song(self, song):
        self.playlist.append(song)

    def get_postion_song(self, song):
        return self.playlist.index(song)

    def search_song(self, song):
        for each_song in self.playlist:
            if each_song.tile.lower() == song.title.lower():
                return each_song

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)

    def get_artist(self):
        return self.artist

    def get_duration(self):
        return self.duration

    def get_title(self):
        return self.title

    def get_lyrics(self):
        return self.lyrics

    def get_language(self):
        return self.language

    def get_play_count(self):
        return self.count

    def get_genre(self):
        return self.genre

    def get_album(self):
        return self.album

    def __str__(self):
        return {'year': self.year, 'title': self.title, 'artist': self.artist, 'language': self.language, 'genre': self.genre, 'duration': self.duration, "Album": self.album}


class Album:
    def __init__(self, album_name, year, cover_photo, artist):
        self.album_name = album_name
        self.year = year
        self.cover_photo = cover_photo
        if artist is None:
            self.artists = Artist("Various Artists")
        else:
            self.artists = [artist]
        self.tracks = []

    def add_song(self, song, position=None):
        if position is None:
            self.tracks.append(song)
        else:
            self.tracks.insert(position, song)

    def get_year(self):
        return self.year

    def get_cover_photo(self):
        return self.cover_photo

    # def get_song_position(self, song_postion):
    #     return self.song_postion

    def get_artists_names(self):
        return self.artists.name


class Artist:
    def __init__(self, name, artist_photo=None, country=None, genre=None):
        self.name = name
        self.country = country
        self.genre = genre
        self.artist_photo = artist_photo
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)

    def get_artist_name(self):
        return self.name

    def get_artist_photo(self):
        return self.artist_photo

    def get_artist_country(self):
        return self.country

    def get_artist_genre(self):
        return self.genre


class Playlist:
    def __init__(self, name, playlist_photo):
        self.name = name
        self.playlist_photo = playlist_photo
        self.playlist = []

    def add_song(self, song):
        self.playlist.append(song)

    def get_postion_song(self, song):
        return self.playlist.index(song)

    def search_song(self, song):
        for each_song in self.playlist:
            if each_song.tile.lower() == song.title.lower():
                return each_song

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)
