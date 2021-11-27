---
title: Comprobar estado de la conexión a Internet
tags: []
---
Cada vez más a menudo nuestras aplicaciones necesitan saber si se dispone de una conexión a Internet para, por ejemplo, activar opciones que sólo tienen sentido en un entorno conectado (actualización de datos, envío de e-mails, etc.). La manera más fácil y rápida de realizar esta tarea es comprobando si nuestro proveedor resuelve la dirección IP de cualquier nombre de dominio.

El ejemplo siguiente utiliza el método _GetHostEntry_ para consultar en un servidor DNS la dirección IP asociada al dominio www.microsoft.com. Si se produce cualquier excepción podemos deducir que no tenemos una conexión a Internet. Este sistema funcionaría incluso si la web de Microsoft estuviese caída, ya que siempre realizamos la consulta a nuestro servidor de DNS y no al servidor de Microsoft.

private bool InternetIsAlive() { try { System.Net.IPHostEntry host = System.Net.Dns.GetHostEntry(“www.microsoft.com”); return true; } catch { return false; } } </pre>

Otro de los entornos donde nos puede ser útil comprobar si tenemos conexión es en la web. Supongamos que tenemos una página de una aplicación web donde el usuario debe rellenar un formulario, que puede ser más o menos extenso. Antes de realizar el _submit_ del formulario podemos comprobar si el navegador mantiene la conexión con el servidor y en caso de no tener conexión podemos alertar al usuario e incluso podemos guardar los datos en local para recuperarlos en cuanto la conexión vuelva a estar disponible.

Con la última versión de Internet Explorer esto lo podemos hacer mediante la propiedad _onLine_. En versiones anteriores esta propiedad también estaba disponible pero indicaba si el navegador trabajaba sin conexión, modo que tenía que elegir el usuario explícitamente desde el menú Archivo. Ahora está propiedad indica si el sistema está realmente conectado a Internet o a una red, y cambia en el momento que deja de estarlo. Para comprobar el estado de la conexión únicamente tenemos que consultar el valor de esta propiedad. Si el estado de la propiedad cambia, se lanzan los evento _offline_ u _online_ según el nuevo estado de la propiedad.

Con el ejemplo que pongo a continuación podemos ver el funcionamiento de esta nueva funcionalidad. Para probarlo simplemente tenemos que desconectar el cable de red o deshabilitar el adaptador de red.

 function InternetIsAlive()
{
    return window.navigator.onLine ? "Está conectado" : "Está desconectado";
}

function changeStatusEvent(e)
{
    if (!e) e = window.event;

    if (e.type == 'online')
    {
        alert('El navegador está conectado');
    }
    else if (e.type == 'offline' )
    {
        alert('El navegador está desconectado');
    }
}

window.onload = function() {
    document.body.ononline = changeStatusEvent;
    document.body.onoffline = changeStatusEvent;
} 

Estado de la conexión

