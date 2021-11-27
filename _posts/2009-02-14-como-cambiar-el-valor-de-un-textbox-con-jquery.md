---
title: ¿Cómo cambiar el valor de un TextBox con jQuery?
tags: []
---
Analizando los registros de visitas, veo que esta es una de las _searchphrases_ que provocan más entradas nuevas en el blog. Lo curioso de esto, es que no hay —hasta hoy— ninguna entrada que trate este tema. Ante semejante situación, he decidido actuar y continuar con una serie de micro-entradas publicadas en 15 segundos, en las que intentaré responder a las consultas más recurrentes.

Comenzamos con una pregunta que parece, por su repetición, un gran misterio, pero que tiene una sencilla solución: leer la [documentación](http://docs.jquery.com/).

Para asignar un valor a un campo de texto con _jQuery_, tenemos que utilizar la función _val_. El siguiente código de ejemplo, asignamos el valor _nuevovalor_ a un campo de texto con el ID _mitexto_.

$(‘#mitexto’).val(‘nuevovalor’);

Sencillo, ¿no? Toda la información sobre el uso de _jQuery_ y de esta función en [http://docs.jquery.com/Attributes/val](http://docs.jquery.com/Attributes/val)

