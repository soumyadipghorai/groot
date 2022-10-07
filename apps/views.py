from django.shortcuts import render, HttpResponse
from datetime import datetime
# from apps.models import Contact
from django.contrib import messages 

# Create your views here.
def index(request) : 
    return render(request, 'index.html')

def loginPage(request) : 
    return render(request, 'login.html')

def about(request) : 
    return render(request, 'about.html')