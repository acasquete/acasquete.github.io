---
title: Canvas colaborativo con Node.js, Socket.IO y Windows 8
tags: [programming, windows_store, nodejs]
reviewed: true
---
Una de las novedades más interesantes que incorpora IE10 es la implementación de la [API de WebSockets definida en la especificación del W3C](http://www.w3.org/TR/websockets/). Los **WebSockets** es una tecnología que nos proporciona un sistema de comunicación bidireccional para aplicaciones web y nos permite intercambiar información con un servidor web con una [latencia](http://es.wikipedia.org/wiki/Latencia) muy baja.

En esta entrada vamos a hacer uso de **WebSockets** para crear una aplicación para **Windows 8** que permita dibujar de forma colaborativa desde varios clientes. Utilizaremos el elemento **canvas de HTML5** para dibujar trazos y mediante **WebSockets** enviaremos la información de los puntos dibujados a nuestro servidor, que se encargará de distribuirlo a todos los clientes conectados.

Dibujando en el canvas
---

Comenzamos con lo básico: cómo dibujar en un elemento canvas. El código que viene a continuación es uno que ya he utilizado en alguna presentación y me permite demostrar que cualquier código JavaScript funciona en una aplicación para Windows 8. En el código se registra un controlador para los eventos **mousemove**, **mousedown** y **mouseup** y según el evento disparado iniciamos un nuevo trazo mediante el método  **beginPath** o dibujamos una línea con los métodos **lineTo** y **stroke**. Si queréis más información sobre estos métodos, podéis consultar la MSDN donde aparecen todos [los métodos disponibles del objeto canvas](http://msdn.microsoft.com/en-us/library/ie/hh826010(v=vs.85).aspx).

```js
var sketch = (function () { “use strict”;

    var context;
    var isPainting;
    
    var onMouseDown = function (event) {
        isPainting = true;
        context.beginPath();
    };
    
    var onMouseMove = function (event) {
      if (isPainting) {
          drawLine({ x: event.clientX, y: event.clientY });
      }   
    };
    
    var onMouseUp = function (event) {
        isPainting = false;
    };
           
    var drawLine = function (data) {
      context.lineTo(data.x, data.y);
      context.stroke();
    }
    
    return {
        init: function () {
            var canvas = document.getElementsByTagName('canvas')[0];
            context = canvas.getContext('2d');
            
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
                        
            context.strokeStyle = "green";
            context.lineJoin = "round";
            context.lineCap = "round";
            context.lineWidth = 15;
           
            canvas.addEventListener('mousemove', onMouseMove, false); 
            canvas.addEventListener('mousedown', onMouseDown, false);
            canvas.addEventListener('mouseup', onMouseUp, false);
        }
    } })();
```

Para probar este c&oacute;digo solo tenemos que crear una p&aacute;gina HTML que tenga la referencia al fichero de script anterior (*sketch.js*), un elemento canvas y una llamada al m&eacute;todo **sketch.init** en el controlador del evento onload.
    
```html
<!DOCTYPE html>
<html>
  <head>
    <script src="sketch.js"></script>
</head>
<body onload=”sketch.init()”>
  <canvas></canvas>
</body>
</html>
```

Servidor WebSockets
---

Una vez tenemos el pintado de trazos solucionado, el siguiente paso es montar el servidor de **WebSockets** que reciba los puntos enviados por cada uno de los clientes y los reenv&iacute;e al resto. El servidor de WebSockets se puede implementar con multitud de tecnolog&iacute;as. Yo he elegido **Node.js** con **Socket.IO** porque me parece de lo m&aacute;s sencillo de implementar y podremos publicarlo posteriormente en Azure. Adem&aacute;s, **Socket.IO** nos proporciona una API que tambi&eacute;n podemos utilizar desde el cliente con la ventaja que determina el mejor mecanismo de conexi&oacute;n, utilizando alternativas de transporte a WebSockets para los escenarios en los que no sea posible su uso. Si no conoc&eacute;is **Node.js** o **Socket.IO** pod&eacute;is encontrar en Internet multitud de tutoriales y gu&iacute;as, pero os recomiendo que comenc&eacute;is por la documentaci&oacute;n de las p&aacute;ginas de los productos: [Node.js](http://nodejs.org/) y [Socket.IO](http://socket.io/).
    
La implementaci&oacute;n b&aacute;sica del servidor es la que aparece a continuaci&oacute;n, en ella estamos indicando que al recibir un mensaje "draw" se reenv&iacute;e la informaci&oacute;n recibida a todos los clientes conectados. Esto lo conseguimos utilizando el m&eacute;todo **broadcast.emit**.
    
```js
var io = require('socket.io').listen(1380);

io.sockets.on('connection', function (socket) {
  socket.on('draw', function (data) {
    socket.broadcast.emit('draw', data);
  });
});
```

Para poner en marcha el servidor tenemos que ejecutar desde la l&iacute;nea de comandos:
    
```bash
node app.js
```

Canvas multiusuario
---    
    
El cliente tal y como lo tenemos planteado funciona perfectamente con un &uacute;nico usuario, pero antes de verlo en ejecuci&oacute;n podemos intuir que no funcionar&aacute; si queremos hacerlo multiusuario. El primer problema que nos encontramos es que en el canvas no podemos tener dos trazos iniciados a la vez, es decir, no podemos utilizar los m&eacute;todos **beginPath** y **stroke** en eventos distintos ya que el trazo no continuar&aacute; en la posici&oacute;n correcta si hay dos llamadas (mi movimiento y el de otro usuario) al m&eacute;todo **beginPath** y no obtendremos el resultado esperado. Por otro lado, el objeto canvas no nos permite tener dos instancias distintas del contexto, as&iacute; que la &uacute;nica soluci&oacute;n es mantener la &uacute;ltima posici&oacute;n del cursor de todos los clientes y recuperarla cuando queramos volver a pintar una l&iacute;nea. Vamos a hacer a continuaci&oacute;n los cambios necesarios en el c&oacute;digo.
    
Necesitamos crear un array (*clients*) y un m&eacute;todo (*setPosition*) que llamaremos en los m&eacute;todos **onMouseDown** y **onMouseMove**. Est&eacute; m&eacute;todo se encargar&aacute; de guardar la posici&oacute;n del puntero (que se pasa por argumentos) por cada uno de los clientes. Para identificar a cada cliente utilizamos un identificador &uacute;nico que se almacena en la variable **selfID**. De momento esta variable tiene un valor fijo, despu&eacute;s veremos c&oacute;mo asignarle uno para cada cliente. El otro cambio a realizar est&aacute; en el m&eacute;todo **drawLine**, al que tambi&eacute;n le tenemos que pasar el identificador. Este m&eacute;todo se encarga ahora de iniciar el trazo y, en el caso de que exista una posici&oacute;n guardada para el ID de cliente, de mover el cursor a esa posici&oacute;n mediante el m&eacute;todo **moveTo**. Ahora mismo no ser&iacute;a necesario pasar el identificador en estos m&eacute;todos, pero como vamos a utilizarlos tambi&eacute;n para pintar las posiciones de los otros clientes, me adelanto y me evito la refactorizaci&oacute;n posterior.
    
El c&oacute;digo siguiente muestra todos los cambios realizados.
    
```js
var sketch = (function () {
    "use strict";
    var context;
    var isPainting;
    var clients =  [];
    var selfID = "self";
   
    var onMouseDown = function (e) {
        isPainting = true;
        setPosition(selfID, {x: e.clientX, y: e.clientY, action: "down" });
    };
    
    var onMouseMove = function (e) {
      if (isPainting) {
        var data = {x: e.clientX, y: e.clientY, action: "move" };
        drawLine(selfID, data);
        setPosition (selfID, data);
      }
    };
    
    var onMouseUp = function (e) {
        isPainting= false;
    };
           
    var drawLine = function (id, data) {
      context.beginPath();
      
      if (clients [id ]) {
        context.moveTo(clients [id ].lastx, clients [id ].lasty);
      }
      
      context.lineTo(data.x, data.y);
      context.stroke();  
    };
    
    var setPosition = function (id, data) {
      clients [id ].lastx=data.x;
      clients [id ].lasty=data.y;
    };

    return {
        init: function () {
            var canvas = document.getElementsByTagName('canvas') [0 ];
            context = canvas.getContext('2d');
            
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
                        
            selfColor = "green";
            context.lineJoin = "round";
            context.lineCap = "round";
            context.lineWidth = 15;
           
            canvas.addEventListener('mousemove', onMouseMove, false); 
            canvas.addEventListener('mousedown', onMouseDown, false);
            canvas.addEventListener('mouseup', onMouseUp, false);
            });
            
        }
    }
})();
```

Conectando con el servidor
---    
 
Vamos a establecer ahora la conexi&oacute;n desde el cliente. Para hacerlo, primero necesitamos a&ntilde;adir la referencia al script **socket.io.js** en la p&aacute;gina HTML.
    
```html
<script src="http://localhost:1380/socket.io/socket.io.js"></script>
```

Tambi&eacute;n podemos incluir nosotros el fichero js u obtenerlo del CDN.
    
```html
<script src="http://cdn.socket.io/stable/socket.io.js"></script>
```

Adem&aacute;s de establecer la conexi&oacute;n con el servidor, necesitamos solventar otros problemas. Como hemos dicho antes, necesitamos tener una lista de identificadores de los clientes para poder mantener la posici&oacute;n del cursor para cada uno. As&iacute; que, al establecer la conexi&oacute;n con el servidor, vamos a solicitar que el usuario introduzca un ID (por ejemplo, un nombre de usuario). Este ID se enviar&aacute; al servidor con el mensaje 'addclient' y el servidor al recibirlo enviar&aacute; otro indicando que la lista de clientes se ha modificado. As&iacute; cada cliente tendr&aacute; una lista actualizada de todos los identificadores.
    
```js
socket = io.connect('http://127.0.0.1:1380');
socket.on('connect', function () {
  selfID = prompt("Your ID?");
  socket.emit('addclient', selfID);
  socket.on('updateclients', onUpdateClients);             
  socket.on('draw', onPaint);
});
```

Es evidente que a este c&oacute;digo le falta la comprobaci&oacute;n para asegurarnos de que el ID sea &uacute;nico, aunque tambi&eacute;n podr&iacute;amos generar un GUID como identificador. De momento, lo dejaremos as&iacute;.  
    
Tambi&eacute;n tenemos que modificar el m&eacute;todo **setPosition** para enviar al servidor la posici&oacute;n del cursor cada vez que se pulsa un bot&oacute;n del rat&oacute;n o se mueve mientras se mantiene pulsado.
    
```js
var setPosition = function (id, data) {
  clients [id ].lastx=data.x;
  clients [id ].lasty=data.y;
  
  if (id != selfID) return; 
  
  socket.emit("draw", data);
};
```

Veamos las modificaci&oacute;n que tenemos que realizar en la parte del servidor para procesar el mensaje "addclient".
    
```js
var io = require('socket.io').listen(1380)

var clients = {};

io.sockets.on('connection', function (socket) {
  
 socket.on('addclient', function(id){
  socket.username = id;
  clients [id ] = id;
  io.sockets.emit('updateclients', clients);
  socket.broadcast.emit('updateclients', clients);
 });
  
  socket.on('draw', function (data) {
    socket.broadcast.emit('draw', socket.username, data);
  });

  socket.on('disconnect', function() {
    delete clients [socket.username ];
  });  
});
```

Vemos que en el servidor tambi&eacute;n tenemos que mantener una lista de ID de clientes que es la que se env&iacute;a (a todos los clientes) cuando se recibe un mensaje "addclient". Tambi&eacute;n establecemos la propiedad "username" del socket para poder eliminarlo de la lista cuando se desconecte y para enviarlo en el mensaje 'draw'.
    
    
A continuaci&oacute;n est&aacute; la implementaci&oacute;n de los m&eacute;todos que responden a los eventos 'updateclients' y 'draw'. En el primero (**onUpdateClients**) &uacute;nicamente se inicializa la posici&oacute;n del array de clientes y establecemos el valor a cero de las propiedades lastx y lasty, donde se guardan las coordenadas del cursor.
    
```js
var onUpdateClients = function(ids) {  
  for (var id in ids)
  {
    if (!clients [id ]) {
      clients [id ] = { lastx: 0, lasty: 0 };
    }
  }
};
```

Y en el segundo (**onPaint**) dibujamos la l&iacute;nea llamando a **drawLine** cuando la acci&oacute;n realizada es un movimiento (cuando el valor de action es *move*). Si solo se ha pulsado un bot&oacute;n del rat&oacute;n (*action == down*), &uacute;nicamente tenemos que establecer la posici&oacute;n.
    
var onPaint = function (id, data) {
  if (data.action === "move") {
    drawLine(id, data);
  }
  setPosition (id, data);
};

Finalizando, de momento...
---    
    
Con todo lo anterior ya tenemos todo lo necesario para poner en marcha la aplicaci&oacute;n. Si ejecutamos la p&aacute;gina desde varios navegadores o varias pesta&ntilde;as veremos c&oacute;mo podemos pintar sobre el lienzo y que cada trazo se pinta en cada uno de los clientes conectados. &iexcl;No est&aacute; mal! Pero esto es solo el principio, la verdad que pintar en un color o con un solo grosor tiene poca gracia. Adem&aacute;s los clientes solo ven el dibujo desde el momento que se conectan, no desde que se conect&oacute; el primero. Y... &iquest;qu&eacute; pasar&aacute; cuando tengamos 10 usuarios conectados? &iquest;Y 100? &iquest;Y 10000? Todo esto lo veremos en pr&oacute;ximas entradas.
    
### Pero... &iquest;y Windows 8?
 
Pues s&iacute;, he dicho que era una aplicaci&oacute;n para **Windows 8**, pero de momento ni rastro de &eacute;l. Todo lo que hemos visto hasta ahora funciona en cualquier navegador web que soporte WebSockets. Lo bueno de esto es que si funciona en IE10, significa que todo el c&oacute;digo de cliente lo podemos trasladar a una aplicaci&oacute;n para Windows 8 (*Windows Store App*) y funcionar&aacute; de la misma forma. Sin embargo, tenemos que tener en cuenta ciertos aspectos que s&oacute;lo nos encontramos en las aplicaciones de Windows 8.
    
Para comenzar con nuesta aplicaci&oacute;n Windows 8, creamos un nuevo proyecto de aplicaci&oacute;n Windows Store con JavaScript utilizando la plantilla en blanco. Una vez generado, a&ntilde;adimos el fichero **sketch.js** en la carpeta **js** y realizamos la llamada m&eacute;todo **sketch.init** en el controlador del evento **onactivated** que lo podemos encontrar en el fichero *default.js*
    
```js
app.onactivated = function (args) {
    if (args.detail.kind === activation.ActivationKind.launch) {
        if (args.detail.previousExecutionState !== activation.ApplicationExecutionState.terminated) {
            // TODO: This application has been newly launched. Initialize
            // your application here.
        } else {
            // TODO: This application has been reactivated from suspension.
            // Restore application state here.
        }
        args.setPromise(WinJS.UI.processAll());
        sketch.init();
    }
};
```

Por supuesto, tampoco tenemos que olvidar agregar el elemento canvas y la referencia al script en la p&aacute;gina default.htm. 
    
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>GangCanvas</title>

    <!-- WinJS references -->
    <link href="//Microsoft.WinJS.1.0/css/ui-light.css" rel="stylesheet" />
    <script src="//Microsoft.WinJS.1.0/js/base.js"></script>
    <script src="//Microsoft.WinJS.1.0/js/ui.js"></script>

    <!-- GangCanvas references -->
    <link href="/css/default.css" rel="stylesheet" />
    <script src="/js/socket.io.js"></script>
    <script src="/js/sketch.js"></script>
    <script src="/js/default.js"></script>

</head>
<body>
    <canvas></canvas>
</body>
</html>
```

Aqu&iacute; es donde nos encontramos la primera diferencia respecto a la p&aacute;gina que ejecutabamos con IE10. Si agregamos la referencia a http://localhost:1380/socket.io/socket.io.js y ejecutamos la aplicaci&oacute;n obtendremos el mensaje siguiente: &laquo;No se puede cargar &lt;http://localhost:1380/socket.io/socket.io.js&gt;. Una aplicaci&oacute;n no puede cargar contenido web remoto en el contexto local.&raquo; Esto es debido a que la p&aacute;gina default.html se ejecuta en el contexto local y en este contexto no pueden haber referencias a scripts externas. Puedes consultar la MSDN para conocer m&aacute;s sobre las [caracter&iacute;sticas y restricciones por contexto](MSDNhttp://msdn.microsoft.com/es-es/library/windows/apps/hh465373.aspx). Para salvar esta restricci&oacute;n tenemos que incluir el fichero socket.io.js en el directorio js. y podremos ejecutar la aplicaci&oacute;n sin problema.
    
El &uacute;ltimo cambio que tenemos que hacer es sustituir la llamada a la funci&oacute;n prompt para solicitar el identificador de usuario. En las aplicaciones Metro con JavaScript no se pueden utilizar los m&eacute;todos alert, confirm ni prompt ya que son m&eacute;todo que bloquean la interfaz de usuario. En su lugar lo vamos a sustituir por el nombre del usuario que ha iniciado sesi&oacute;n. 
    
```js
socket.on('connect', function () {
    Windows.System.UserProfile.UserInformation.getDisplayNameAsync().done(function (result) {
        if (result) {
            selfID = result;
        } else {
            selfID = (Math.random() * 10000) >> 0;
        }

        socket.emit('addclient', selfID);
        socket.on('updateclients', onUpdateClients);
        socket.on('draw', onPaint);
    });
});
```

Si no se pudisese obtener el nombre del usuario se utilizaría un número aleatorio.

Conclusiones
---

En esta entrada hemos visto cómo dibujar trazos en un elemento canvas y enviar la información a un servidor de websockets creado con Node.js y Socket.IO para permitir dibujar sobre el mismo canvas desde distintos dispositivos. Por último hemos visto como aprovechar todo el código JavaScript para crear una aplicación para la Windows Store realizando unos sencillos cambios debido a varias restricciones del entorno de ejecución.
