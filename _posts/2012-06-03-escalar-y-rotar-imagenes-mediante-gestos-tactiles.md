---
title: Escalar y rotar imágenes mediante gestos táctiles
tags: [windows_store, winjs]
---
En Internet Explorer 10 y por lo tanto también en las aplicaciones Metro con JavaScript se ha incluido por primera vez soporte para gestos táctiles. De esta forma vamos a poder permitir que el usuario pueda interactuar (escalar, mover y rotar) sobre cualquier elemento de la interfaz gráfica y esto lo vamos a poder hacer sin excesivas complicaciones. En esta entrada vamos a ver cómo ponerlo en práctica implementando un ejemplo sencillo de escalado y rotación de imágenes mediante gestos.

[gestures](/img/gestures.png)] Nuestra aplicación va a mostrar un conjunto de imágenes que vamos a poder mover, girar y escalar por toda la pantalla. Para comenzar lo primero a hacer es crear la lista de imágenes a las que le aplicamos un estilo común (\*touchable\*) y definimos el estilo para mostrarlas a la mitad de su tamaño y con posición absoluta. \*\*default.htm\*\* <img class="touchable" src="images/image1.jpg" /> <img class="touchable" src="images/image2.jpg" /> <img class="touchable" src="images/image3.jpg" /></pre> \*\*default.css\*\*

.touchable {
    width: 50%;
    position: absolute;
}

Como no estamos definiendo una posición para cada una de las imágenes, éstas aparecerán superpuestas en la esquina superior. Ahora desde JavaScript obtenemos todos los elementos que tengan la clase “touchable” y nos suscribimos al evento del puntero \*\*MSPointerDown\*\* y al evento de gesto \*\*MSGestureChange\*\*. Podemos hacerlo mediante el siguiente código.

var elements = document.getElementsByClassName("touchable");
Object.keys(elements).forEach(function (key) {
    var target = elements\[key\];
    target.addEventListener("MSPointerDown", onmsPointerDown, false);
    target.addEventListener("MSGestureChange", onmsGestureChange, false);

});

Un puntero es un punto de contacto en la pantalla, ya sea del dedo, ratón o lápiz. Para saber cuándo pulsamos, movemos o soltamos un puntero tenemos a nuestra disposición una serie de eventos similares a los del ratón. La diferencia principal es que con los eventos del ratón sólo tenemos un único puntero y, si utilizamos una superficie multi-táctil podemos tener varios punteros a la vez sobre la pantalla. En estos casos es cuando tenemos que utilizar los eventos de puntero ya que se disparará un evento separado para cada uno de los puntos de contacto. Para nuestro ejemplo solo necesitamos suscribirnos al evento \*\*MSPointerDown\*\*. Por otro lado tenemos el evento \*\*MSGestureChange\*\* que se dispara cuando los puntos de contacto asociados a un gesto se mueven por la pantalla. Para poder crear esta asociación necesitamos utilizar un objeto \*\*MSGesture\*\*.

var msGestures = \[\];

var elements = document.getElementsByClassName("touchable");
Object.keys(elements).forEach(function (key) {
    var target = elements\[key\];
    target.addEventListener("MSPointerDown", onmsPointerDown, false);
    target.addEventListener("MSGestureChange", onmsGestureChange, false);

    var msGesture = new MSGesture();
    msGesture.target = target;
    msGestures\[target.uniqueID\] = msGesture;
});

En este código hemos creado un array que contiene los objetos \*\*MSGesture\*\*. Estamos creando uno por cada elemento y lo estamos definiendo como target del MsGesture. Ahora, añadimos el código del evento MsPointDown para que cuando se dispare añada el puntero al objeto \*\*MsGesture\*\* del elemento donde se ha disparado.

function onmsPointerDown(e) {
    msGestures\[e.target.uniqueID\].addPointer(e.pointerId);
}

Sólo nos queda el código para aplicar las transformaciones al elemento cada vez que se produzca un cambio y se dispare el evento MsGestureChange. Para esto nos vamos a ayudar del objeto \*\*MSCSSMatrix\*\*.

function onmsGestureChange(e) {
    var matrix = new MSCSSMatrix(e.target.style.msTransform); 
    e.target.style.msTransform = matrix.
        translate(e.offsetX, e.offsetY).                             
        rotate(e.rotation \* 180 / Math.PI).                          
        scale(e.scale).                                                        
        translate(e.translationX, e.translationY).
        translate(-e.offsetX, -e.offsetY);
    e.stopPropagation();
}

Primero instanciamos el objeto \*\*MSCSSMatrix\*\* pasando el valor de la propiedad CSS \*\*msTransform\*\* y aplicamos los cambios mediante los métodos \*\*translate\*\*, \*\*rotate\*\* y \*\*scale\*\*. El código completo del módulo es este:

(function () {
    "use strict";

    var msGestures = \[\];

    function initGestures() {
        var elements = document.getElementsByClassName("touchable");
        Object.keys(elements).forEach(function (key) {
            var target = elements\[key\];
            target.addEventListener("MSPointerDown", onmsPointerDown, false);
            target.addEventListener("MSGestureChange", onmsGestureChange, false);

            var msGesture = new MSGesture();
            msGesture.target = target;
            msGestures\[target.uniqueID\] = msGesture;
        });

    }

    function onmsPointerDown(e) {
        msGestures\[e.target.uniqueID\].addPointer(e.pointerId);
    }

    function onmsGestureChange(e) {
        var matrix = new MSCSSMatrix(e.target.style.msTransform); 

        e.target.style.msTransform = matrix.
            translate(e.offsetX, e.offsetY).                             
            rotate(e.rotation \* 180 / Math.PI).                          
            scale(e.scale).                                                        
            translate(e.translationX, e.translationY).
            translate(-e.offsetX, -e.offsetY);

        e.stopPropagation();
    }

    WinJS.Namespace.define("Gestures", {
        init: initGestures
    });
})();

Hasta aquí esta entrada donde hemos visto cómo podemos utilizar los eventos de punteros y de gestos para aplicar transformaciones a cualquier elemento HTML.

Referencias
---

[Eventos de puntero y de gestos](http://msdn.microsoft.com/es-es/library/ie/hh673557(v=vs.85).aspx) 

