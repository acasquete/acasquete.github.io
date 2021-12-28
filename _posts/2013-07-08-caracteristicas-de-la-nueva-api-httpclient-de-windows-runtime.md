---
title: Características de la nueva API HttpClient de Windows Runtime
tags: [windows_store, winrt]
---
Una de las novedades incluidas en **Windows 8.1 Preview** es la nueva API para conectar con servicios HTTP. Esta nueva API que está disponible en el _namespace_ **Windows.Web.Http**, viene a reemplazar a los sistemas que utilizamos hasta ahora: la clase _System.Net.HttpClient_ en C# y la función _WinJS.xhr_ en JavaScript. En esta entrada vamos a ver las ventajas y las características que nos aporta esta nueva API.

La primera ventaja, que ya se puede intuir por el título, es que **HttpClient** es un componente Windows Runtime. Esto significa que lo vamos a poder utilizar independientemente del lenguaje que utilicemos para desarrollar **Windows Store apps**: C#, Javascript o C++. A partir de ahora vamos a tener una forma unificada de llamar a los servicios, sea cual sea nuestra elección de lenguaje. Veamos un primer ejemplo de cómo se utiliza desde Javascript.

var uri = new Windows.Foundation.Uri(“http://idlebit.azurewebsites.net”);

var httpClient = new Windows.Web.Http.HttpClient(); var requestMessage = new Windows.Web.Http.HttpRequestMessage(Windows.Web.Http.HttpMethod.get, uri);

httpClient.sendRequestAsync(requestMessage).then(function (response) {

    response.content.readAsStringAsync().then(function (content) {
        document.getElementById("result").innerText = content;
    }); });</pre> En este ejemplo utilizamos la clase **HttpRequestMessage** para crear el mensaje que queremos enviar al servidor. En este objeto podemos establecer toda la información que necesitamos para realizar la petición (contenido, encabezados y método HTTP) y después llamamos a **httpClient.sendRequestAsync** para realizar la petición. Este método nos devuelve una *promise* que al completarse nos devolverá un objeto **HttpResponseMessage** con la respuesta del servidor que, además del contenido, código de respuesta y estado, contendrá la petición original.
    

Para leer el contenido de la respuesta disponemos de varios métodos dependiendo del tipo de contenido: **readAsStringAsync**, **readAsBufferAsync** o **ReadAsInputStreamAsync**. En el ejemplo utilizamos **readAsStringAsync** que nos devuelve el contenido como cadena de texto.

    ## Métodos por verbo HTTP
    

La clase **HttpClient** pone a nuestra disposición una serie de métodos que crean el objeto **HttpRequestMessage** por nosotros y son específicos para un verbo HTTP. Así por un lado tenemos los métodos **DeleteAsync**, **GetAsync**, **PostAsync** y **PutAsync** que nos permiten enviar peticiones DELETE, GET, POST y PUT. Y por otro lado tenemos métodos que buscan en el contenido de la respuesta y nos devuelven el valor directamente. Estos métodos son **GetStringAsync**, **GetBufferAsync**, **GetInputStreamAsync**. En el ejemplo, **GetStringAsync** buscará en el contenido de la respuesta y nos devolverá una cadena. Así que utilizando estos métodos, podemos simplificar bastante el ejemplo anterior de la siguiente forma:

var uri = new Windows.Foundation.Uri("http://idlebit.azurewebsites.net");

var httpClient = new Windows.Web.Http.HttpClient();

httpClient.getStringAsync(uri).done(function (result) {
    document.getElementById("result").innerText = result;
});

    ## Encabezados tipados
    

Otra de las ventajas de usar **HttpClient** es el uso de encabezados tipados. Esto que para desarrolladores de C# o C++ no representará ninguna novedad, sí lo será para los de JavaScript. Con la nueva API vamos a poder establecer la colección encabezados mediante propiedades de la colección _headers_ de **HttpRequestMessage** y vamos a poder leerlos de la misma forma en la respuesta. Aunque esta característica no parece muy espectacular, os aseguro que el uso de estos encabezados evitará más de un error al escribir algún que otro nombre de encabezado.

var requestMessage = new Windows.Web.Http.HttpRequestMessage(Windows.Web.Http.HttpMethod.get, uri);

requestMessage.headers.referer= "http://www.site2.com";

httpClient.sendRequestAsync(requestMessage).then(function (response) {

    response.content.readAsStringAsync().then(function (content) {
        document.getElementById("result").innerText = content;
    });
});

Además de los encabezados estándar, también podemos añadir encabezados personalizados mediante el método **TryAppendWithoutValidation**.

request.Headers.TryAppendWithoutValidation("X-Requested-With", "XMLHttpRequest");

y también podemos iterar por todos los encabezados de la siguiente forma:

for (var header in response.headers) 
{
    console.log(header + "=" + response.headers\[header\]);
}

for (var header in response.content.headers) {
    console.log(header + "=" + response.content.headers\[header\]);
}

Como podemos ver, se hace distinción entre dos tipos de encabezados: los encabezados de la petición y los del contenido. Los encabezados de petición dan información sobre el servidor y sobre el acceso al recurso (_Retry-After_, _Server_,\* Age_, etc.) y los del contenido definen metainformación sobre el cuerpo del mensaje, entre los que podemos encontrar \*Content-Encoding_, _Content-Length_, _Expires_ o _Last-Modified_.

    ## Cookies
    

Otra de las novedades es la gestión de _cookies_, la nueva API nos permite insertar, eliminar y listar _cookies_. Pero antes de ver cómo se utilizan las _cookies_, hay que introducir un nuevo personaje en esta historia. Se trata de la clase **HttpBaseProtocolFilter** a la que le tenemos que prestar la debida atención porque detrás de esta clase se encuentra la característica más potente de toda esta nueva API: los filtros, que determinan cómo se envía y se recibe la información.

Una propiedad de **HttpBaseProtocolFilter** es **CookieManager**, que como podréis intuir nos va ayudar a gestionar las _cookies_. Echemos un vistazo al siguiente código para crear una cookie.

var bpf = new HttpBaseProtocolFilter();
var cookieManager = bpf.CookieManager;
var cookie = new HttpCookie("myCookieName", ".example.com", "/");
cookie.Value = "myValue";
cookieManager.SetCookie(cookie);

var httpClient = new HttpClient(bpf);

Primero creamos la cookie mediante la clase **HttpCookie** pasando el nombre, dominio y la establecemos mediante el método **SetCookie** del **CookieManager**. Para poder utilizar este filtro lo pasamos en el constructor al instanciar **HttpClient**. Ahora este filtro se utilizará en todas las peticiones de esa instancia de HttpClient.

El **CookieManager** también nos da la opción de poder leer todas las _cookies_ que nos llegan en una petición. Para esto utilizaremos el método getCookies de la siguiente forma:

var bpf = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();
var cookieManager = bpf.cookieManager;
var uri = new Windows.Foundation.Uri("http://www.bing.com");

var cookies = cookieManager.getCookies(uri);

for (var i in cookies) {
   console.log(cookies\[i\].name + " " + cookies\[i\].value + " " + cookies\[i\].expires);
}

El resultado de este código mostrará tanto las cookies generadas en la petición a bing.com como las generadas anteriormente ya que incluye también las cookies persistentes.

    ## Caché
    

La nueva API nos proporciona mucho más control sobre cómo funciona la caché. Ahora podemos decidir cuando se guarda el contenido de una respuesta en la caché y podemos decidir la forma en que utilizamos estos datos. Esta capacidad de cambiar estos comportamientos es nueva para todos los lenguajes.

El primer cambio es que disponemos de una propiedad en el objeto **HttpResponse** que nos indica si los datos devueltos en una petición web provienen de la caché local o de la red. Lo vemos en el siguiente código.

 
httpClient.getAsync(uri).done(function (httpResponse) {

  switch (httpResponse.source)
  {
      case Windows.Web.Http.HttpResponseMessageSource.cache:
      break;
   
      case Windows.Web.Http.HttpResponseMessageSource.network:
      break;
   
      case Windows.Web.Http.HttpResponseMessageSource.none:
      break;
  }

});

La propiedad **httpResponseMessage.Source** puede tomar tres valores: **Cache**, **Network** o **None**. Aunque el valor **None** es un valor por defecto y no debería ser devuelto nunca.

Pero como comentaba al principio, la característica importante referente a la caché es que podemos establecer comportamientos para la lectura y escritura, es decir, al hacer una petición a un servicio web podemos indicar si queremos que la respuesta se guarde en caché o no. Este comportamiento lo indicamos mediante la propiedad **CacheControl** de la clase **HttpBaseProtocolFilter**.

var bpf = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();

bpf.cacheControl.writeBehavior = Windows.Web.Http.Filters.HttpCacheWriteBehavior.default;
// or
bpf.cacheControl.writeBehavior = Windows.Web.Http.Filters.HttpCacheWriteBehavior.noCache;

var hc = new Windows.Web.Http.HttpClient(bpf);

El valor **HttpCacheWriteBehavior.default** es el comportamiento predeterminado, en el que todas las respuestas se guardan en la caché local HTTP. Es el comportamiento que estamos acostumbrados a ver en los navegadores, si un servidor devuelve una respuesta correcta (200), el resultado se guardará en caché. Sin embargo, si queremos forzar a que nunca se guarde en cache tenemos que utilizar el valor **HttpCacheWriteBehavior.noCache**.

Además de establecer cuando se guarda la respuesta en caché, podemos indicar el comportamiento en la lectura de datos de la caché. Si tenemos información en caché y que no haya expirado, por defecto, se leerá de caché, aunque también en este caso podemos modificar el comportamiento predeterminado mediante la propiedad **ReadBehaviour**.

var bpf = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();

bpf.cacheControl.readBehavior = Windows.Web.Http.Filters.HttpCacheReadBehavior.default;
// or
bpf.cacheControl.readBehavior = Windows.Web.Http.Filters.HttpCacheReadBehavior.mostRecent;
// or
bpf.cacheControl.readBehavior = Windows.Web.Http.Filters.HttpCacheReadBehavior.onlyFromCache;

var hc = new Windows.Web.Http.HttpClient(bpf);

El valor **MostRecent** hace que se utilice la caché local si está disponible, pero siempre se consultará al servicio si hay una versión más reciente. Este modo funciona si el servidor devuelve el encabezado “Last-Modified”. En la siguiente petición que hagamos, se enviará el encabezado “If-Modified-Since” y si el contenido no ha cambiado desde la fecha indicada, el servidor devolverá un valor 304 (Not modified) con lo que no se transmitirá nada, nos ahorraremos la transferencia de contenido y los datos se leerán de la caché.

El caso opuesto es el valor **onlyFromCache** en el que indicamos que se utilice la caché local siempre. En este caso no se realizará ninguna petición y si el contenido no está disponible en la caché devolverá un error. Este comportamiento es el ideal para ofrecer que nuestra aplicación siga funcionando de forma offline o también para crear la primera petición al abrir nuestra aplicación.

Haciendo uso de la caché correctamente vamos a ofrecer al usuario una experiencia mucho más fluida y sin las esperas en la carga de imágenes a las que estamos acostumbrados. Además hay una nueva característica en Windows 8.1 llamada “_Fresh apps_” que permite tener los datos de la aplicación actualizados aunque nuestra aplicación no este funcionando. Aunque esto lo veremos en otro post os dejo el enlace de la MSDN a la clase [**ContentPrefetcher** que permite tener actualizados nuestros contenidos](https://web.archive.org/web/20210123141000/http://msdn.microsoft.com/en-us/library/windows/apps/windows.networking.backgroundtransfer.contentprefetcher).

    ## Filtros
    

En los dos apartados anteriores hemos introducido el concepto de filtro, algo que será familiar para los desarrolladores de .NET ya que el mismo concepto detrás de los **Handlers HTTP**. Los filtros son piezas de código que nos permiten mantener la lógica de nuestra aplicación simple dejando otras responsabilidades, como la implementación de seguridad o la gestión de errores, a los filtros.

[![mockup](https://web.archive.org/web/20210123141000im_/http://www.casquete.es/wp-content/uploads/2013/07/mockup.png)](https://web.archive.org/web/20210123141000/http://www.casquete.es/wp-content/uploads/2013/07/mockup.png)

Podemos insertar en la _pipeline_ tantos filtros como necesitemos. Los mensajes de peticiones enviados por el objeto **HttpClient** son manipulados por todos los filtros que hemos introducido en el _pipeline filter_ antes de que se envíe al servicio web. Y de la misma forma, la respuesta también pasa a través de todos esos filtros. Estos filtros pueden modificar los datos que viajan en los dos sentidos, tanto en la petición como en la respuesta.

En los ejemplos de la [Microsoft Developer Network](https://web.archive.org/web/20210123141000/http://code.msdn.microsoft.com/) tenemos varias implementaciones de filtros que nos van a permitir ver cómo están implementados. Los filtros que tenemos disponibles son: **503 Retry Filter**, **Metered Network** y **Auth Filter**. Los dos primeros filtros los tenemos disponibles en la solución de [ejemplo de HttpClient](https://web.archive.org/web/20210123141000/http://code.msdn.microsoft.com/HttpClient-sample-55700664) y el tercero en el ejemplo de [Web authentication broker](https://web.archive.org/web/20210123141000/http://code.msdn.microsoft.com/Web-Authentication-d0485122). Si nos bajamos estos ejemplos veremos que estos filtros son componentes Windows Runtime y están escritos en C++. Podemos utilizarlos en nuestras aplicaciones agregando el proyecto a nuestra solución, pero parece evidente que estos filtros formarán parte de WinRT en la versión final.

Veamos qué nos proporcionan cada uno de estos filtros:

    ### 503 Retry Filter
    

El error 503 es un error que devuelve el servidor cuando no puede atender la petición termporalmente, normalmente provocado por una sobrecarga. Lo normal es que se devuelva un encabezado Retry-After que indica el tiempo en segundos para que reintentemos la petición. Este mecanimo de reintento es algo que hasta ahora deberíamos implementar en nuestra lógica de aplicación. Sin embargo, nuestra lógica de negocio no tiene porque conocer y responder los estados y problemas de conectividad, ahora toda la lógica de reintento está encapsulada en el filtro. La forma de utilizar este filtro es bien sencilla. Solo tenemos que instanciar el filtro **HttpRetryFilter** pasando una instancia de **HttpBaseProtocolFilter** y después pasarlo en el constructor del HttpClient.

var baseProtocolFilter = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();

var retryFilter = new HttpFilters.HttpRetryFilter(baseProtocolFilter);

httpClient = new Windows.Web.Http.HttpClient(retryFilter);

    ### Metered Network Filter
    

Este filtro nos permite determinar que peticiones se realizan en base a unas prioridades por petición y según el tipo y estado de la red al que estemos conectados. Para poder utilizarlo tenemos que indicar una prioridad en las peticiones mediante una propiedad en el requestMessage.

request.properties\["meteredConnectionPriority"\] = HttpFilters.MeteredConnectionPriority.low

El filtro procesará todas las conexiones en modo “Normal”, cuando no estemos en Roaming ni tengamos un coste asociado a la conexión. Si estamos en modo Conservador (_Conservative_), es decir, si no estamos en Roaming y no hemos sobrepasado el límite de datos, pero tenemos un coste asociado a la conexión, solo se procesarán las peticiones marcadas con prioridad media (_Medium_) o alta (_High_). En cualquier otro caso solo se permitirán las peticiones marcadas con alta prioridad y hayamos establecido el valor de la propiedad OptIn (_Opted in_) a true. Esta una forma de que el usuario pueda dar su confirmación para que se realicen peticiones cuando llevan un coste asociado.

Para probar este filtro tendremos que utilizar el simulador ya que ahora podemos establecer las distintas propiedades de la red. Podemos indicar si estamos en roaming, el tipo de coste (variable o fijo), o si estamos por debajo del límite de datos según el plan de datos.

    ### Auth Filter
    

El último filtro que nos queda por ver es de autorización. Este filtro nos permite tener toda la lógica de autorización con OAuth 2.0 separada de la de nuestra aplicación. Implementar la autorización con OAuth requiere de varios pasos, obtener un Request Token, redirigir al servicio para autenticar y autorizar al usuario y obtener el token de acceso. Ahora con el filtro OAuth2Filter solo tenemos que pasar la configuración. En el ejemplo siguiente se muestra como realizar la autenticación con el OAuth de Facebook.

var bpf = new Windows.Web.Http.Filters.HttpBaseProtocolFilter();
switchf = new AuthFilters.SwitchableAuthFilter(bpf);

var facebookFilter = new AuthFilters.OAuth2Filter(bpf);

var config = {
    clientId: clientId,

    // Common to all developers for this site
    technicalName: "facebook.com",
    apiUriPrefix: "https://graph.facebook.com/",
    sampleUri: "https://graph.facebook.com/me",

    redirectUri: "https://www.facebook.com/connect/login\_success.html",
    clientSecret: "",
    scope: "read\_stream",
    display: "popup",
    state: "",
    additionalParameterName: "",
    additionalParameterValue: "",
    responseType: "", // blank==default "token:.  null doesn't marshall.
    accessTokenLocation: "", // blank=default "query",
    accessTokenQueryParameterName: "", // blank=default "access\_token",
    authorizationUri: "https://www.facebook.com/dialog/oauth",
    authorizationCodeToTokenUri: ""
};

facebookFilter.authConfiguration = config;

switchf.addOAuth2Filter(facebookFilter);

var httpClient = new Windows.Web.Http.HttpClient(switchf);

A parte de estos tres filtros, podemos crearnos nuestros filtros personalizados utilizando C++ o C#. Pero esto lo veremos en la siguiente entrada.


## Resumiendo


En esta entrada hemos visto las nuevas características que incluye la nueva API de \*\*Windows.Web.HttpClient\*\* de Windows Runtime para conectarse a servicios Web. Hemos visto que podemos establecer los encabezados de las peticiones HTTP de una forma tipada y que tenemos métodos para listar, establecer o eliminar cookies. Además, esta nueva API nos da una nueva forma de trabajar con la caché permitiéndonos controlar la forma en que la aplicación guarda y lee los datos en caché. Y por último hemos visto la característica más potente de esta nueva API, los filtros, que nos permite tener una pieza de código separada de nuestra lógica de aplicación y manipular tanto la petición antes de que se envíe al servicio web como la respuesta recibida.


## Referencias


\[Windows.Web.Http namespace\](http://msdn.microsoft.com/library/windows/apps/dn279692)
\[Building Great Service Connected Apps\](http://channel9.msdn.com/Events/Build/2013/3-090)
\[Five Great Reasons to Use the New HttpClient API to Connect to Web Services\](http://channel9.msdn.com/Events/Build/2013/4-092)

