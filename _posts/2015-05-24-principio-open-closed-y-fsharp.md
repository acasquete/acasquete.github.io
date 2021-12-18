---
title: El principio Open-Closed y F#
tags: [fsharp, functional_programming]
reviewed: true
---
![Agents](/img/open-sign.png){:.fullview}

En la programación orientada a objetos, el **principio Open/Closed** (_Open/Close Principle_, OCP) establece que “las entidades de software deben estar abiertas a extensión, pero cerradas a modificación”. Detrás de este enunciado nos encontramos con el corazón de la OOP, ya que la conformidad con este principio es lo produce los mayores beneficios en cuanto mantenibilidad y reusabilidad del código.

El OCP intenta evitar los “malos” diseños, entendiendo como tales, aquellos en los que al realizar un solo cambio en un programa da como resultado una serie de cambios en los módulos de los que depende. Por lo tanto, **para poder crear diseños que son estables a los cambios durante su ciclo de vida, tenemos que extender el comportamiento añadiendo nuevo código y no cambiar el código antiguo que funciona**.

La forma que tenemos en la OOP de extender el comportamiento de una clase es mediante el uso de abstracciones (clases base abstractas) que representan un conjunto limitado de comportamientos. Estos comportamientos se pueden ampliar mediante la creación de nuevas clases derivadas a partir de la abstracción. De esta forma tenemos una clase que está cerrada a modificación, que depende de una abstracción fija, pero que puede ser ampliada mediante la creación de nuevas clases derivadas.

Como vemos, el OCP está orientado a lenguajes en los que se utiliza la herencia como mecanismo de polimorfismo. Sin embargo, en F# y en la programación funcional en general no utilizamos la herencia ni el polimorfismo. En esta entrada vamos a ver qué métodos podemos utilizar en F# para extender el comportamiento, centrándonos básicamente en explicar en qué consiste la composición de funciones y el aumento o extensión de tipos.

Composición de funciones
------------------------

La composición de funciones consiste en la creación de una nueva función basada en otras funciones. Por ejemplo, supongamos que tenemos las siguientes dos funciones:

```csharp
let double x = x * 2

let negative x = x * -1
```

y queremos definir una nueva función que sea resultado de la composición de las dos funciones definidas previamente. Utilizando el operador de composición podemos declararla de la siguiente forma:

```csharp
let doublenegative = double >> negative
```

La función **doublenegative** no devuelve un valor, sino que devuelve otra función cuya firma es `(int -> int)`. De esta forma, estamos creando una nueva función a partir de la composición de las funciones **double** y **negative**. En este caso, primero se aplica la función **double** y luego se aplica la función **negative** sobre el resultado anterior.

Si ejecutamos la función **doublenegative** obtendremos el siguiente resultado:

```bash
> doublenegative 2;;
val it : int = -4
```

Aunque en un primer momento este operador podría parecer similar al operador de canalización (o _pipeline_), si nos fijamos en la implementación veremos que es radicalmente distinta ya que el operador de composición `>>` acepta dos funciones y devuelve una función y el de canalización devuelve un valor a partir de una función y un argumento. En F#, la función de composición está definida de la siguiente forma:

```csharp
let inline (>>) f g x = g (f x)
```

Mientras que el operador de canalización está definido con la siguiente función:

```csharp
let inline (|>) x f = f x
```

Adicionalmente, en F# también disponemos del operador `<<` (operador de composición hacia atrás), con el que podemos realizar composición de funciones en el orden inverso. En este caso, la función que define el operador de composición inverso es la siguiente:

```csharp
let inline (<<) f g x = f (g x)
```

A continuación se muestra un sencillo ejemplo que muestra el comportamiento de los dos operadores de composición de funciones.

```csharp
let negative x = x * -1 

let square x = x * x

let negativesquare = negative >> square

let squarenegative = negative << square

> negativesquare 2;;
val it : int = 4

> squarenegative 2;;
val it : int = -4
```

Aumento de tipo
---------------

En [entradas anteriores](/uniones-discriminadas-y-jerarquia-de-objetos/) vimos como en F# podemos añadir funciones adjuntas a las **uniones discriminadas** y a los **_record types_**. En el ejemplo siguiente se muestra la declaración de un _record type_ con la función **area** adjunta.

```csharp
type Shape = 
    { width: int; height: int }
    member this.area =
        this.width * this.height
```

En lugar de escribir el código de la función a la vez que la definición del tipo, podemos implementar la funcionalidad asociada con el tipo en una función separada y utilizar el aumento de tipo para hacer esa funcionalidad disponible como un miembro. El siguiente código muestra cómo hacerlo siguiendo el ejemplo anterior:

```csharp
type Shape = { width: int; height: int }

let area shape = shape.width * shape.height 

type Shape with
    member this.area = area this
```

Esto permite inyectar fácilmente nuevas funcionalidades a los tipos conocidos y hacer los DSL más legibles. Otro beneficio del uso de este patrón es que la inferencia de tipos funciona mucho mejor con el estilo de programación funcional que con el estilo orientado a objetos.

Los aumentos de tipo también reciben el nombre de **extensiones de tipo**, diferenciando en este caso, las extensiones de tipo **intrínsecas** de las **opcionales**. Una extensión intrínseca es la que aparece en el mismo espacio de nombres y ensamblado que el tipo que se extiende y la extensión opcional es la que aparece fuera del módulo, espacio de nombres o ensamblado.

Los aumentos de tipo, cuando se definen en el mismo módulo, espacio de nombres y fichero, pasan a formar parte del tipo cuando se compila. Por el contrario, las extensiones de tipo opcionales, se implementan con los métodos de extensión de .NET. Los dos tipos de extensiones se declaran utilizando la misma sintaxis, la única consideración a tener en cuenta es que debemos utilizar el tipo cualificado completo cuando utilicemos extensiones de tipo opcionales.

Resumen
-------

A diferencia de la Programación Orientada a Objetos en la que hacemos uso de la herencia y el polimorfismo para poder extender el comportamiento de una clase, en F# utilizamos dos características del lenguaje, la composición de funciones y el aumento de tipo, para extender la funcionalidad de nuestros tipos haciendo el código mucho más legible y mantenible.

Referencias
-----------

[Principles of Ood](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod)  
[SOLID Part I – The Open/Closed-Principle – C# vs. F#](http://www.navision-blog.de/blog/2009/08/24/the-openclosed-principle-c-vs-f/)  
[F# and Design Principles - SOLID](http://7sharpnine.com/posts/FSharp_solid/)  
[F# and the Open/Closed Principle](https://jamessdixon.wordpress.com/2014/04/15/f-and-the-openclosed-principle/)
