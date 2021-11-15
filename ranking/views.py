from django.shortcuts import render
from django.http import HttpResponse

import os

# Create your views here.
def index():
    return HttpResponse("welcome to ranking dashboard")
