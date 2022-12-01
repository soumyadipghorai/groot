import numpy as np 
from PIL import Image 
from rembg import remove 
from threading import Thread
from camera import VideoCamera
from rich.logging import RichHandler 
from werkzeug.utils import secure_filename
import os, sys, cv2, time, pyrebase, pickle, datetime, logging as LOGGING
from flask import Flask, render_template, request, session, Response, jsonify, redirect, url_for

# sign up logout 
# image capture 
# about page 
# bg recommendation
# pop up message

# LOGGING messages 
FORMAT = "%(message)s"
LOGGING.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)  
logger = LOGGING.getLogger("rich")

# upload image 
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
        return redirect(url_for('index'))
    
    if request.method == 'POST' : 
        email = request.form.get('email') 
        password = request.form.get('password') 
        
        try : 
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email 
            return redirect(url_for('index'))
        
        except : 
            return render_template('loginNew.html')  
    
    return render_template('loginNew.html')

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
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    
        return render_template('index_upload_and_display_image_page2.html')

# cartoonifying using clustering 
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

# create transperent image 
def convertImage(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    img = img.convert("RGBA")
 
    datas = img.getdata()
 
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    img.putdata(newData)
    img.save(output_image_path, "PNG")

# main pipeline 
def image_processing_pipeline() :
    img_file_path = session.get('uploaded_img_file_path', None)
    image = cv2.imread(img_file_path)
    
    rembg_curr = time.time()
    output = remove(image)  
    LOGGING.debug('background remove time --> ' + str(time.time() - rembg_curr))
    
    image_file_name = img_file_path.split('/')[-1].split('.')[0]
    LOGGING.debug('Extracted image file name --> ' + str(image_file_name))

    background = Image.open('static/backgrounds/mountain.jpg')
    backgroundcopy = background.copy()
    backgroundcopy = backgroundcopy.convert("RGBA")
    
    bg_removed_path = 'static/bg_removed/'+ image_file_name
    cv2.imwrite(bg_removed_path+'bg_removed.png',output)
    
    convertImage(
        input_image_path= bg_removed_path+'bg_removed.png', 
        output_image_path= 'static/transperantbg/'+ image_file_name + 'bg_removed_trans.png'
        )
    
    foregraound = Image.open('static/transperantbg/'+ image_file_name + 'bg_removed_trans.png')
    foregraoundCopy = foregraound.copy() 
    foregraoundCopy = foregraoundCopy.convert("RGBA")

    pasting_curr = time.time()
    backgroundcopy.paste(
            foregraoundCopy, 
            (int((background.width - foregraound.width)/2), background.height - foregraound.height), 
            foregraoundCopy
        ) #(x, y)

    LOGGING.debug("pasting image time --> " + str(time.time() - pasting_curr))
    bg_changed_path = 'static/bg_changed/'+ image_file_name
    backgroundcopy.save(bg_changed_path+'bg_changed.png')

    changed_img = cv2.imread(bg_changed_path+'bg_changed.png')

    # k_means_curr = time.time()
    # recommended_image = color_quantization(changed_img, 14)
    # LOGGING.debug("k_means cartoon time --> " +str(time.time() - k_means_curr))
    
    filter_curr = time.time()
    colored_image=cv2.bilateralFilter(changed_img,9,350,350)
    grayscale_image=cv2.cvtColor(changed_img, cv2.COLOR_BGR2GRAY)
    smooth_grayscale=cv2.medianBlur(grayscale_image,5)
    image_edge=cv2.adaptiveThreshold(smooth_grayscale,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    recommended_image = cv2.bitwise_and(colored_image,colored_image,mask=image_edge)
    LOGGING.debug("filter time --> " + str(time.time() - filter_curr))


    cartoonified_path = 'static/cartoonified/'+ image_file_name
    cv2.imwrite(cartoonified_path+'cartoonified.png',recommended_image)

    session['preprocessed_image'] = cartoonified_path+'cartoonified.png'


@app.route('/show_image')
def displayImage():
    image_processing_pipeline()
    img_file_path = session['preprocessed_image']
    LOGGING.debug('uploaded image path --> '+ str(img_file_path))
    return render_template('show_image.html', user_image = img_file_path)


@app.route('/captureImage', methods = ['GET', 'POST'])
def captureImage():
    if request.method == 'POST' : 
        if request.form.get('click') == 'Capture Image':
            
            LOGGING.debug('catpure pressed')
            
            camera = cv2.VideoCapture(0)
            success, frame = camera.read()
            now = datetime.datetime.now()
            p = os.path.sep.join(['static/shots', "shot_{}.png".format(str(now).replace(":",''))])
            cv2.imwrite(p, frame) 
            
            LOGGING.debug('path saved --> '+ str(p))
            LOGGING.debug('image saved')
            
            session['uploaded_img_file_path'] = p.replace('\\', '/') 
            
            return redirect(url_for('caturedImagePage'))

    return render_template('captureImage.html')
    
@app.route('/caturedImagePage', methods = ['GET', 'POST'])    
def caturedImagePage() : 
    
    image_file_path = session['uploaded_img_file_path']
    image_file_path = image_file_path.replace('\\', '/')
    
    LOGGING.debug('Captured_image_path --> ' + str(image_file_path))
    
    if request.method == 'POST' : 
    
        if request.form.get('click') == 'Capture Image' : 
            LOGGING.debug('button pressed from captured Image page ')
            return redirect(url_for('captureImage'))
    
        if request.form.get('predict') == 'Make Cartoon' : 
            return redirect(url_for('displayImage'))
    
    return render_template('caturedImagePage.html', user_image = image_file_path)


def video_stream():
    video_camera = None
    global_frame = None

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
   
if __name__=='__main__':
    app.run(debug = True, threaded=True)