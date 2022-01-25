---
title: Enviar notificaciones push mediante WNS
tags: [programming, windows_store]
reviewed: true
---
En la entrada anterior introdujimos las notificaciones en aplicaciones Metro viendo cómo [enviar notificaciones toast programadas](/notificaciones-toast-programadas-en-aplicaciones-metro). En la entrada de hoy vamos a ver un ejemplo completo de cómo montar un servicio web en Azure para que envíe notificaciones push a nuestra aplicación haciendo uso del sistema de notificaciones push de Windows (WNS). La solución de la aplicación se compondrá por un proyecto Windows Metro en JavaScript y por un servicio WCF. En este primer ejemplo, el servicio expondrá dos métodos para mantener la lista de canales registrados y otro para enviar una notificación toast a todos los canales.

En este artículo no voy a explicar los conceptos básicos de funcionamiento del servicio de notificaciones push de Windows, por lo que es muy recomendable leer la [información general sobre notificaciones push](http://msdn.microsoft.com/es-es/library/windows/apps/xaml/hh913756.aspx) que está disponible en la MSDN para conocer los requisitos y su funcionamiento.

Servicio WCF
---

Comenzamos creando un proyecto _WCF Service Application_ que nos servirá para registrar el canal de notificaciones y para enviar las notificaciones a todos los canales registrados. Como este servicio va a ser consumido desde JavaScript marcamos las dos operaciones con el atributo **WebInvoke** para indicar el método y el formato de las solicitudes y respuestas. El contrato del servicio queda de la siguiente forma:

```csharp
[ServiceContract] 
public interface INotificationService 
{ 
    [OperationContract]
    [WebInvoke(Method = “POST”, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)] 
    int Register(string uri);

    [OperationContract]
    [WebInvoke(Method = "POST", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
    string SendToast(); 
}
```
Una particularidad del servicio que vamos a crear es que necesitamos que mantenga una lista con todos los canales registrados. Para conseguir esto establecemos la propiedad **InstanceContextMode** del atributo **ServiceBehavior** a **Single**, para indicar que se utilice una sola instancia del servicio para todas las llamadas. Esto, como podréis intuir, es simplemente para fines demostrativos, en un servicio real en un entorno de producción deberíamos guardar la lista de canales en un repositorio. Veamos a continuación la implementación de los dos métodos del servicio:
    
```csharp
[ServiceBehavior(InstanceContextMode = InstanceContextMode.Single)]
public class NotificationService : INotificationService
{
    private static readonly List<string> channels = new List<string>();

    public int Register(string uri)
    {
        lock (((ICollection)channels).SyncRoot)
        {
            if (!channels.Contains(uri))
            {
                channels.Add(uri);
            }
        }

        return channels.Count;
    }

    public string SendToast()
    {
        string image = "http://www.microsoft.com/global/surface/en/us/publishingimages/new/hero.jpg";
        string text = String.Format("Notificación enviada el {0} a las {1}", DateTime.Now.ToShortDateString(), DateTime.Now.ToShortTimeString());

        string toastTemplate = String.Format("<toast><visual><binding template="ToastImageAndText01"><image id="1" src="{0}" alt="image1"/><text id="1">{1}</text></binding></visual></toast>", image, text);

        var wns = new WNSNotification();
        foreach (var channel in channels)
        {
            wns.PostToWns(channel, toastTemplate);
        }

        return "OK";
    }
}
```

Autenticación y envío a WNS
---    

El método **Register** añade la dirección que se pasa como parámetro a la lista _channels_ y devuelve el número total de canales registrados. El método **SendToast** es el que se encarga de crear la notificación y enviar la notificación al WNS por cada uno de los canales registrados. Este método hace una llamada al método **PostToWns** de nuestra clase **WNSNotification**, que es la que se encarga de autenticarse en el WNSy enviar en último término la notificación. Echemos un vistazo a código del método PostToWns.

```csharp
public string PostToWns(string uri, string xml, string type = "wns/toast")
{
  var accessToken = GetAccessToken(secret, sid);

  byte[] contentInBytes = Encoding.UTF8.GetBytes(xml);

  HttpWebRequest request = HttpWebRequest.Create(uri) as HttpWebRequest;
  request.Method = "POST";

  request.Headers.Add("X-WNS-Type", type);
  request.Headers.Add("Authorization", String.Format("Bearer {0}", accessToken.AccessToken));

  using (Stream requestStream = request.GetRequestStream())
  requestStream.Write(contentInBytes, 0, contentInBytes.Length);

  using (HttpWebResponse webResponse = (HttpWebResponse)request.GetResponse())
  return webResponse.StatusCode.ToString();
}
```

La primera acción a realizar es obtener el token de acceso previa autenticación en el WNS. Para realizar esta autenticación, tenemos que enviar una petición a _https://login.live.com/accesstoken.srf_ con una serie de parámetros entre los que están el identificador de seguridad del paquete (SID) y la clave secreta que se asignan al registrar la aplicación en la [Windows Store](https://appdev.microsoft.com/StorePortals/). Si no disponéis de cuenta de desarrollador de la **Windows Store**, podéis registrar las aplicaciones en el portal temporal [manage.dev.live.com](https://manage.dev.live.com/). En la imagen podemos ver la información que obtenemos al registrar la aplicación en la Windows Store. Los datos que tenemos que utilizar son el Package name, SID y client secret.

Los otros parámetros que tenemos que enviar (grant_type y scope) tienen unos valores fijos. Este es el código para realizar la petición de autenticación.

```csharp
protected OAuthToken GetAccessToken(string secret, string sid)
{
    var urlEncodedSecret = HttpUtility.UrlEncode(secret);
    var urlEncodedSid = HttpUtility.UrlEncode(sid);

    var body = String.Format("grant_type=client_credentials&client_id={0}&client_secret={1}&scope=notify.windows.com",
                             urlEncodedSid,
                             urlEncodedSecret);

    string response;
    using (var client = new WebClient())
    {
        client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
        response = client.UploadString("https://login.live.com/accesstoken.srf", body);
    }
    return GetOAuthTokenFromJson(response);
}
```

Si obtenemos una respuesta de “200 Correcto” significa que la autenticación se realizó correctamente y que la respuesta incluye un token de acceso que deberemos enviar con cada notificación, hasta que el token de acceso expire.

Después de realizar la autenticación, el método *PostToWns *realiza una solicitud de envío de notificación a la URI del canal añadiendo los encabezados obligatorios.

request.Headers.Add("X-WNS-Type", type);
request.Headers.Add("Authorization", String.Format("Bearer {0}", accessToken.AccessToken));

El encabezado **X-WNS-Type** define el tipo de notificación que se envía: tile, toast, badge o raw. Los valores posibles que se pueden indicar en este encabezado son: wns/badge, wns/tile, wns/toast o wns/raw. El encabezado de autorización se utiliza para indicar el token de acceso obtenido con el método **GetAccessToken**. Una vez tenemos nuestro servicio funcionando sólo nos queda implementar el cliente, la aplicación Windows Metro.

Aplicación Windows Metro
---    

El primer paso que debe realizar el cliente Metro es obtener el canal de notificación para registrarlo en el servicio. Mediante el método **createPushNotificationChannelForApplicationAsync** obtenemos el objeto **PushNotificationChannel** asociado a la aplicación. De este objeto nos interesan sus 2 propiedades (_ExpirationTime_ y _Uri_). Es importante que nuestro servicio tenga en cuenta el tiempo de caducidad ya que cualquier notificación enviada después de esa fecha será rechazada. Al iniciar la aplicación o mediante un proceso en segundo plano debemos comprobar si el canal todavía es válido. En el ejemplo no he implementado esta comprobación, pero es algo que debemos realizar para evitar que nuestra aplicación deje de recibir notificaciones.

Una vez hemos obtenido el canal de notificación, lo enviamos a nuestro método **Register** del servicio realizando la llamada mediante **WinJS.xhr**.

```js
var push = Windows.Networking.PushNotifications;
push.PushNotificationChannelManager.

createPushNotificationChannelForApplicationAsync().then(function (ch) {
    var uri = ch.uri;
    var expiry = ch.expirationTime;
    updateChannelUri(uri, expiry);
});

function updateChannelUri(channel, expiry) {
    if (channel) {
        var serverUrl = "http://localhost:58762/notificationservice.svc/Register";

        var xhr = new WinJS.xhr({
            type: "POST",
            url: serverUrl,
            headers: { "Content-Type": "application/json; charset=utf-8" },
            data: JSON.stringify(channel)
        }).then(function (req) {
            document.getElementById("result").innerHTML = "Hay " + req.responseText + " canales registrados";

        }, function (req) {
            console.log(req);
        });
    }
}
```

Al tener registrado el canal en nuestro servicio, ya estamos preparados para poder enviar notificaciones. En la aplicación de ejemplo he añadido un botón para hacer una petición al servicio para que envíe una notificación toast a todos los canales registrados, haciendo una llamada al método **SendToast **que hemos visto al comienzo. De esta forma estamos simulando una acción externa que provoca una notificación a todos los clientes registrados.

```js
document.getElementById("sendToast").addEventListener("click", function () {

  var serverUrl = "http://localhost:58762/notificationservice.svc/SendToast";

  var xhr = new WinJS.xhr({
      type: "POST",
      url: serverUrl,
      headers: { "Content-Type": "application/json; charset=utf-8" }
  }).then(function (req) {
      console.log(req);
  }, function (req) {
      console.log(req);
  });
});
```

Para que la aplicación sea capaz de recibir notificaciones debemos marcar la opción Toast capable en la pestaña Application UI del manifiesto de la aplicación. Además tenemos que cambiar en nombre del paquete (*Package name*) por el que nos asignaron al registrar la aplicación en la Windows Store.

Si ejecutamos la aplicación y pulsamos el botón Enviar nos aparecerá unos instantes después la notificación. Con esto ya hemos visto el código mínimo para poder utilizar las notificaciones push en nuestras aplicaciones Metro. Pero aún queda un último detalle, hacer disponible nuestro servicio en Internet. Todas las pruebas las hemos hecho utilizando nuestro servicio ejecutando en el IIS Express local, vamos a ver ahora como subir nuestro servicio a Azure.

Servicio en la nube de Azure
---

Si tenemos alguna suscripción de Windows Azure los pasos para subir nuestro servicio son muy sencillos. Si no tenéis suscripción, podéis obtener una [evaluación gratuita de 90 días.](https://www.windowsazure.com/es-es/pricing/free-trial/) Para crear el servicio en Azure pulsamos con el botón secundario del ratón sobre el proyecto de WCF en el explorador de la solución y seleccionamos la opción *Add Windows Azure Cloud Service Project*. Esto generará un nuevo proyecto en la solución que estará listo para ser publicado en Azure.

Al publicar aparecerá un asistente en el que tendremos que seleccionar nuestra suscripción y el servicio Cloud donde queremos publicar el servicio.

Una vez tengamos el servicio publicado sólo tendremos que cambiar las URL de las dos llamadas que se hacen a los servicios en localhost a los servicios en Azure.

Resumen
---

En esta entrada hemos visto como enviar notificaciones Push desde un servicio alojado en Azure. Lo primero que hemos visto es cómo crear el servicio para ser consumido desde un cliente JavaScript, la forma de autenticarse, obtener el token de acceso y cómo enviar una notificación a través de WNS. Después hemos creado el cliente y hemos visto como obtener el canal de notificación para la aplicación y cómo realizar la llamada a nuestro servicio. Por último hemos visto como crear y publicar el servicio en Azure.

Referencias
---

[Push notification overview (Metro style apps)](http://msdn.microsoft.com/es-es/library/windows/apps/xaml/hh913756.aspx)  
[Envío de notificaciones de inserción](http://msdn.microsoft.com/es-es/library/windows/apps/hh465460.aspx)  
[Cómo autenticar con los Servicios de notificaciones de inserción de Windows (WNS)](http://msdn.microsoft.com/es-es/library/windows/apps/hh465407.aspx)  

