from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from .models import Museo, Comentario
from .parsear import parsearXML
from django.template import Context
# Create your views here.

@csrf_exempt
def home(request):

    if request.method == "GET":
        DB_Museos = Museo.objects.all()
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
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he pinchado sobre Actualizar datos
            parsearXML('museos.xml')
            return redirect("/")

    template = get_template('RedTie/index.html')
    c = Context({'msg': form1})
    return HttpResponse(template.render(c))

@csrf_exempt
def milogin(request):
    name_user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=name_user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")
