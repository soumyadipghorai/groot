from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
# from rembg import remove  
# import PIL.Image
# if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
#     PIL.Image.Resampling = PIL.Image

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
UPLOAD_FOLDER_PREPROCESSED = 'static/preprocessed/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PREPROCESSED'] = UPLOAD_FOLDER_PREPROCESSED
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def color_quantization(img, k):
    # Transform the image
    data = np.float32(img).reshape((-1, 3))

    # Determine criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    # Implementing K-Means
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
# @app.route('/')
# def home():
#     return render_template('indexCopy.html')

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/')
def homeindex():
    return render_template('indexCopy.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # print(file)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        input_image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], file))
        output = color_quantization(input_image, 14)
        cv2.imshow(input_image)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER_PREPROCESSED'], output))

        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('indexCopy.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    return render_template('result.html')
 
if __name__ == "__main__":
    app.run(debug=True)