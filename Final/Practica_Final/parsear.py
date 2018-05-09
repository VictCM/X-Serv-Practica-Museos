#!/usr/bin/python3
from .models import Museo
import xml.etree.ElementTree as ETree
import sys
import traceback

def parsearXML(file):

    doc = ETree.parse('museos.xml')

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
        ID_ENTIDAD = museo.get('ID-ENTIDAD', None)
        NOMBRE = museo('NOMBRE', None)
        HORARIO = museo['HORARIO', None)
        DESCRIPCION_ENTIDAD = museo('DESCRIPCION_ENTIDAD', None)
        EQUIPAMIENTO = museo['EQUIPAMIENTO', None)
        TRANSPORTE = museo['TRANSPORTE', None)
        DESCRIPCION = museo['DESCRIPCION', None)
        ACCESIBILIDAD = museo['ACCESIBILIDAD', None)
        CONTENT_URL = museo['CONTENT_URL', None)
        NOMBRE_VIA = museo['NOMBRE_VIA', None)
        CLASE_VIAL = museo['CLASE_VIAL', None)
        TIPO_NUM = museo['TIPO_NUM', None)
        NUM = museo['NUM', None)
        PLANTA = museo['PLANTA', None)
        LOCALIDAD = museo['LOCALIDAD', None)
        PROVINCIA = museo['PROVINCIA'. None)
        CODIGO_POSTAL = museo['CODIGO_POSTAL'. None)
        BARRIO = museo['BARRIO', None)
        DISTRITO = museo['DISTRITO', None)
        COORDENADA_X = museo['COORDENADA_X', None)
        COORDENADA_Y = museo['COORDENADA_Y']
        LATITUD = museo['LATITUD']
        LONGITUD = museo['LONGITUD']
        TELEFONO = museo['TELEFONO']
        FAX = museo['FAX']
        EMAIL = museo['EMAIL']
        TIPO = museo['TIPO']

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
