#! /usr/bin/python2
# -*- coding: utf-8 -*-
'''
Script para modificar un archivo .pyproj de un projecto Django creado con Visual Studio.

La modificación (parche) se utiliza para mantener compatible un projecto que ha sido 
modificado desde un ambiente distinto a Visual Studio, por ejemplo Visual Studio Code.

Permite trabajar con un projecto Django tanto en Linux como en Windows (Visual Studio).

Requerimientos para ejecutar el script:
    * Python >= 2.7 < 3
    * lxml

Instalar requerimientos:
    python2 -m pip -r requirements.txt

Uso: 
    python2 vspypatcher --pyproj=app_django.pyproj [--out=out_file.pyproj]

    o

    python2 vspatcher -p app_django.pyproj [-o out_file.pyproj]


Fecha:    15/11/2018
Versión:  1.0.0
'''
import sys, getopt

version = "1.0.0"

print "\n--- Visual Studio Django Project Patcher v%s ---\n" % version

## Parsea las opciones de la linea de comandos
try:
    opts, args = getopt.getopt(sys.argv[1:], 'p:o:', ["pyproj=", "out="])
except getopt.GetoptError as opterr:
    print "No .pyproj file specified."
    print 'Usage:  \n        python2 vspatcher.py --pyproj="PATH_TO_PYPROJ_FILE" [--out=out_file.pyproj]\n        o\n        python2 vspatcher.py -p PATH_TO_PYPROJ_FILE [-o out_file.pyproj]\n'
    sys.exit(0)

# Inicializa la variable para el nombre del archivo
pyproj_file_path = None
output_file_path = None

## Recorre la lista de opciones parseadas en busca de la opción --pyproj o -p
## en caso de encontrarla asigna el valor a la variable del nombre del archivo
for opt, arg in opts:
    if opt in ("-p", "--pyproj"):
        pyproj_file_path = arg.strip()
    elif opt in ("-o", "--out"):
        output_file_path = arg.strip()

## Si no se expecifico un archivo o el archivo no tiene la extensión .pyproj muestra error
if pyproj_file_path == None or pyproj_file_path == '' or 'pyproj' not in pyproj_file_path.split('.'):
    print "No .pyproj file specified."
    print 'Usage:  \n        python2 vspatcher.py --pyproj="PATH_TO_PYPROJ_FILE" [--out=out_file.pyproj]\n        o\n        python2 vspatcher.py -p PATH_TO_PYPROJ_FILE [-o out_file.pyproj]\n'
    sys.exit(0)

## Muestra información del archivo .pyproj
print "File *.pyproj from Django Visual Studio Project is '%s'\n" % arg

## Intenta abrir el archivo .pyproj
print "Opening file..."
try:
    f = open(pyproj_file_path)
except IOError as ioerr:
    print ioerr
    print ''
    sys.exit(1)

## Lee el contenido del archivo y elimina el atributo xmlns (namespace)
file_data = f.read()
file_data = file_data.replace('xmlns="http://schemas.microsoft.com/developer/msbuild/2003"', '')
f.close()

## Importa el paquete para parsear XML
print "Importing xml package..."
try:
    from lxml import etree
    print "running with lxml.etree"
except ImportError:
    print("Failed to import ElementTree from any known place")


# Parsea el archivo .pyproj
print "Parsing xml project data..."
pyproj = etree.XML(file_data)

## Banderas para saber si ya se agregaron los nuevos tags
is_compile_added = False
is_content_added = False

## Recorre todos los elementos del archivo XML
for element in pyproj:
    # Si el elemento tiene el tag ItemGroups recorre sus elementos.
    if element.tag == 'ItemGroup':
        for el in element:
            # Si el elemento hijo de ItemGroup es Compile, agrega los nuevos tags al inicio y actualiza la bandera de compile
            if el.tag == 'Compile' and not is_compile_added:
                print "Adding New Compile Tags..."
                is_compile_added= True
                element.insert(0, etree.Element('Compile', Remove='*_proxy.py'))
                element.insert(0, etree.Element('Compile', Remove='deployFiles\**'))
                element.insert(0, etree.Element('Compile', Remove='bin\*.py'))
                element.insert(0, etree.Element('Compile', Remove='env*\**\*.py'))
                element.insert(0, etree.Element('Compile', Include='.\**\*.py'))
            # Si no, si el elemento hijo de ItemGroup es Content, agrega los nuevos tags al inicio y actualiza la bandera de content
            elif el.tag == 'Content' and not is_content_added:
                print "Adding New Content Tags..."
                is_content_added = True
                element.insert(0, etree.Element('Content', Remove='deployFiles\**'))
                element.insert(0, etree.Element('Content', Remove='*_proxy.py'))
                element.insert(0, etree.Element('Content', Remove='*.pyproj.user'))
                element.insert(0, etree.Element('Content', Remove='sh_scripts\**'))
                element.insert(0, etree.Element('Content', Remove='staticfiles\**'))
                element.insert(0, etree.Element('Content', Remove='static\**'))
                element.insert(0, etree.Element('Content', Remove='bin\**'))
                element.insert(0, etree.Element('Content', Remove='obj\**'))
                element.insert(0, etree.Element('Content', Remove='env*\**'))
                element.insert(0, etree.Element('Content', Remove='.\**\__pycache__'))
                element.insert(0, etree.Element('Content', Remove='.\**\*.pyc'))
                element.insert(0, etree.Element('Content', Remove='.git\**'))
                element.insert(0, etree.Element('Content', Include='.\**'))

# Agrega de nuevo el atributo xlmns (namespace) al elemento root
pyproj.set('xmlns', "http://schemas.microsoft.com/developer/msbuild/2003")


## Intenta abrir el archivo para escribir los cambios
if output_file_path == None or output_file_path == '':
    output_file_path = pyproj_file_path

if not 'pyproj' in output_file_path.split('.'):
    output_file_path += '.pyproj'

print "Writting changes to %s..." % output_file_path
try:
    f = open(output_file_path, "w")
except IOError as ioerr:
    print ioerr
    print ''
    sys.exit(1)
            
f.write('<?xml version="1.0" encoding="utf-8"?>')
f.write(etree.tostring(pyproj, pretty_print=True))
f.close()