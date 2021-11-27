---
title: WAT y notificaciones con Windows Azure Notification Hub
tags: [windows_store, azure]
---
Muchos ya conocéis lo poco que me gustan los generadores de aplicaciones y lo peligrosos que pueden llegar a ser según en manos de quien caigan. Sin embargo, en esta ocasión voy a comentar el soporte de notificaciones de **WAT** (_Web Application Template_), una plantilla que nos permite convertir una web en una aplicación de **Windows 8** o **Windows Phone 8**.

Para los que no conozcáis WAT, no os hagáis ideas equivocadas, no existe ningún tipo de magia oculta detrás de esta plantilla, básicamente en lo que se basa es en mostrar una web incrustada en un elemento **x-ms-webview**. Lo interesante es que, más allá de ver simplemente una web como una aplicación, es posible personalizar la aplicación. Entre otras opciones, podemos agregar una barra de aplicación y de navegación, configurar la integración con los contratos compartir, búsqueda y configuración, configurar la actualización de las tiles y recibir notificaciones. Todo esto simplemente modificando un fichero de configuración, un fichero JSON. Además, podemos inyectar CSS para modificar la apariencia de la web o podemos ocultar los elementos no deseados, como menús de navegación o pies de página.

Para comenzar a utilizar WAT, tenemos disponible una extensión para Visual Studio que nos añade la plantilla para generar de forma automática el proyecto de Windows 8.1. En el caso de Windows Phone, tendremos que utilizar el código como base de nuestro proyecto.

Podéis descargar la extensión y el código de **CodePlex** ([wat.codeplex.com](http://wat.codeplex.com/)) y la documentación completa está disponible en [wat-docs.azurewebsites.net](http://wat-docs.azurewebsites.net/). Si queréis conocer más a fondo la posibilidades de esta plantilla, este mes podéis asistir a una [sesión formativa de WAT](https://msevents.microsoft.com/CUI/EventDetail.aspx?EventID=1032578107&Culture=es-ES&community=0) en la oficinas de Microsoft el próximo día 27. Los detalles del evento están en este [post de Luis Guerrero](http://blogs.msdn.com/b/esmsdn/archive/2014/01/28/techday-jueves-wat-web-app-template.aspx).

Bien, pues como he comentado al principio, de todas las características de WAT, la que me ha llamado la atención es que tenemos soporte para utilizar el Hub de notificaciones de Azure para recibir notificaciones push, y es en lo que me voy a centrar en esta entrada.

Configurando el Hub de notificaciones
-------------------------------------

El primer paso para poder enviar notificaciones a nuestra aplicación es generar un **Notification Hub** mediante el asistente del portal de Azure, en el que tenemos que indicar el nombre para el _Notification Hub_ y para el _Namespace_ de Service Bus.

[![create-notification-hub](create-notification-hub.png)](create-notification-hub.png)

Una vez generado, tenemos que configurar el Hub para que pueda autenticarse con el servicios WNS para enviar las notificaciones. Para esto necesitamos tener una aplicación creada en el **[Dev Center](https://appdev.microsoft.com/StorePortals/)** y obtener el **Package Security Identifier (SID)** y **Client Secret**.

[![wns-live](wns-live.png)](wns-live.png)

Y añadirlas a la sección de _Windows Notification Settings_ del hub de notificaciones.

[![wns-settings-azure](wns-settings-azure.png)](wns-settings-azure.png)

Lo último que nos queda por hacer en el portal de Azure es obtener las dos cadenas de conexión para comunicarnos en el Hub de Notificaciones. Podemos ver estas cadenas en el Dashboard del hub de notificaciones o pulsando en “Connection Information”.

[![access-connection-hub](access-connection-hub.png)](access-connection-hub.png)

La primera cadena, _DefaultListenSharedAccessSignature_, la utilizaremos en nuestra aplicación cliente Windows 8 para recibir las notificaciones y la segunda (_DefaultFullSharedAccessSignature_) para enviar notificaciones desde nuestro servicio back-end.

Activando las notificaciones en WAT
-----------------------------------

Como he comentando al principio, toda la configuración en WAT se realiza mediante un fichero JSON. Para activar las notificaciones Push simplemente tenemos que modificar la sección _notifications_.

    "notifications": {
      "enabled": true,
      "azureNotificationHub": {
        "enabled": true,
        "endpoint": "https://tokiota-ns.servicebus.windows.net/",
        "secret": "[Secret]",
        "path": "tokiota",
        "tags": [
          "Live Tiles", "Events", "News"
        ]
      }
    }
    </pre>
    
    Los elementos importantes son **endpoint**, **secret**, **path** y **tags**. En **endpoint** indicaremos la dirección del namespace del servicio de Service Bus. En **secret** tendremos que establecer la clave de la cadena de conexión *DefaultListenSharedAccessSignature*. En **path** indicaremos el nombre del hub de notificaciones y, por último, en **tags** podemos definir un array de cadenas que indicarán las categorías a las que el usuario se podrá suscribir. 
    
    Si ejecutamos la aplicación y accedemos a través del *charm* a la configuración de las notificaciones, veremos una pantalla con la posibilidad de activar las notificaciones para cada unas de las categorías que hemos definido. Por defecto, todas las notificaciones estarán activadas. 
    
    <a href="notifications.png">![notifications](notifications.png)</a>
    
    
    
    ## Recibir notificaciones
    
    
    
    Para que la aplicación pueda recibir notificaciones, solo tenemos que asociar (*Project/Store/Associate App with the Store*) la aplicación Windows 8 con la Windows Store. El proceso de asociación cambia distintos valor del *manifest*: *package display name*, *package name*, *published ID*, *Publisher Display Name* y versión.
    
    Después de realizar esto ya podremos realizar las pruebas de notificaciones. Si la aplicación va a recibir notificaciones toast, tendremos que activar también la opción *Toast Capable* en el *manifest* de la aplicación.
    
    Ahora ya tenemos todo listo para poder recibir notificaciones, solo queda ver cómo las enviamos.
    
    
    
    ## Enviar notificaciones
    
    
    Para enviar las notificaciones podemos utilizar la opción de depuración en el portal de Windows Azure, crear un script en **Mobile Services** o crear una aplicación que envíe la notificación. 
    
    Para poder enviar notificaciones desde un servicio back-end, tenemos que agregar una referencia al SDK de Windows Azure Service Bus, añadiendo el paquete de **WindowsAzure.ServiceBus** de Nuget y utilizar la clase **NotificationHubClient**. En el método **SendWindowsNativeNotificationAsync** podemos pasar el tag de destino, que se corresponde con la categoría que hemos definido en el JSON de configuración de WAT. En el siguiente ejemplo estamos enviando una notificación toast con la etiqueta "News".
    
    <pre class="brush:csharp">
    NotificationHubClient hub = NotificationHubClient.CreateClientFromConnectionString("Endpoint=sb://tokiota-ns.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=[SharedAccessKey]", "tokiota");
    
    var toast = @"&lt;toast&gt;&lt;visual&gt;&lt;binding template=""ToastText01""&gt;&lt;text id=""1""&gt;Sample toast notification!&lt;/text&gt;&lt;/binding&gt;&lt;/visual&gt;&lt;/toast&gt;";
    
    await hub.SendWindowsNativeNotificationAsync(toast, "News");
    </pre>
    
    Si utilizamos un servicio de **Azure Mobile Services**, mediante el siguiente script podemos enviar el mismo tipo de notificación que en el ejemplo anterior.
    
    <pre class="brush:js">
    var azure = require('azure');
    
    var notificationHubService = azure.createNotificationHubService(
            'tokiota', 
            'Endpoint=sb://tokiota-ns.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=[SharedAccessKey]');
    
    notificationHubService.wns.sendToastText01("News", {
                text1: 'Sample toast notification!'
    }, sendComplete);
    

Conclusiones
------------

El resultado que podemos obtener con WAT es una aplicación bastante decente, aunque siempre vamos a depender de lo bien construida que esté la web que estemos utilizando. Si es una web responsive y que permita ocultar fácilmente elementos no deseados, nos será mucho más fácil obtener buenos resultados.

Además, como hemos visto en este artículo, podemos integrar la aplicación con el sistema operativo sin tener conocimientos de WinJS, que al final es la idea detrás de todos estos sistemas de generación de apps.

Referencias
-----------

[TechDay Jueves - WAT, Web app template](http://blogs.msdn.com/b/esmsdn/archive/2014/01/28/techday-jueves-wat-web-app-template.aspx) 
[Web App Template](http://wat.codeplex.com/) 
[Use Notification Hubs to send breaking news](http://www.windowsazure.com/en-us/documentation/articles/notification-hubs-windows-store-dotnet-send-breaking-news/?fb=es-es)

