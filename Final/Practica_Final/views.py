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

acces = 0

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
    username = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")

@csrf_exempt
def home(request):
    if request.method == "GET":
        peticion = "No hay ningun museo todavía"
        if acces ==0:
            DB_Museos = Museo.objects.all()
            Museos_Con_Coment = Museo.objects.order_by('-NUM_COMENTS')
            TOP5Museos_Con_Coment = Museos_Con_Coment[:5]
            DB_Users_Pag = Pag_Usuario.objects.all()
            DB_Comments = Comentario.objects.all()

            peticion = "<br>¿Mostras solo accesibles?<br>"
            peticion += "<form action='/' method='post'>"
            peticion += "<input type= 'hidden' name='opcion' value='2'>"
            peticion += "<input type= 'submit' value='Ir'>"
            peticion += "</form>"
        if acces == 1:
            DB_Museos = Museo.objects.all()
            DB_Museos = DB_Museos.filter(ACCESIBILIDAD = "1")
            Museos_Con_Coment = Museo.objects.order_by('-NUM_COMENTS').filter(ACCESIBILIDAD = "1")
            TOP5Museos_Con_Coment = Museos_Con_Coment[:5]
            DB_Users_Pag = Pag_Usuario.objects.all()
            DB_Comments = Comentario.objects.filter(MUSEO__ACCESIBILIDAD = "1" )

            peticion = "Mostrando solo los museos accesibles <br>¿Ver todos?<br>"
            peticion += "<form action='/' method='post'>"
            peticion += "<input type= 'hidden' name='opcion' value='3'>"
            peticion += "<input type= 'submit' value='Ir'>"
            peticion += "</form>"
        info = "<h2>Mensaje de SHIELD: </h2> <br>"
        if len(DB_Museos) == 0: #Significa que la base de datos esta vacia
            info += "No hay datos disponibles en la base de datos"
            # POST para cargar los datos
            info += "<br>¿Actualizar Datos?<br>"
            info += "<form action='/' method='post'>"
            info += "<input type= 'hidden' name='opcion' value='1'>"
            info += "<input type= 'submit' value='Actualizar'>"
            info += "</form>"

        else:
            if len(DB_Comments) == 0:
                info += "No hay comentarios para ningún museo"
            else:
                for museo in TOP5Museos_Con_Coment:
                    if museo.NUM_COMENTS !=0:
                        info += "<a href=" + museo.CONTENT_URL + ">" + museo.NOMBRE +"</a><br>"
                        info += "<h4>Dirección: </h4>" + museo.NOMBRE_VIA + " " + museo.CLASE_VIAL + " " + museo.TIPO_NUM
                        info += " " + museo.NUM + ", " + museo.PLANTA + ", " +museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
                        info += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", " + museo.DISTRITO + "<br>"
                        info += "<a href=/museos/" + museo.ID_ENTIDAD + ">Página del museo</a><br><br>"
        users_pag = "<h4>Paginas de los usuarios registrados: </h4><br>"
        if len(DB_Users_Pag) == 0:
            users_pag = "Ningun usuario registrado."
        else:
            for pag in DB_Users_Pag:
                users_pag += "<a href=/" + pag.USUARIO + ">" + pag.TITULO + "</a><br>"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he pinchado sobre Actualizar datos
            parsearXML('museos.xml')
            return redirect("/")
        elif opcion == "2":
            global acces
            acces = 1
            return redirect("/")
        elif opcion == "3":
            global acces
            acces = 0
            return redirect("/")
    template = get_template('index.html')
    c = Context({'msg': info ,'users_pag': users_pag, 'login': Login_info(request), 'peticion': peticion,
                    'propietary':request.user.username})
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
    template = get_template('index.html')
    c = Context({'msg': form1, 'login': Login_info(request)})
    return HttpResponse(template.render(c))

@csrf_exempt
def Pagina_Usuario(request, user):

    DB_Users = User.objects.all()
    DB_Users_Pag = Pag_Usuario.objects.get(USUARIO = user)
    if request.method == "GET":
        titulo = DB_Users_Pag.TITULO
        selec_museos = DB_Users_Pag.MUSEOS.all()
        if acces == 1:
            print("Access 1")
            select_museos = DB_Users_Pag.MUSEOS.all().filter(MUSEO__ACCESIBILIDAD = "1")
            print(select_museos)
        if len(selec_museos) == 0:
            museos = "No hay ningun museo añadido"
        else:
            museos = "Los museos añadidos son: <br>"
            for museo in selec_museos:
                museos += "<a href=" + museo.MUSEO.CONTENT_URL + ">" + museo.MUSEO.NOMBRE + "</a><br>"
                museos += "Dirección: " + museo.MUSEO.NOMBRE_VIA + " "
                museos += museo.MUSEO.CLASE_VIAL + " " + museo.MUSEO.TIPO_NUM + " "
                museos += museo.MUSEO.NUM + ", " + museo.MUSEO.PLANTA + ", "
                museos += museo.MUSEO.LOCALIDAD + ", " + museo.MUSEO.PROVINCIA + ", "
                museos += museo.MUSEO.CODIGO_POSTAL + ", "+ museo.MUSEO.BARRIO + ", "
                museos += museo.MUSEO.DISTRITO + "<br>"
                museos += "Añadido el: " + museo.FECHA + "<br><br>"
        if user == request.user.username:
            # formulario para Cambiar titulo
            peticion = "<br>¿Cambiar Titulo? "
            peticion += "<form action='" + user + "' method='post'>"
            peticion += "Titulo: <input type= 'text' name='titulo'>"
            peticion += "<input type= 'hidden' name='opcion' value='2'>"
            peticion += "<input type= 'submit' value='enviar'>"
            peticion += "</form>"
            # Muestro todos los museos y doy la opcion de añadirlos
        else:
            peticion = "No eres propietario de la pagina"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # He pinchado sobre Actualizar datos
            parsearXML('museos.xml')
        elif opcion == "2":
            titulo = request.POST['titulo']
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            pag_object.TITULO = titulo
            pag_object.save()

        url = "http://localhost:1234/" + user
        return redirect(url)
    else:
        error = "Method not Allowed"

    template = get_template('pag_user.html')
    c = Context({'user': user, 'titulo': DB_Users_Pag.TITULO,'museos': museos, 'peticion': peticion,
                    'login': Login_info(request), 'propietary':request.user.username})
    return HttpResponse(template.render(c))

@csrf_exempt
def Pagina_Museos(request):
    DB_Museos = Museo.objects.all()
    if request.method == "GET":
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
                form1 += museo.NOMBRE + "<br>"
                form1 += "<a href=/museos/" + museo.ID_ENTIDAD +">Su pagina </a><br>"
                if request.user.is_authenticated():
                    form1 += "<form action='/museos' method='post'>"
                    form1 += "<input type= 'hidden' name='museo' value=" + museo.ID_ENTIDAD +">"
                    form1 += "<input type= 'hidden' name='opcion' value='3'>"
                    form1 += "<input type= 'submit' value='Añadir a mi página'>"
                    form1 += "</form>"
                    form1 += "<form action='/museos' method='post'>"
                    form1 += "<input type= 'hidden' name='museo' value=" + museo.ID_ENTIDAD +">"
                    form1 += "Comentario: <input type= 'text' name='texto'>"
                    form1 += "<input type= 'hidden' name='opcion' value='2'>"
                    form1 += "<input type= 'submit' value='Enviar'>"
                    form1 += "</form><br><br>"

            # Para filtrar por distrito
            distritos = DB_Museos.values_list('DISTRITO', flat=True).distinct()
            peticion = "Seleccionar distrito: <br>"
            peticion += "<form action='/museos/' method='post'>"
            peticion += "<select name='Distrito'>"
            for distrito in distritos:
                peticion += "<option value='" + distrito + "'>" + distrito
                peticion += "</option>"
            peticion += "<input type= 'submit' value='Filtrar'>"
            peticion += "</form><br><br>"

            # Para tener toda la lista de museos
            peticion += "<form action='/museos' method='post'>"
            peticion += "<input type= 'hidden' name='opcion' value='1'>"
            peticion += "<input type= 'submit' value='Todos los museos'>"
            peticion += "</form>"

    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he pinchado sobre Actualizar datos
            parsearXML('museos.xml')
        elif opcion == "2":
            ID_museo = request.POST['museo']
            museo = Museo.objects.get(ID_ENTIDAD = ID_museo)
            fecha = str(time.ctime())
            texto = request.POST['texto']
            museo.NUM_COMENTS = museo.NUM_COMENTS + 1
            museo.save()
            coment_object = Comentario(MUSEO = museo, USUARIO = "Anónimo", TEXTO = texto, FECHA = fecha)
            coment_object.save()
        elif opcion == "3":
            ID_museo = request.POST['museo']
            museo = Museo.objects.get(ID_ENTIDAD = ID_museo)
            fecha = str(time.ctime())
            pag_object = Pag_Usuario.objects.get(USUARIO = request.user.username)
            user_museo_object = Museo_Usuario(MUSEO = museo, FECHA = fecha)
            user_museo_object.save()
            pag_object.MUSEOS.add(user_museo_object)
            pag_object.save()
        return redirect("/museos")

    template = get_template('pag_museos.html')
    c = Context({'museos': form1, 'peticion': peticion, 'login': Login_info(request)})
    return HttpResponse(template.render(c))

@csrf_exempt
def Pagina_Museo(request, id):
    museo = Museo.objects.get(ID_ENTIDAD = id)
    if request.method == "GET":
        info = "<h1><stron>" + museo.NOMBRE + "</h1></strong><br>"
        info += "<a href=" + museo.CONTENT_URL + ">Link a la página de la Comunidad de MADRID</a><br>"
        info += "<h4>Dirección: </h4>" + museo.NOMBRE_VIA + " " + museo.CLASE_VIAL + " " + museo.TIPO_NUM
        info += " " + museo.NUM + ", " + museo.PLANTA + ", " +museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
        info += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", " + museo.DISTRITO + "<br>"
        info += "<h4>Accesibilidad: </h4>" + museo.ACCESIBILIDAD + "<br>"
        info += "<h4>Contacto: </h4><br> Telefono: " + museo.TELEFONO
        info += "   Email: " + museo.EMAIL + "   Fax: " + museo.FAX
        if museo.NUM_COMENTS != 0:
            comments = Comentario.objects.filter(MUSEO = museo)
            comentarios = "<h3>Comentarios: </h3><br>"
            for comment in comments:
                comentarios += "\"" + comment.TEXTO + "\" - " + comment.USUARIO + "<br>"
        else:
            comentarios = " "

    template = get_template('pag_museo.html')
    c = Context({'info': info, 'comentarios': comentarios, 'login': Login_info(request)})
    return HttpResponse(template.render(c))

@csrf_exempt
def XML_Usuario(request, user):
    if request.method == "GET":
        if request.user.is_authenticated():
            pag = Pag_Usuario.objects.get(USUARIO=request.user.username)
            user = request.user.username
            titulo = pag.TITULO
            selec_museos = pag.MUSEOS.all()
            if len(selec_museos) == 0:
                museos = "No hay ningun museo añadido"
                form1 = " "
            else:
                museos = "Los museos añadidos son: <br>"
                for museo in selec_museos:
                    museos += "<a href=" + museo.MUSEO.CONTENT_URL + ">" + museo.MUSEO.NOMBRE + "</a><br>"
                    museos += "Dirección: " + museo.MUSEO.NOMBRE_VIA + " "
                    museos += museo.MUSEO.CLASE_VIAL + " " + museo.MUSEO.TIPO_NUM + " "
                    museos += museo.MUSEO.NUM + ", " + museo.MUSEO.PLANTA + ", "
                    museos += museo.MUSEO.LOCALIDAD + ", " + museo.MUSEO.PROVINCIA + ", "
                    museos += museo.MUSEO.CODIGO_POSTAL + ", "+ museo.MUSEO.BARRIO + ", "
                    museos += museo.MUSEO.DISTRITO + "<br>"
                    museos += "Añadido el: " + museo.FECHA + "<br><br>"
        else:
            user = " nadie"
            titulo = "Login needed <br>"
            museos = "No estas logueado, para añadir museos a tu página deberás hacerlo."
    else:
        respuesta = "Method not Allowed"

    template = get_template('pag_user.html')
    c = Context({'user': user, 'titulo': titulo,'museos': museos, 'peticion': " ", 'login': Login_info(request)})
    return HttpResponse(template.render(c))
