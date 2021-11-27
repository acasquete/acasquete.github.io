---
title: Transferencia de datos en background con autenticación
tags: [windows_store, winjs]
---
En la entrada anterior vimos cómo las [transferencias en segundo plano](/transferencia-de-datos-en-background) nos permiten descargar y subir archivos aunque la aplicación no esté en ejecución. Antes de pasar al siguiente escenario de operaciones en _background_, voy a aprovechar esta entrada para responder a algunas dudas que me habéis hecho llegar sobre las descargas con servidores con autenticación habilitada.

Autenticación HTTP básica
-------------------------

Al igual que haríamos en una petición web normal, si en el servidor está activada la autenticación de acceso básica, tenemos que añadir un encabezado HTTP personalizado que proporcione un nombre de usuario y una contraseña válidos para obtener acceso al fichero. En el caso de las transferencias en _background_, esto lo conseguimos mediante el método _setRequestHeader_ del objeto **BackgroundDownloader**.

Para enviar las credenciales al servidor, añadimos a la petición el encabezado _Authorization_ con la información de autenticación que se construye codificando en base 64 el usuario y la contraseña. Los pasos concretos son los siguientes:

1.  Concatenar el usuario y la contraseña separados por dos puntos (:) “usuario:contraseña”.
2.  Codificar la cadena resultante en Base64.
3.  Añadir al principio de la cadena el literal “Basic” más un espacio en blanco. El código siguiente muestra cómo añadir el encabezado pasando las credenciales. La función \*base\_auth \*devuelve el valor del encabezado siguiendo los pasos anteriores:

var downloader = new Windows.Networking.BackgroundTransfer.BackgroundDownloader(); downloader.setRequestHeader(‘Authorization’, base\_auth(“alex”, “mipassword”)); download = downloader.createDownload(uri, newFile);

promise = download.startAsync().then(completed, failed, progress);

function base\_auth(user, password) { var token = user + ‘:’ + password; var hash = btoa(token); return “Basic “ + hash; }</pre> Este código añadirá el encabezado siguiente en la petición HTTP.

Authorization: Basic YWxleDptaXBhc3N3b3Jk

El inconveniente de la autenticación básica es evidente, ya que estamos transmitiendo las contraseñas codificadas en base 64 sin cifrar. Así que sólo deberiamos utilizar este tipo de autenticación cuando la conexión entre el cliente y el servidor sea segura.

    ## Controlando los errores de transferencia
    

Si intentamos descargar un archivo de un servidor con autenticación y nuestra petición no incluye el encabezado con las credenciales, el servidor nos devolverá un error. La forma de capturar este error y reaccionar, por ejemplo, solicitando las credenciales al usuario, es haciendo uso de la clase **BackgroundTransferError**, con la que podemos obtener los errores que se producen durante las operaciones de transferencia.

En el siguiente código utilizamos el método _getStatus_ de la clase **BackgroundTransferError** pasando el número de error (error.number). Este método nos devuelve un error específico de los definidos en la enumeración _[WebErrorStatus](http://msdn.microsoft.com/es-es/library/windows/apps/windows.web.weberrorstatus)._

function failed(error) {
    var backgroundTransferError = Windows.Networking.BackgroundTransfer.BackgroundTransferError;
    var errorStatus = backgroundTransferError.getStatus(error.number);

    if (errorStatus === Windows.Web.WebErrorStatus.cannotConnect ||
        errorStatus === Windows.Web.WebErrorStatus.notFound ||
        errorStatus === Windows.Web.WebErrorStatus.requestTimeout) {
        displayStatus("No se pudo conectar con el servidor.");
    } else if (errorStatus == Windows.Web.WebErrorStatus.unauthorized) {
        displayStatus("No se pudo realizar la autenticación o aún no se han proporcionado las credenciales.");
    } else {
        displayStatus("Error #" + errorStatus);
    }
}

Con este código solamente estamos mostrando un mensaje de error personalizado según el tipo de error devuelto, pero en el caso de un acceso no autorizado, podríamos, por ejemplo, mostrar una pantalla para que el usuario introdujese unas credenciales válidas o utilizar unas credenciales por defecto.

    ## Acceso a FTP
    

Creo que este escenario es de sobra conocido, pero ya que la clases de **BackgroundTransfer** también soportan transferencias vía FTP (aunque únicamente para realizar descargas), no está de más comentar cómo pasar las credenciales en el caso de que queramos descargar un archivo de un servidor FTP con autenticación básica habilitada.

En esta situación no tendremos que añadir ningún encabezado personalizado, simplemente tendremos que pasar las credenciales en la misma URL, utilizando el formato ftp:// usuario : contraseña @ servidorftp / ruta.

downloadFile("ftp://alex:mipassword@ftp.idlebit.es/wwwroot/downloads/fichero.zip");

Y con esto termino esta breve entrada para utilizar las transferencias en background con servidores con autenticación habilitada. Mañana más. Stay tuned!

