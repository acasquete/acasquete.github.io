---
title: Procesos en background en aplicaciones Metro con JavaScript
tags: [programming, windows_store, winjs, winrt]
reviewed: true
---
Creo que uno de los cambios más importantes, y del que tenemos que ser más conscientes al programar **aplicaciones Metro para Windows 8**, es el cambio de filosofía que se introduce en la gestión del tiempo de vida de los procesos. En las versiones anteriores de Windows y en el escritorio clásico de Windows 8, ejecutamos aplicaciones y somos nosotros los responsables de su tiempo de vida. Es decir, nosotros decidimos cuando cerrar una aplicación, o bien cuando no la necesitamos más o, cuando al tener muchas aplicaciones abiertas, provocamos problemas de rendimiento.

De esta forma hemos estado viviendo durante estos años, abriendo procesos sin tener que preocuparnos de cuantos procesos están abiertos y de qué es lo que están haciendo, simplemente cambiamos entre tareas y vemos que las aplicaciones siguen ahí. De una forma más sintetizada podemos decir que las aplicaciones o procesos clásicos de Windows tienen dos estados: o lo tenemos en ejecución o no lo tenemos. En las **aplicaciones Metro de Windows 8** tenemos un modelo distinto, donde el propio sistema es quien gestiona el tiempo de vida de las aplicaciones. Recordemos que una de las características de las aplicaciones **Windows Metro** es que todas se ejecutan a pantalla completa y el usuario sólo puede interactuar con una de ellas cuando está en primer plano.

Cuando el usuario cambia de tarea y mueve la aplicación fuera del primer plano, Windows envía un mensaje a la aplicación indicando que va a entrar en suspensión (_suspending_). Cinco segundos después de recibir este mensaje, la aplicación entrará en suspensión. Una aplicación en este estado permanece en memoria, pero no tiene ningún impacto en el procesador ni en el tráfico de red ya que el código no se ejecuta y todos los hilos se paran. Es un estado similar al pulsar el botón de pausa en Visual Studio. Todo esto significa que una aplicación que está en primer plano tiene asignados todos los recursos disponibles del sistema. Nosotros como usuarios podemos realizar dos acciones con una aplicación suspendida. La podemos finalizar o la podemos traer de nuevo a primer plano, en este caso Windows notificará con otro mensaje (_resuming_) a la aplicación que puede continuar con la ejecución de todos sus hilos. La experiencia de reanudar una aplicación es instantánea ya que todo el código de la aplicación está en memoria.

Pero existe una cosa más que puede suceder con una aplicación en suspensión. Windows, dependiendo de la cantidad de memoria disponible, puede finalizar la aplicación. Además, esta finalización se produce sin que haya ningún tipo de notificación a la aplicación. Es decir, la aplicación no puede realizar ninguna acción para evitar que sea finalizada. Pero, ¿por qué se hace esto? Pues además de para que la aplicación que tiene el foco reciba todos los recursos disponibles en el sistema, se mejora la vida de la batería ya que no tenemos procesos en segundo plano que consuman recursos y se evitan demoras causadas por la ejecución de otras aplicaciones. El problema es que si volvemos a la aplicación, como usuarios, no tenemos porqué saber que el sistema ha finalizado nuestra aplicación. Lo que debemos esperar es que todo esté en el mismo sitio en que lo dejamos. Pero esto no sucede sin que nosotros, como desarrolladores, pongamos los medios para guardar y recuperar el estado de la aplicación. No voy a entrar en detalle de cómo conseguir esto, porque da para otra entrada más, pero simplemente comentar que se puede conseguir mediante el objeto [Application.sessionState](http://msdn.microsoft.com/en-us/library/windows/apps/hh440965.aspx) de WinJS o la clase [Windows.Storage.ApplicationData](http://msdn.microsoft.com/en-us/library/windows/apps/windows.storage.applicationdata). Además, todas las acciones que queramos hacer para guardar el estado lo debemos hacer mientras la aplicación está en ejecución o durante los cinco segundos siguientes a la recepción del mensaje de suspensión. Una vez llegados a este punto, nos encontramos con una duda y el motivo principal de este post.

Según todo lo escrito anteriormente, parece que no podamos ejecutar procesos en segundo plano. ¿Qué pasa si, por ejemplo, queremos escuchar música, consultar un servicio web, o realizar un cálculo? ¿También se finalizarán esos procesos? Pues no, **Windows 8** permite la ejecución de diversos procesos en segundo plano: podemos ejecutar audio, podemos utilizar la API de Background Transfer para cargar y descargar archivos. También se puede simular que nuestra aplicación está en funcionamiento mediante las **Windows Push Notification**. Todos estos procesos los veremos en próximos artículos, pero en este vamos a ver como podemos ejecutar código cuando no tenemos ninguno de los escenarios anteriores. **Windows 8** nos permite ejecutar código mientras nuestra aplicación está suspendida mediante las Background Tasks. El entorno de ejecución de estas tareas es un entorno restringido y solo recibe una cantidad de tiempo de CPU. Por lo tanto, las tareas de segundo plano se deben utilizar para realizar pequeñas tareas que no tengan interacción con el usuario. Escenarios que requieran cargas de trabajo excesivas no son apropiados para utilizar este tipo de tareas. La tarea en segundo plano se puede implementar como un worker de JavaScript. Nuestro ejemplo es bien sencillo, vamos a hacer una tarea que al ejecutarse aumente el valor de un contador simulando la ejecución de una tarea más pesada.

```js
(function() { 
  “use strict”; 
  var progress= 0, backgroundTask = Windows.UI.WebUI.WebUIApplication.backgroundTask;

  function onTimer() { 
    if (progress < 100) { 
      setTimeout(onTimer, 1000); 
      backgroundTask.taskInstance.progress = progress; 
      progress += 1; 
    } else { 
      backgroundTask.success = true; 
      backgroundTask.taskInstance.progress = progress; close(); 
      } 
    } 
    setTimeout(onTimer, 1000); 
  })();
```

Vemos que en este script para poder acceder a la tarea utilizamos la propiedad **Windows.UI.WebUI.WebUIApplication.backgroundTask** que devuelve la tarea actual en _background_. Después, establecemos el valor de progreso en la instancia de la tarea. Y por último, cuando la tarea se ha completado, se hace una llamada al método _close_ para cerrar la tarea. Para registrar una tarea utilizamos la clase [BackgroundTaskBuilder](http://msdn.microsoft.com/en-us/library/windows/apps/windows.applicationmodel.background.backgroundtaskbuilder). El código siguiente es el necesario para registrar una tarea en segundo plano.

```js
function RegisterBackgroundTask() { 
  var builder = new Windows.ApplicationModel.Background.BackgroundTaskBuilder();
  builder.name = "BackgroundTestWorker";
  builder.taskEntryPoint = "BackgroundTestWorker.js";
  var myTrigger = new Windows.ApplicationModel.Background.SystemTrigger(Windows.ApplicationModel.Background.SystemTriggerType.internetNotAvailable, false); 
  builder.setTrigger(myTrigger); 
  var task = builder.register(); 
  task.addEventListener("progress", task\_Progress); 
  task.addEventListener("completed", task\_Completed); 
}
```

En la propiedad **taskEntryPoint** se ha establecido el nombre del fichero del worker y mediante el método **SetTrigger** se establece el tipo de disparador (_trigger_) que lanzará la tarea. Los _triggers_ que tenemos disponibles son los siguientes:

**InternetAvailable** - La conexión a Internet está disponible. **InternetNotAvailable** - La conexión a Internet no está disponible. **LockScreenApplicationAdded** - Un tile de aplicación se añade a la pantalla de bloqueo. **LockScreenApplicationRemoved** - Un tile de applicación se elimina de la pantalla de bloqueo. **NetworkNotificationChannelReset** - Se restablece un cana de red. **NetworkStateChange** - Se produce un cambio de red, como un cambio en la conectividad. **ServicingComplete** - El sistema ha finalizado la actualización de una aplicación. **SessionConnected** - La sesisón se ha conectado. **SessionDisconnected** - La sesión se ha desconectado. **SessionStart** - El usuario inicia la sesión. **SmsReceived** - Se ha recibido un mensaje SMS. **TimeTrigger** - Evento de tiempo. **TimeZoneChange** - La zona horaria cambia (cuando el sistema ajusta el reloj para horari ode verano) **UserAway** - El susuario se ausenta. **UserPresent** - El usuario está presente

En nuestro ejemplo y para facilitar la prueba he utilizado el _trigger_ **InternetNotAvailable** que se dispara cuando la conexión a Internet se pierde, así que para probar el ejemplo habrá que deshabilitar o desconectar el dispositivo de red. Después de llamar al método register, que registra y nos devuelve la tarea, registramos las funciones _callback_ para los eventos _progress_ y _completed_ de la tarea. En estas funciones simplemente vamos a mostrar el progreso de la tarea y el mensaje “completado” al finalizar.

```js
function task_Progress(args) { 
  document.getElementById("result").innerHTML = args.progress; 
}
function task_Completed(args) {
  document.getElementById("result").innerHTML = "completado!"; 
}
```

Ahora solo queda indicar en el fichero **manifest** de la aplicación que se va a hacer uso de la extensión de contrato de tareas en _background_.

```xml
<Applications>
  <Application Id="App" StartPage="default.html"> 
    <VisualElements DisplayName="BackSample" Logo="imageslogo.png" SmallLogo="imagessmalllogo.png" Description="BackSample" ForegroundText="light" BackgroundColor="#0084FF" InitialRotationPreference="portrait">
      <DefaultTile ShowName="true" />
      <SplashScreen Image="imagessplashscreen.png" />
    </VisualElements> 
    <Extensions>
      <Extension Category="windows.backgroundTasks" StartPage="BackgroundTestWorker.js">
        <BackgroundTasks>
          <Task Type="systemEvent" />
        </BackgroundTasks>
      </Extension>
    </Extensions>
  </Application>
</Applications>
```

Cuando el _trigger_ se dispara, la tarea en segundo plano se lanza sin tener en cuenta el estado de la aplicación. Si la aplicación está en ejecución la tarea de background se ejecuta normalmente. Si la aplicación está suspendida los hilos de aplicación se «descongelan» y se lanza la tarea en background. Y por último, si la aplicación está finalizada, ya sea porque nunca se ha lanzado o porque ha sido finalizada por el sistema después de entrar en suspensión, la aplicación se activará y la tarea se ejecutará. En este ultimo caso la aplicación no pasará a estar en primer plano. Para finalizar, podemos añadir varias condiciones que se deben cumplir para que la tarea se lance. La siguiente lista muestra todas las posibles condiciones que podemos utilizar.

**InternetAvailable** - Debe haber conexión a Internet. **InternetNotAvailable** - No debe haber conexión a Internet. **SessionConnected** - La sesión debe estar conectada. **SessionDisconnected** - La sesión debe estar desconectada. **UserNotPresent** - El usuario debe estar ausente. **UserPresent** - El usuario debe estar presente.

Por ejemplo, si queremos añadir que la tarea se lance cuando se pierda la conexión a Internet, pero cuando el usuario no esté ausente, deberíamos utilizar el siguiente código.

```js
function RegisterBackgroundTask() { 
  var builder = new Windows.ApplicationModel.Background.BackgroundTaskBuilder(); 
  builder.name = "BackgroundTestWorker";
  builder.taskEntryPoint = "BackgroundTestWorker.js";
  var myTrigger = new Windows.ApplicationModel.Background.SystemTrigger(Windows.ApplicationModel.Background.SystemTriggerType.internetNotAvailable, false); 
  builder.setTrigger(myTrigger);
  var condition = new Windows.ApplicationModel.Background.SystemCondition(Windows.ApplicationModel.Background.SystemConditionType.userPresent); builder.addCondition(condition);
  var task = builder.register(); 
  task.addEventListener("progress", task_Progress); 
  task.addEventListener("completed", task_Completed);
}
```

Hasta aquí esta primera entrada dedicada a los procesos de Background. En próximos articulos veremos cómo reproducir un fichero de audio, subir y descargar archivos, y lo veremos en Javascript y en C#.

Referencias
---

[Introduction to Background Tasks](http://www.microsoft.com/download/en/details.aspx?id=27411)  

