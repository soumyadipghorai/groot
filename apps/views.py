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
    context = {
        "bannerText" : "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.", 
        "techUsed" : ['akmjancjnd', 'cnadcnd', 'dcjadcnd'], 
        'image-text' : ['ckdnc', 'adjdjn', 'sdjvndjn']
    } 
    if True : 
        for key in context.keys() : 
            context[key] = convertIntoGrootText(context[key])
    # if request.user.is_anonymous : 
    #     return ('/login')
    print(context)
    return render(request, 'index.html', context)

def loginPage(request) : 
    return render(request, 'login.html')

def about(request) : 
    return render(request, 'about.html')