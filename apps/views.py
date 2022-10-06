from django.shortcuts import render, HttpResponse
from datetime import datetime
# from apps.models import Contact
from django.contrib import messages 

# Create your views here.
def index(request) : 
    return render(request, 'index.html')