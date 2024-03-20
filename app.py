import os
import subprocess
from flask import Flask, Response, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'webm', 'mp4', 'wmv', 'avi', 'flv', 'mov', 'webp', 'mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            video_filename = secure_filename(file.filename)
            audio_filename = ".".join(video_filename.split(".")[:-1]) + ".mp3"

            video_filepath = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)

            file.save(video_filepath)
            output = subprocess.run(['ffmpeg', '-i', video_filepath, audio_filepath], stdout=subprocess.PIPE).stdout.decode('utf-8')
            return redirect(url_for('download_file', name=audio_filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="POST" action="/" enctype="multipart/form-data">
      <input type="file" name="file" />
      <input type="submit" value="Upload" />
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
