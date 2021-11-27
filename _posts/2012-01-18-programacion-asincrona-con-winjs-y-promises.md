---
title: Programación asíncrona con WinJS y «Promises»
tags: [windows_store, winjs, winrt]
---
En la anterior entrada, en la que hicimos una introducción a los [controles WinJS y al databinding](/controles-winjs-y-databinding-de-un-vistazo), vimos que para poder acceder a todos los controles creados de forma declarativa teníamos que llamar a la función _WinJS.UI.processAll_, que se encargaba de crear todas las instancias. Además nos aprovechábamos de que esta función devolvía un objeto **Promise** para realizar una serie de acciones. Bien, hasta aquí nada nuevo, ¿pero qué es exactamente un objeto Promise? Esto es lo voy a intentar explicar en esta entrada.

Uno de los problemas con el que nos encontramos al lidiar con programación asíncrona en JavaScript es la complejidad que adquiere el código cuando tenemos que sincronizar una serie de llamadas asíncronas, por ejemplo, cuando hacemos una llamada a un servicio y a partir de la respuesta de éste tenemos que realizar otra llamada a otro servicio. Además, si añadimos una gestión de errores mínima, el código que obtenemos es todavía más complejo. En definitiva, tenemos un código complejo de seguir a pesar de que es un código que, según su lógica, debería ejecutarse linealmente. La comunidad JavaScript propuso una solución a este problema a través del estándar [Common JS Promises/A](http://wiki.commonjs.org/wiki/Promises/A). Básicamente una _Promise_ es un objeto que nos «promete» un resultado en algún momento en el futuro y nos permite programar cualquier operación cuando ese valor esté establecido. Esto nos permite escribir código no bloqueante que se ejecuta de forma asíncrona y sin necesidad de escribir código para manejar la sincronización. Ahora mismo existen implementaciones de Promises en los principales frameworks de JavaScript (jQuery, node.js, dojo, etc.) y WinJS no podía quedarse atrás.

La especificación es muy sencilla, y dice simplemente que hay que tener un objeto con un método llamado _then_ y que este método debe aceptar tres parámetros. Estos tres paramétros serán tres funciones callback que se llamarán cuando la Promise se complete, cuando se produzca un error o cuando se produzca algún evento de progreso. En WinJS el objeto es **WinJS.Promise** y podemos ver su implementación en el fichero **base.js**. Ya he comentado antes que la función _WinJS.UI.processAll_ devuelve un objeto **Promise**, veamos otro ejemplo que utilizaremos a menudo.

WinJS.Application.onmainwindowactivated = function (e) { WinJS.xhr({ url: “http://idlebit.es/rss” }).then( function (result) { console.log(“Promise completada con éxito.”); }, function (error) { console.log(“Promise completada con error.”); }, function (progress) { console.log(“Promise en progreso.”); }); }</pre> En este caso hemos llamado a la función **WinJS.xhr** que realiza una petición **XmlHttpRequest** como una **Promise**. Esta función devuelve un objeto **Promise** que se completa cuando la propiedad _readyState_ es igual a 4 y el valor de _status_ está entre 200 y 300. Si la propiedad _readyState_ es igual a 4 pero el _status_ no está entre 200 y 300, la _Promise_ se completará pero en este caso se llamará a la función callback de error y para el resto de llamadas a _XMLHttpRequest.onreadystatechange_ se llamará a la función callback de progreso. Si ejecutamos el código, podremos comprobar que a cada una de las funciones callback se le pasa el objeto XMLHttpRequest. En este caso he elegido la función _WinJS.xhr_ porque implementa la notificación de los tres estados, pero hay que tener en cuenta que no todas las Promises lo implementan ya que es opcional. Ahora veamos un ejemplo en los que queremos concatenar una serie de peticiones.

WinJS.xhr({ url: "http://idlebit.es/rss" }).then( 
  function (result) { console.log("Promise 1 completada con éxito."); 
  return WinJS.xhr({url: "http://idlebit.es/atom"}); }).then(
    function(result) { console.log("Promise 2 completada con éxito."); 
  });

En este ejemplo realizamos una primera petición (http://idlebit.es/rss) y cuando se completa hacemos una nueva llamada a la función WinJS.xhr y devolvemos su resultado, es decir, devolvemos un nuevo objeto Promise. Esto nos permite encadenar otra llamada al método _then_ que podemos utilizar de nuevo para mostrar el resultado de la petición, facilitándonos mucho la codificación en este tipo de escenario. WinJS también nos permite coordinar Promises mediante los métodos _any_ y _join_. Estos dos métodos aceptan como parámetro un array de objetos Promise, la diferencia está en que el método _any_ devuelve una Promise que se completa cuando alguna Promise del array se completa, y el método _join_ devuelve una Promise que se completa cuando todas las Promises del array se completado. Veamos el siguiente ejemplo:

promises.push(WinJS.xhr({ url: "http://idlebit.es/rss" })); 
promises.push(WinJS.xhr({ url: "http://idlebit.es/atom" }));

WinJS.Promise.join(promises).then(function (results) {
  console.log("Todas las promises se han completado"); 
}); 

WinJS.Promise.any(promises).then(function (results) { 
  console.log("La promise "+ results.key + " se ha completado");
});

Y por último vamos a ver como crear nuestras propias _Promises_. Para el ejemplo vamos a crear una función que devuelva un objeto WinJS.Promise con el número de Fibonnaci. Posiblemente el código no es el óptimo, pero para ver el funcionamiento de las Promises nos sirve.

function fibonnaci(n) { 
  return new WinJS.Promise( function (c, e, p) { 
    setTimeout(function () { 
      var var1 = 0; 
      var var2 = 1; 
      var var3; 
      if (n == 0) {
        e("número no válido"); 
      } else if (n == 1) { 
        c(var1); 
      } else if (n == 2) { 
        p(var1); 
        c(var2);
      } else { 
        p(var1); 
        for (var i = 3; i <= n; i++) { 
          var3 = var1 + var2; 
          var1 = var2; 
          var2 = var3; p(var3);
        } 
        c(var3);
      }
    }, 1); 
  }); 
}

En este código estamos creando un objeto WinJS.Promise al que le pasamos en el constructor la función con tres argumentos (complete, error, progress). El detalle importante está en la línea 4, en la que se está llamando a la función _setTimeout_ para evitar que el código bloquee la interfaz de usuario. El código para utilizar esta función sería este:

var valor = fibonnaci(10).then( 
  function (results) { console.log(results); }, 
  function (error) { console.log(error); }, 
  function (progress) { console.log(progress); });

Aquí llamamos a la función fibonnaci pasando el valor 10 y en el método then pasamos las tres funciones que mostrarán el progreso y el resultado final. En el caso de que pasemos el valor 10, la Promise se completará con un error. Hasta aquí este repaso a la programación asíncrona con WinJS en el que hemos visto como utilizando \*Promises\* podemos escribir un código asíncrono más claro y más fácil de depurar.

Referencias:
---

[CommonJS: Promises/A](http://wiki.commonjs.org/wiki/Promises/A) 
[WinJS.Promise Object](http://msdn.microsoft.com/en-us/library/windows/apps/br211867.aspx) 
[Asynchronous programming in JavaScript using promises](http://msdn.microsoft.com/en-us/library/windows/apps/hh464930.aspx) 
[Asynchronous Programming in JavaScript with “Promises”](http://blogs.msdn.com/b/ie/archive/2011/09/11/asynchronous-programming-in-javascript-with-promises.aspx)

