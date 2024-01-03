---
title: BcnDevCon, Aplicaciones robustas con Programación Orientada a Aspectos
tags: [aop, event]
reviewed: true
---
Este pasado jueves di una breve charla durante la [Barcelona Developers Conference](http://www.bcndevcon.org/) sobre Programación Orientada a Aspectos. Fue una charla introductoria de cuarenta y cinco minutos en la que vimos los conceptos básicos de [PostSharp](http://www.sharpcrafters.com/postsharp/) y [DynamicProxy](http://www.castleproject.org/dynamicproxy/index.html), dos librerías que podemos utilizar para implementar aspectos en nuestras aplicaciones. En esta entrada voy a intentar resumir lo que ya fue una charla muy resumida de lo que es AOP.

**¿Qué es AOP?** La programación orientada a aspectos es un paradigma de programación cuya principal intención es que escribamos buen código, código más limpio. Como comenté durante la charla este es un tema bastante curioso, porque el concepto de AOP es bastante antiguo (se desarrolló hace 15 años), mucha gente lo conoce, existen librerías desde hace también bastante tiempo, pero lo curioso es que en muy pocos proyectos he visto una implementación de aspectos.

De hecho, me ha sucedido varias veces, que lo primero que pregunta mucha gente cuando oye este término (sobre todo programadores de .NET) es: ¿Ya no programamos con orientación a objetos? Y la respuesta siempre es: No, AOP no sustituye la orientación a objetos. Pero lo que sucede es que la OOP es un modelo que se queda corto cuando tenemos que implementar temas transversales, cuando tenemos que implementar comportamientos que se utilizan en gran parte de las funcionalidades de negocio y además estos comportamientos no se pueden aislar fácilmente.

**Cross-cutting concerns** Los temas transversales más comunes son el registro (logging), seguridad, transacciones, multithreading, interfaz de usuario, caché, validaciones, etc. Al final cuando tenemos toda esta funcionalidad implementada en nuestra aplicación, nos damos cuenta que tenemos el código esparcido por toda la aplicación, haciendo de ese código algo difícil de mantener y de depurar.

Los problemas que provoca tener que implementar toda esta funcionalidad transversal se pueden resumir en estos: más número de líneas, más código duplicado y código de negocio mezclado y acoplado con el código transversal.

Para minimizar el impacto de la implementación de esta transversalidad normalmente se utilizan distintas técnicas como puede ser la generación de código, programación funcional o proxies dinámicos, pero al no estar diseñados para implementar AOP no es la solución ideal para todos los casos.

**Beneficios de la Programación Orientada a Aspectos** Al finalizar la charla comenté varios de los beneficios que obtenemos al aplicar AOP en nuestras aplicaciones. Estos beneficios quedan resumidos en la siguiente lista: 

**Menos costes** – El coste de la creación de software es casi directamente proporcional al número de líneas de código que se hemos generado, y que luego tenemos que mantener. 

**Menos fallos** – Menos código es sinónimo de menos fallos. Aunque los aspectos también pueden tener fallos, es más fácil solucionar un error en la clase de los aspectos que en cada uno de los métodos donde se aplica. 

**Aseguramiento de la Calidad** - La programación orientada a aspectos, permite la activación de las funcionalidades transversales sin afectar la calidad de la aplicación. 

**Mejora el mantenimiento** – Al reducir la dispersión del código transversal los desarrolladores pueden encontrar el código afectado por un cambio más fácilmente. 

**Mejora el trabajo en equipo** – Los equipos de desarrollo no tienen que lidiar con la forma en que se debe implementar la funcionalidad transversal, permitiendo así que solo tengan que trabajar con el código de negocio. Además, los nuevos miembros tendrán una curva de aprendizaje menos prolongada para comenzar a ser productivos.

Hasta aquí este pequeño resumen, dejo también varios enlaces de referencia que mostré al final de la presentación así como el código que utilicé durante las demos.

**Descarga código fuente:** [BcnDevCon.AOP.zip](/files/BcnDevCon.AOP.zip)

Enlaces relacionados
---
[Aspect-Oriented Software Development](http://aosd.net/)  
[PostSharp](http://www.sharpcrafters.com/postsharp)  
[DynamicProxy](http://www.castleproject.org/dynamicproxy)
