---
title: Reproducir audio en background
tags: [programming, windows_store, winjs, winrt]
reviewed: true
---
Continuamos con la serie de entradas dedicadas a los procesos en segundo plano en las aplicaciones para la **Windows Store**. En las entradas anteriores vimos cómo realizar la transferencia de archivos y que estas continúen en marcha aunque nuestra aplicación esté en suspensión. Los enlaces a las entradas de la serie son estos:

*   [Transferencia de datos en background](/transferencia-de-datos-en-background)
*   [Transferencia de datos en background con autenticación](/transferencia-de-datos-en-background-con-autenticacion) 

En esta ocasión vamos a ver otro de los procesos en *background* que podemos utilizar desde nuestras aplicaciones, concretamente vamos a explicar cómo reproducir audio y que este continúe reproduciéndose aunque pasemos la aplicación a segundo plano. Esto nos permitirá crear aplicaciones en las que vamos a poder reproducir audio y video tanto local como en streaming, crear listas de reproducción y poder escucharlas aunque no tengamos la aplicación en primer plano.

Todo empieza con <audio>
------------------------

En las aplicaciones _JavaScript_ tenemos la suerte de contar con el tag **audio** de **HTML 5**, así que la forma más sencilla de poder añadir audio a nuestra aplicación es mediante el siguiente código.

```xml
<audio autoplay=”autoplay”> 
    <source src=”media/pogues.mp3” /”> 
</audio>
```

Enseguida comprobaremos que si ponemos solo este código y cambiamos la aplicación a segundo plano, el audio no continúa reproduciéndose. Para poder reproducir audio en _background_ tenemos que realizar una serie de cambios en nuestro código.

El primero de todos es utilizar un atributo adicional del tag HTML 5 que nos proporciona Microsoft, **msAudioCateogory**, que nos permite cambiar el comportamiento del audio. Los valores que acepta este atributo los puedes ver en detalle en el artículo de la MSDN ([Propiedad msAudioCategory](http://msdn.microsoft.com/es-es/library/windows/apps/hh767375.aspx)). De entre todos los valores permitidos, el que nos interesa es **BackgroundCapableMedia**, con el que indicamos que el audio se tiene que reproducir en segundo plano.

```xml
<audio autoplay="autoplay" msaudiocategory="BackgroundCapableMedia">
  <source src="media/pogues.mp3" />
</audio>
```

Añadiendo la declaración en el *manifest*
---    

El segundo cambio que tenemos que hacer es sobre el manifiesto de la aplicación. Tenemos que añadir la declaración de Tareas de background y marcar la casilla Audio. En la imagen se puede ver la configuración.

Pero aún haciendo esto, falta un detalle más ya que si en este momento ejecutamos la aplicación, la reproducción se seguirá parando cuando pasemos la aplicación a segundo plano.

Escuchar eventos de MediaControl
---    

El tercer y último requisito es escuchar los eventos del objeto **MediaControl**. Como mínimo, para que el audio se ejecute en _background_, debemos añadir un controlador para los eventos **playpausetogglepressed**, **playpressed**, **pausepressed**, **stoppressed**. Si no añadimos todos estos, no conseguiremos que el audio se ejecute en segundo plano. Además, es importante recordar que este paso es muy importante ya que es **uno de los principales motivos por el que las aplicaciones no suelen superar la certificación** de la Windows Store. Este es el código para registrar los controladores de eventos.

```js
var mediaControls;
var audiotag;

audiotag = document.getElementsByTagName("audio")[0];
mediaControls = Windows.Media.MediaControl;

mediaControls.addEventListener("playpausetogglepressed", playpausetoggle, false);
mediaControls.addEventListener("playpressed", playbutton, false);
mediaControls.addEventListener("pausepressed", pausebutton, false);
mediaControls.addEventListener("stoppressed", pausebutton, false);

function playpausetoggle() {
    if (mediaControls.isPlaying === true) {
        audiotag.pause();
    } else {
        audiotag.play();
    }
}

function pausebutton() {
    audiotag.pause();
}

function playbutton() {
    audiotag.play();
}
```

Si ahora ejecutamos la aplicación y la pasamos a segundo plano, podremos, por fin, escuchar que la música sigue en reproducción y que si pulsamos los controles de volumen, aparece el control de reproducción de Windows 8 superpuesto en la pantalla.

Añadiendo una lista de reproducción
---    

Con esto ya tendríamos la funcionalidad mínima para ejecutar audio en segundo plano. Adicionalmente si nuestra aplicación tiene una lista de reproducción, podemos registrar los controles para pasar a la pista siguiente o volver a la anterior. Esto lo conseguimos registrando los eventos **nexttrackpressed** y **previoustrackpressed**. Además tendremos que tener la lógica necesaria para mantener la lista de reproducción. En el momento que registremos un controlador de evento, se activará el botón correspondiente, así que tenemos que ir añadiendo o eliminado el controlador según nuestras necesidades. El código siguiente muestra el código completo para gestionar una lista de reproducción con varios elementos.

```js
var mediaControls;
var audiotag;
var currentIndexTrack = 0;
var isPreviousRegistered = false, isNextRegistered = false;

var playList = [
    { trackName: "TrackA", artistName: "Artist1", albumArt: "ms-appdata:///local/trackA.jpg", audio: "/media/trackA.mp3" },
    { trackName: "TrackB", artistName: "Artist2", albumArt: "ms-appdata:///local/trackB.jpg", audio: "/media/trackB.mp3" },
    { trackName: "TrackC", artistName: "Artist3", albumArt: "ms-appdata:///local/trackC.jpg", audio: "/media/trackC.mp3" }
    ];

audiotag = document.getElementById("audiotag");

mediaControls = Windows.Media.MediaControl;

mediaControls.addEventListener("playpausetogglepressed", playpausetoggle, true);
mediaControls.addEventListener("playpressed", playbutton, false);
mediaControls.addEventListener("pausepressed", pausebutton, false);
mediaControls.addEventListener("stoppressed", pausebutton, false);

playbutton();

function playpausetoggle() {
    if (audiotag.paused) {
        playbutton();
    } else {
        pausebutton();
    }
}

function pausebutton() {
    audiotag.pause();
}

function playbutton() {
    setAudioInfo();
    updateNextPrevious();
    audiotag.play();
}

function nextTrack() {
    currentIndexTrack++;
    playbutton();
}

function previousTrack() {
    currentIndexTrack--;
    playbutton();
}

function setAudioInfo() {
    audiotag.src = playList[currentIndexTrack].audio;
    mediaControls.trackName = playList[currentIndexTrack].trackName;
    mediaControls.artistName = playList[currentIndexTrack].artistName;
    mediaControls.albumArt = new Windows.Foundation.Uri(playList[currentIndexTrack].albumArt);

}

function updateNextPrevious() {
    if (currentIndexTrack == 0) {
        if (isPreviousRegistered) {
            mediaControls.removeEventListener("previoustrackpressed", previousTrack, false);
            isPreviousRegistered = false;
        }
        if (!isNextRegistered && playList.length > 1) {
            mediaControls.addEventListener("nexttrackpressed", nextTrack, false);
            isNextRegistered = true;
        }
    }
    if (currentIndexTrack == playList.length - 1) {
        if (isNextRegistered) {
            mediaControls.removeEventListener("nexttrackpressed", nextTrack, false);
            isNextRegistered = false;
        }
        if (!isPreviousRegistered) {
            mediaControls.addEventListener("previoustrackpressed", previousTrack, false);
            isPreviousRegistered = true;
        }
    }
}
```

Descargar imagen al almacenamiento local
---    

La función _updateNextPrevious_ actualiza el estado de los botones siguiente y anterior registrando el controlador de los eventos. El objeto **MediaControl** dispone también de varias propiedades para personalizar la información que aparece en el control de reproducción: _ArtistName_, _TrackName_ y _AlbumArt_, que nos permiten establecer el nombre del artista, de la pista y la imagen del album respectivamente. Si no proporcionamos esta información, se mostrará el nombre de la aplicación por defecto. En la función setAudioInfo se establece el valor de estas tres propiedades.

```js
mediaControls.trackName = playList[currentIndexTrack].trackName;
mediaControls.artistName = playList[currentIndexTrack].artistName;
mediaControls.albumArt = new Windows.Foundation.Uri(playList[currentIndexTrack].albumArt);
```

Vamos a prestar un poco de atención a la última línea. La propiedad _AlbumArt_ requiere que pasemos un objeto Uri, pero además la dirección de este objeto tiene que referenciar a una imagen que esté en el paquete de la aplicación (protocolo **ms-appx**) o en el almacenamiento local de la aplicación (protocolo **ms-appdata**). Es decir, no podemos referenciar directamente una imagen que esté en un servidor externo. Sin embargo, este es un escenario muy habitual, así que si tenemos las imagenes fuera del paquete de la aplicación tendremos que descargarla previamente al almacenamiento local. El código siguiente muestra como conseguirlo:

```js
function downloadAndSave(url) {
  var fileName = url.substring(url.lastIndexOf('/') + 1);

  return new WinJS.Promise(function(completed) {
      WinJS.xhr({ url: url, responseType: "blob" }).done(function(resultA) {
          writeBlobToFile(resultA.response, fileName).done(function () {
              completed(fileName);
          });
      });
  });
}

function writeBlobToFile(blob, filename) {
  var applicationData = Windows.Storage.ApplicationData.current;
  var localFolder = applicationData.localFolder;
  return localFolder.createFileAsync(filename, Windows.Storage.CreationCollisionOption.replaceExisting).then(function (file) {
      file.openAsync(Windows.Storage.FileAccessMode.readWrite).then(function (output) {
          var input = blob.msDetachStream();
          Windows.Storage.Streams.RandomAccessStream.copyAsync(input, output).then(function () {
              output.flushAsync().done(function () {
                  input.close();
                  output.close();
              });
          });
      });
  });
}
```

La función downloadAndSave descarga el fichero que le pasamos por parámetro y devuelve un objeto **Promise** que se completa cuando se ha podido escribir en el almacenamiento local de la aplicación (Windows.Storage.ApplicationData.current.localFolder). Para usar esta función, simplemente tenemos que pasar la URL de la imagen que queremos descargar y asignar el valor del nombre del fichero a la propiedad albumArt del objeto MediaControl de la siguiente forma.

```js
downloadAndSave("http://www.idlebit.es/images/art/albumArt.jpg").done(function (filename) {
  mediaControls.albumArt = new Windows.Foundation.Uri("ms-appdata:///local/" + filename);
});
```

Resumen
---

En esta entrada hemos visto como añadir capacidad de audio en background en nuestra aplicación. Adema´s hemos visto como personalizar el reproductor para que aparezca la información de la pista en reproducción. Y por último hemos visto como descargar una imagen y guardarla en el almacenamiento local para poder utilizarla como portada.


Referencias
---

[Inicio rápido: Agregar audio a una aplicación](http://msdn.microsoft.com/en-us/library/windows/apps/hh452730.aspx)  
[Cómo reproducir audio en segundo plano](http://msdn.microsoft.com/es-es/library/windows/apps/hh700367.aspx)  
[Audio Playback in a Windows Store App](http://msdn.microsoft.com/en-us/library/windows/hardware/hh770517)  
[System Transport Controls Developer Guide](http://msdn.microsoft.com/en-us/library/windows/hardware/hh833781.aspx)  
