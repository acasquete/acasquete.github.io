---
title: HTML 5 vs Silverlight, una lucha desigual
tags: [personal]
---
Durante la preparación del examen de **Silverlight** he tropezado con un rumor que se está extendiendo rápidamente: el futuro incierto de Silverlight debido a la popularización de **HTML 5**. ¿Quiere decir esto que Microsoft piensa reemplazar a Silverlight? La verdad es que nunca hubiese dado más importancia a estos comentarios ya que el debate de si HTML 5 reemplazará o no a Silverlight, me parece un debate que no tiene razón de ser, al menos a día de hoy. Sin embargo, al hacer una [simple búsqueda en Google](http://www.google.com/search?q=html5+vs+silverlight) he podido ver la gran cantidad de ruido, e incluso preocupación, que ha generado este asunto, pero además, y esto es lo que me ha llevado definitivamente a escribir esta entrada, esta semana se me ha planteado esa misma cuestión en unos de los proyectos en los que estoy implicado: ¿Cambiarías Silverlight por HTML 5?

Tengo la sensación de que esta repentina preocupación, por lo menos en esta ocasión, viene provocada de alguna forma por los [comentarios](http://twitter.com/MossyBlog/status/23980240394) en Twitter de [Scott Barnes](http://twitter.com/MossyBlog), ex jefe de producto de Silverlight, en los que comentaba la [guerra abierta dentro de Microsoft](http://twitter.com/MossyBlog/status/23980976666) entre los favorables al desarrollo de HTML 5 contra los de Silverlight. Barnes llegaba a poner en duda, incluso, el futuro de WPF. Aunque desconozco si esa guerra existe realmente, voy a intentar exponer brevemente cuales son los motivos por los que creo que no es un debate oportuno y que, además, es muy injusto para HTML 5. Comencemos presentando a los aguerridos contrincantes.

HTML 5 se presenta como una plataforma para desarrollar aplicaciones web ricas, olvidémonos por lo tanto de asociar exclusivamente HTML 5 con la etiqueta `<video>` que tanto gusta enseñar en las presentaciones. HTML 5 permite, entre otras cosas, crear aplicaciones off-line, ejecución de scripts en paralelo, acceso a base de datos locales, geolocalización, etc. En la tabla que podéis ver a continuación he puesto algunas de estas características y el soporte que hay en las últimas versiones de los principales navegadores.

*Características de HTML 5 soportadas por los distintos navegadores*  
| Feature       | Chrome | IE9 Beta | FF 4 Beta 6 |
|---------------|:------:|:--------:|:----------:|
| Canvas        | X | X | X |
| Canvas Text   | X | X | X |
| Video  | X | X | X |
| Video Formats  | Ogg Theora H.264 WebM | H.264 | Ogg Theora WebM |
| Local Storage  | X | X | X |
| IndexedDB  | - | - | - |
| Web Workers  | X | - | X |
| Offline Web Applications  | X | - | X |
| GeoLocation  | X | - | X |
| Input types  | 13 de 13 | - | 4 de 13 |
| Placeholder Text  | X | - | X |
| Form Autofocus | X | - | X |
| Microdata | X | - | X |

[Silverlight](http://msdn.microsoft.com/es-es/library/bb404713(v=VS.95).aspx), como ya sabemos, es una realidad. Sin entrar en detalle: es un subconjunto del .NET Framework que nos permite crear aplicaciones ricas para web utilizando orientación a objetos y que pueden ser ejecutadas en distintos navegadores y sistemas operativos. Algunas características añadidas en la última versión son el soporte para webcam y micrófono, nuevas funciones de DRM, mejoras en la ejecución _out-of-browser_, etc. Además, se ha convertido en la plataforma de desarrollo para Windows Phone 7.

La comparación de las dos tecnologías es una lucha desigual, puesto que hoy en día, todos los navegadores tienen una implementación de HTML 5 en fase beta. No olvidemos tampoco que la especificación de HTML 5 no estará terminada en varios años. Según la [WHATWG]((http://wiki.whatwg.org/wiki/FAQ#When_will_HTML5_be_finished.3F), la _Candidate Recommendation_ estará disponible en 2012. Aunque esto no quiere decir nada, muy a pesar de lo que piensan los [detractores de HTML 5](http://ishtml5readyyet.com/), ya que lo importante no es cuando estará la recomendación final sino cuando vamos a poder utilizar las nuevas funcionalidades, y según vemos en la tabla anterior ya podemos utilizar muchas de ellas con los últimos navegadores. Sin embargo, creo que tendremos que esperar unos cuantos años más para ver desarrolladas completamente todas las demás. Si al final Microsoft apostase por HTML 5, un punto al que deberá dedicar grandes esfuerzos es a la creación de herramientas de desarrollo, que hasta el momento no han aparecido, ¿quizás un exportador de Silverlight a HTML 5?

En cuanto a Silverlight, parece casi evidente que su evolución hará mucho más difusa la separación entre WPF y Silverlight, y no parece descabellado pensar que en alguna próxima versión se fusionen, desaparezca WPF como tal, o incluso, como sugería Scott Barnes, Silverlight se convierta en el motor de renderizado de HTML 5. ¿Quién sabe? Lo que está claro es que Microsoft tiene mucho trabajo por delante para desarrollar ambas tecnologías, y no es de extrañar que surjan «facciones» en ambos bandos.

Nos esperan unos años en los que van a convivir las dos tecnologías. En algunos casos podremos sustituir Silverlight por HTML 5 pero no creo que HTML 5 nos proporcione, ni de lejos, la productividad y la funcionalidad con la que contamos actualmente. Pensemos que Silverlight tiene hoy más características de las que HTML 5 tiene previsto incluir, así que el debate no tiene que ser si HTML 5 reemplazará a Silverlight, sino en definir los límites de aplicación de HTML 5, definir en qué tipo de aplicaciones utilizaremos HTML 5 y en cuales Silverlight.

Enlaces relacionados
---
[HTML 5 and the Future of Silverlight](http://www.devproconnections.com/article/silverlight/HTML-5-and-the-Future-of-Silverlight.aspx)  
[Top 10 Reasons why HTML 5 is not ready to replace Silverlight](http://silverlighthack.com/post/2010/02/08/Top-Reasons-why-HTML-5-is-not-ready-to-replace-Silverlight.aspx)  
[Why HTML 5 Won’t Kill Flash or Silverlight](http://blog.iqinteractive.com/?p=338)  
[Microsoft wrestles with HTML5 vs Silverlight futures](http://www.itwriting.com/blog/3127-microsoft-wrestles-with-html5-vs-silverlight-futures.html) 
[Dive into HTML5](http://diveintohtml5.org/)  
[The HTML5 Test](http://html5test.com/)
