---
title: Cerrar ventana sin mensaje de confirmación
tags: [programming]
reviewed: true
---
Si intentamos cerrar la ventana principal del navegador mediante Javascript utilizando un simple _window.close()_, Internet Explorer muestra un mensaje de confirmación. Para evitar este mensaje debemos utilizar el siguiente código:

```js
window.open(‘’,’\_parent’,’’); window.close();
```

Esta solución funciona en IE6 y en IE7. En Chrome no es necesario realizar ninguna acción especial ya que nunca se solicita confirmación al cerrar la ventana.

