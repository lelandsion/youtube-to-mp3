from flask import Flask, request, jsonify, send_file, after_this_request
from pytube import YouTube
import os


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    youtube_link = request.form.get('youtube_link')

    try:
        yt = YouTube(youtube_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = f"{yt.title}.mp3"
        audio_stream.download(filename=filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)


