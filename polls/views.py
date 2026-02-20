from django.http import HttpResponse
from django.shortcuts import render  # noqa: F401


# Create your views here.
def index(_request):
    return HttpResponse("Hello, world. You're at the polls index.")
