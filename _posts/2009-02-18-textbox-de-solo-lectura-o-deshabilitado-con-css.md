---
title: TextBox de sólo lectura o deshabilitado con CSS
tags: [programming]
reviewed: true
---
De nuevo nos encontramos ante una pregunta muy frecuente entre los nuevos programadores web y más aún entre los nuevos visitantes del blog. La respuesta es muy clara: **NO** se puede crear un _TextBox_ de sólo lectura o deshabilitado mediante CSS; estas características son propiedades del control, no estilos.

Lo que sí que se puede hacer, es aplicar un estilo concreto a los _TextBox_ que tienen la propiedad _disabled_ o _readonly_ activada. Esto lo vemos en el siguiente ejemplo, en el que asignamos un color de fuente y fondo a los controles deshabilitados y de sólo lectura:

```css
[disabled] { 
    background-color:#0c0; 
    color:#fff; 
} 

[readonly] { 
    background-color:#00c; 
    color:#fff; 
}
```

Con este código cualquier control que tenga la propiedad _disabled_ activada aparecerá con el color de fondo en verde y los que tengan la propiedad _readonly_ lo tendrán de color azul. Eso sí, en cualquier navegador menos en Internet Explorer.

Para terminar, si lo que queremos es deshabilitar un control programáticamente, tendremos que recurrir a Javascript. Los siguientes fragmentos de código asignan a dos controles HTML que tienen los identificadores _inputtext1_ y _inputext2_ las propiedades _disabled_ y _readonly_ respectivamente.

```js
document.getElementById('inputtext1').disabled = true;
document.getElementById('inputtext2').readOnly = true;
```

o utilizando jQuery:

```js
$('#inputtext1').attr('disabled', true); 
$('#inputtext2').attr('readonly', true);
```
