from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import Form,validators, StringField, PasswordField,SubmitField,SelectField
from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy
import os
import boto3

from dotenv import load_dotenv
load_dotenv()
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
S3_Bucket_Name = 'cds-apple-music'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'applemusic'
#remove warning message in the console
app.config['SQLALCHEMY_DATABASE_URI'] = ''
#remove warning message in the console
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


class EditSongInformationForm(Form):
    new_song_title = StringField('Title', [validators.DataRequired(message='Field required')])
    new_song_artist = StringField('Artist', [validators.DataRequired(message='Field required')])
    new_song_rating = SelectField('Rating (From 0 to 5)',
                                 choices=[('0', '0'),('1', '1'), ('2', '2'), ('3', '3'),('4', '4'), ('5', '5')],
                                 default='HI')
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


@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    db.session.add(Song(year="2020", rating=1, title="No time to die",
                        artist="Billie Eillish", language="English", genre="pop", duration="3:50"))
    db.session.add(Song(year="2010", rating=4, title="I don't care",
                        artist="Ed Sheeran ft Justin Bieber", language="English", genre="pop", duration="3:40"))
    db.session.commit()
    users = Song.query.all()
    # print(users[0].title)
    return render_template('index.html', users=users)
    # return render_template('index.html')


@app.route('/editSong/<song_id>',methods=['POST', 'GET'])
def edit_song(song_id):
    form = EditSongInformationForm()
    return render_template('modifySongDetails.html',form=form,id=song_id)

@app.route('/saveSongInfo/<song_id>',methods=['POST', 'GET'])
def save_song_info(song_id):
    #print(song_id)
    form = EditSongInformationForm(request.form)
    if request.method == 'POST' and form.validate():
        # print(form.new_song_title.data)
        # print(form.new_song_artist.data)
        # print(form.new_song_rating.data)
        song =  Song.query.filter_by(id=song_id).first()
        # print(song.title)
        # print(song.artist)
        # print(song.rating)
        song.title = form.new_song_title.data
        song.artist = form.new_song_artist.data
        song.rating = form.new_song_rating.data

        db.session.commit()
    users = Song.query.all()
    print(users)
    return render_template('index.html',users=users)


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
s3 = boto3.resource('s3', aws_access_key_id=S3_ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                s3.Bucket(S3_Bucket_Name).put_object(
                    Key=f.filename, Body=f.filename)
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
