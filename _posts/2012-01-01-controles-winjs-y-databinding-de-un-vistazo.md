---
title: Controles WinJS y databinding de un vistazo
tags: [programming, windows_store, winjs]
reviewed: true
---
WinJS (_Windows Library for JavaScript_) es una librería que nos ayuda en la tarea de crear **aplicaciones Metro style para Windows 8** utilizando **JavaScript**. Esta librería esta compuesta por un conjunto de ficheros JavaScript y CSS que nos proporcionan además de los estilos por defecto para que nuestras aplicaciones tengan el estilo Windows Metro, los controles de uso común como el selector de fecha y hora, la barra de aplicación, listas de selección, barra de progreso, etc. Así, hasta unos 20 controles WinJS que tenemos disponibles en la _preview_. Pero no sólo esto, WinJS nos da soporte entre otras funciones para interacción táctil, navegación y programación asíncrona. En esta entrada nos vamos a centrar en como declarar **controles WinJS** y como enlazarlos con un origen de datos.

A diferencia de los controles HTML, los controles WinJS no tienen un elemento dedicado, es decir, si queremos añadir un elemento de selección de hora (Timepicker) no haremos añadiendo el elemento <timepicker /> a nuestro código HTML, sino que tenemos que crear un objeto JavaScript que estará enlazado a un elemento HTML. Tenemos dos métodos para instanciar estos controles, lo podemos hacer de forma declarativa, utilizando atributos desde el código HTML, o programáticamente. Primero veamos cómo podemos crear el control WinJS de forma declarativa. Añadimos un elemento div y utilizamos el attributo **data-win-control** para especificar el tipo de control que queremos. Con esto estamos indicando que el elemento sera el host del control WinJS. En el siguiente ejemplo vemos como crear un control **TimePicker**.

```xml
<div data-win-control=”WinJS.UI.TimePicker”></div>
```

Una vez lo tenemos declarado en el HTML tenemos que llamar a la función **WinJS.UI.processAll** que se encarga de parsear todo el código HTML e instanciar los controles WinJS que contenga el documento. El mejor sitio para llamar a esta función es en el evento DOMContentLoaded que se lanza cuando se ha terminado de parsear toda la página.

```js
document.addEventListener("DOMContentLoaded", function (e) {
  WinJS.UI.processAll(); 
});
```

Además de crear el objeto, podemos establecer el valor de las propiedades de los controles WinJS mediante el atributo **data-win-options**. En nuestro ejemplo, el control _TimePicker_ tiene la propiedad _minuteIncrement_con la que podemos establecer el intervalo de minutos que se mostrarán en el control. Por ejemplo, si establecemos el valor en 15, el desplegable mostrará los valores, 0, 15, 30 y 45. Aquí vemos el código para conseguir esto:

```xml
<div data-win-control="WinJS.UI.TimePicker" data-win-control="{minuteIncrement: 15}"></div>
```

Ahora veamos cómo podemos crear un control de forma programática, creándolo por código. Para esto seguimos necesitando un elemento HTML que haga de host del control WinJS, así que declaramos un elemento div y le asignamos un id.

```xml
<div id="fecha"></div>
```

El identificador lo necesitamos para poder acceder a él, y ahora lo único que tenemos que hacer es instanciar el control pasando el elemento asociado y el valor de las opciones. En este caso vamos a instanciar un control de selección de fecha (WinJS.UI.DatePicker) estableciendo el valor de las propiedades _maxYear_ y _minYear_.

```js
var target = document.getElementById("fecha"); 
var dateControl = new WinJS.UI.DatePicker(target, { maxYear: 2020, minYear: 2000 });
```

Un detalle a tener en cuenta es que cuando creamos los controles por código, no es necesario realizar la llamada a la función _WinJS.UI.processAll_ ya que lo que hace esta función precisamente es instanciar los controles.

Para crear controles de forma declarativa la mejor herramienta que tenemos a nuestra disposición es Blend ya que disponemos de la lista completa de controles y podemos ver todas las propiedades disponibles para cada control. Si abrimos nuestro proyecto con Blend, veremos que en la pestaña _Assets_ tenemos todos los controles disponibles y en la ventana de atributos del control podemos ver todas las propiedades disponibles. En la imagen se puede ver el entorno de desarrollo de Blend con el control _DatePicker_ seleccionado y podemos ver que además de las propiedades _maxYear_ y _minYear_ que hemos utilizado en el ejemplo, aparecen todas las demás propiedades disponibles (current, disabled, element).

Sigamos con nuestro ejemplo, ahora lo que queremos hacer es obtener el valor del control, una acción bastante habitual. Para eso vamos añadir un evento que al cambiar el valor del control nos muestre el valor de la fecha seleccionado. La función WinJS.UI.processAll devuelve un objeto **Promise** que se completa cuando se han terminado de procesar todos los controles, así que aprovechando esto, utilizaremos el siguiente código para ejecutar código en el evento _change_. Primero creamos un elemento donde mostrar la información (en este caso he elegido el encabezado h1).

```xml
<h1 id="fechaSeleccionada"></h1>
```

Y obtenemos el control mediante la función **WinJS.UI.getControl** a la que le pasamos el identificador del control que queremos obtener. Una vez tenemos el control registramos el evento.

```js
document.addEventListener("DOMContentLoaded", function (e) {
  var target = document.getElementById("fecha"); 
  var dateControl = new WinJS.UI.DatePicker(target, { maxYear: 2020, minYear: 2000 });

  WinJS.UI.processAll().then(function () { 
    var control = WinJS.UI.getControl(document.getElementById("fecha"));
    control.addEventListener("change", dateChanged);
  });
});
```

La función dateChanged simplemente muestra el valor actual del control.

```js
function dateChanged(eventInfo) { 
  var outputParagraph = document.getElementById("fechaSeleccionada");
  outputParagraph.innerHTML = eventInfo.currentTarget.winControl.current;
}
```

Para terminar, vamos a ver un breve introducción al enlace a datos o _Databinding_ que consiste básicamente en mostrar en la interfaz de usuario un conjunto de datos que tenemos en JavaScript. Para poder utilizar _databinding_ debemos incluir el fichero _binding.js_manteniendo este orden con los restantes ficheros WinJS:

```html
<script src="/winjs/js/base.js"></script>
<script src="/winjs/js/ui.js" type="text/javascript"></script>
<script src="/winjs/js/binding.js"></script> 
<script src="/winjs/js/controls.js" type="text/javascript"></script> 
<script src="/winjs/js/wwaapp.js"></script>
```

Para mostrar la funcionalidad de enlace a datos, vamos a modificar nuestro ejemplo para que el elemento h1 que muestra el valor de fecha seleccionada esté enlazado a un objeto de JavaScript en lugar de tener que establecerlo nosotros. Para conseguir esto añadimos el atributo **data-win-bind** en el elemento de la siguiente forma:

```html
<h1 data-win-bind="innerText: fechaSeleccionada"></h1>
```

Es importante destacar que ya no necesitamos establecer el id del elemento ya que desde el código JavaScript no vamos a necesitar acceder al elemento. La parte izquierda del valor atributo data-win-bind indica la propiedad de destino y la parte de la derecha indica el origen de datos. Y de forma análoga a lo que hacíamos para procesar todos los controles, para que se procesen todos los bindings tenemos que llamar a la función **WinJS.Binding.processAll**, así que añadimos la llamada después de que se procesen todos los controles.

```js
document.addEventListener("DOMContentLoaded", function (e) {
  var target = document.getElementById("fecha"); 
  var dateControl = new WinJS.UI.DatePicker(target, { maxYear: 2020, minYear: 2000 }); 
  WinJS.UI.processAll().then(function () { 
    var control = WinJS.UI.getControl(document.getElementById("fecha")); 
    control.addEventListener("change", dateChanged); 
    WinJS.Binding.processAll(document.body, dataContext); 
  });
});
```

La función **WinJS.Binding.processAll** necesita que le pasemos el documento inicial por el que se empezará a buscar elementos que se tienen que enlazar y un objeto _DataContext_, que servirá como origen de datos. En el ejemplo he pasado _document.body_para procese todos los elementos del cuerpo del documento y el objeto dataContext que todavía no hemos definido, así que hagámoslo ahora:

```js
var dataContext = WinJS.Binding.as({ fechaSeleccionada: new Date(2011,1,1) });
```

En este caso, la función **WinJS.Binding.as** crea un proxy observable de un objeto, esto significa que cuando hagamos un cambio en este objeto se notificarán automáticamente a todos los controles que estén enlazados a este dato. Ahora sólo queda modificar la función _dateChanged_para que en lugar de modificar el contenido del elemento, modifique el valor del DataContext:

```js
function dateChanged(eventInfo) {
  dataContext.fechaSeleccionada = eventInfo.currentTarget.winControl.current;
}
```

Si ejecutamos veremos que al cambiar el valor del campo fecha se actualiza automáticamente el valor del elemento h1 que es el que tiene el enlace a datos. Bien sencillo, ¿no? Hasta aquí este primer post del año, en el que hemos visto de una forma rápida en qué consisten los controles WinJS y cómo podemos realizar un enlace a datos muy sencillo en nuestras aplicaciones JavaScript para Windows 8.

Referencias
---

[Adding WinJS controls and styles](http://msdn.microsoft.com/en-us/library/windows/apps/hh465493.aspx)   
[Windows Library for JavaScript reference](https://web.archive.org/web/20210123141002/http://msdn.microsoft.com/en-us/library/windows/apps/br211669.aspx)  
[Introducing the Windows libraries for JavaScript](http://channel9.msdn.com/Events/BUILD/BUILD2011/TOOL-501T) 
