from django.shortcuts import render, HttpResponse
from datetime import datetime
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from pyrebase import pyrebase

# cred = credentials.Certificate("C:\\Users\\aditi\\Desktop\\test folder\\testProject\\sampleApp\\serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()


# Create your views here.
firebaseConfig = {
  apiKey: "AIzaSyB2rhB-iVdfihzWhYwuhK8i9ZmE78vA0YU",
  authDomain: "groot-2d621.firebaseapp.com",
  projectId: "groot-2d621",
  storageBucket: "groot-2d621.appspot.com",
  messagingSenderId: "917162023467",
  appId: "1:917162023467:web:550f3abb96f4514a8f686e",
  measurementId: "G-4Y9NFD7GLT"
};

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

# converting each text on home page to I am groot
def convertIntoGrootText(text) : 
    corpus = ""
    for t in text : 
        corpus += t 

    grootCount = len(corpus)//10
    return ["I am Groot" for i in range(grootCount)]

def signIn(request):
    return render(request,"Login.html")

def home(request):
    return render(request,"Home.html")
 

def index(request) : 
    context = {
        "bannerText" : "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.", 
        "techUsed" : ['akmjancjnd', 'cnadcnd', 'dcjadcnd'], 
        'image-text' : ['ckdnc', 'adjdjn', 'sdjvndjn']
    }  
    # if True : 
    #     for key in context.keys() : 
    #         context[key] = convertIntoGrootText(context[key])
    # if request.user.is_anonymous : 
    #     return ('/login')
    print(context)
    return render(request, 'index.html', context)

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"Home.html",{"email":email})
 
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")
 
def signUp(request):
    return render(request,"Registration.html")
 
def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
    except:
        return render(request, "Registration.html")
    return render(request,"Login.html")