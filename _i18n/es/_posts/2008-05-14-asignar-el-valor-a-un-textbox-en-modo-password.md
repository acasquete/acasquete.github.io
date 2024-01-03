---
title: Asignar el valor a un TextBox en modo password
tags: [programming]
reviewed: true
---
Si intentamos asignar desde servidor un valor a un control _TextBox_ que está configurado en modo _password_, .NET lo ignora y no envía el contenido en la respuesta de la página, lo que provoca que el control se muestre vacío.

Para evitar esto, la solución más sencilla es asignar el valor añadiendo el atributo _value_ a la colección de atributos del control:

```vb
txtPassword.Attributes.Add(“value”, “contraseña”);
```
