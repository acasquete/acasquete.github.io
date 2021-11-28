---
title: Cambiar el valor a un TextBox con atributo de solo lectura
tags: []
---
De la misma forma que podemos [asignar un valor a un TextBox en modo password](/asignar-el-valor-a-un-textbox-en-modo-password), también podemos hacer que no podamos modificar el contenido de un _TextBox_, pero si que se pueda cambiar mediante _script_. El ejemplo claro es si tenemos una página en la que el valor de un _TextBox_ (que está configurado como solo lectura) se calcula a partir de otro. Si utilizamos la propiedad _Readonly_ del control, cuando la página realice un _postback_ no vamos a tener este valor en servidor, ya que .NET lo impide.

Una alternativa es añadir el atributo _readonly_, de esta forma mantenemos la misma funcionalidad en cliente y además tendremos en servidor el valor que se haya asignado en cliente. El código necesario es este:

txtReadOnly.Attributes.Add(“readonly”, “readonly”);

