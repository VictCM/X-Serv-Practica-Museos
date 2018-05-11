from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import get_template
from .models import Museo, Comentario
from .parsear import parsearXML
from django.template import Context
# Create your views here.

@csrf_exempt
def home(request):

    if request.method == "GET":
        DB_Museos = Museo.objects.all()
        DB_Users = User.objects.all()
        print(User.objects.all())
        if len(DB_Museos) == 0: #Significa que la base de datos esta vacia
            form1 = "No hay datos disponibles en la base de datos"
            # POST para cargar los datos
            form1 += "<br>¿Actualizar Datos?<br>"
            form1 += "<form action='/' method='post'>"
            form1 += "<input type= 'hidden' name='opcion' value='1'>"
            form1 += "<input type= 'submit' value='Actualizar'>"
            form1 += "</form>"
        else:
            form1 = "<br>Los museos para esconderse de Thanos:<br><br>"
            for museo in DB_Museos:
                form1 += "<a href=" + museo.CONTENT_URL + ">" + museo.NOMBRE + "</a><br>"
                form1 += "Dirección: " + museo.NOMBRE_VIA + " "
                form1 += museo.CLASE_VIAL + " " + museo.TIPO_NUM + " "
                form1 += museo.NUM + ", " + museo.PLANTA + ", "
                form1 += museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
                form1 += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", "
                form1 += museo.DISTRITO + "<br><br>"
        if len(DB_Users) == 0:
            users = "No se ha dado con ningún Vengador"
        else:
            users = "Solo han venido: <br>"
            for user in DB_Users:
                users += user.username + "<br>"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he pinchado sobre Actualizar datos
            parsearXML('museos.xml')
            return redirect("/")

    template = get_template('RedTie/index.html')
    c = Context({'msg': form1 ,'user': users})
    return HttpResponse(template.render(c))


@csrf_exempt
def Registro(request):
    if request.method == "GET":
        form1 = "Crear Usuario: "
        form1 += "<form action='/registro/' method='post'>"
        form1 += "User: <input type= 'text' name='user'>"
        form1 += "Email: <input type= 'text' name='email'>"
        form1 += "Password: <input type= 'password' name='password'>"
        form1 += "<input type= 'submit' value='enviar'>"
        form1 += "</form>"
    elif request.method == "POST":
        user = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(user, email, password)
        user.save()
        form1 = " "
        #url = "http://localhost:1234/"
        return redirect("http://localhost:1234/")
    else:
        form1 = "Method not allowed"
    print(form1)
    template = get_template('RedTie/index.html')
    c = Context({'user': form1})
    return HttpResponse(template.render(c))

@csrf_exempt
def Usuario(request, user):
    pag = Pag_Usuario.objects.get(Usuario=user)
    if request.method == "GET":
        museos = pag.Museos.all()


@csrf_exempt
def milogin(request):
    name_user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=name_user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")
