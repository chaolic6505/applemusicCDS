from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, PasswordField, SubmitField, SelectField
from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy
from logic import track_get_info, album_cover_get_info, get_song_lyric
import requests
import os
import boto3

from dotenv import load_dotenv
load_dotenv()

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
LAST_FM_API_key = os.getenv("LAST_FM_API_key")

# Adjust album cover size by increasing 0 from 1 or 2 or 3
ALBUM_COVER_SIZE = 3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'applemusic'
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


song_playlist_relationship = db.Table('song_playlist_relationship',
                                      db.Column('song_id', db.Integer, db.ForeignKey(
                                          'song.id'), primary_key=True),
                                      db.Column('playlist_id', db.Integer, db.ForeignKey(
                                          'playlist.id'), primary_key=True),
                                      db.Column('artist_id', db.Integer, db.ForeignKey(
                                          'artist.id'), primary_key=True)
                                      )


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
    lyrics = db.Column(db.String)
    duration = db.Column(db.Integer)
    song_url = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    song_playlist_relationship = db.relationship('Artist', secondary=song_playlist_relationship, lazy='subquery',
                                                 backref=db.backref('Song', lazy=True))


class Album(db.Model):
    __tablename__ = "album"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_name = db.Column(db.String)
    year = db.Column(db.Integer)
    cover_photo = db.Column(db.String)
    artist = db.Column(db.String)
    songs = db.relationship('Song', backref='owner')


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


basedir = os.path.abspath(os.path.dirname(__file__))

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    DROPZONE_ALLOWED_FILE_TYPE='audio',
    DROPZONE_MAX_FILE_SIZE=100,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=False,
)


@app.route('/')
def home():
    
    db.create_all()
    return render_template('landingPage.html')


@app.route('/songs')
def song():
    form = SongInformationForm(request.form)
    db.session.commit()
    songs = Song.query.all()
    return render_template('songlist.html', songs=songs, form=form)

@app.route('/artists')
def artists():
    form = SongInformationForm(request.form)
    db.session.commit()
    songs = Song.query.all()
    return render_template('songlist.html', songs=songs, form=form)



@app.route('/album')
def disply_album():
    form = SongInformationForm(request.form)
    songs = Song.query.all()
    return render_template('albumlist.html', form=form, songs=songs)


@app.route('/editSong/<int:song_id>', methods=['POST', 'GET'])
def edit_song(song_id):
    form = SongInformationForm(request.form)
    song = Song.query.filter_by(id=song_id).first()
    return render_template('modifySongDetails.html', form=form, id=song_id, song=song)


@app.route('/saveSongInfo/<int:song_id>', methods=['POST', 'GET'])
def save_song_info(song_id):
    form = SongInformationForm(request.form)
    if request.method == 'POST' and form.validate():
        album_Cover = album_cover_get_info(
            LAST_FM_API_key, form.new_song_artist.data, form.new_song_title.data, requests, ALBUM_COVER_SIZE)
        genre = track_get_info(LAST_FM_API_key, form.new_song_artist.data,
                               form.new_song_title.data, requests, ALBUM_COVER_SIZE)
        lyric = get_song_lyric(form.new_song_artist.data,
                               form.new_song_title.data)
        song = Song.query.filter_by(id=song_id).first()
        song.title = form.new_song_title.data
        song.artist = form.new_song_artist.data
        song.album = album_Cover
        song.genre = genre
        song.rating = form.new_song_rating.data
        song.lyrics = lyric
        db.session.commit()
    songs = Song.query.all()
    print(songs)
    return redirect('/songs')


@app.route('/deleteSong/<int:song_id>')
def delete_song(song_id):
    print(song_id)
    form = SongInformationForm(request.form)
    Song.query.filter_by(id=song_id).delete()
    db.session.commit()
    songs = Song.query.all()
    return redirect('/songs')


dropzone = Dropzone(app)
s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,)
S3_Bucket_Name = 'cds-apple-music'


@app.route('/save', methods=['POST', 'GET'])
def save():
    form = SongInformationForm(request.form)
    if request.method == 'POST' and form.validate():
        Album_Cover = album_cover_get_info(
            LAST_FM_API_key, form.new_song_artist.data, form.new_song_title.data, requests, ALBUM_COVER_SIZE)
        song_genre = track_get_info(LAST_FM_API_key, form.new_song_artist.data,
                                    form.new_song_title.data, requests, ALBUM_COVER_SIZE)
        lyric = get_song_lyric(form.new_song_artist.data,
                               form.new_song_title.data)
        print(lyric)
        f = request.files.get('file')
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                s3.upload_file(f'./upload/{f.filename}', S3_Bucket_Name,
                               f'{f.filename}', ExtraArgs={'ContentType': 'audio/mpeg'})
                url = f"https://cds-apple-music.s3-us-west-2.amazonaws.com/{f.filename}"
                print(url)
                db.session.add(Song(rating=form.new_song_rating.data, title=form.new_song_title.data,
                                    artist=form.new_song_artist.data, album=Album_Cover, genre=song_genre, song_url=url, lyrics=lyric))
                db.session.add(Album(cover_photo=Album_Cover))
                db.session.commit()
    songs = Song.query.all()
    return redirect('/songs')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
if __name__ == "__main__":
    app.run(debug=True, port=5000)
