---
title: Two-way data binding con WinJS
tags: [windows_store, winjs]
---
El enlace de datos bidireccional o _Two-way Data Binding_ es una de las características más demandadas en WinJS, sobre todo porque es una característica que tenemos de serie en otros frameworks JavaScript como es el caso de **KnockouJS**. Descrito en pocas palabras, este modo de enlace nos permite que los cambios realizados en un control HTML se actualicen automáticamente en el modelo de datos origen, evitando de esta forma que tengamos que acceder directamente al elemento del DOM para poder obtener el valor actualizado.

A pesar de que por defecto el enlace de datos en WinJS es unidireccional, podemos extender el comportamiento del inicializador del enlace a datos mediante la función **WinJS.Binding.initializer**. En esta entrada vamos a ver el ejemplo de implementación más sencillo, que es el que [Josh Williams](http://channel9.msdn.com/Events/Speakers/josh-williams) explicó durante [su sesión de la BUILD 2012](http://channel9.msdn.com/Events/Build/2012/4-101). Pero antes de entrar en materia, repasemos brevemente cómo funciona el enlace de datos en WinJS.

Enlazando datos mediante “Observables”
--------------------------------------

Por un lado tenemos el modelo de datos en JavaScript. En nuestro caso vamos a utilizar el modelo más simple posible, que es en un objeto con una propiedad _name_.

var data = { name: “IdleBit” }; </pre>

    Para poder enlazar este objeto con un elemento HTML tenemos que hacerlo "observable", es decir que notifique cuando el valor de la propiedad cambie. Esto lo conseguimos mediante la funci&oacute;n **WinJS.Binding.as **que devuelve un objeto observable a partir del objeto JS. Este nuevo objeto tiene la misma propiedad *name*, pero ahora dispar&aacute; una notificaci&oacute;n cuando se modifique su valor.
    

var data = WinJS.Binding.as({ name: "IdleBit" });

    En el c&oacute;digo HTML, tenemos que utilizar el atributo **data-win-bin** en los elementos que queremos enlazar con el objeto observable que acabamos de crear, el modelo JavaScript. Por ejemplo, en el siguiente ejemplo definimos un elemento &lt;div&gt; y un TextBox enlazados a la propiedad *name*.
    

<div data-win-bind="textContent: name"></div>
<input data-win-bind="value: name" type="text" />

    En el caso del &lt;div&gt; estamos enlazando el valor de la propiedad *name* con la propiedad **textContent**&nbsp;del control y en el caso del input con la propiedad **value**.
    
    
    
    Para que todo esto funcione, tenemos que llamar a la funci&oacute;n **WinJS.Binding.processAll**. Esta funci&oacute;n se encarga de *parsear* todos los elementos del DOM que tienen el atributo **data-win-bind** y enlazarlos con el objeto JavaScript. El primer par&aacute;metro que pasamos a la funci&oacute;n es el elemento ra&iacute;z por el cual comenzar&aacute; a buscar. En nuestro caso le pasamos el todo el cuerpo del documento, y el segundo par&aacute;metro es el contexto de datos, nuestro modelo JS.
    

WinJS.Binding.processAll(document.body, data);

    ## Creando el modo Two-way
    
    
    
    
    Hasta aqu&iacute; nada nuevo, hemos descrito el comportamiento normal del enlace a datos con WinJS. Si modificamos desde JS el contenido de la propiedad *name, *el nuevo valor se ver&aacute; actualizado en todos los controles en los que se est&eacute; utilizando.
    
    
    
    Llegamos ahora al motivo principal que quer&iacute;a tratar en esta entrada. Si modificamos el valor en el Textbox, comprobaremos que el valor no se actualiza en el modelo, ya que el enlace se est&aacute; realizando en un solo sentido. Aqu&iacute; es donde entra en juego la funci&oacute;n&nbsp;**WinJS.Binding.initializer**, con la que podemos extender la forma en que se inicializa el enlace a datos entre el objeto JS y el elemento HTML.&nbsp;
    

var twoWay = WinJS.Binding.initializer(function (source, sourceProps, dest, destProps) {
  WinJS.Binding.defaultBind(source, sourceProps, dest, destProps);
  
  dest.onchange = function () {
    var d = dest\[destProps\[0\]\];
    var s = source\[sourceProps\[0\]\];
    if (s!==d) {
      source\[sourceProps\[0\]\] = d;
  }
});

    Al utilizar el inicializador en declaraci&oacute;n del binding se pasan los objetos y propiedades origen y destino que intervienen en el enlace de datos. La propiedad *source*&nbsp;es el modelo JavaScript al que se est&aacute; enlazando y en el valor *dest* tenemos el elemento HTML o el control WinJS destino. El par&aacute;metro *destProps* es un array que contiene las propiedades del elemento modificado. Lo primero que tenemos que hacer es llamar a la funci&oacute;n **defaultBind** para establecer el enlace a datos por defecto (unidireccional), pero el cambio que vemos en el c&oacute;digo es que estamos a&ntilde;adiendo un manejador para el evento "onchange" para el el elemento de destino, pensando que lo utilizaremos en un Textbox.
    
    
    
    En este manejador comprobamos si el valor de la propiedad del elemento es igual al modelo JavaScript y si no lo es, actualizamos el valor del modelo. Para poder utilizar este inicializador, podemos exponerlo definiendo un Namespace de la siguiente forma:
    

WinJS.Namespace.define("AppJS.Binding", {
  TwoWay: twoWay
});

    De esta forma podremos aplicarlo en la declaraci&oacute;n del enlace a datos en el elemento HTML del control en el que queramos aplicar el enlace en bidireccional. El siguiente c&oacute;digo muestra la forma de hacerlo:
    

<input data-win-bind="value: text AppJS.Binding.twoWay" type="text" />




Si ahora escribimos en el campo de texto y cambiamos de control, el valor se actualizará en el modelo JavaScript y en todos los elementos en los que la propiedad este enlazada. Como ya viene siendo habitual, el ejemplo está disponible en la \[solución JS de GitHub\](https://github.com/acasquete/StoreAppJSReady). 



## Referencias


[Deep dive into WinJS](http://channel9.msdn.com/Events/Build/2012/4-101)  
[Data Binding in a Windows Store App with JavaScript](http://msdn.microsoft.com/en-us/magazine/jj651576.aspx)
