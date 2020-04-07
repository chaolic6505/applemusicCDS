# applemusicCDS

<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://static.billboard.com/files/media/streaming-illustration-v-2019-billboard-1548-1024x677.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Music Streaming Clone</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> A music management application that allow users to add, play, edit and delete their personal playlist.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [TO-DOs](#todo)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>
Apple music is one of the most popular music streaming platform, however, a web player of Apple Music was never developed. That's why we want to create a music streaming web application that works similar to Apple Music.

## 🏁 Getting Started <a name = "getting_started"></a>
  

### Prerequisites
This is the complete list of dependencies to run this program, which are included in the requirement.txt.
<br>
You will need to run ```pip3 install -r requirements.txt``` to install them.

```
appdirs==1.4.3
autopep8==1.5
boto3==1.12.31
botocore==1.15.31
Click==7.0
distlib==0.3.0
docutils==0.15.2
filelock==3.0.12
Flask==1.1.1
Flask-Dropzone==1.5.4
Flask-SQLAlchemy==2.4.1
Flask-WTF==0.14.3
itsdangerous==1.1.0
Jinja2==2.11.1
jmespath==0.9.5
MarkupSafe==1.1.1
pycodestyle==2.5.0
python-dateutil==2.8.1
python-dotenv==0.12.0
s3transfer==0.3.3
six==1.14.0
SQLAlchemy==1.3.13
urllib3==1.25.8
virtualenv==20.0.7
Werkzeug==1.0.0
WTForms==2.2.1
```



## 🎈 Usage <a name="usage"></a>
A .env folder will need to have the following keys: 
* AWS client key and client secret from aws
* S3 bucket name 
* Last.fm API key 

## 🚀 Start The Program <a name = "deployment"></a>
To start the program you will need to go to the program directory and open up your terminal and
1.  Type ```pip3 install``` and Enter to download all the dependencies
2.  Type ```source venv/bin/activate``` to get into the virtual environemnt
3.  Type ``` python3 server.py``` to start the program

## ⛏️ Built Using <a name = "built_using"></a>
- [SQLalchemy](https://www.sqlalchemy.org/) - ORM
- [SQLite](https://www.sqlite.org/index.html) - Database
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Server Framework
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) - Templating
- [Python3](https://www.python.org/) - Server Environment

## TO-DOs <a name = "todo"></a>

There are still some functionalities we are working on
- Music player is not fully function, ie. users are not able to skip songs
- Users are not able to create a sub-playlist
- User authentication

## ✍️ Developers <a name = "authors"></a>
- Cindy Le
- Steven Chen
- Daniel Na


## 📜 License <a name = "license"></a>

The MIT License (MIT)

Copyright (c) 2015 Eugene Obrezkov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

