---
title: Actualizar assemblies de una aplicación web
tags: []
---
Desde hace unos días varios compañeros de trabajo están buscando una forma para poder actualizar los ensamblados de una aplicación web mediante una aplicación de escritorio que utiliza las mismas DLL que están en el _bin_ de la aplicación web. La verdad es que ya el planteamiento es bastante rocambolesco, pero hoy me he puesto a _googlear_ para ver que opciones teníamos y he encontrado una entrada en el [blog de Nik Kalyani](http://www.techbubble.net/) (que es a su vez un comentario a otra [publicación](http://west-wind.com/Weblog/posts/449761.aspx)), que en principio no tiene nada que ver con el problema que he planteado inicialmente, pero me ha gustado por la idea que propone de organizar los assemblies en subcarpetas, ya que además de mejorar el reinicio de la aplicación minimizando los errores de servidor también puede ser de utilidad para mantener un histórico de versiones.

Aquí está la traducción de la entrada de su blog y [aquí](http://www.techbubble.net/2008/08/13/Updating+ASPNET+Assemblies.aspx) la entrada original:

> Yo uso el siguiente método:

Dejar los ensamblados que sean poco susceptibles de cambio en el bin (es decir, componentes, librerías de terceros, etc.) Poner los ensamblados de la aplicación en una subcarpeta del bin a la que asignamos el nombre en función de la fecha (por ejemplo: bin20080801)

Modificar el archivo web.config de la forma siguiente:

<runtime> <assemblybinding xmlns=”urn:schemas-microsoft-com:asm.v1”> <probing privatepath=”bin;bin20080801;”></probing> </assemblybinding> </runtime>

Cuando necesito actualizar los ensamblados, los subo en una nueva subcarpeta en el bin, de nuevo con el nombre correspondiente con la fecha actual (bin20080812). Después de completar la carga, subo el fichero web.config con el cambio en el nombre del directorio. La aplicación se reinicia de nuevo y recoge los nuevos ensamblados y se olvida de la antigua carpeta, que se puede dejar o eliminar.

Parece funcionar y tiene el beneficio añadido de acelerar el inicio de la aplicación ya que la subcarpeta de ensamblados es ignorada hasta que se necesita.

