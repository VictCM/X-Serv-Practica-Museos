from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import get_template
from .models import Museo, Comentario, Pag_Usuario, Museo_Usuario
from .parsear import parsearXML
from django.template import Context
import time
# Create your views here.

def Login_info(request):
    if request.user.is_authenticated():
        log = "<p>Logged in as " + request.user.username
        log += "<a href='/logout'> Logout </a></p>"
    else:
        log = "<form action='/login' method='post'>"
        log += "user: <input type= 'text' name='user'>"
        log += "password: <input type= 'password' name='password'>"
        log += "<input type= 'submit' value='enviar'>"
        log += "</form>"
        log += "<a href='/registro/'>Register </a>"
    return log


@csrf_exempt
def Login(request):
    user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")

@csrf_exempt
def home(request):

    if request.method == "GET":
        DB_Museos = Museo.objects.all()
        DB_Users = User.objects.all()
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
    c = Context({'msg': form1 ,'user': users, 'login': Login_info(request)})
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
        # Me creo el usuario y la pagina asociada a el
        user = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']
        user_object = User.objects.create_user(user, email, password)
        user_object.save()
        titulo = str("Página de " + user)
        print(titulo + "en Registro")
        pag_object = Pag_Usuario(USUARIO = user, TITULO = titulo)
        pag_object.save()
        form1 = " "
        #url = "http://localhost:1234/"
        return redirect("http://localhost:1234/")
    else:
        form1 = "Method not allowed"
    print(form1)
    template = get_template('RedTie/index.html')
    c = Context({'user': form1, 'login': Login_info(request)})
    return HttpResponse(template.render(c))

@csrf_exempt
def Pagina_Usuario(request, user):
    print(user)
    DB_Museos = Museo.objects.all()
    DB_Users = User.objects.all()
    pag = Pag_Usuario.objects.get(USUARIO=user)
    if request.method == "GET":
        if len(DB_Museos) == 0: #Significa que la base de datos esta vacia
            museos = "No hay datos disponibles en la base de datos"
            # POST para cargar los datos
            museos += "<br>¿Actualizar Datos?<br>"
            museos += "<form action='" + user + "' method='post'>"
            museos += "<input type= 'hidden' name='opcion' value='1'>"
            museos += "<input type= 'submit' value='Actualizar'>"
            museos += "</form>"
        else:
            museos = "<br>Los museos para esconderse de Thanos:<br><br>"
            for museo in DB_Museos:
                museos += "<a href=" + museo.CONTENT_URL + ">" + museo.NOMBRE + "</a><br>"
                museos += "Dirección: " + museo.NOMBRE_VIA + " "
                museos += museo.CLASE_VIAL + " " + museo.TIPO_NUM + " "
                museos += museo.NUM + ", " + museo.PLANTA + ", "
                museos += museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
                museos += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", "
                museos += museo.DISTRITO + "<br>"
                if user == request.user.username:
                    museos += "<form action='" + user + "' method='post'>"
                    museos += "<input type= 'hidden' name='museo' value=" + museo.ID_ENTIDAD +">"
                    museos += "<input type= 'hidden' name='opcion' value='3'>"
                    museos += "<input type= 'submit' value='Añadir'>"
                    museos += "</form><br><br>"
        if user == request.user.username:
            # formulario para Cambiar titulo
            form1 = "<br>¿Cambiar Titulo? "
            form1 += "<form action='" + user + "' method='post'>"
            form1 += "Titulo: <input type= 'text' name='titulo'>"
            form1 += "<input type= 'hidden' name='opcion' value='2'>"
            form1 += "<input type= 'submit' value='enviar'>"
            form1 += "</form>"
            # Muestro todos los museos y doy la opcion de añadirlos
        else:
            form1 = "No eres propietario de la pagina"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # He pinchado sobre Actualizar datos
            parsearXML('museos.xml')
        elif opcion == "2":
            titulo = request.POST['titulo']
            print(titulo + "en Cambio de pag")
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            pag_object.TITULO = titulo
            pag_object.save()
        elif opcion == "3":
            ID_museo = request.POST['museo']
            print(ID_museo)
            museo = Museo.objects.get(ID_ENTIDAD = ID_museo)
            fecha = str(time.ctime())
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            user_museo_object = Museo_Usuario(MUSEO = museo, FECHA = fecha)  ###problema aqui
            user_museo_object.save()
            pag_object.MUSEOS = user_museo_object
            pag_object.save()
        else:
            respuesta = "Method not Allowed"
        url = "http://localhost:1234/" + user
        return redirect(url)
    else:
        respuesta = "Method not Allowed"

    template = get_template('RedTie/pag_user.html')
    c = Context({'user': user, 'titulo': pag.TITULO,'museos': museos, 'peticion': form1, 'login': Login_info(request)})
    return HttpResponse(template.render(c))

def Añadir(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            # formulario para añadir Comentario
            form2 += "<br>¿Añadir Comentario? "
            form2 += "<form action='/aparcamientos/" + str(id) + "' method="
            form2 += "'post'>Texto: <input type= 'text' name='texto'>"
            form2 += "<input type= 'hidden' name='opcion' value='1'>"
            form2 += "<input type= 'submit' value='enviar'>"
            form2 += "</form>"
            # formulario para añadir
            form1 += "<br>¿Añadir a tu pagina? "
            form1 += "<form action='/aparcamientos/" + str(id)
            form1 += "'method='post'><input type= 'hidden' name='opcion'"
            form1 += "value='2'><input type= 'submit' value='enviar'>"
            form1 += "</form>"


def Usuario_XML(request):
    pag = Pag_Usuario.objects.get(USUARIO=user)
    if request.method == "GET":
        museos = pag.MUSEOS.all()
        if len(museos) == 0:
            lista_museos = "No hay ningun museo añadido"
            form1 = " "
        else:
            form1 = "Los museos añadidos son: <br>"
            for museo in museos:
                form1 += "<a href=" + museo.CONTENT_URL + ">" + museo.NOMBRE + "</a><br>"
                form1 += "Dirección: " + museo.NOMBRE_VIA + " "
                form1 += museo.CLASE_VIAL + " " + museo.TIPO_NUM + " "
                form1 += museo.NUM + ", " + museo.PLANTA + ", "
                form1 += museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
                form1 += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", "
                form1 += museo.DISTRITO + "<br><br>"