#!/usr/bin/python3

import xml.etree.ElementTree as ETree

def parsearXML(file):

  doc = ETree.parse(file)

  #Cojo el primer elemento del árbol, la raiz
  raiz = doc.getroot()

  for museo in raiz.iter('atributo')
    museo = {}
    print(raiz[1][1][1].text)

    print(museo.text)
