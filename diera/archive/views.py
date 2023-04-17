from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'archive/archive.html')

