---
title: Reemplazar Notepad por Notepad2
---
Si eres de los que utilizas -al igual que yo- el editor de texto [Notepad2](http://en.wikipedia.org/wiki/Notepad2) y estás disfrutando de sus ventajas, seguramente estarás interesado en sustituir por completo la antigua versión del [Notepad](http://es.wikipedia.org/wiki/Notepad) incluido con Windows, al menos para no ver como se sigue abriendo el viejo Bloc de notas cada vez que quieres ver el código fuente (en Internet Explorer, claro) de una página Web. Si no sabes que es Notepad2 te recomiendo que lo descargues de la [Web de Florian Balmer](http://www.flos-freeware.ch/) (está disponible en [español](http://www.flos-freeware.ch/np2intl/notepad2_es.zip), [catalán](http://www.flos-freeware.ch/np2intl/notepad2_ca.zip) ([traducido](http://www.studio4net.com/alex/2004/10/notepad2-in-catalan.html) por un servidor) y [otros](http://www.flos-freeware.ch/np2intl.html) tantos idiomas) y lo pruebes. No te arrepentirás.  
  
Para reemplazar el antiguo Bloc de notas (notepad.exe) por nuestro nuevo y flamante Notepad2 debemos realizar unas operaciones bien sencillas:  

1.  Cambiamos el nombre del fichero notepad2.exe por notepad.exe (naturalmente en una carpeta donde no exista previamente)
2.  Reemplazamos el archivo notepad.exe de la carpeta c:\\windows\\system32\\dllcache. Al reemplazar este archivo aparece un mensaje de sistema indicando que se ha reemplazado un archivo de Windows y que se debe restaurar solicitando para ello que se introduzca el CD original de instalación de Windows. Este es el mensaje que aparece (en mi Windows 2003 en inglés): «Files that are required for Windows to run properly have been replaced by unrecognized versions. To maintain system stability. Windows must restore the original versions of these files».
3.  Pulsamos el botón Cancelar y aparecerá el siguiente mensaje: «You chose not to restore the original versions of the files. This may affect Windows stability. Are you sure you want to keep these unrecognized file versions?».
4.  Respondemos afirmativamente a la pregunta y ya sólo nos falta reemplazar el archivo en dos ubicaciones más: en c:\\windows y c:\\windows\\system32.  
    

Una vez hecho esto ya podemos decir adiós al antiguo Notepad: _Au revoir Notepad_.

