---
title: Crear texto vertical con CSS y SVG
tags: []
---
Ya me había encontrado en muchas ocasiones con el problema de rotar una cadena de texto en una página web. Normalmente salía del paso creando una imagen con el texto girado, y si el texto tenía que ser dinámico (por ejemplo, en una aplicación multi-idioma), utilizaba un objeto _Flash_ al que pasaba en un parámetro la cadena de texto. Nunca me había puesto a pensar en como resolver este problema de otra forma, hasta hoy…

En esta entrada veremos las diferentes opciones que tenemos para poder rotar texto en los diferentes navegadores, léase Explorer (en las versiones 6, 7 y 8), Firefox, Chrome, Safari y Opera. Más correcto sería decir que vamos a ver dos formas, como casi siempre: una para Explorer y otra para todos los demás.

La forma de rotar un texto en IE mediante CSS es utilizando la propiedad _writing-mode_ de la siguiente forma:

Vertical

</pre> Con esto obtenemos un texto vertical orientado hacia la izquierda, si lo que queremos es rotarlo en la posición contraria tenemos que utilizar los [filtros](http://msdn.microsoft.com/en-us/library/ms532847(VS.85).aspx) que Microsoft introdujo allá por el año 97. En este caso utilizamos los filtros para voltear el texto en los dos ejes.

Vertical

Para rotar texto en el resto de navegadores tenemos que recurrir a los gráficos [SVG (Scalable Vector Graphics)](http://www.w3.org/Graphics/SVG/), un lenguaje para definir gráficos en aplicaciones XML. En el siguiente ejemplo creamos una etiqueta de texto a la que aplicamos una transformación de rotación:

 Vertical 

Como Internet Explorer es el único navegador que no implementa SVG de forma nativa, si queremos hacer, por ejemplo una tabla que contenga una etiqueta vertical, y que sea visible en todos los navegadores, tenemos que utilizar los [comentarios condicionales](http://msdn.microsoft.com/en-us/library/ms537512.aspx), otro gran invento de Microsoft. En el siguiente código tenemos un ejemplo de como hacerlo.

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>Tabla con etiqueta vertical 
<style>
  body { font-family: Arial; }
  html>body .ie\_vert { display: none; }
  html>body .ff\_vert { display: block; }
  .ie\_vert, .ff\_vert { height:80px; width: 25px; font-size: 20px; }
</style> 
<!\[if IE\]> 
<style> 
  .ff\_vert { display: none }
  .ie\_vert { writing-mode: tb-rl; filter: flipv fliph; display: block;  }
</style> 
<!\[endif\]> 
</head> 
<body> 
  <table border="1" width="320px" style="text-align:center;" >
    <caption>\*Una tabla de ejemplo con etiqueta vertical\*</caption>
    <tr>
      <th></th>
      <th>Columna #1</th>
      <th>Columna #2</th>
    </tr>
    <tr>
      <th>
        <div class="ie\_vert">Fila #1</div> 
        <!\[if !IE\]> 
        <object class="ff\_vert" type="image/svg+xml" data="data:image/svg+xml, 
         <svg xmlns='http://www.w3.org/2000/svg'>
        <text x='-70' y='20' font-weight='bold' font-family='Arial' font-size='20px' transform='rotate(270)'>Fila #1</text>
        </svg>"> 
        </object> 
        <!\[endif\]>
      </th>
      <td>-</td>
      <td>-</td>
    </tr>
  </table>
</body> 
</html>
```
