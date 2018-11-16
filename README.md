# vspypatcher

## **_Visual Studio Django Project Patcher_**

Script para modificar un archivo .pyproj de un proyecto Django creado con Visual Studio.

La modificación (parche) se utiliza para mantener compatible un proyecto que ha sido modificado fuera de Visual Studio


### **_Requerimientos_**

* python == 2.7
* lxml == 4.2.5
* pip = 18.1

### **_Instalación en linux_**

    sudo make requirements
    sudo make install

### **_Instalación Windows_**
    python2 -m pip install -r requirements.txt


### **_Uso_**

#### Windows
    python2 vspypatcher --pyproj=RUTA_ARCHIVO_PYPROJ [--out=salida.pyproj]

    o

    python2 vspypatcher -p RUTA_ARCHIVO _PYPROJ [-o salida.pyproj]

#### Linux

    vspypatcher --pyproj=RUTA_ARCHIVO_PYPROJ [--out=salida.pyproj]

    o

    vspypatcher -p RUTA_ARCHIVO _PYPROJ [-o salida.pyproj]


El archivo de entrada debe tener la extensión **_.pyproj_**

