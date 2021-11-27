---
title: Creando live tiles y notificaciones as easy as pie
tags: [windows_store, winjs]
---
Durante el pasado [#W8IO](http://www.desarrolloweb.com/en-directo/live-tiles-windows-8-w8io-8030.html) de [desarrolloweb.com](http://www.desarrolloweb.com/) en el que participé junto a [@tonirecio](http://twitter.com/tonirecio) y [@carballude\_es](https://twitter.com/carballude_es) y que dedicamos a hablar de las _Live Tiles_, comentamos que existía una librería para poder crear fácilmente _tiles_ y notificaciones. La librería en cuestión es un componente WinRT C# llamado **NotificationsExtensions** que podemos obtener a través del [código de ejemplo de la MSDN](http://code.msdn.microsoft.com/windowsapps/app-tiles-and-badges-sample-5fc49148). La gran ventaja es que nos permite establecer el contenido de las plantillas sin tener que acceder y modificar directamente los elementos XML que las definen. Además y gracias al Intellisense de Visual Studio, podemos ver el nombre de las propiedades que podemos utilizar con cada plantilla. Esto, junto con ciertas validaciones que incorpora, nos ayuda a evitar errores a la hora de crear el contenido de nuestras _tiles_. Podéis ver cómo utlilizar esta librería en el siguiente artículo de MSDN: [Usar la biblioteca NotificationsExtensions en el código](http://msdn.microsoft.com/en-us/library/windows/apps/hh969156.aspx).

Aunque es posible referenciar y utilizar fácilmente componentes WinRT escritos en C# desde JavaScript, en esta entrada vamos a ver una alternativa basada puramente en JavaScript. He creado un módulo que expone un objeto muy similar al objeto **wns** que se utiliza en **Azure Mobile Services**. y que nos permitirá actualizar la _tile_ y programar notificaciones. El módulo forma parte de una solución de ejemplo que he creado para facilitar la creación de aplicaciones para la **Windows Store** utilizando JavaScript y a la que he incorporando los elementos más habituales. ¡Ideal para un Megathon! Pensado para que no nos tengamos que preocupar por la implementación, si no por el contenido de nuestra aplicación. Tanto la [solución completa](https://github.com/acasquete/StoreAppJSReady), como el [módulo de notificaciones](https://github.com/acasquete/StoreAppJSReady/blob/master/StoreAppJSReady/js/notifications.js) se pueden descargar desde GitHub.

Para utilizar este módulo solo se tiene que descargar, copiarlo en la carpeta de _scripts_ de la solución y agregar la referencia en el fichero _default.htm_.

<!– StoreAppJSReady references –> <script src=”js/notifications.js”></script></pre> Básicamente lo que nos proporciona este módulo es una serie de métodos para actualizar la _tile_, el distintivo (o _badge_) y programar una notificación toast. Esto lo conseguimos a través de estos tres métodos: **updateTile**_, **scheduleToast**_ y **updateBadge**. El asterisco en los métodos updateTile y scheduleToast es el marcador para poner el nombre de una de las plantillas, por ejemplo: **updateTileWideText03** o **scheduleToastImageAndText02**. En MSDN tenemos el listado completo tanto de las [plantillas de tile](http://msdn.microsoft.com/en-us/library/windows/apps/hh761491.aspx), como de [notificaciones de sistema](http://msdn.microsoft.com/es-es/library/windows/apps/hh761494.aspx). Veamos varios ejemplos de cómo pasar el contenido para utilizar estos métodos.

    ## Actualizar la tile
    

El siguiente script muestra como actualizar la _tile_ utilizando la pantilla [TileWidePeekImageCollection01](http://msdn.microsoft.com/en-us/library/windows/apps/hh761491.aspx#TileWidePeekImageCollection01) que contiene 5 imágenes y 2 líneas de texto. Para cada elemento de texto utilizamos el formato **textN** y para cada elemento de imagen, **imageNsrc**.

Notifications.updateTileWidePeekImageCollection01(
{
    text1: "Título de la Tile",
    text2: "Segundo campo de la Tile",
    image1src: "http://localhost:37725/images/image1.png",
    image2src: "ms-appx:///images/image2.jpg",
    image3src: "ms-appx:///images/image3.jpg",
    image4src: "ms-appx:///images/image4.jpg",
    image5src: "http://localhost:37725/images/image5.jpg"
});

Si omitimos algún texto o imagen, se reemplazará automáticamente por una cadena vacía. Adicionalmente, podemos incluir el texto alternativo para las imágenes.

Notifications.updateTileWideSmallImageAndText05(
  {
      text1: "Text Header Field 1",
      text2: "Text Field 2",
      image1src: "http://localhost:37725/images/image1.png",
      image1alt: "Alternate text for image",
  });

Por defecto, está habilitada la cola de notificaciones, así que cada llamada a un método **updateTile** encolará la actualización. Si queremos deshabilitar la cola de notificaciones debemos utilizar el método _enableNotificationQueue_ de la siguiente forma, pasando _false_ como parámetro.

Notifications.enableNotificationQueue(false);

Y, por último, para limpiar la tile tenemos el método clearTile();

Notifications.clearTile();

    ## Cambiar el distintivo de la tile
    

Para cambiar el distintivo, tenemos que utilizar el método _updateBadge_. Cómo primer parámetro, podemos pasar un número de 1 al 99 o uno de los siguientes valores para mostrar uno de los glifos predefinidos: activity, alert, available, away, busy, newMessage, paused, playing, unavailable, error, attention. El siguiente _script_ muestra dos ejemplos para actualizar con un número y con el indicador ‘disponible’.

Notifications.updateBadge(8, 10);
Notifications.updateBadge("available", 10);

El segundo parámetro indica el tiempo de expiración en segundos. Si no pasamos ningún valor, nunca caducará.

    ## Programar una notificación de sistema
    

Por último, queda mostrar la forma de programar una notificación del sistema. Al igual que con las _tiles_, tenemos un método por tipo de plantilla y el contenido lo establecemos de la misma forma. En el siguiente ejemplo se muestra cómo programar una notificación que se mostrará al cabo de 1 hora (3600 segundos).

Notifications.scheduleToastImageAndText01(
  {
      text1: "Demo notificación toast!",
      image1src: "http://localhost:37725/images/image1.png",
      image1alt: "Image 1"
  }, 3600);



## Resumen


Aunque todavía queda añadir un poco de funcionalidad, como enviar las dos tiles (cuadrada y ancha) a la vez, cancelar notificaciones o personalizar aún más las notificaciones, este módulo nos facilita la creación de \*tiles \*y notificaciones para los escenarios más sencillos y es fácilmente modificable para aquellos usuarios que no quieran pelearse con el componente WinRT de NotificationsExtensions.


## Referencias


[Solución StoreAppReadyJS en GitHub](https://github.com/acasquete/StoreAppJSReady)
