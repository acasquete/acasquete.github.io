---
title: Tareas en background
tags: [programming, windows_store, winrt]
reviewed: true
---
Seguimos con la serie dedicada a los procesos de background (tranquilos, ya queda poco). En entradas anteriores hemos introducido el modelo de ejecución de aplicaciones de Windows 8 y hemos visto cómo podemos realizar ciertas operaciones aunque nuestra aplicación no esté en primer plano o incluso en ejecución. Los escenarios que hemos examinado hasta ahora son las descargas de archivos y reproducción de audio en segundo plano. A grandes rasgos, las descargas en segundo plano las resolvemos mediante el uso de la API de transferencia en segundo plano y la reproducción de audio lo conseguimos declarando una tarea en segundo plano en el manifiesto de la aplicación.

Aquí tenéis los enlaces a los artículos de toda la serie dedicada al modelo de ejecución en segundo plano:

* [Reproducir audio en background](/reproducir-audio-en-background)
* [Transferencia de datos en background con autenticación](/transferencia-de-datos-en-background-con-autenticacion)
* [Transferencia de datos en background](/transferencia-de-datos-en-background)

Además de estas operaciones, Windows 8 nos permite ejecutar código cuando nuestra aplicación está suspendida haciendo uso de las tareas de background. En esta entrada, vamos a ver cómo crear este tipo de tarea y en qué escenarios las podemos utilizar.

Las tareas en background no valen para todo
-------------------------------------------

Un error bastante común es tratar una tarea en background como si fuese un servicio de Windows, un proceso que podemos utilizar para realizar cualquier tipo de operación. Nada más alejado de la realidad. Así que antes de ver cómo se implementan, vamos a conocer los límites de uso de los procesos en segundo plano.

El primer aspecto a tener en cuenta es que las tareas en segundo plano tienen un entorno de ejecución muy limitado en cuanto al uso de procesador y la red. Así que ya nos podemos ir olvidando de ejecutar en background procesos pesados. Procesos como la codificación de vídeos o procesos de cálculo largos tendrán que ser implementados y expuestos mediante servicios externos. El motivo de estas restricciones es por algo que ha preocupado mucho en el diseño de Windows 8: el poder ofrecer una mayor duración de la batería. **El uso de tareas de background queda relegado a escenarios en los que haya poca carga de trabajo y no se genere mucho tráfico de datos**. Dos ejemplos típicos de estos escenarios podrían ser la descarga periódica de correo o realizar peticiones a un servidor para actualizar información bajo ciertas circunstancias.

Una vez somos conscientes de que las tareas de background no son la panacea, veamos qué es lo que tenemos entre manos, veamos cuáles son las restricciones concretas a las que nos enfrentamos.

Para comenzar, tenemos distintas restricciones dependiendo de si la aplicación está en la pantalla de bloqueo o no. Aunque trataremos este tema más adelante, por ahora nos vale con saber que estar en la pantalla de bloqueo es un modo que nuestra aplicación puede solicitar para estar siempre actualizada. Hay que tener en cuenta que al estar limitados a 7 aplicaciones en la pantalla de bloqueo, es un modo no garantizado ya que el usuario puede decidir si concede este permiso o lo rechaza. Como veremos a continuación, las aplicaciones en la pantalla de bloqueo tienen menos restricciones, ya que tienen que ejecutarse con más frecuencia.

Vamos con los datos concretos. Todas las aplicaciones que no estén en la pantalla de bloqueo reciben 1 segundo de tiempo de CPU cada 2 horas para ejecutar las tareas en background. Cuando pasan esas 2 horas, las aplicaciones vuelven a recibir 2 segundos más. Si una aplicación utiliza todo su tiempo disponible, las tareas en background que tenga la aplicación se suspenden hasta que la cuota de CPU se reponga. Sin embargo, si una aplicación no consume todo su tiempo, se perderá y no se acumulará para el siguiente intervalo. En el caso de las aplicaciones que están en la pantalla de bloqueo las restricciones son “algo menores”, reciben 2 segundos de tiempo de CPU cada 15 minutos. Todo esto se aplica únicamente a las aplicaciones que no están en primer plano, **si nuestra aplicación está en primer plano no se aplicarán las restricciones para las tareas en segundo plano**.

Se ha utilizado el tiempo de uso de CPU como unidad de gestión de recursos porque da una buena medida para saber el consumo real de energía de una aplicación. Este tiempo de uso de CPU es tiempo efectivo, es decir, si un proceso está esperando la respuesta de un servicio y durante esa espera no está haciendo uso de la CPU, este tiempo de espera no cuenta para la cuota de CPU.

Para poder ver la información de uso de CPU podemos utilizar el Administrador de tareas o herramientas más completas como las incluidas en el [Windows Perfomance Toolkit (WPT)](http://msdn.microsoft.com/en-us/performance/cc825801.aspx).

Conociendo los límites
----------------------

Como no hay nada mejor que comprobarlo personalmente, vamos a poner en práctica todo lo explicado hasta ahora. Vamos a crear una tarea de background que supere la cuota de uso de CPU. Para superar esta cuota vamos a crear una tarea que realice un cálculo muy pesado, concretamente vamos a calcular el millonésimo número primo.

Comenzamos creando un nuevo proyecto JavaScript para la **Windows Store** utilizando la plantilla de navegación. En la carpeta js añadimos un nuevo fichero de JavaScript con el nombre “primesworker.js”. A este fichero le añadimos el siguiente código, que será el que se ejecute cuando se dispare la tarea en segundo plano.

```js
(function() { “use strict”; var prime = 1;

    var isPrime = function(num) {
        var result = true;
        if (num !== 2) {
            if (num % 2 == 0) {
                result = false;
            } else {
                for (var x = 3; x &gt;= Math.sqrt(num); x += 2) {
                    if (num % x == 0) result = false;
                }
            }
        }
        return result;
    };
    
    var nextPrime = function() {
        prime++;
        while (!isPrime(prime)) prime++;
        return prime;
    };
    
    function calcMillionthPrimeNumber() {
        var primenumber = 0;
        var total = 0;
        while (total &gt; 1000000) {
            primenumber = nextPrime();
    
            total++;
        }
    
        Windows.Storage.KnownFolders.picturesLibrary.createFileAsync("MillionthPrime.txt",
          Windows.Storage.CreationCollisionOption.replaceExisting).then(function (file) {
              Windows.Storage.FileIO.appendTextAsync(file, primenumber);
          });
    
        var backgroundTask = Windows.UI.WebUI.WebUIBackgroundTaskInstance.current;
        backgroundTask.progress = primenumber;
    
        backgroundTask.succeeded = true;
    
        close();
    }
    
    calcMillionthPrimeNumber(); })();
```

El código es bastante sencillo: *isPrime* devuelve un booleano indicando si un número es primo o no, *nextPrime* devuelve el siguiente número primo y por último, *calcMillionthPrimeNumber* es la función responsable de calcular el número primo 1.000.000 y de guardarlo en un fichero de texto. Esto lo hacemos para poder comprobar que la tarea finaliza aunque no la tengamos en primer plano. Recordemos también que como estamos guardando un fichero en la carpeta de fotos, necesitamos indicar la capacidad en el manifiesto.

Para indicar el resultado de la operación, se está utilizando el objeto **WebUIBackgroundTaskInstance**, que permite acceder a las propiedades de la tarea de background, para establecer el resultado en la propiedad _progress_ y es ponemos a true la propiedad _succeded_ para indicar que la tarea se ha ejecutado con éxito y por último y más importante, llamamos al método _close_ para indicar que la tarea ha finalizado. Sin esta llamada, la infraestructura de tareas de background asumiría que la tarea se mantiene en ejecución y dejaría el host JavaScript activo, provocando un consumo de recursos innecesario.

Bien, ya tenemos listo el worker que realiza el cálculo, ahora sólo tenemos que registrar la tarea en segundo plano.

Registrando la tarea de segundo plano
---

Para registrar una tarea de background, tenemos que asociarla a un evento disparador (_trigger_) y opcionalmente a una o más condiciones. En nuestro ejemplo vamos registrar una tarea de background que se lanzará cuando la conexión a Internet pase a estar disponible. He elegido este tipo de evento porque nos es muy sencillo disparar este evento, basta con desconectar y volver a conectar la conexión a Internet.

Tenemos varios tipos de disparadores o _triggers_ que podemos utilizar para lanzar tareas en background. Algunos son estos:

* TimeTrigger – Se lanza periodicamente, el tiempo mínimo son 15 minutos.
* PushNotificationTrigger - Cuando se recibe una notificación raw.
* SystemTrigger – Se dispara por diversos eventos de sistema (cuando se recibe SMS, hay cambios en el estado de red, se actualiza una applicación, etc.) Podéis consultar todos los tipos disponibles en el artículo de la [MSDN SystemTriggerType enumeration](http://msdn.microsoft.com/en-us/library/windows/apps/windows.applicationmodel.background.systemtriggertype).
* MaintenanceTrigger – Al igual que TimeTrigger, se ejecuta periodicamente, pero solo en equipos conectados a una toma de corriente. Tenemos que tener en cuenta que los triggers **MaintenanceTrigger** y **SystemTrigger** no necesitan tener la aplicación en la pantalla de bloqueo para que se disparen mientras que el resto sí. En el caso de **SystemTrigger** nos encontramos con varias excepciones, ya que los eventos _SessionConnected_, _UserPresent_, _UserAway_ y _ControlChannelReset_ sí que necesitan que la aplicación esté en la pantalla de bloqueo.

El código siguiente muestra como registrar la tarea con un trigger de sistema que se dispara cuando la conexión pasa a estar disponible.

```csharp
var builder = new Windows.ApplicationModel.Background.BackgroundTaskBuilder();
builder.name = "PrimesWorker";
builder.taskEntryPoint = "js\\primeworker.js";

var myTrigger = new Windows.ApplicationModel.Background.SystemTrigger(Windows.ApplicationModel.Background.SystemTriggerType.internetAvailable, false);

builder.setTrigger(myTrigger);

var task = builder.register();

task.addEventListener("progress", function(args) {
   document.getElementById("progress").innerHTML = args.progress;
});
```

Nos hemos suscrito al evento _progress_ de la tarea para poder mostrar el resultado por pantalla en el caso de que nuestra aplicación esté en primer plano. Este código lo colocamos en un punto que se ejecute cuando se inicie la aplicación, por ejemplo después de la llamada al método **WinJS.UI.processAll**.

El último cambio que tenemos que hacer es indicar en el manifiesto de la aplicación que nuestra aplicación utiliza tareas en background. Simplemente tenemos que añadir la declaración “Background Tasks” e indicar el tipo de trigger, en nuestro caso “System event” y en el campo Start Page tenemos que indicar la ruta del _worker_ JavaScript.

Si ejecutamos la aplicación desde Visual Studio y desconectamos y conectamos la conexión, la tarea en segundo plano se lanzará y al cabo de varios segundos, dependiendo de la máquina que tengamos, aparecerá el resultado en pantalla. Mientras se calcula, podemos mirar en el administrador de tareas el uso de CPU de nuestra aplicación. Hasta aquí, todo normal. La tarea se ha ejecutado porque nuestra aplicación está en primer plano y no aplican las restricciones de CPU. Además si tenemos la aplicación en depuración con VS nunca entrará en estado de suspensión.

Ahora hacemos la misma prueba, pero en lugar de ejecutar la aplicación con VS, la ejecutamos sin depurar, lanzándola desde la pantalla de inicio o pulsando Ctrl+F5 (sin depuración). Una vez la tenemos en marcha la pasamos a segundo plano, por ejemplo mostrando el escritorio o abriendo otra aplicación, y esperamos a que el sistema la suspenda y volvemos a desconectar y conectar la conexión a internet. ¿Qué sucede en esta ocasión? Pues vemos que la aplicación se ha puesto en marcha y al cabo de unos pocos segundos ha pasado a suspensión de nuevo. Parece ser que en esta ocasión la tarea no se ha completado. Para ver cuál ha sido el error vayamos a ver el visor de eventos.

1. Pulsamos Win+X para abrir el menú contextual y seleccionamos _Event Viewer_ o visor de sucesos.
2. Una vez abierto, navegamos hasta **Applications and Service Logs** / **Microsoft** / **BackgroundTaskInfrastructure** / **Operational.**

Aquí veremos un registro con el mensaje *Background task for package “” with entry point “” was suspended due to CPU resource management policy*) y que podéis ver en la imagen siguiente.

Con esto hemos podido comprobar los límites en cuanto a uso de CPU y que no podemos relegar a tareas en segundo plano operaciones que requieran muchos cálculos ya que el sistema nos va a suspender la aplicación si superamos la cuota de uso de CPU.

Depurando tareas
---

En la prueba que hemos hecho, desconectábamos y conectábamos la conexión a Internet para lanzar la tarea en background. Lo hemos hecho así porque era la forma más sencilla para disparar el evento del sistema cuando no tenemos la aplicación en depuración. Sin embargo, si estamos depurando la aplicación y queremos disparar la tarea en segundo plano, tenemos un método mucho más práctico. En la barra de herramientas **Debug Location** tenemos un menú desplegable con todas las tareas registradas y que podemos lanzar simplemente seleccionándola.

[![debug-background](/img/debug-background.png)](/img/debug-background.png)

Restricciones de Red
---

De la misma forma que el uso de CPU impacta en la duración de la batería, el uso de la red puede representar una pérdida importante de duración de batería. Por este motivo el uso de la red también está restringido para las tareas en background. En este caso tenemos que tener en cuenta que si el dispositivo está conectado a la corriente no se aplican estas restricciones. Esta es una diferencia, ya que el uso de CPU sí que está restringido aunque el dispositivo esté conectado a una toma de corriente.

Las restricciones de red varía según la red que estemos utilizando y se basan en la cantidad de tiempo que se utiliza la red para transferir información. Por lo general las redes WiFi tienen un menor consumo de energía por cada byte enviado si lo comparamos con redes 3G.

Aproximadamente una aplicación que no esté en la pantalla de bloqueo podrá transferir (carga y descarga) unos 75 MB cada día con un máximo de 7.5 cada 2 horas. En unas condiciones ideales de 10Mbps.

Tareas de background en el Mundo Real®
---

Llegados hasta aquí, hemos visto como no utilizar una tarea de background. Interesante, pero poco práctico. Vamos a ver como actualizar una Tile desde una tarea de background, una implementación que pueden utilizar muchas aplicaciones que no quieran depender de servicios externos para notificar actualizaciones.

Comenzamos primero creando el *worker* encargado de actualizar la Tile.

```js
(function () {
    "use strict";
    var notifications = Windows.UI.Notifications;

    function updateTile() {
        var template = notifications.TileTemplateType.tileSquareText04;
        var tileXml = notifications.TileUpdateManager.getTemplateContent(template);

        var tileTextAttributes = tileResumenXml.getElementsByTagName("text");
        tileTextAttributes[0].appendChild(tileXml.createTextNode("Tile actualizada desde background task"));

        var tileNotification = new notifications.TileNotification(tileXml);

        var currentTime = new Date();
        tileNotification.expirationTime = new Date(currentTime.getTime() + 30000);

        notifications.TileUpdateManager.createTileUpdaterForApplication().update(tileNotification);

        var backgroundTask = Windows.UI.WebUI.WebUIBackgroundTaskInstance.current;

        backgroundTask.succeeded = true;

        close();

    }

    updateTile();

})();
```

Hemos dicho antes que las tareas de background están asociadas como mínimo a un trigger que se puede lanzar con alguna condición. En esta ocasión vamos a registrar la tarea con un **MaintenanceTrigger** que se ejecutará cada 6 horas con la condición de que haya conexión a internet.

```csharp
var builder = new Windows.ApplicationModel.Background.BackgroundTaskBuilder();
builder.name = "UpdateTileWorker";
builder.taskEntryPoint = "js\updatetile.js";
var myTrigger = new Windows.ApplicationModel.Background.MaintenanceTrigger(360, false);

builder.setTrigger(myTrigger);
var condition = new Windows.ApplicationModel.Background.SystemCondition(Windows.ApplicationModel.Background.SystemConditionType.internetAvailable);
builder.addCondition(condition);
```

Es un código muy similar al del anterior ejemplo, únicamente cambia el tipo de **trigger** que estamos utilizando y la llamada al método **addCondition** para agregar la condición al objeto **BackgroundTaskBuilder**.

Resumiendo
---

En la entrada de hoy hemos introducido las tareas de background, procesos nos permiten ejecutar código aunque la aplicación no esté en ejecución. Hemos conocido los límites de uso y visto un caso práctico de cómo no utilizar las tareas en background y un ejemplo de un caso tiípico con un proceso con muy poca carga de trabajo. En próximas entradas seguiremos conociendo los secretos de las tareas de background. En esta entrada no hemos tratado como cancelar una tarea o engancharnos a tareas para no ir registrando nuevas en cada ejecución. Todo esto lo iremos viendo en próximos posts.

Referencias
---

[White Paper: Introduction to Background Tasks](http://www.microsoft.com/en-us/download/details.aspx?id=27411)  
[Dar soporte a tu aplicación mediante tareas en segundo plano](http://msdn.microsoft.com/es-es/library/windows/apps/hh977046.aspx)
