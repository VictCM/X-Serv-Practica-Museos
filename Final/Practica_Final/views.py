from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
# Create your views here.

def home(request):
    return HttpResponse("Hola, no entiendo una puta mierda")

@csrf_exempt
def milogin(request):
    name_user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=name_user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")
