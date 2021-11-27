---
title: Fresh apps en Windows 8.1
tags: [windows_store, azure]
---
«Be fast & fluid». Este es el principio de diseño de **aplicaciones para la Windows Store** que nos dice que debemos responder a las acciones del usuario rápidamente. Sin embargo, muchas veces debido a la gran cantidad de información que tenemos que descargar, es inevitable que el usuario tenga que esperar hasta que la aplicación esté lista para mostrar la información.

La pantalla de presentación extendida (_extended splash screen_) con un indicador de progreso mientras la aplicación descarga los datos necesarios, es un recurso al que ya nos hemos acostumbrado. El uso de esta pantalla sucede en el mejor de los casos, en otros casos vemos como las imágenes se van cargando progresivamente. Estos dos problemas son un ejemplo de los que nos encontramos en todas las aplicaciones que tienen su origen de datos en un servicio web, encontrándonos con aplicaciones que no ofrecen la mejor experiencia al usuario.

Ahora con Windows 8.1, tenemos un nuevo mecanismo para indicar al sistema operativo el contenido que queremos que se descargue sin que la aplicación esté en ejecución. Estos recursos se precargan para que estén disponibles y actualizados al lanzar la aplicación y evitar tener que realizar peticiones durante la carga inicial. Toda esta información estará disponible como si la misma aplicación hubiese hecho la petición, todo el contenido se guardará en la caché especifica de la aplicación.

Para poder utilizar esta nueva funcionalidad, no necesitamos realizar ningún cambio en nuestra aplicación en cuanto a la forma en que hacemos las peticiones. Este sistema funciona tanto si hacemos las peticiones utilizando **WinJS.xhr** o [la nueva **API HttpClient**](/caracteristicas-de-la-nueva-api-httpclient-de-windows-runtime/ "La nueva API HttpClient de Windows Runtime") de la que hablé en el post anterior. Sin embargo, la clase System.Net.Http.HttpClient no está soportada, otro motivo más para cambiar a la nueva API.

Para indicar estos recursos tenemos que utilizar la clase **ContentPrefetcher** y podemos hacerlo de dos maneras diferentes. Mediante la propiedad **ContentUris** podemos indicar las URL de una forma local. Simplemente tenemos que añadir las URL al array **ContentUris** y el sistema se encargará de descargar esta información por nosotros. Veamos el código de ejemplo:

var uris = \[new Windows.Foundation.Uri(“/feed”), new Windows.Foundation.Uri(“/status.jpg”)\];

Windows.Networking.BackgroundTransfer.ContentPrefetcher.ContentUris.Clear();

for (vari=0; i < uris.length; i++) { Windows.Networking.BackgroundTransfer.ContentPrefetcher.ContentUris.Append(uris\[i\]); } </pre>

Este sistema nos será útil para las aplicaciones en las que las URI son estáticas, por ejemplo, la URL de un feed de noticias.

La segunda forma de especificar contenido es utilizando un servicio web. Por un lado, tenemos que crear un fichero XML en nuestro servidor que debe contener los recursos que queremos precargar. Este fichero XML debe tener la siguiente estructura.

<?xml version="1.0" encoding="utf-8"?>
<prefetchUris>
    <uri>/2013-07-16-feed.json</uri>
    <uri>/A457985689.jpg</uri> 
    <uri>/B487989889.jpgg</uri>
</prefetchUris>

Y en nuestra aplicación tenemos que indicar la URL de este fichero XML mediante la propiedad **IndirectContentUri**.

var indirectContentUri = new Windows.Foundation.Uri("/prefetch.xml");

Windows.Networking.BackgroundTransfer.ContentPrefetcher.indirectContentUri = indirectContentUri;

Este método, a diferencia del primero, nos será útil cuando las URL de nuestro contenido sean muy dinámicas y además con la ventaja de que podremos tener un servicio que actualice este XML cuando queramos.

    ## ¿Y qué pasa con la batería?
    

Cuando comenzamos a hablar de procesos en _background_ y que además hacen uso de red, seguramente la única pregunta que se nos pasa por la cabeza sea esta: ¿y qué pasa con la batería? Microsoft sigue con la promesa de proporcionar una vida larga a las baterías y un buen rendimiento del sistema, así que la precarga de contenido esta sujeta a varias condiciones para ofrecer la mejor experiencia de usuario. Veamos cuales.

**Condiciones del sistema** – El sistema tiene que tener suficiente batería, cobertura de red y suficiente CPU libre para que no impacte en la experiencia de usuario utilizando el dispositivo. Además nunca se descargará información si estamos conectados a redes de uso medido (_metered networks_).

**Uso de la aplicación** – El sistema solo descargará información de las aplicaciones que el usuario utiliza realmente, no de todas las que tenga instaladas. El sistema operativo sabe que aplicaciones utilizamos y cuando las utilizamos, y en base a esta información el sistema decide qué y cuándo descargar.

**Beneficio previo** – El sistema calculará cual es la mejora en cuanto a experiencia de usuario al utilizar _prefetchig_ en cada aplicación, priorizando las aplicaciones que realmente aprovechan el contenido que se descarga sobre las aplicaciones que no lo hacen.

Además de estas condiciones, tenemos que tener en cuenta que solo podemos definir 40 URI por aplicación y que el sistema da prioridad a las URI definidas localmente que a las definidas en un servicio web.

    ## El ejemplo
    

Para probar el funcionamiento de la precarga de información, he realizado un ejemplo similar al que [Matt Merry hizo en su sesión “_Building Great Service Connected Apps_” de la pasada BUILD](http://channel9.msdn.com/Events/Build/2013/3-090). Tenemos, por un lado, una aplicación que obtiene un listado de imágenes de Flickr y por otro, mediante una tarea del Scheduler de **Azure Mobile Services** creamos el fichero XML con el mismo listado de imágenes. Si la lista de imágenes cambia, con el uso de **ContentPrefetcher**, el sistema mantendrá las imágenes actualizadas y esarán disponibles antes de que la aplicación se inicie.

Este es el script de la tarea del programador (Scheduler) de Azure Mobile Services. Para guardar el fichero XML estamos haciendo uso de un Blob Storage.

var request = require('request');
var azure = require('azure');
var accountName = '{your account name';
var accountKey = '{your account key}';
var flickerApiKey = '{your flickr API key}';
var containerName = "prefetch";

var blobService = azure.createBlobService(accountName, accountKey);
 
function GeneratePrefetchXml() {
  var xml = "n";
  
  var url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&nojsoncallback=1&api\_key=" + flickerApiKey + "&per\_page=40&text=red&safe\_search=1&content\_type=1&sort=interestingness+desc&extras=url\_l,url\_m,url\_o";
  
  request(url, function photosLoaded(error, response, body) {
    if (!error && response.statusCode == 200) {

      var results = JSON.parse(body);

      if (results.photos.photo) {
        results.photos.photo.forEach(function processPhoto(photo) {

          if (photo.url\_o)
            xml+="t"+photo.url\_o+"n";
          else if (photo.url\_l)
            xml+="t"+photo.url\_l+"n";
          else if (photo.url\_m)
            xml+="t"+photo.url\_m+"n";

        });
        
        xml+="";
        
        console.log("Generated prefetch XML: n" + xml);
        
        blobService.createContainerIfNotExists('prefetch', function (error) {
          if(error){
              console.log("Error creating container: " + error);
          } 
          else {
            blobService.setContainerAcl('prefetch', 'blob', function (error) {
              if (error) {
                console.log("Error setting container ACL: " + error);
              }
              else {
                blobService.createBlockBlobFromText('prefetch', 'prefetch.xml', xml, function(error) {
                  if (error)  {
                      console.log("Error creating Blob: " + error);
                  }
                  else {
                      console.log('Created prefetch file');
                  }
                });
              }
            });
          }
        });
      }
    }
  });
}

Ahora solo tenemos que ejecutar el script para generar el fichero XML, comprobar que se genera correctamente revisando el log e indicar al iniciar la aplicación (en el default.js) la URL del fichero XML:

var indirectContentUri = new Windows.Foundation.Uri("http://youraccount.blob.core.windows.net/prefetch/prefetch.xml");

Windows.Networking.BackgroundTransfer.ContentPrefetcher.indirectContentUri = indirectContentUri;





## Conclusiones


Con este nuevo mecanismo de precarga de contenido tenemos una buena oportunidad de mejorar la experiencia de usuario al iniciar nuestra aplicación. Sin embargo, tenemos que utilizar correctamente este mecanismo. No debemos precargar información que el usuario no vaya a consumir nada más iniciar la aplicación. Y tampoco precargar contenido que tenga un tiempo de vida muy corto, tenemos que precargar contenido del que tengamos la certeza de que será válido cuando se lance nuestra aplicación.

\*\*Descarga código fuente\*\*
\[FlickrColors\_ContentPrefetcher.zip\](http://sdrv.ms/13inUVi)

\*\*Recursos online\*\*
\[ContentPrefetcher class\](http://msdn.microsoft.com/en-us/library/windows/apps/windows.networking.backgroundtransfer.contentprefetcher)
\[BUILD 2013: Building Great Service Connected Apps\](http://channel9.msdn.com/Events/Build/2013/3-090)
\[How to Use the Blob Service\](http://www.windowsazure.com/en-us/develop/nodejs/how-to-guides/blob-storage/) 
\[Schedule recurring jobs in Mobile Services\](http://www.windowsazure.com/en-us/develop/mobile/tutorials/schedule-backend-tasks/)
