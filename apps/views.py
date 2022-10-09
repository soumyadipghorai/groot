from django.shortcuts import render, HttpResponse
from datetime import datetime
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

# Create your views here.

# converting each text on home page to I am groot
def convertIntoGrootText(text) : 
    corpus = ""
    for t in text : 
        corpus += t 

    grootCount = len(corpus)//10
    return ["I am Groot" for i in range(grootCount)]

def index(request) : 
    text = {
        'banner-text' : 'lorkjcdjcndem', 
        'tech-used' : ['akmjancjnd', 'cnadcnd', 'dcjadcnd'], 
        'image-text' : ['ckdnc', 'adjdjn', 'sdjvndjn']
    }
    if True : 
        for key in text.keys() : 
            text[key] = convertIntoGrootText(text[key])
    # if request.user.is_anonymous : 
    #     return ('/login')
    print(text)
    return render(request, 'index.html', text)

def loginPage(request) : 
    return render(request, 'login.html')

def about(request) : 
    return render(request, 'about.html')