---
title: Gamepad táctil para Windows Store Apps con Javascript e Internet Explorer 10
tags: [windows_store, winjs]
reviewed: true
---
En los dispositivos táctiles, el ratón y el teclado han dejado de ser los principales dispositivos controladores de videojuegos. Ahora, para controlar el movimiento de un personaje solo podemos interactuar con la pantalla y el típico control con las teclas del cursor ha sido sustituido, en muchas ocasiones, por un _gamepad_ o control táctil, emulando a los tradicionales que utilizamos en las consolas de videojuegos.

En esta entrada vamos a ver cómo implementar un control _gamepad_ táctil utilizando JavaScript para poder integrarlo en juegos desarrollados para **Internet Explorer 10** y para **aplicaciones para la Windows Store**. El ejemplo que voy a mostrar está hecho desde cero, pero está basado en una demo del gran [Seb Lee-Delisle](https://twitter.com/seb_ly) de hace ya un tiempo, y que he decidido actualizar ya que no era compatible con los nuevos eventos táctiles incorporados en Internet Explorer 10.

Comenzamos por el lienzo
------------------------

Como en la mayoría de juegos, toda la interacción y el dibujado del juego lo realizaremos en un elemento **canvas** que se mostrará a pantalla completa, así que este es el único elemento que tendremos que declarar en el HTML.

Lo que queremos conseguir es que cuando pulsemos sobre cualquier punto de este canvas, aparezca el control _(_que para nuestra humilde demostración nos conformaremos con que sea una simple circunferencia) y al movernos sobre ella nos aparezca una segunda circunferencia, simulando la palanca de un _gamepad_ estándar. A partir de los puntos inicial y final, podremos obtener un vector que nos dará la dirección, el sentido y la distancia entre ellos. Más tarde podremos aplicar este vector a cualquier otro objeto de la pantalla para dotarlo de movimiento.

Con el elemento canvas declarado en el HTML, creamos el siguiente objeto que se encargará de inicializarlo, de momento solo tenemos que ajustarlo al tamaño de la pantalla.

```js
var game = (function () {

        "use strict";
    
        var gameCanvas, gamepad, context;
    
        var initCanvas = function () {
          gameCanvas = document.getElementById("canvas");
          context = canvas.getContext( '2d' );
          resetCanvas();
        };
    
        var resetCanvas = function () {  
          canvas.width = window.innerWidth; 
          canvas.height = window.innerHeight;
        };
    
        var initGame = function () {
          initCanvas();
        };
    
        return {
          init: initGame
        };
    })();
```

Aunque por ahora el objeto **game** solo se encarga de redimensionar el canvas, más adelante le daremos otra responsabilidad, la de coordinar y dibujar todos los objetos visibles en pantalla. Si nos fijamos, he declarado la variable Ga*mepad*, que utilizaremos para guardar una instancia del objeto encargado de dibujar el controlador y definirá su comportamiento. Pero no nos adelantemos, todo llegará a su debido tiempo...
        
## Los vectores y el *Gamepad*

Para poder obtener un vector que nos proporcione la dirección, el sentido y la distancia, necesitamos guardar la posición de los 2 puntos del canvas, la posición inicial donde se ha pulsado, y la posición actual del puntero. Para guardar está información nos vamos a apoyar en la siguiente implementación del objeto **vector**.

```js
var vector = (function () {
        "use strict";
    
        var x, y; 
    
        var vector = function (x, y) {
          this.x = x || 0;
          this.y = y || 0;
        };
    
        var reset = function (x, y) {
          this.x = x;
          this.y = y;
    
          return this;
        };
    
        var copyFrom = function (v) {
          this.x = v.x;
          this.y = v.y;
    
          return this;
        };
    
        var minus = function (v) {
          this.x -= v.x;
          this.y -= v.y;
    
          return this;
        };
    
        vector.prototype = {
            constructor: vector,
            reset: reset,
            copyFrom: copyFrom,
            minus: minus
        };
    
        return vector;
    })();
```

Este objeto, además de permitirnos guardar las coordenadas X e Y de un punto, nos permite establecer nuevos valores mediante la función *reset*, copiar los valores de otro vector (mediante *copyFrom)* y calcular la resta entre dos vectores mediante la función *minus*.
    
Además de estos sencillos cálculos iniciales, el objeto **vector **encapsulará todos los cálculos que tengamos que realizar más adelante con los vectores para aplicarlos a otros objetos.
    
Y llegamos a la implementación del objeto **gamePad**... Como he comentado antes, este objeto guardará los 3 vectores de posición (inicial, final y de diferencia), pero además, será el responsable de responder a los eventos táctiles sobre el canvas y de dibujar las dos circunferencias. Echemos un vistazo al esqueleto inicial del código.

```js
var gamePad = (function () {
    
      "use strict";
    
      var cnvs, ctx, startVector, currentVector, diffVector, isDown;
    
      var gamePad = function (canvas, context) {
        cnvs = canvas;
        ctx = context;
        startVector = new vector();
        currentVector = new vector();
        diffVector = new vector();
        isDown = false;
      };
    
      var init = function () {
        cnvs.addEventListener( 'MSPointerDown', onMSPointerDown, false );
        cnvs.addEventListener( 'MSPointerMove', onMSPointerMove, false );
        cnvs.addEventListener( 'MSPointerUp', onMSPointerUp, false );
      };
    
      var onMSPointerDown = function (e) {
        /// ... 
      };
    
      var onMSPointerMove = function (e) {
        /// ...
      };
    
      var onMSPointerUp = function (e) { 
        /// ...
      };
    
      var draw = function () {
        /// ...
      };
    
      gamePad.prototype = {
        constructor: gamePad,
        init: init
      };
    
      return gamePad;
    })();
```

Como vemos, estamos utilizando manejadores para los nuevos eventos de puntero de Internet Explorer 10: **MSPointerDown**, **MSPointerMove** y **MSPointerUp**. Estos eventos nos permiten controlar mediante un mismo código todos los puntos de contacto en la pantalla, independientemente de si ha sido provocado por el mouse, un lápiz o un dedo tocando la pantalla. **Esto nos evita que tengamos que crear código para controlar por separado cada dispositivo de entrada**.
    
El código en cada uno de estos eventos no tiene ninguna complejidad, simplemente tenemos que ir estableciendo o actualizando la posición del puntero en los distintos vectors a partir de las propieades clientX y clientY.

```js    
function onMSPointerDown(e) {
        startVector.reset(e.clientX, e.clientY); 
        currentVector.copyFrom(startVector); 
        isDown=true;
    }
    
    var onMSPointerMove = function (e) {
      if (isDown) {
          currentVector.reset(e.clientX, e.clientY); 
    
          diffVector = diffVector.copyFrom(currentVector);
          diffVector.minus(startVector);
      }
    };
    
    var onMSPointerUp = function (e) { 
      isDown=false; 
    };
```

En **onMSPointerDown** establecemos la misma posición en el vector inicial y en actual. Además, establecemos a **true** el valor de a propiedad *isDown* que nos permite saber si seguimos manteniendo un punto de contacto presionado. En el método **onMSPointerMove** solo actualizamos los valores en el vector *currentVector* y calculamos el vector resta que se obtiene restando los componentes de *currentVector* de *startVector*. Por último, en el método **onMSPointerUp** restablecemos el valor de la propiedad *isDown*para indicar que ya no hay puntos de contacto. Con todo esto, tenemos toda la funcionalidad que necesitamos implementada, pero todavía no hemos dibujado nada en el canvas. Veamos cómo hacerlo.
     
## Dibujando en el canvas
    
En el método **draw **dibujamos la dos circunferencias solo si existe algún punto de contacto (*isDown=true*). Además mostramos los valores X e Y del vector resta.
    
```js
var draw = function () {
      if (isDown) {
        ctx.beginPath(); 
        ctx.strokeStyle = "green"; 
        ctx.lineWidth = 6; 
        ctx.arc(startVector.x, startVector.y, 40, 0, Math.PI*2, true); 
        ctx.stroke();
        ctx.beginPath(); 
        ctx.strokeStyle = "blue"; 
        ctx.lineWidth = 4; 
        ctx.arc(currentVector.x, currentVector.y, 30, 0, Math.PI*2, true); 
        ctx.stroke(); 
    
        ctx.fillStyle = "white";
        ctx.fillText("Diff Vector x: "+diffVector.x+" y:"+diffVector.y, currentVector.x - 45, currentVector.y-40); 
      }
    };
```

Aunque el objeto **gamepad** está dibujando en el contexto del canvas, no vamos a definir aquí el bucle de pintado, si no que lo vamos a crear en el objeto **game** que hemos creado anteriormente. Así que por un lado, tenemos que crear una nueva instancia de **gamePad** a la que le pasaremos el canvas y el contexto, y por otro lado registraremos la función **gameLoop** para el dibujado de pantalla llamando a **requestAnimationFrame**. En la función gameLoop unicamente limpiamos el canvas y llamamos al método **draw** del objeto **gamepad**.

```js
var gameLoop = function () {
      context.clearRect(0,0,canvas.width, canvas.height); 
      gamepad.draw();
    
      requestAnimationFrame(gameLoop);
    }
    
    var initGame = function () {
      initCanvas();
      gamepad = new gamePad(gameCanvas, context);
      gamepad.init();
    
      requestAnimationFrame(gameLoop);
    };
```
 
## El truco final
        
Para terminar el post, vamos a añadir una pequeña mejora al movimiento del controlador y aprovechamos para hacer un repaso a las matemáticas.
    
Ahora, una vez pulsamos sobre el canvas y se muestra el gamepad, tenemos libertad de movimiento sobre toda la pantalla, con lo que podemos obtener vectores con una magnitud muy grande. Para simular un funcionamiento más parecido a los gamepads reales, vamos a limitar el radio de movimiento de la circunferencia pequeña al tamaño de la circunferencia grande. De esta forma, la pequeña nunca podrá sobrepasar los límites de la grande.
    
Lo primero que tenemos que hacer en cada movimiento del puntero es comprobar si las coordenadas están dentro de la circunferencia grande. Para saber esto, tenemos que calcular la magnitud del vector *diffVector *que, recuerdo para los más olvidadizos, se obtiene **calculando la raíz cuadrada de la suma de los cuadrados de cada componente del vector**.

```js    
var magnitude = function () {
      return Math.sqrt((this.x*this.x)+(this.y*this.y));
    }
```

Si esta magnitud es superior al radio de la circunferencia (en este caso está establecido en 40), significa que estamos fuera de ella y no podemos movernos a esa posición. En este caso, tenemos que calcular la posición máxima, que obtenemos a partir del ángulo que estamos formando en la posición actual y el radio máximo. El ángulo en un punto determinado se obtiene calculando la arcotangente.

```js
var angle = function () {
      return  Math.atan2(this.y, this.x);
    }
```

Y ahora que ya tenemos las coordenadas polares (el ángulo y el radio), podemos calcular fácilmente las coordenadas rectangulares, multiplicando el seno y el coseno del ángulo por el radio máximo.

```js
var rect = function (radius) {
      var angle = this.angle();
    
      this.x = Math.cos(angle) * radius;
      this.y = Math.sin(angle) * radius;
    
      return this;
    };
```

Trigonometry rocks!!! Este será el vector máximo dado un determinado ángulo y radio. Con todo esto claro, podemos modificar el código del evento **onMSPointerMove **de la siguiente forma para incorporar los límites de movimiento.

```js
var onMSPointerMove = function (e) {
      if (isDown) {
          var radius = 40;
    
          currentVector.reset(e.clientX, e.clientY); 
          diffVector = diffVector.copyFrom(currentVector);
          diffVector.minus(startVector);
    
          if (diffVector.magnitude() &gt; radius) {
            diffVector.rect(radius);
            currentVector.copyFrom(startVector)
                         .sum(diffVector);
          }
      }
    };
```

Y hasta aquí llegamos por el momento. En próximas entradas seguiremos añadiendo elementos a este juego y con un poco de suerte algún día lo veremos publicado en la Store.

Referencias
---

[Multi-touch game controller in JavaScript/HTML5 for iPad](http://seb.ly/2011/04/multi-touch-game-controller-in-javascripthtml5-for-ipad/)  
[El método requestAnimationFrame](http://msdn.microsoft.com/es-es/library/ie/hh920765(v=vs.85).aspx)
