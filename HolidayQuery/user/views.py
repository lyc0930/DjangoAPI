from django.shortcuts import render
from django.http import HttpResponse


def signup(request):
    message = "signup"
    return HttpResponse(message)


def login(request):
    message = "login"
    return HttpResponse(message)
