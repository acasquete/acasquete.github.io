---
title: Arquitecturas Lambda en Azure (Recopilando eventos)
---
Los dispositivos móviles se utilizan para detectar nuestra presencia en centros comerciales, salas de exposiciones, estaciones de tren, aeropuertos, hospitales, museos y un sinfín de lugares más. Esto es posible porque los dispositivos móviles pueden detectarse mediante puntos de acceso WiFi, independientemente del estado de asociación, lo que significa que incluso si un usuario no conecta su dispositivo a la red WiFi, la presencia del dispositivo puede detectarse mientras esté dentro del alcance de la red y, obviamente, la conexión WiFi del dispositivo esté habilitada.

Este es el punto de partida para crear un proceso que permita recopilar y analizar las trazas de posicionamiento WiFi emitidas por los puntos de acceso (AP). El objetivo final de esta solución es obtener información sobre el comportamiento de los visitantes: tiempo medio de las visitas, ubicaciones más populares, tiempo medio por ubicación, tipo de dispositivo utilizado, recencia, etc. Esta información se podrá utilizar para mejorar las estrategias de marketing y comprender mejor el comportamiento de los visitantes.

En esta entrada vamos a centrarnos exclusivamente en la obtención y almacenamiento de los datos de los eventos para poder analizarlos. Para esto vamos a necesitar los siguientes servicios en Azure:

* **Azure Function** - para exponer una API donde un proveedor de terceros pueda enviar la información de los eventos y enviarlos a un _Event Hub_ para procesarlos en tiempo real.
* **Event Hub** - para recopilar, almacenar eventos y para permitir la lectura de los datos en varias aplicaciones mediante suscripción.
* **Stream Analytics** - para extraer los eventos del _Event Hub_, procesar los datos de las trazas y guardarlos en un contenedor de _Azure Storage_.
* **Azure Storage** - para almacenamiento de los datos en reposo y realizar un análisis posterior.

## Recopilando trazas de localización 

En un mundo perfecto, los AP podrían conectarse directamente a **Event Hub** para enviar la información de los eventos, pero en el “Mundo Real” esto casi nunca es posible y en muchos casos tendremos que realizar desarrollos _ad hoc_ para integranos con los distintos proveedores de información.

Para nuestro ejemplo, he elegido un caso real, el formato que utiliza **Cisco Meraki** para enviar los datos de sus dispositivos. La documentación del funcionamiento del análisis de localización se puede encontrar [aquí](https://documentation.meraki.com/MR/Monitoring_and_Reporting/Location_Analytics).

Los AP de Cisco generan una firma de presencia desde cualquier dispositivo con la WiFi habilitada detectando tramas de datos 802.11, esten asociados o no a la red. Como decíamos al principio de la entrada, esto es posible porque todos los dispositivos Wifi emiten una petición para descubrir redes cercanas en intervalos regulares. La frecuencia de envío de tramas de cada dispositivo puede puede ir desde una a múltiples veces por minuto y depende de multiples factores: del fabricante, del estado del dispositivo (en espera, dormido, asociado), de las actualizaciones que el dispositovo tenga instaladas o el estado de carga de la batería.

## Creación de un proyecto Azure Functions 

Vamos a comenzar creando una **Function App** para exponer una API que sea capaz de recoger las trazas del sistema de localización de Cisco Meraki y enviarlas a un **Event Hub** para que puedan ser procesadas posteriormente. El formato de los eventos que Cisco Meraki envía es el siguiente:

    {
      "apMac": <string>,
      "apTags": [<string, ...],
      "apFloors": [<string>, ...],
      "observations": [
        {
          "clientMac": <string>,
          "ipv4": <string>,
          "ipv6": <string>,
          "seenTime": <string>,
          "seenEpoch": <integer>,
          "ssid": <string>,
          "rssi": <integer>,
          "manufacturer": <string>,
          "os": <string>,
          "location": {
            "lat": <decimal>,
            "lng": <decimal>,
            "unc": <decimal>,
            "x": [<decimal>, ...],
            "y": [<decimal>, ...]
          },
        },
        //[...]
      ]
    }
    

Esta información se enviará por cada uno de los AP e incluye información para identificar el AP que envía los datos mediante la dirección Mac (_apMac_) y una serie de etiquetas (_apTags_) que se asignan manualmente a cada uno de los AP. En nuestro caso vamos a utilizar estas propiedades para definir la ubicación, planta y sección donde se encuentra el dispositivo. Para nuestro ejemplo, definiremos un _tag_ para indicar que el dispositivo está en Barcelona o Madrid y otro para indicar la planta del edificio, de esta forma podremos saber fácilmente dónde se encontraba el dispositivo cuando esté fue detectado.

En el _array_ _observations_ recibimos toda la información de los dispositivos detectados por el AP, incluyendo datos como la dirección Mac (_clientMac_) y datos de geoposicionamiento: latitud (_lat_), longitud (_lon_) y su grado de incertidumbre en metros (_unc_).

Una vez familiarizados con el formato, vamos a crear el proyecto de **Azure Function**. Para esto, podemos utilizar tanto **Visual Studio 2017** como **Visual Studio Code** con las [Azure Functions CLI](https://www.npmjs.com/package/azure-functions-cli).

En esta ocasión voy a crear el proyecto utilizando la línea de comandos escribiendo el siguiente comando:

    func init LocationAnalytics
    

La salida debe mostrar algo similar a lo siguiente:

    Writing .gitignore
    Writing host.json
    Writing local.settings.json
    Created launch.json
    Initialized empty Git repository in C:/Code/LocationAnalytics/.git/
    

Ahora generaremos una función **HTTP Trigger** en C# ejecutando:

    func new --language C# --template HttpTrigger --name MerakiTraces
    

Esto generará una función por defecto.

    Select a language: C#
    Select a template: HttpTrigger
    Function name: [MerakiTraces] Writing C:\Code\LocationAnalytics\MerakiTraces\readme.md
    Writing C:\Code\LocationAnalytics\MerakiTraces\run.csx
    Writing C:\Code\LocationAnalytics\MerakiTraces\sample.dat
    Writing C:\Code\LocationAnalytics\MerakiTraces\function.json
    

Para poder enviar mensajes a **Event Hub**, tenemos que añadir la referencia al paquete [NuGet de ServiceBus](https://www.nuget.org/packages/Microsoft.Azure.ServiceBus.EventProcessorHost/) creando el archivo **project.json** dentro del directorio **MerakiTraces** con el siguiente contenido:

    {
      "frameworks": {
        "net46":{
          "dependencies": {
            "Microsoft.Azure.ServiceBus.EventProcessorHost": "3.1.2"
          }
        }
       }
    }
    

Y cambiar el código de la función del fichero **run.csx** por el siguiente:

    using System.Net;
    using Microsoft.ServiceBus.Messaging;
    using System.Text;
    using System.Configuration;
    
    public static async Task<HttpResponseMessage> Run(HttpRequestMessage req, TraceWriter log)
    {
        log.Info("MerakiTraces function processed a request.");
    
        dynamic data = await req.Content.ReadAsAsync<object>();
    
        var secret = data?.secret;
        
        SendEvent(data, log);
        
        return secret != ConfigurationManager.AppSettings["MerakiSecret"]
            ? req.CreateResponse(HttpStatusCode.Unauthorized, "No valid secret key")
            : req.CreateResponse(HttpStatusCode.Accepted);
    }
    
    static void SendEvent(object msg, TraceWriter log)
    {
       string eventHubName = ConfigurationManager.AppSettings["EventHubName"];
       string connectionString = ConfigurationManager.AppSettings["EventHubConnectionString"];
       
       var eventHubClient = EventHubClient.CreateFromConnectionString(connectionString, eventHubName);
       
        try
        {
            var message = msg.ToString();
            
            log.Info($"{DateTime.Now} > Sending message: {message}");
            
            eventHubClient.Send(new EventData(Encoding.UTF8.GetBytes(message)));
        }
        catch (Exception exception)
        {
            log.Info($"{DateTime.Now} > Exception: {exception.Message}");
        }
    }
    

Ahora solo queda añadir la configuración en el fichero **local.settings.json** para establecer los valores de la clave secreta de Meraki (la que se enviará en cada petición), el nombre y la cadena de conexión de **Event Hub**.

    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "",
        "MerakiSecret": "12345",
        "EventHubName": "event-input",
        "EventHubConnectionString": "Endpoint=sb://eventhub-location-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XXX" 
      }
    }
    

Podemos ejecutar la función localmente, ejecutando el siguiente comando:

    func host start
    

Para probar que la función funciona correctamente, podemos modificar el fichero **sample.dat** con el siguiente ejemplo de traza:

    {
      "secret": "12345",
      "version": "1.0",
      "type": "",
      "data": {
        "apFloors": [ "" ],
        "apTags": [ "Barcelona", "1stFloor" ],
        "apMac": "string",
        "Observations": [
          {
            "clientMac": "aa:bb:cc:dd:ee:ff",
            "seenTime": "2017-09-11T22:05:10.178Z",
            "seenEpoch": 1505167546,
            "ipv4": "123.45.67.89",
            "ipv6": "string",
            "rssi": 0,
            "ssid": "Cisco WiFi",
            "Manufacturer": "Meraki",
            "os": "Linux",
            "location": {
              "lat": 37.77057805947924,
              "lng": -122.38765965945927,
              "unc": 15.13174349529074,
              "x": [ 0 ],
              "y": [ 0 ]
            }
          }
        ]
      }
    }
    

Y ejecutar el siguiente comando:

    func run MerakiTraces -f .\MerakiTraces\sample.dat
    

En el código de la función podemos ver que básicamente verificamos que la petición que recibimos es válida (comprobando la propiedad _secret_) y en caso afirmativo enviamos el objeto recibido sin ninguna transformación al **Event Hub**.

Para comprobar que la función está enviando eventos correctamente, podemos ver en el [Portal de Azure](https://portal.azure.com/) el número de eventos que están entrando en el **Event Hub**. En la próxima entrada veremos cómo procesar esta información mediante **Stream Analytics**.

## Resumen 

En esta entrada nos hemos centrado exclusivamnete en cómo recoger mediante una **Azure Function** los eventos de trazas WiFi, utilizando a modo de ejemplo el modelo de trazas de un proveedor específico, para enviarlos a un servicio **Event Hub** que nos permitirá posteriormente procesarlo con, por ejemplo, un _job_ de **Stream Analytics**.

## Referencias 

[Location Analytics](https://documentation.meraki.com/MR/Monitoring_and_Reporting/Location_Analytics)  
[Vehicle telemetry analytics solution playbook](https://docs.microsoft.com/en-us/azure/machine-learning/cortana-analytics-playbook-vehicle-telemetry)  
[Codificación y comprobación de las funciones de Azure en un entorno local](https://docs.microsoft.com/es-es/azure/azure-functions/functions-run-local)

