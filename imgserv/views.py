from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, FileResponse
import os


def index(request):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    p = os.path.join(PROJECT_ROOT, 'sticker.webp')
    f = open(p, 'rb')
    return HttpResponse(f.read(), 'image/webp')


def path(request):
    return HttpResponse(os.getcwd())
