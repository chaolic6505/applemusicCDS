from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, PasswordField, SubmitField, SelectField
from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import boto3

from dotenv import load_dotenv
load_dotenv()
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
LAST_FM_API_key = os.getenv("LAST_FM_API_key")

# Adjust album cover size by increasing 0 from 1 or 2 or 3
ALBUM_COVER_SIZE = 0

S3_Bucket_Name = 'cds-apple-music'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'applemusic'
# remove warning message in the console
app.config['SQLALCHEMY_DATABASE_URI'] = ''
# remove warning message in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)

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
    new_song_rating = SelectField('Rating (From 0 to 5)',
                                  choices=[('0', '0'), ('1', '1'), ('2', '2'),
                                           ('3', '3'), ('4', '4'), ('5', '5')],
                                  default='unrated')
    # lyrics = StringField('Lyrics', [validators.Length(min=0, max=500)])
    submit = SubmitField('Save')


class Song(db.Model):
    _tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String)
    language = db.Column(db.String(10))
    genre = db.Column(db.String)
    album = db.Column(db.String)
    duration = db.Column(db.Integer, nullable=False)
    count_total_played = db.Column(db.Integer)

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


basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='audio',
    DROPZONE_MAX_FILE_SIZE=100,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=True

)


@app.route('/')
def home():
    return render_template('header.html')


@app.route('/songs')
def index():

    form = SongInformationForm(request.form)
    response1 = requests.get(
        f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist=Billie Eillish&album=No time to die&format=json")

    response2 = requests.get(
        f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist=Ed Sheeran&album=I don't care&format=json")
    Billie = response1.json()

    # print(Billie['album']['image'][1]['#text'] == '')
    Billie_Album_Cover = "Single" if Billie['album']['image'][ALBUM_COVER_SIZE][
        '#text'] == '' else Billie['album']['image'][ALBUM_COVER_SIZE]['#text']
    # print(Billie_Album_Cover)
    Ed = response2.json()

    db.drop_all()
    db.create_all()
    db.session.add(Song(year="2020", rating=1, title="No time to die",
                        artist="Billie Eillish", language="English", album=Billie_Album_Cover, genre="pop", duration="3:50"))
    db.session.add(Song(year="2010", rating=4, title="I don't care",
                        artist="Ed Sheeran ft Justin Bieber", language="English", album=Ed['album']['image'][ALBUM_COVER_SIZE]['#text'], genre="pop", duration="3:40"))
    db.session.commit()
    songs = Song.query.all()
    # print(songs[0].title)
    return render_template('index.html', songs=songs, form=form)

    # return render_template('index.html')


@app.route('/editSong/<song_id>', methods=['POST', 'GET'])
def edit_song(song_id):
    form = SongInformationForm()
    return render_template('modifySongDetails.html', form=form, id=song_id)


@app.route('/saveSongInfo/<song_id>', methods=['POST', 'GET'])
def save_song_info(song_id):
    # print(song_id)
    form = SongInformationForm(request.form)
    if request.method == 'POST' and form.validate():
        response = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={form.new_song_artist.data}&album={form.new_song_title.data}&format=json")
        answer = response.json()

        # Adjust album cover size by increasing 0 to 1, or,2 ,3
        Album_Cover = "Single" if answer['album']['image'][ALBUM_COVER_SIZE][
            '#text'] == '' else answer['album']['image'][ALBUM_COVER_SIZE]['#text']
        # print(form.new_song_title.data)
        # print(form.new_song_artist.data)
        # print(form.new_song_rating.data)
        song = Song.query.filter_by(id=song_id).first()
        # print(song.title)
        # print(song.artist)
        # print(song.rating)
        song.title = form.new_song_title.data
        song.artist = form.new_song_artist.data
        song.album = Album_Cover
        song.genre = form.new_song_genre.data
        song.rating = form.new_song_rating.data

        db.session.commit()
    songs = Song.query.all()
    print(songs)
    return render_template('index.html', songs=songs, form=form)


@app.route('/deleteSong/<song_id>')
def delete_song(song_id):
    form = SongInformationForm(request.form)
    Song.query.filter_by(id=song_id).delete()
    # print(song_id)
    # print(song.title)
    db.session.commit()
    songs = Song.query.all()
    return render_template('index.html', songs=songs, form=form)


dropzone = Dropzone(app)

s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,)


@app.route('/save', methods=['POST', 'GET'])
def save():
    form = SongInformationForm(request.form)
    if request.method == 'POST' and form.validate():
        response = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LAST_FM_API_key}&artist={form.new_song_artist.data}&album={form.new_song_title.data}&format=json")
        answer = response.json()

        # Adjust album cover size by increasing 0 to 1, or,2 ,3
        Album_Cover = "Single" if answer['album']['image'][ALBUM_COVER_SIZE][
            '#text'] == '' else answer['album']['image'][ALBUM_COVER_SIZE]['#text']

        # print(response.json())
        # print(form.new_song_title.data)
        # print(form.new_song_artist.data)
        # print(form.new_song_rating.data)

        db.session.add(Song(year="???", rating=form.new_song_rating.data, title=form.new_song_title.data,
                            artist=form.new_song_artist.data, language="???", album=Album_Cover, genre=form.new_song_genre.data, duration="???"))
        db.session.commit()

    songs = Song.query.all()
    return render_template('index.html', songs=songs, form=form)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                # client.put_object(Bucket='cds-apple-music',
                #     Key=f.filename, Body=f.filename, ContentType='audio/mpeg')

        s3.upload_file(f'./upload/{f.filename}', S3_Bucket_Name,
                           f'{f.filename}', ExtraArgs={'ContentType': 'audio/mpeg'})
        # s3.Object(S3_Bucket_Name, f.filename).upload_fileobj(
        #     f.filename, ExtraArgs={'ContentType': 'audio/mpeg'})
        form = SongInformationForm(request.form)
        songs = Song.query.all()
        return render_template('index.html', songs=songs, form=form)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     search = User(request.form)
#     if request.method == 'GET':
#         return User
#
#     return render_template('index.html', form=search)
#
# @app.route('/user/<username>')
# def show_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('show_user.html', user=user)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     search = User(request.form)
#     if request.method == 'GET':
#         return User
#
#     return render_template('index.html', form=search)

#
# @app.route('/user/<username>')
# def show_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('show_user.html', user=user)
