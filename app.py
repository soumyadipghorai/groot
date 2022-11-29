from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
import cv2
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pyrebase 
from rembg import remove 

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
 
# firebase authetication 
config = {
    'apiKey': "AIzaSyB2rhB-iVdfihzWhYwuhK8i9ZmE78vA0YU",
    'authDomain': "groot-2d621.firebaseapp.com",
    'projectId': "groot-2d621",
    'storageBucket': "groot-2d621.appspot.com",
    'messagingSenderId': "917162023467",
    'appId': "1:917162023467:web:550f3abb96f4514a8f686e",
    'measurementId': "G-4Y9NFD7GLT", 
    'databaseURL' : ""
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth() 

app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/signUp")
def signUp() : 
    return render_template("signUp.html")


@app.route('/login', methods = ['POST', 'GET'])
def login() : 
    if ('user' in session) : 
        return render_template('index.html')
    if request.method == 'POST' : 
        email = request.form.get('email') 
        password = request.form.get('password') 
        try : 
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email 
            return render_template('index.html')
        except : 
            return render_template('loginNew.html')  
    return render_template('loginNew.html')

# @app.route('/signUp', methos = ['GET', 'POST'])
# def signUp() :
#     if request.method == 'POST' : 
#         email = request.form.get('email')
#         password = request.form.get('password')
#         try : 
#             user = auth.create_user_with_email_and_password(email, password)
#             return render_template('loginNew.html')
#         except : 
#             pass 
    

@app.route('/logout')    
def logout() : 
    session.pop('user')
    return render_template('index.html')

@app.route('/Imageupload')
def uploadPage() : 
    return render_template('index_upload_and_display_image.html')

@app.route('/Imageupload',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        uploaded_img = request.files['uploaded-file']
        img_filename = secure_filename(uploaded_img.filename)
        image = cv2.imread(img_filename)
        img_filename = remove(image)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('index_upload_and_display_image_page2.html')


def color_quantization(img, k):
    data = np.float32(img).reshape((-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

@app.route('/show_image')
def displayImage():
    img_file_path = session.get('uploaded_img_file_path', None)
    # img_file_path = remove(open(img_file_path))
    return render_template('show_image.html', user_image = img_file_path)
 
if __name__=='__main__':
    app.run(debug = True)