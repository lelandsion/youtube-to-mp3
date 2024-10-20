from flask import Flask, request, jsonify, send_file, after_this_request
import yt_dlp
import re
import os


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    youtube_link = request.form.get('youtube_link')

    # If no link is inputted return nothing, continue
    if not youtube_link:
        return '', 204

    # If an invalid link is inputted, return nothing, continue
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})$'
    if not re.match(youtube_regex, youtube_link):
        print("Please input a valid YouTube URL.")  # log the message
        return '', 204
    try:
        # Ensure the downloads directory exists
        os.makedirs('downloads', exist_ok=True)

        # Setup yt-dlp options for audio extraction
        ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio quality
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save with video title
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,  # Avoid downloading playlists if a video URL is provided
        }

        # Use yt-dlp to download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=True)
            filename = ydl.prepare_filename(info_dict)


        # Create the MP3 filename
        mp3_filename = f"downloads/{re.sub(r'[<>:\"/\\|?*]', '', info_dict['title'])}.mp3"

        # Check if the MP3 file was created successfully
        if not os.path.exists(mp3_filename):
            return jsonify({"error": "Conversion to MP3 failed."}), 500

        # Send the MP3 file to the user
        return send_file(mp3_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)


