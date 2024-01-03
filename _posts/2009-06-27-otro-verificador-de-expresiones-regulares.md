---
title: Otro verificador de expresiones regulares
tags: [programming]
reviewed: true
---
Existen infinidad de validadores o verificadores de expresiones regulares, pero no he encontrado ninguno _online_ que evalúe la expresión conforme se va escribiendo. Así que he dedicado un par de horas a realizar otro verificador de expresiones regulares, y como no podía ser de otra forma, lo he hecho en Silverlight.

Como se puede comprobar, el funcionamiento es muy simple: hay 3 campos de texto donde podemos escribir la expresión regular a verificar (indicando si distingue o no mayúsculas de minúsculas), una cadena de texto de prueba y otra cadena de texto que se utilizará para reemplazar las coincidencias. Al ir escribiendo en cualquiera de los tres campos se evalúa la expresión regular y se muestra el número de coincidencias encontradas y la cadena resultante después de realizar el reemplazo.

El código fuente es extremadamente sencillo, pero dejo un enlace para descargar el código fuente por si alguien quiere realizar alguna mejora. También he creado una página para poder acceder al evaluador directamente, donde he puesto los ejemplos de expresiones regulares utilizadas para verificar los patrones más comunes (GUID, dirección IP, nombre de dominio, dirección de e-mail, etc.) y una lista de los principales caracteres especiales o _metacaracteres_ que se pueden utilizar y su comportamiento.

**Descarga código fuente:** [Silverlight_AnotherRegExTest_CSharp.zip](/files/Silverlight_AnotherRegExTest_CSharp)

