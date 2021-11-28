---
title: Aplicación como servicio de Windows
---
Para crear un servicio de Windows a partir de un ejecutable debemos utilizar dos programas del kit de recursos: instsrv.exe y srvany.exe.  
  
Para crear el servicio tenemos que escribir y ejecutar en la lí­nea de comandos lo siguiente:  
  
instsrv.exe "Nombre del Servicio" srvany.exe  
  
Ahora ejecutamos el editor del registro (regedit) y en HKEY\_LOCAL\_MACHINE\\system\\CurrentControlSet\\Services aparecerá¡ un nueva clave con el Nombre del servicio. Dentro de esta clave debemos crear una nueva subclave llamada "Parameters", y dentro de esta clave crear un valor de cadena llamado "Application" con la ruta del ejecutable. Y ya tenemos creado el servicio.
