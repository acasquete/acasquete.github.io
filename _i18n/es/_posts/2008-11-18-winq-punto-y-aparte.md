---
title: WinQ, punto y aparte
tags: [programming]
reviewed: true
---
**Julio 2013:** La página del proyecto de Codeplex ya no existe y no se puede descargar. 

Hoy, dos meses después de la última actualización, he subido las dos últimas correcciones de [WinQ](http://www.codeplex.com/winq/Release/ProjectReleases.aspx?ReleaseId=13870), y digo últimas porque he decido no continuar con el desarrollo actual. Esta versión cumple con las necesidades iniciales: tener una aplicación que pudiese activar fácilmente en cualquier momento y que me permitiese realizar sencillos cálculos, conversiones o traducciones. De hecho hay muchas funciones que no he utilizado nunca pero que me han llevado bastante tiempo implementar, un motivo más por el no continúo con las mejoras que tenía planeadas.

Hay bastantes aspectos de WinQ que no me gustan, el principal es que el lenguaje de los scripts externos tenga que ser Javascript, me gustaría utilizar otro lenguaje o un sistema de _plugins_ implementado mediante _Reflection_. Otro de los grandes problemas a solucionar es el autocompletar, que es bastante pobre, lo ideal sería implementar un sistema parecido al _Intellisense_ de Microsoft. Y así, podría continuar con muchos otros problemas que he detectado…

A partir de ahora voy a trabajar con la versión 2008 de Visual Studio, aunque no sé si enfocar WinQ como una aplicación WPF. Estoy pensando también en realizar una versión para el escritorio Gnome porque la extensión de la calculadora de _Deskbar_ no me acaba de seducir, aunque entonces el nombre WinQ perderá su sentido, ¿quizás GnomeQ? En definitiva, sea cual sea el siguiente paso que realice con WinQ, será en un nuevo proyecto iniciado desde cero, pero con la experiencia de estos meses de uso y programación y siempre con los mismos seis principios fundamentales:

1.  Programa independiente, se descarta el desarrollo de un plugin.
2.  Libre, sin más.
3.  Interface de usuario muy sencilla, de fácil acceso e integrado en el sistema.
4.  Pensado siempre para el perfil programador.
5.  Funcionalidad ampliable por el usuario.
6.  Menos pulsaciones, más productividad.

