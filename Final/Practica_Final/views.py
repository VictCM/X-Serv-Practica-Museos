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
import os
# Create your views here.

acces = 0
district = "Null"

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
        elif acces == 1:
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
        msg = "<h2>Museos con más comentarios: </h2> <br>"
        if len(DB_Museos) == 0: #Significa que la base de datos esta vacia
            msg += "No hay datos disponibles en la base de datos"
            # POST para cargar los datos
            msg += "<br>¿Actualizar Datos?<br>"
            msg += "<form action='/' method='post'>"
            msg += "<input type= 'hidden' name='opcion' value='1'>"
            msg += "<input type= 'submit' value='Actualizar'>"
            msg += "</form>"

        else:
            if len(DB_Comments) == 0:
                msg += "No hay comentarios para ningún museo"
            else:
                for museo in TOP5Museos_Con_Coment:
                    if museo.NUM_COMENTS !=0:
                        msg += "<a href=" + museo.CONTENT_URL + ">" + museo.NOMBRE +"</a><br>"
                        msg += "<h4>Dirección: </h4>" + museo.NOMBRE_VIA + " " + museo.CLASE_VIAL + " " + museo.TIPO_NUM
                        msg += " " + museo.NUM + ", " + museo.PLANTA + ", " +museo.LOCALIDAD + ", " + museo.PROVINCIA + ", "
                        msg += museo.CODIGO_POSTAL + ", "+ museo.BARRIO + ", " + museo.DISTRITO + "<br>"
                        msg += "<a href=/museos/" + museo.ID_ENTIDAD + ">Página del museo</a><br><br>"
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
    c = Context({'msg': msg ,'users_pag': users_pag, 'login': Login_info(request), 'peticion': peticion,
                    'propietary':request.user.username, 'estilo_color': Estilo(request, "color"),
                     'estilo_tamaño':Estilo(request, "tamaño")})
    return HttpResponse(template.render(c))


@csrf_exempt
def Registro(request):
    if request.method == "GET":
        msg = "Crear Usuario: "
        msg += "<form action='/registro/' method='post'>"
        msg += "User: <input type= 'text' name='user'>"
        msg += "Email: <input type= 'text' name='email'>"
        msg += "Password: <input type= 'password' name='password'>"
        msg += "<input type= 'submit' value='enviar'>"
        msg += "</form>"
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
        msg = " "
        #url = "http://localhost:1234/"
        return redirect("http://localhost:1234/")

    template = get_template('index.html')
    c = Context({'msg': msg, 'login': Login_info(request), 'color': Estilo(request, "color"),
         'estilo_tamaño':Estilo(request, "tamaño")})
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
            # Formulario para cambiar titulo
            peticion = "<br>¿Cambiar Titulo? "
            peticion += "<form action='" + user + "' method='post'>"
            peticion += "Titulo: <input type= 'text' name='titulo'>"
            peticion += "<input type= 'hidden' name='opcion' value='2'>"
            peticion += "<input type= 'submit' value='enviar'>"
            peticion += "</form>"
            # Formulario para cambiar color del sitio
            colores = ["azul", "verde", "amarillo", "rojo", "naranja", "rosa", "morado", 
                        "marrón", "gris", "default"]
            peticion += "<br><br>Seleccionar color: <br>"
            peticion += "<form action='" + user + "' method='post'>"
            peticion += "<select name='Color'>"
            for color in colores:
                peticion += "<option value='" + color + "'>" + color
                peticion += "</option>"
            peticion += "<input type= 'hidden' name='opcion' value='3'>"
            peticion += "<input type= 'submit' value='Cambiar'>"
            peticion += "</form><br><br>"

            # Formulario para cambiar tamaño de fuente del sitio
            tamaños = ["pequeña", "normal", "grande"]
            peticion += "<br><br>Seleccionar tamaño: <br>"
            peticion += "<form action='" + user + "' method='post'>"
            peticion += "<select name='Tamaño'>"
            for tamaño in tamaños:
                peticion += "<option value='" + tamaño + "'>" + tamaño
                peticion += "</option>"
            peticion += "<input type= 'hidden' name='opcion' value='4'>"
            peticion += "<input type= 'submit' value='Cambiar'>"
            peticion += "</form><br><br>"
        else:
            peticion = "No eres propietario de la pagina"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "2":
            titulo = request.POST['titulo']
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            pag_object.TITULO = titulo
            pag_object.save()
        elif opcion == "3":
            # He pinchado sobre cambiar el color del sitio
            color = request.POST['Color']
            if color == "verde":
                color = "#BCF5A9"
            elif color == "azul":
                color = "#81DAF5"
            elif color == "rojo":
                color = "#F78181"
            elif color == "amarillo":
                color = "#F3F781"
            elif color == "naranja":
                color = "#FAAC58"
            elif color == "marrón":
                color = "#B18904"
            elif color == "gris":
                color = "#BDBDBD"
            elif color == "rosa":
                color = "#F6CEEC"
            elif color == "morado":
                color = "#BE81F7"
            elif color == "default":
                color = "#fff"
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            pag_object.COLOR = color
            pag_object.save()
        elif opcion == "4":
            # He pinchado sobre cambiar el tamaño de letra
            tamaño = request.POST['Tamaño']
            if tamaño == "pequeño":
                tamaño = "60%"
            elif tamaño == "normal":
                tamaño = "100%"
            elif tamaño == "grande":
                tamaño = "150%"
            pag_object = Pag_Usuario.objects.get(USUARIO = user)
            pag_object.TAMAÑO = tamaño
            pag_object.save()

        url = "http://localhost:1234/" + user
        return redirect(url)

    template = get_template('pag_user.html')
    c = Context({'user': user, 'titulo': DB_Users_Pag.TITULO,'museos': museos, 'peticion': peticion,
                    'login': Login_info(request), 'propietary':request.user.username, 'estilo_color': Estilo(request, "color"),
                     'estilo_tamaño':Estilo(request, "tamaño")})
    return HttpResponse(template.render(c))

@csrf_exempt
def Pagina_Museos(request):
    if acces ==0:
            DB_Museos = Museo.objects.all()
    elif acces == 1:
            DB_Museos = Museo.objects.all()
            DB_Museos = DB_Museos.filter(ACCESIBILIDAD = "1")
    if district != "Null":
            DB_Museos = DB_Museos.filter(DISTRITO = district)
            museos = "<h4>Mostando los museos filtrados por el distrito " + district + ": <br><br></h4>"
    else:
            museos = ""
    if request.method == "GET":
        peticion=""
        if len(DB_Museos) == 0: #Significa que la base de datos esta vacia
            if acces == 0 and district == "Null":
                museos = "No hay datos disponibles en la base de datos"
                # POST para cargar los datos
                museos += "<br>¿Actualizar Datos?<br>"
                museos += "<form action='/museos' method='post'>"
                museos += "<input type= 'hidden' name='opcion' value='1'>"
                museos += "<input type= 'submit' value='Actualizar'>"
                museos += "</form>"
            else: 
                museos += "No hay museos con el filtro aplicado"
        else:        
            # Muestro todos los museos y doy la opcion de añadirlos
            for museo in DB_Museos:
                museos += "<br> " +museo.NOMBRE + "<br>"
                museos += "<a href=/museos/" + museo.ID_ENTIDAD +">Su pagina </a><br>"
                if request.user.is_authenticated():
                    museos += "<form action='/museos' method='post'>"
                    museos += "<input type= 'hidden' name='museo' value=" + museo.ID_ENTIDAD +">"
                    museos += "<input type= 'hidden' name='opcion' value='3'>"
                    museos += "<input type= 'submit' value='Añadir a mi página'>"
                    museos += "</form>"
                    museos += "<form action='/museos' method='post'>"
                    museos += "<input type= 'hidden' name='museo' value=" + museo.ID_ENTIDAD +">"
                    museos += "Comentario: <input type= 'text' name='texto'>"
                    museos += "<input type= 'hidden' name='opcion' value='2'>"
                    museos += "<input type= 'submit' value='Enviar'>"
                    museos += "</form><br><br>"

            # Para filtrar por distrito
            distritos = DB_Museos.values_list('DISTRITO', flat=True).distinct()
            peticion = "Seleccionar distrito: <br>"
            peticion += "<form action='/museos' method='post'>"
            peticion += "<select name='Distrito'>"
            for distrito in distritos:
                peticion += "<option value='" + distrito + "'>" + distrito
                peticion += "</option>"
            peticion += "<input type= 'hidden' name='opcion' value='4'>"
            peticion += "<input type= 'submit' value='Filtrar'>"
            peticion += "</form><br><br>"

            # Para tener toda la lista de museos
            peticion += "<form action='/museos' method='post'>"
            peticion += "<input type= 'hidden' name='opcion' value='5'>"
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
        elif opcion == "4":
            distrito = request.POST['Distrito']
            global district
            district = distrito
        elif opcion == "5":
            global district
            district = "Null"
        return redirect("/museos")

    template = get_template('pag_museos.html')
    c = Context({'museos': museos, 'peticion': peticion, 'login': Login_info(request),
                'propietary':request.user.username, 'estilo_color': Estilo(request, "color"),
                 'estilo_tamaño':Estilo(request, "tamaño")})
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
            comentarios = "<h3>Comentarios: </h3><br><br>"
            for comment in comments:
                comentarios += "\"" + comment.TEXTO + "\" - " + comment.USUARIO + "<br><br>"
        else:
            comentarios = " "

    template = get_template('pag_museo.html')
    c = Context({'info': info, 'comentarios': comentarios, 'login': Login_info(request),
                        'propietary':request.user.username, 'estilo_color': Estilo(request, "color"),
                         'estilo_tamaño':Estilo(request, "tamaño")})
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
                msg = "No hay ningun museo añadido"
            else:
                msg = "<Contenidos>\n"
                msg += "    <infoDataset>\n"
                msg += "        <nombre>Museos de la ciudad de Madrid añadido a la página de " + request.user.username +"</nombre>\n"
                msg += "        <uri>https://datos.madrid.es/egob/catalogo/201132-0-museos</uri>\n"
                msg += "        <descripcion> Datos de los Museos de la ciudad de Madrid. Localización, transportes, horarios, visitas, datos de contacto.\n"
                msg += "     </descripcion>\n"
                msg += "    </infoDataset>\n"
                msg += "    <contenido>\n"
                for museo in selec_museos:
                    msg += '        <tipo>EntidadesYOrganismos</tipo>\n'
                    msg += '        <atributos idioma="es">\n'
                    msg += '            <atributo nombre="ID-ENTIDAD">' + museo.MUSEO.ID_ENTIDAD + '</atributo>\n'
                    msg += '            <atributo nombre="NOMBRE">' + museo.MUSEO.NOMBRE + '</atributo>\n'
                    msg += '            <atributo nombre="DESCRIPCION-ENTIDAD">'  + museo.MUSEO.DESCRIPCION_ENTIDAD + '</atributo>\n'
                    msg += '            <atributo nombre="HORARIO">' + museo.MUSEO.HORARIO  + '</atributo>\n'
                    msg += '            <atributo nombre="TRANSPORTE">' + museo.MUSEO.TRANSPORTE + '</atributo>\n'
                    msg += '            <atributo nombre="ACCESIBILIDAD">' + museo.MUSEO.ACCESIBILIDAD + '</atributo>\n'
                    msg += '            <atributo nombre="CONTENT-URL">' + museo.MUSEO.CONTENT_URL + '</atributo>\n'
                    msg += '            <atributo nombre="LOCALIZACION">\n'
                    msg += '                <atributo nombre="NOMBRE-VIA">' +museo.MUSEO.NOMBRE_VIA + '</atributo>\n'
                    msg += '                <atributo nombre="CLASE-VIAL">' + museo.MUSEO.CLASE_VIAL + '</atributo>\n'
                    msg += '                <atributo nombre="TIPO-NUM">' + museo.MUSEO.TIPO_NUM + '</atributo>\n'
                    msg += '                <atributo nombre="NUM">' + museo.MUSEO.NUM + '</atributo>\n'
                    msg += '                <atributo nombre="LOCALIDAD">' + museo.MUSEO.LOCALIDAD + '</atributo>\n'
                    msg += '                <atributo nombre="PROVINCIA">' + museo.MUSEO.PROVINCIA + '</atributo>\n'
                    msg += '                <atributo nombre="CODIGO-POSTAL">' + museo.MUSEO.CODIGO_POSTAL + '</atributo>\n'
                    msg += '                <atributo nombre="BARRIO">' + museo.MUSEO.BARRIO + '</atributo>\n'
                    msg += '                <atributo nombre="DISTRITO">' + museo.MUSEO.DISTRITO + '</atributo>\n'
                    msg += '                <atributo nombre="COORDENADA-X">' + museo.MUSEO.COORDENADA_X + '</atributo>\n'
                    msg += '                <atributo nombre="COORDENADA-Y">' + museo.MUSEO.COORDENADA_Y + '</atributo>\n'
                    msg += '                <atributo nombre="LATITUD">' +  museo.MUSEO.LATITUD + '</atributo>\n'
                    msg += '                <atributo nombre="LONGITUD">' + museo.MUSEO.LONGITUD + '</atributo>\n'
                    msg += '            </atributo>\n'
                    msg += '            <atributo nombre="DATOSCONTACTOS">\n'
                    msg += '                <atributo nombre="TELEFONO">' + museo.MUSEO.TELEFONO + '</atributo>\n'
                    msg += '                <atributo nombre="FAX">' + museo.MUSEO.FAX + '</atributo>\n'
                    msg += '                <atributo nombre="EMAIL"> '+ museo.MUSEO.EMAIL + '</atributo>\n'
                    msg += '            </atributo>\n'
                msg += '            <atributo nombre="TIPO">/contenido/entidadesYorganismos/Museos</atributo>\n'
                msg += '        </atributos>\n'
                msg += '    </contenido>\n'
        else:

            msg = "No estas logueado, para crear el XML deberás hacerlo."


    template = get_template('pag_user_xml.html')
    c = Context({'login': Login_info(request), 'msg':msg, 'estilo_color': Estilo(request, "color"), 'estilo_tamaño':Estilo(request, "tamaño")})
    return HttpResponse(template.render(c))

def Estilo(request, peticion):
    if peticion == "color":
        if request.user.is_authenticated():
            DB_User_Pag = Pag_Usuario.objects.get(USUARIO = request.user.username)
            estilo = DB_User_Pag.COLOR
        else:
            estilo = "#fff"
    elif peticion == "tamaño":
        if request.user.is_authenticated():
            DB_User_Pag = Pag_Usuario.objects.get(USUARIO = request.user.username)
            estilo = DB_User_Pag.TAMAÑO
        else:
            estilo = "100%"
    return estilo


@csrf_exempt
def About(request):
    if request.method == "GET":
        msg = "Página con la finalidad de agrupar los museos de Madrid y que se puedan filtrar y valorar por todos los usuarios<br>"
        msg += "Desde cualquier sitio de la web se puede acceder a la Página principal ('Home'), a una lista de todos los museos ('Museos'), a la página personal si estas logueado('Mi página') y a la página actual ('About').<br>"
        msg += " Además, se podra loguear o hacer logout en cualquier momento o acceder a una página para registrarse. <br>"

        msg += "<br>En la <strong>página principal, 'home',</strong> podemos ver los 5 museos con más comentarios y una lista con los titulos de todas las páginas de usuarios"
        msg += "también se puede filtrar por accesibilidad y que solo aparezcan los museos que hayan indicado que son accesibles.<br>"
        msg += " La página muestra un botón que aparecera la primera vez haciendo referencia a que no se puede mostrar ningún museo porque la base de datos esta vacia. Pulsado el botón se cargará la base de datos y se podrán ver todos."


        msg += "<br>En <strong>Museos</strong> veremos todos los museos de la C.Madrid y podremos filtrarlos por el distrito al que pertenecen. Se incluyen para cada museo dos opciones, una para añadirlo a la página principal del usuario registrado"
        msg += ", indicando a que hora se hizo, y otra para hacer un comentario que será anónimo sobre dicho museo. Debajo del nombre se cada museo  "
        msg += "se verá información de interés y un link hacia la página de ese propio museo en la web en la que se encontraran todos los comentarios asociados a este.<br>"
        
        msg += "<br>En <strong>Mi página</strong> cada usuario registrado y logueado podrá ver su seleccion de museos, junto con la fecha en que lo añadió. Se incluyen varios formularios para poder editar esta página,"
        msg += " como cambiar el color de fondo, el tamaño de la letra y el titulo de la página. A su vez, debajo de estos se encuentra un link propio para cada usuario que nos creara el código xml perteneciente a la selección de museos de cada persona.<br>"

    template = get_template('about.html')
    c = Context({'login': Login_info(request), 'msg':msg, 'estilo_color': Estilo(request, "color"), 'estilo_tamaño':Estilo(request, "tamaño")})
    return HttpResponse(template.render(c))
