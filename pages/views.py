from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return HttpResponse("О нас")

def contact(request):
    return HttpResponse("Контакты")
