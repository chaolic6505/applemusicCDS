from wtforms import Form, validators, StringField, PasswordField, SubmitField, SelectField
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'applemusic'
# remove warning message in the console
app.config['SQLALCHEMY_DATABASE_URI'] = ''
# remove warning message in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"

class SongInformationForm(Form):
    new_song_title = StringField(
        'Title', [validators.DataRequired(message='Field required')])
    new_song_artist = StringField(
        'Artist', [validators.DataRequired(message='Field required')])
    new_song_album = StringField('Album')
    new_song_genre = StringField('Genre')
    new_song_lyric = StringField('Lyric')
    new_song_rating = StringField('Rating (From 0 to 5)')
    new_song_lyrics = StringField(
        'Lyrics', [validators.Length(min=0, max=500)])
    submit = SubmitField('Save')


class Song(db.Model):
    _tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String)
    genre = db.Column(db.String)
    album = db.Column(db.String)
    big_album = db.Column(db.String)
    lyrics = db.Column(db.String)
    duration = db.Column(db.Integer)
    song_url = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))

    song_playlist_relationship = db.relationship('Artist', secondary=song_playlist_relationship, lazy='subquery',
                                                 backref=db.backref('Song', lazy=True))


class Artist(db.Model):
    _tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    genre = db.Column(db.Integer, nullable=False)
    album = db.Column(db.String, nullable=False)


class Playlist (db.Model):
    _tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_name = db.Column(db.String, nullable=False)
    song_in_playlist = db.Column(db.String, nullable=False)

    song_id = db.Column(db.Integer, db.ForeignKey("song.id"))
    song_playlist_relationship = db.relationship('Song', secondary=song_playlist_relationship, lazy='subquery',
                                                 backref=db.backref('Playlist', lazy=True))
