#!/usr/bin/python3

import xml.etree.ElementTree as ETree

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
      museos[museo['ID-ENTIDAD']] = museo
    museo = {}
    print('\n')
  if '\n' in atributo.text:
    # Porque se ha detectado un fallo en el XML
    museo[atributo.attrib['nombre']] = atributo.text.split('\n')[0]
  else:
    museo[atributo.attrib['nombre']] = atributo.text
    print(atributo.text)
museos[museo['ID-ENTIDAD']] = museo
    return museos
