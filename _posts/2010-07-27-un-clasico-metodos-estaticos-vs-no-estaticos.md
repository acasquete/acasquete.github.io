---
title: Un clásico, métodos estáticos vs no estáticos
tags: [programming]
reviewed: true
---
Efectivamente, como ya aviso en el título, la entrada trata un tema muy manido, lo podríamos denominar un clásico de las discusiones entre programadores. Es un clásico, pero por algún motivo las discusiones siempre van acompañadas de mitos y leyendas que no sé muy bien de dónde surgen.

Aun lo trillado del tema, no me resisto a escribir una nueva entrada porque en estos días se me ha vuelto a plantear y, ¡cómo no!, han surgido de nuevo los fantasmas alrededor de los métodos estáticos. Voy a tratar de recopilar en esta entrada las ideas esenciales que nos ayudarán a reconocer las situaciones en las que es recomendable el uso de métodos estáticos y en cuáles no.

Antes de comentar estas ideas básicas, vamos a ponernos en situación: Por un lado tenemos los **métodos no estáticos**, también llamados **métodos de instancia**. Estos métodos sólo pueden ser llamados en un objeto de la clase a la que pertenece, y pueden acceder tanto a miembros estáticos como no estáticos. Por otro lado, están los **métodos estáticos**, también llamados **métodos de clase**, que se pueden llamar tanto en la clase como en un objeto de la clase, pero, por contra, sólo pueden acceder a miembros estáticos.

Después de esta más que breve introducción, una serie de directrices que nos ayudarán a decidir cuándo utilizar cada tipo de implementación:

1.  Debemos implementar métodos de clase cuando el método no utilice miembros de clase y, previsiblemente **no lo vaya a hacer en el futuro**. Otra forma de decir esto sería que debemos utilizar métodos de instancia cuando su implementación dependa de miembros, propiedades u otros métodos de instancia y debemos utilizar métodos estáticos si el método depende **sólo** de sus parámetros. Si, por ejemplo, dependemos de configuraciones o bases de datos externas, optaríamos por métodos de instancia, y si queremos realizar cálculos que no cambian según el estado del objeto, como una conversión de grado _Celsius_ a _Fahrenheit_, haríamos uso de métodos de clase.
    
2.  Se podrían dar situaciones (raras situaciones) en las que un método no utiliza miembros de una clase, pero de forma lógica pertenece a una instancia, en ese caso deberíamos utilizar métodos de instancia.
    
3.  Si queremos hacer que el método sea accesible vía COM interop, debemos utilizar métodos de instancia ya que no es posible llamar a métodos estáticos, aunque existen soluciones que lo permiten.
    
4.  No hay que utilizar **clases estáticas** como un cajón de elementos que hagan muchas cosas. Aunque esto parece evidente, he visto muchas veces clases en las que todos los métodos están definidos cómo estáticos y realizan infinidad de funciones diferentes. No debemos olvidar nunca que el abuso de clases estáticas y por ende de métodos estáticos, nos puede hacer crear código difícil de manejar en muy poco tiempo.
    
También se suele decir muchas veces que el rendimiento de los métodos estáticos es mucho mejor, he escuchado lo contrario incluso, pero la realidad es que la diferencia de rendimiento entre métodos estáticos y los no estáticos es realmente muy pequeña. En este artículo: [_Speed Test: Static vs Instance Methods_](http://www.blackwasp.co.uk/SpeedTestStaticInstance.aspx), podemos ver la comparación de los tiempos de ejecución según el tipo de método, confirmando que esta diferencia no es significativa.

Otra de las creencias es que con métodos estáticos no se libera la memoria de los objetos utilizados. Esto creo que es debido a que se confunden los miembros con los métodos. Observemos el siguiente código:

```csharp
class TestClass { 
    static object testObj1;`

    static void testMethod() 
    { 
        testObj1 = new object(); 
        object testObj2 = new object(); 
    } 
}
```

Si utilizamos un código similar al anterior, el GC no recogerá el objeto _testObj1_ hasta que se iguale a _null_, ya que el objeto (al ser estático) siempre está disponible. No sucede lo mismo con el objeto _testObj2_ que estará disponible para recolección al finalizar la ejecución del método.

En definitiva y para concluir, la idea principal con la que nos tenemos que quedar es que la elección entre crear métodos de clase o de instancia debe estar siembre basada en cuestiones de diseño y nunca de rendimiento.

**Enlaces relacionados** 

Blackwasp: [_Speed Test: Static vs Instance Methods_](http://www.blackwasp.co.uk/SpeedTestStaticInstance.aspx)  
Biblioteca MSDN: [Diseño de clases estáticas](http://msdn.microsoft.com/es-es/library/ms229038(VS.80).aspx)  
