#!/usr/bin/python3
from .models import Museo
import xml.etree.ElementTree as ET
import sys
import traceback

def parsearXML(file):

    doc = ET.parse('Practica_Final/museos.xml')

    #Cojo el primer elemento del árbol, la raiz
    raiz = doc.getroot()
    museos = {}
    # Llevo al Element que contiene a cada museo
    for atributo in raiz.iter('atributo'):
        # Me creo diccionario de cada museo y lo añado a un diccionario mayor: "museos"
        if atributo.attrib['nombre'] == 'ID-ENTIDAD':
            # Si el primer museo no coincide con el que estoy mirando ahora guardo el museo anterior en el dicc 'museos'
            if raiz[1][1][0].text != atributo.text:
                SaveObj(museo)
            museo = {}
        if '\n' in atributo.text:
            museo[atributo.attrib['nombre']] = atributo.text.split('\n')[0]
        else:
            museo[atributo.attrib['nombre']] = atributo.text
            print(atributo.text)
    SaveObj(museo)

def SaveObj(museo):
    ID_ENTIDAD = museo.get('ID-ENTIDAD', "Null")
    NOMBRE = museo.get('NOMBRE', "Null")
    HORARIO =  museo.get('HORARIO', "Null")
    DESCRIPCION_ENTIDAD =  museo.get('DESCRIPCION-ENTIDAD', "Null")
    EQUIPAMIENTO =  museo.get('EQUIPAMIENTO',"Null")
    TRANSPORTE =  museo.get('TRANSPORTE', "Null")
    DESCRIPCION =  museo.get('DESCRIPCION', "Null")
    ACCESIBILIDAD =  museo.get('ACCESIBILIDAD', "Null")
    CONTENT_URL =  museo.get('CONTENT-URL', "Null")
    NOMBRE_VIA =  museo.get('NOMBRE-VIA', "Null")
    CLASE_VIAL =  museo.get('CLASE-VIAL', "Null")
    TIPO_NUM =  museo.get('TIPO-NUM', "Null")
    NUM =  museo.get('NUM', "Null")
    PLANTA =  museo.get('PLANTA', "Null")
    LOCALIDAD =  museo.get('LOCALIDAD', "Null")
    PROVINCIA =  museo.get('PROVINCIA',"Null")
    CODIGO_POSTAL =  museo.get('CODIGO-POSTAL',"Null")
    BARRIO =  museo.get('BARRIO', "Null")
    DISTRITO =  museo.get('DISTRITO', "Null")
    COORDENADA_X =  museo.get('COORDENADA-X', "Null")
    COORDENADA_Y =  museo.get('COORDENADA-Y', "Null")
    LATITUD =  museo.get('LATITUD', "Null")
    LONGITUD =  museo.get('LONGITUD', "Null")
    TELEFONO =  museo.get('TELEFONO', "Null")
    FAX =  museo.get('FAX', "Null")
    EMAIL =  museo.get('EMAIL', "Null")
    TIPO =  museo.get('TIPO', "Null")

    museo_object = Museo(ID_ENTIDAD = ID_ENTIDAD,
                        NOMBRE = NOMBRE,
                        HORARIO = HORARIO,
                        DESCRIPCION_ENTIDAD = DESCRIPCION_ENTIDAD,
                        EQUIPAMIENTO = EQUIPAMIENTO,
                        TRANSPORTE = TRANSPORTE,
                        DESCRIPCION = DESCRIPCION,
                        ACCESIBILIDAD = ACCESIBILIDAD,
                        CONTENT_URL = CONTENT_URL,
                        NOMBRE_VIA = NOMBRE_VIA,
                        CLASE_VIAL = CLASE_VIAL,
                        TIPO_NUM = TIPO_NUM,
                        NUM = NUM,
                        PLANTA = PLANTA,
                        LOCALIDAD = LOCALIDAD,
                        PROVINCIA = PROVINCIA,
                        CODIGO_POSTAL = CODIGO_POSTAL,
                        BARRIO = BARRIO,
                        DISTRITO = DISTRITO,
                        COORDENADA_X = COORDENADA_X,
                        COORDENADA_Y = COORDENADA_Y,
                        LATITUD = LATITUD,
                        LONGITUD = LONGITUD,
                        TELEFONO = TELEFONO,
                        FAX = FAX,
                        EMAIL = EMAIL,
                        TIPO = TIPO)
    museo_object.save()
