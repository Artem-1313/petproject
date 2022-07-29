from django.http import HttpResponse
from django.shortcuts import render
from .utils import get_wheather
import requests

# Create your views here.


def whether(request):

    tmp = get_wheather
    return render(request, template_name="wheatherapp/wheather.html", context={"context": tmp})
