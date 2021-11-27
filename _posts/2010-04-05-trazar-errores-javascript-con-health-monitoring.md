---
title: Trazar errores JavaScript con Health Monitoring
tags: []
---
Hace unos meses, [José Manuel Alarcón](http://www.jasoft.org/blog/) dio una charla en la CodeCamp 2009 sobre [Instrumentación en ASP.NET](http://www.secondnug.com/CodeCamp2009/TrackMSDN/tabid/95/Default.aspx). En la parte final de la presentación, que es recomendable al 100%, podemos ver una interesante _demo_ de cómo gestionar los errores JavaScript utilizando [_Health Monitoring_](http://msdn.microsoft.com/es-es/library/ms178703%28v=VS.80%29.aspx). Me gustó tanto esta presentación, que me propuse implementar esta funcionalidad en las pocas webs de clientes que aún tengo desperdigadas por ahí (y que puedo administrar); pero no ha sido hasta estos días de vacaciones que me he decidido y me he puesto manos a la obra…

**Health Monitoring** nos proporciona un sistema para supervisar y diagnosticar aplicaciones web, pero además, y esto es lo más interesante, nos permite registrar eventos que no estén relacionados directamente con errores de ASP.NET. Esta última funcionalidad es la que vamos a utilizar para el ejemplo de esta entrada.

El planteamiento general es muy sencillo: utilizar el evento _window.onerror_ de JavaScript para pasar toda la información del error (mensaje, dirección url, y número de línea) al servidor mediante la llamada a un _handler_. Este _handler_ levantará un evento **WebBaseEvent** personalizado que será gestionado por cualquier proveedor configurado en la infraestructura de _Health Monitoring_. Con esto tendremos un registro de todos los errores JavaScript que se produzcan en nuestra aplicación web. Interesante, ¿no? Pues comencemos por el principio…

Lo primero que tenemos que hacer es crear una función JavaScript que realice una llamada a nuestro _handler_ mediante el objeto **XmlHttpRequest**. Esta función debe aceptar tres parámetros que son los que se pasan por defecto al dispararse el evento _window.onerror_. El ejemplo siguiente muestra un ejemplo de como enviar a nuestro _handler_ (LogJSError.ashx) los 3 parámetros vía POST.

function LogJSError (sMsg, sUrl, sLine) { var handler\_url = “LogJSError.ashx”; var params = “msg=” + encodeURIComponent(sMsg); params += “&url=” + encodeURIComponent(sUrl); params += “&line=” + encodeURIComponent(sLine);

    var http = XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    
    http.open("POST", handler_url, true);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length", params.length);
    http.send(params);
    
    return true; }
    

window.onerror = LogJSError; </pre>

Este código presenta un pequeño problema (como siempre) y es que sólo funciona en Internet Explorer y en Firefox. En Chrome y Opera el evento _window.onerror_ no es funcional, parece ser que es por un [bug](http://code.google.com/p/chromium/issues/detail?id=7771) ya reportado. En las aplicaciones donde pretendo implementar este sistema de traza, los usuarios de Chrome no superan el 12% del total y no hay ni un usuario de Opera, así que, me conformo con controlar los errores en los dos principales navegadores.

El paso siguiente es crear el _handler_ que obtenga los parámetros de error que se le pasen y lance el evento. En el ejemplo se obtiene, adicionalmente, el valor de la [variable HTTP\_USER\_AGENT](http://msdn.microsoft.com/es-es/library/ms524602.aspx) que contiene la descripción del navegador que ha realizado la petición. Una vez tenemos toda la información necesaria, lanzamos el evento mediante el método **Raise** de la clase **WebBaseEvent**. A este método le pasamos una nueva instancia de un tipo de evento que vamos a crear continuación (_WebJSErrorEvent_), y al que pasamos en el constructor la instancia del handler y las propiedades del error.

public void ProcessRequest(HttpContext context)
{
    HttpRequest request = context.Request;

    string msg = request\["msg"\];
    string url = request\["url"\];
    string line = request\["line"\];
    string agent = request.ServerVariables\["HTTP\_USER\_AGENT"\];

    if (!string.IsNullOrEmpty(msg))
    {
        WebBaseEvent.Raise(new WebJSErrorEvent(this, msg, line, url, agent));
    }
}

Ahora sólo queda crear el nuevo tipo de evento. Para esto, debemos crear una clase que herede de **WebBaseErrorEvent**. En el constructor de la clase asignamos los valores de las variables miembro y sobrecargamos el método **FormatCustoEventDetails**, en el que añadimos la información que queremos mostrar al objeto **formatter**.

using System.Web.Management;

namespace LogJSError
{
    public class WebJSErrorEvent : WebBaseErrorEvent
    {
       public string msg { get; set; }
       public string line { get; set; }
       public string url { get; set; }
       public string agent { get; set; }

       public WebJSErrorEvent(object source, string msg, string line, string url, string agent)
           : base (msg, source, WebEventCodes.WebExtendedBase, new System.Exception(msg))
       {
           this.msg = msg;
           this.line = line;
           this.url = url;
           this.agent = agent;
       }

       public override void FormatCustomEventDetails(WebEventFormatter formatter)
       {
           base.FormatCustomEventDetails(formatter);

           formatter.AppendLine("Error message: " + this.msg);
           formatter.AppendLine("Line: " + this.line);
           formatter.AppendLine("Url: " + this.url);
           formatter.AppendLine("Agent: " + this.agent);
       }
    }
}

Para terminar y una vez tenemos todo implementado, solo resta configurar _Health Monitoring_ en nuestro _web.config_ para que utilice alguno de los proveedores existentes para registrar los eventos. En el ejemplo, creamos un _eventMapping_ indicando el nombre y el tipo (_namespace_ y nombre de la clase). Y, mediante un elemento de la colección _rules_, asignamos el evento que acabamos de definir (_JavaScript Error Events_) al proveedor _EventLogProvider_, que escribirá la información en el registro de eventos de Windows.

 

En el código HTML he añadido código para que se intente ejecutar una función que no existe en el \*onload\* de la página, de esta forma estaremos provocando un error en cada recarga. Si ejecutamos la aplicación, no veremos ningún mensaje de error, pero si miramos en el visor de sucesos, podremos ver una nueva advertencia de ASP.NET con la información detallada que hemos añadido en el método \*\*FormatCustomEventDetails\*\*.

**Descarga código fuente:** 

[LogJSError.zip](http://sdrv.ms/14OUvpX)

