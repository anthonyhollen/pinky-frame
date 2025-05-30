from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import uuid
from display import display_image

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4()}.png"
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Resize and save the image
            img = Image.open(file)
            img = img.convert('RGB')  # optional
            img = img.resize((800, 480))  # Resize to match Inky display
            img.save(path, optimize=True)

            return redirect(url_for('index'))

    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/display/<filename>')
def display(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    display_image(path)  # Trigger e-ink display
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
