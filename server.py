import os
import boto3

from dotenv import load_dotenv
load_dotenv()
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
S3_Bucket_Name = 'cds-apple-music'
from flask import Flask, render_template, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone

app = Flask(__name__)

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


@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    db.session.add(Song(year="2020",rating=1, title="No time to die",
                        artist="Billie Eillish", language="English", genre="pop", duration="3:50"))
    db.session.add(Song(year="2010",rating=4, title="I don't care",
                        artist="Ed Sheeran ft Justin Bieber", language="English", genre="pop", duration="3:40"))
    db.session.commit()
    users = Song.query.all()
    # print(users[0].title)
    return render_template('index.html', users=users)
    # return render_template('index.html')


@app.route('/editSong/<song_id>')
def edit_song(song_id):

    return render_template('modifySongDetails.html')



@app.route('/deleteSong/<song_id>')
def delete_song(song_id):
    Song.query.filter_by(id=song_id).delete()
    # print(song_id)
    # print(song.title)
    db.session.commit()
    users = Song.query.all()
    return render_template('index.html', users=users)



# basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    # UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='audio',
    DROPZONE_MAX_FILE_SIZE=100,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=True
)
dropzone = Dropzone(app)
s3 = boto3.resource('s3',aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                s3.Bucket(S3_Bucket_Name).put_object(Key= f.filename, Body=f.filename)
    return render_template('index.html')

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
    app.run(debug=True, port=6969)

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
