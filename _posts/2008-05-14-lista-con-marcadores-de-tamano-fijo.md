---
title: Lista con marcadores de tamaño fijo
tags: []
---
La mayor parte de las preguntas que me llegan son sobre todo problemas relacionados con maquetación con CSS y HTML (aún no sé muy bien porqué). Algunas veces encuentro la respuesta y muchas otras no… Para comenzar con mi primera entrada he elegido una de estas dudas, la más insólita que me han hecho en mucho tiempo: ¿cómo hacer una lista (utilizando el _tag_ UL) de forma que el marcador no cambie de tamaño al modificar la configuración del tamaño de fuente del Explorer? Bueno, dicho así parece como si escribiese en chino, mejor voy a explicarlo con un ejemplo.

Lo primero que necesitamos es crear una lista desordenada, una simple y sencilla lista como esta:

*   Primero
*   Segundo
*   Tercero

</pre> Bien, una vez tenemos la lista y utilizando Internet Explorer tenemos que modificar el tamaño de fuente de la página mediante la opción «Tamaño de texto» del menú «Página». ¿Qué es lo que sucede? Pues que el marcador o _bullet_ cambia de tamaño aunque la fuente este definida con un tamaño fijo.

Como resolver este «grave problema» del Explorer, que para un mortal pasaría desapercibido, era imprescindible, me puse a buscar una solución…

Mi primera idea fue utilizar una imagen como marcador, pero en la aplicación donde se estaba dando el problema no se podían utilizar imágenes ya que el color del marcador debía ser personalizable por el usuario y no podíamos debíamos hacer tantas imágenes como colores. Sin más imaginación de la que echar mano, me puse a _googlear_ un poco, y encontré la solución: [entidades de carácter HTML](https://web.archive.org/web/20210123141012/http://html.conclase.net/w3c/html401-es/sgml/entities.html). Lo que hice fue añadir un elemento SPAN antes del elemento LI con la entidad HTML que quería utilizar, en este caso el clásico marcador redondo (&bull;). El código HTML final quedó más o menos así:

\*   &bull;Primero
\*   &bull;Segundo
\*   &bull;Tercero

Después apliqué varios estilos CSS para que la apariencia fuese lo más parecida a la de la lista estándar.

UL.fixed { 
   list-style-type: none; 
   margin-left: 25px; 
}

UL.fixed SPAN { 
   color: #000; 
   margin: auto 5px -2px auto; 
   float: left; 
   clear: left; 
} 



Ahora sí, objetivo conseguido. Tenemos una lista en la que el tamaño de los marcadores no se ve afectado por la configuración de fuente de Internet Explorer. El único inconveniente que encuentro a esta solución es que el código HTML no valida correctamente ya que el elemento UL no permite otro contenido que no sea un elemento LI.

