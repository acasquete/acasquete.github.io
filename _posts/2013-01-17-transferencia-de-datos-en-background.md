---
title: Transferencia de datos en background
tags: [programming, windows_store, winrt]
reviewed: true
---
Después de todas las presentaciones que el equipo de [[T]echdencias](http://twitter.com/techdencias) hemos realizado mostrando las novedades de **Windows 8**, creo que no me equivocaré si afirmo que los temas que causan más dudas y preguntas son los relacionados con el nuevo modelo de ejecución de aplicaciones y la administración del ciclo de vida de los procesos. Algo normal, por otro lado, ya que este nuevo modelo nos plantea nuevos escenarios y nos hacer cambiar la forma de desarrollar aplicaciones respecto al desarrollo clásico de aplicaciones de escritorio.

Como ya expliqué en un [post](/procesos-en-background-en-aplicaciones-metro-con-javascript-i) anterior, cuando el usuario pasa una aplicación a segundo plano, el sistema la suspende a los de pocos segundos y puede, incluso, llegar a finalizarla si no hay recursos suficientes. Este comportamiento tiene dos objetivos claros: maximizar el tiempo de duración de la batería y ofrecer al usuario la mejor experiencia posible, ya que no hay aplicaciones en segundo plano que interfieran y ralenticen la ejecución. Explicado así, esto nos plantea un entorno aparentemente muy restrictivo y en cierta manera lo es, ya que no podemos ejecutar código de nuestra aplicación si la aplicación está en suspensión. Afortunadamente Windows 8 nos proporciona varios mecanismos para dar la sensación al usuario de que nuestra aplicación está activa incluso cuando no está en ejecución, son estos: 

* Reproducir audio en segundo plano mediante **Playback Manager**. 
* Descargar y subir archivos en background mediante **Background Transfer**. 
* Actualización periódicas de *tiles*. 
* Notificaciones programadas y *push*. 

Adicionalmente a estos escenarios, si la operación que queremos hacer es distinta a las anteriores, tenemos la posibilidad de ejecutar código de nuestra aplicación incluso cuando la aplicación no está en ejecución a través de las tareas de background. En esta entrada y durante las siguientes de este mes vamos a ir examinando cada uno de estos escenarios, comenzando por el funcionamiento de la API para la transferencia de datos en segundo plano. 

# API Windows.Networking.BackgroundTransfer

Todas las clases para utilizar las funcionalidades para la transferencia de datos en segundo plano se encuentran incluidas dentro en el namespace **Windows.Networking.BackgroundTransfer**. Las clases principales a utilizar serán **BackgroundDownloader** y **BackgroundUploader** que nos servirán para configurar la operación de carga y descarga. En el siguiente ejemplo iniciamos la descarga de un fichero utilizando el método **createDownload** al que pasamos la URI del fichero a descargar y el fichero (*IStorageFile*) donde se guardará. Este método nos devuelve un objeto **DownloadOperation **que podremos utilizar para iniciar la descarga mediante método *StartAsync*. 

```js
var download = null; 
var promise = null; 

function downloadFile(uriString) { 
    var fileName = uriString.substring(uriString.lastIndexOf('/') + 1); 
    Windows.Storage.KnownFolders.videosLibrary.createFileAsync(fileName, Windows.Storage.CreationCollisionOption.generateUniqueName).done(function (newFile) { 
        var uri = Windows.Foundation.Uri(uriString); 
        var downloader = new Windows.Networking.BackgroundTransfer.BackgroundDownloader(); 
        download = downloader.createDownload(uri, newFile); 
        promise = download.startAsync().then(completed, failed, progress); 
        }); 
    };
```

Un detalle importante de este código es que estamos guardando a nivel de módulo tanto el objeto *DownloadOperation* como la promise que devuelve startAsync. Esto nos será útil cuando queramos cancelar, pausar o reanudar la descarga. 

# Mostrar el progreso de transferencia 

El método startAsync devuelve una promise que nos informa de cuando ha finalizado con éxito, cuando ha fallado y el progreso de la transferencia. En la función de progreso, podemos obtener el estado del progreso mediante la propiedad **progress** del objeto **DownloadOperation**. Entre otra información, podemos obtener la tamaño total de la transferencia (*totalBytesToReceive*) y los bytes recibidos (*bytesReceived*). En el ejemplo siguiente utilizamos esta información para mostrarla mediante un control *progressBar*.

```js
function progress() {
    var currentProgress = download.progress;

    var progressBar = document.getElementById("progressBar");
    progressBar.value = currentProgress.bytesReceived;
    progressBar.max = currentProgress.totalBytesToReceive;

    document.getElementById("dataTransfer").innerHTML = currentProgress.bytesReceived + " bytes recibidos / " + currentProgress.totalBytesToReceive + " bytes totales";

    if (currentProgress.status === Windows.Networking.BackgroundTransfer.BackgroundTransferStatus.pausedByApplication) {
        displayStatus("Descarga en pausa por la aplicación.");
    } else if (currentProgress.status === Windows.Networking.BackgroundTransfer.BackgroundTransferStatus.pausedCostedNetwork) {
        displayStatus("Descarga en pausa debido a la directiva de costos.");
    } else if (currentProgress.status === Windows.Networking.BackgroundTransfer.BackgroundTransferStatus.pausedNoNetwork) {
        displayStatus("Descarga en pausa debido a una falta de conectividad.");
    }
}

function completed() { 
  displayStatus("Descarga completada."); 
} 
function failed() { 
  displayStatus("Descarga finalizada."); 
}
```

Pausar, reanudar y cancelar una descarga 
---

El objeto *DownloadOperation* dispone de los métodos *pause* y *resume* que nos permiten poner en pausa y reanudar una descarga. En el ejemplo siguiente definimos las funciones para realizar estas dos acciones:

```js
function pauseDownload () {
    if (download) {
        if (download.progress.status === Windows.Networking.BackgroundTransfer.BackgroundTransferStatus.running) {
            download.pause();
            displayStatus("Descarga pausada.");
        }
        else {
            displayStatus("No hay ningúna descarga activa.");
        }
    }
}

function resumeDownload() {
    if (download) {
        if (download.progress.status === Windows.Networking.BackgroundTransfer.BackgroundTransferStatus.pausedByApplication) {
            download.resume();
            displayStatus("Descarga reanudada.");
        }
        else {
            displayStatus("No hay ningúna descarga activa.");

        }
    }
}
```

Como podemos ver, antes de llamar a los métodos, comprobamos si tenemos una descarga activa y en progreso verificando el valor de la propiedad *progress.status*. Para cancelar la descarga tenemos que cancelar la promise llamando al método *cancel*.

```js
function cancelDownload() {
    if (promise) {
        promise.cancel();
        promise = null;
        displayStatus("Descarga cancelada.");
    }
    else {
        displayStatus("No hay ningúna descarga activa.");
    }
}
```

Recuperando información de descarga 
---

Cuando utilizamos la transferencia en segundo plango el sistema controla cada operación de transferencia de manera independiente y la separa de la aplicación que la lanza. Así que podemos cambiar de aplicación e incluso finalizarla y la transferencia continuará ejecutándose. Si el usuario de nuestra aplicación finaliza la aplicación y después vuelve a activarla antes de que la transferencia haya finalizado, tendremos que seguir mostrando el progreso de transferencia. Para conseguir esto, nos ayudaremos del método *getCurrentDownloadAsync* de la clase **BackgroundDownloader** que nos devuelve una colección de de descargas pendientes. Para cada una de estas descargas podremos utilizar el método *attachAsync* con el que nos adjuntaremos a la descarga y podremos monitorizar el progreso. En el siguiente ejemplo obtenemos la descargas activas y nos adjuntamos a la primera de la colección.

```js
Windows.Networking.BackgroundTransfer.BackgroundDownloader.getCurrentDownloadsAsync().done(function (downloads) {
        attachDownload(downloads[0]);
});

function attachDownload(loadedDownload) {
    download = loadedDownload;
    promise = download.attachAsync().then(completed, failed, progress);
}
```

Conclusiones
---

En esta entrada hemos visto como iniciar y gestionar la transferencia de un archivo mediante la API de **BackgroundTransfer**. Este tipo de transferencia está pensada para ser utilizada con ficheros de gran tamaño (video, música, etc.) y lo podemos utilizar haciendo uso de los protocolos HTTP o HTTPS y FTP para operaciones de descarga. En la siguiente entrada seguiremos explorando nuevos escenarios en los que podemos ejecutar operaciones aunque las aplicaciones no estén en ejecución.

Referencias
---

[Ciclo de vida de la aplicación](http://msdn.microsoft.com/es-es/library/windows/apps/hh464925.aspx)  
[Transferencia de datos en segundo plano](http://msdn.microsoft.com/es-es/library/windows/apps/hh452979.aspx)  

