---
title: Expresiones de cálculo personalizadas
tags: [fsharp, functional_programming]
---
En posts anteriores hemos conocido el funcionamiento de las [expresiones de consulta](/expresiones-de-consulta-en-f-sharp/) y de los [workflows asíncronos](/workflows-asincronos-con-f-sharp/), dos características del lenguaje que nos facilitan la ejecución de consultas sobre distintos orígenes de datos y la creación de operaciones asíncronas. Vimos también que cada una de estas características es un uso particular de una construcción más general llamada expresiones de cálculo (_computation expressions_), también denominados _workflows_ aunque nada tienen que ver con los _workflows_ que se utilizan para modelar los procesos de negocio.

En esta entrada veremos qué son las expresiones de cálculo, cuál es su funcionamiento interno y cómo crear nuestras propias expresiones de cálculo personalizadas, ya que son construcciones muy fáciles de usar, pero algo más complejas de implementar. Espero que esta entrada ayude a aclarar un poco más este último aspecto.

Comenzando
----------

Las expresiones de cálculo no estuvieron disponibles hasta la versión 1.9 de F# y surgieron como una generalización de las expresiones de secuencia para **proporcionar una forma de representar un programa de una forma más natural, reutilizando elementos básicos de la sintaxis de F#, con los que dotar a los programas de un comportamiento totalmente distinto al predeterminado**. Es decir, las expresiones de cálculo nos permiten utilizar un enlace con **let**, un bucle **for** o **while** o cualquier otro elemento de la sintaxis del lenguaje, en los que, mediante la aplicación de transformaciones sintácticas, se les da una funcionalidad añadida. Un ejemplo utilizado en muchas ocasiones para introducir este concepto es la creación de un sistema de registro para una serie de operaciones. Por ejemplo, podemos realizar una llamada a la función de registro después de cada instrucción, como se muestra en el siguiente código.

    let x = 10
    trace x
    let y = 20
    trace y
    let z = x + y
    trace z
    

Sin embargo, haciendo uso de una expresión de cálculo, podemos escribir el siguiente código para obtener el mismo resultado.

    tracer {
        let! x = 10
        let! y = 20
        let! z = x + y
        return z
    }
    

Con lo que obtenemos un código mucho más limpio y expresivo, ya que nos transmite la intención. Veremos a continuación cómo crear este tipo de construcción.

Tipo de cálculo o _builder_
---------------------------

Las expresiones de cálculo se diseñan sobre un tipo de cálculo, que recibe el nombre de _builder_, y que **expone una serie de métodos necesarios para interpretar y establecer el comportamiento personalizado de las operaciones de la expresión de cálculo**. La forma general de las expresiones de cálculo es la siguiente.

    builder-instance { comp-expression }
    

Donde **builder-instance** representa una instancia de la clase _builder_ y **comp-expression** representa una serie de operaciones que son las que se «mapearán» con una llamada a los métodos del tipo de cálculo.

Comenzaremos creando la expresión de cálculo personalizada que he utilizado como ejemplo en la introducción. Es un ejemplo muy sencillo, pero nos servirá para asentar los conceptos principales y para ver a qué nos estamos refiriendo cuando decimos que queremos cambiar el comportamiento predeterminado de la sintaxis del lenguaje.

Supongamos que estamos realizando una serie de asignaciones.

    let a = 10
    let b = 20
    let c = a + b
    

Y queremos guardar un registro de cada operación después de realizar cada asignación, después de cada instrucción. La solución más directa sería, como hemos visto anteriormente, crear una función que guardase un registro y llamar a esa función después de cada instrucción. Algo que podemos conseguir fácilmente con el siguiente código:

    let trace info = printfn "expression is %A" info
    
    let a = 10
    trace a
    let b = 20
    trace b
    let c = a + b
    trace c
    

No obstante, no hace falta decir que en este caso hemos solucionado el problema, pero ensuciando bastante nuestro código. Con las **expresiones de cálculo vamos a poder simplificar el código modificando el comportamiento del enlace mediante _let_**.

Comenzamos creando un nuevo tipo en el que definimos un método **Bind** y **Return**.

    type TracingBuilder() =
        let trace p = printfn "expression is %A" p
    
        member this.Bind(x, f) = 
            trace x
            f x
    
        member this.Return(x) = 
            x
    

Además de la implementación de los dos métodos, también hemos incluido la definición de la función **trace** dentro del tipo. Pero, ¿cuál es el objetivo de los métodos **Bind** y **Return**? Veámoslo a continuación.

El método **Bind** se invocará para las expresiones **let!** y **do!** y el método **Return** para las expresiones **return**. **Los métodos que estamos obligados a implementar en el _builder_ dependen de las construcciones que necesitemos en las expresiones de cálculo**. En este ejemplo solo necesitaremos estos dos métodos.

Una vez tenemos el tipo _builder_ creado, crearemos una instancia para poder utilizarlo.

    let trace = new TracingBuilder()
    

Y todo lo que tenemos que hacer ahora es utilizar esta instancia con la forma de las expresiones de cálculo y escribir el código que queremos ejecutar entre las dos llaves.

    let tracer = new TracingBuilder()
    
    tracer {
        let! x = 10
        let! y = 20
        let! z = x + y
        return z
    }
    

Si lanzamos este código en la FSI veremos que obtenemos exactamente el mismo resultado que en el primer ejemplo, pero ahora con la ventaja de que en este segundo ejemplo no tenemos ningún código repetitivo.

Para explicar lo que ha sucedido al ejecutar este código, podemos decir que la expresión de cálculo se ha dividido en múltiples llamadas al objeto _builder_. El método al que se llama depende del tipo de instrucción que se utiliza en cada operación. En el caso de las asignaciones con **let**, se llama al método **Bind** en el que hemos definido cómo se debe calcular cada enlace, y en el caso de la palabra **return** se llamará al método **Return**.

Es importante destacar también que **dentro de un _workflow_ personalizado podemos escribir cualquier código F#, excepto crear un nuevo tipo** y además podemos utilizar nuevas palabras clave como **let!**, **return** y **yield**. En el ejemplo anterior hemos utilizando una de estas nuevas palabras clave: **let!** en lugar de **let**, ya que es la única forma de interferir el flujo de ejecución para ejecutar una lógica personalizada dentro de una expresión de cálculo.

Otro detalle es que en este ejemplo solo hemos utilizado los métodos **Bind** y **Return** y nos ha sido suficiente para crear el _workflow_, pero existen otros métodos que vamos a poder utilizar con otras expresiones. En la **MSDN** podemos [consultar todas las firmas de los métodos que se pueden utilizar al crear la clase _builder_](http://msdn.microsoft.com/en-us/library/dd233182.aspx).

Recordemos que **si el tipo _builder_ de una expresión de cálculo no contiene una implementación para un determinado método, no podemos asociar la construcción dentro de la expresión de cálculo**. Por ejemplo, si en nuestro ejemplo no hubiésemos implementado el método **Return**, obtendríamos un error de compilación al intentar ejecutar el código.

Sintaxis desazucarada
---------------------

Al ejecutar la expresión de cálculo, cada **let!** es reemplazado por una llamada al método **Bind** del _builder_, donde la evaluación del lado derecho del igual es el primer parámetro y el segundo parámetro es la función que representa el resto del cálculo a realizar. Para verlo más claramente, el siguiente código muestra la sintaxis desazucarada del ejemplo anterior.

    tracer.Bind(10, fun a -> tracer.Bind(20, fun b -> tracer.Return(a + b)))
    

Básicamente pasamos el valor que obtenemos de la expresión a la derecha del **let!** y una función que representa el resto de la expresión de cálculo, que contiene a su vez otra llamada al método **Bind** con otra función que llama al método **Return** y devuelve un valor que representa el resultado de la expresión de cálculo.

Otro ejemplo: producto cartesiano
---------------------------------

Otro ejemplo sencillo en el que podemos implementar una expresión de cálculo utilizando solo los métodos **Bind** y **Return** es el cálculo de producto cartesiano de dos conjuntos. Supongamos que queremos realizar el producto cartesiano de dos listas de elementos.

    let list1 = ["1"; "2"]
    let list2 = ["a"; "b"]
    

La forma más directa es utilizando llamadas anidadas a la función **List.collect**, con la que podemos aplicar una determinada transformación a cada elemento de una lista para generar una sublista, concatenar todos los resultados y devolver la lista combinada. El siguiente código siguiente muestra cómo conseguirlo.

    List.collect (fun a -> List.collect (fun b -> [(a,b)]) list2) list1
    

Y este es el resultado que obtenemos:

    val it : (string * string) list =
      [("1", "a"); ("1", "b"); ("2", "a"); ("2", "b")]
    

Si quisiésemos añadir una tercera lista y generar el producto cartesiano con ella, tendríamos que añadir otra llamada a **List.collect**. En general, tendríamos que realizar tantas llamadas anidadas para cada una de las listas. Sin embargo, si observamos la estructura de la expresión, parece que se adapta perfectamente a la del método Bind de un tipo _builder_. Ya que el parámetro inicial es una función con el resto de llamadas anidadas y en el último nivel se devuelve el valor de todos los elementos.

Así que siguiendo esta misma composición, podemos crear el tipo _builder_ como se muestra a continuación.

    type Cartesian () =
      member this.Bind (l,f) =
        List.collect f l
    
      member this.Return n = 
        [n]
    

En el método **Bind** llamamos a la función **List.collect** pasando como primer parámetro la función que representa el resto de la expresión de cálculo y como segundo, la lista de elementos. Ahora, como en los casos anteriores, simplemente tenemos que crear una instancia del tipo _builder_.

    let cartesian = new Cartesian()
    

Y ya podremos obtener el producto cartesiano de las dos listas escribiendo el siguiente código.

    cartesian {
        let! a = ["1";"2"]
        let! b = ["a";"b"]
        return a,b
    }
    

De nuevo, para entender cómo funciona internamente la expresión de cálculo, podemos ver a continuación el código con la sintaxis desazucarada.

    cartesian.Bind(list1, fun a -> cartesian.Bind(list2, fun b -> cartesian.Return(a,b)))
    

Además, podemos añadir más listas como parámetro de entrada añadiendo instrucciones **let** y añadiendo el valor a la tupla de resultados del **return**.

    cartesian {
        let! a = ["1";"2"]
        let! b = ["a";"b"]
        let! c = ["y";"z"]
        return a,b,c
    }
    

_Maybe monad_
-------------

En un post sobre expresiones de cálculo, es inevitable que surja esta deliciosa palabra: Monad. La utilizo al final del post, pero esto es debido a que en F# los monads no se llaman monads, se llaman expresiones de cálculo y es lo que hemos estado viendo durante todo el post bajo ese concepto. Seguramente el equipo de F# decidió no utilizar la palabra monad para alejarlo de lo difícil o complejo que es a veces explicar en qué consiste un monad. Sin ir más lejos, solo hace falta leer la definición de la [Wikipedia](http://en.wikipedia.org/wiki/Monad_(functional_programming) "Monad") para imaginarnos lo complejo y profundo que es este concepto. Sin embargo, las tres ideas principales que podemos extraer de esa definición las siguientes:

1.  Un monad es una estructura de programación que representa cálculos.
2.  Un monad permite al programador encadenar acciones.
3.  Un monad se construye definiendo dos operaciones (bind y return).

Como vemos, estas tres características las comparten los dos ejemplos que hemos realizado hasta ahora. En esta última parte del post, vamos a ver otro uso donde las expresiones de cálculo nos aportan una solución a un problema muy común, vamos a implementar el _Maybe Monad_.

Supongamos que tenemos la siguiente lista de instrucciones.

    let a = div 10 5
    let b = div 10 0
    let c = div 10 1
    

No es muy dificil intuir que si ejecutamos este código obtendremos una excepción **DivideByZeroException**. Si queremos controlar que la operación no se realice cuando el divisor sea 0, tenemos implementar una estructura con una serie de ifs anidados.

La expresión de cálculo que vamos a escribir es una que nos permitirá escribir una secuencia de operaciones con asignaciones **let** y que de forma condicional ejecutará el resto de operaciones si la expresión devuelve algún valor. Para poder implementar esta expresión nos vamos a ayudar del tipo **option**, es decir si alguna expresión devuelve **None**, el valor de la expresión de cálculo será **None**, sin importar el resto de las expresiones. Sin embargo, si la expresión devuelve **Some valor** se ejecutará el resto de la expresión de cálculo.

A continuación creamos el _builder_ con el método **Bind** que acepta un valor **option** y una función y devuelve otro valor de tipo **option**:

    type MaybeBuilder() =
        member this.Bind(v, f) = 
            match v with
            | None -> None
            | Some value -> f value
    

Con este código estamos indicando que si **v** es **None**, el método **Bind** devolverá **None** y no evaluará el resto de la expresión. Por el contrario, si **v** es **Some value**, entonces devolverá el resto de la función aplicada a **value**.

Y por último, en el método **return** tendremos que devolver también un **option**.

    type MaybeBuilder() =
        member this.Bind(p, rest) = 
            match p with
            | None -> None
            | Some value -> rest value
    
        member this.Return(x) = 
            Some x
    

De esta forma ya podemos escribir el siguiente código.

    let maybe = MaybeBuilder()
    
    maybe {
        let! a = div 10 5
        let! b = div 10 2
        let! c = div 10 0
        return c
    }
    

Resumen
-------

Las expresiones de cálculo que nos proporciona F# simplifican el trabajo cuando creamos secuencias, realizamos operaciones asíncronas o ejecutamos consultas. En esta entrada hemos visto cómo crear varias expresiones de cálculo personalizas que nos han servido para simplificar el registro de operaciones, el cálculo del producto cartesiano y la ejecución condicional mediante Maybe Monad.

Las expresiones de cálculo son una excelente forma de encapsular estado, gestión de excepciones, etc. Con estos ejemplos básicos, tenemos la base suficiente para explorar en próximas entradas más formas de crear otras expresiones de cálculo más sofisticadas.

Referencias
-----------

[Workflows – A Monad alias](http://blogs.msdn.com/b/doriancorompt/archive/2012/05/25/7-workflows-a-monad-alias.aspx)  
[Humbly simple F# Maybe monad application scenario](http://alfredodinapoli.wordpress.com/2012/04/02/humbly-simple-f-maybe-monad-application-scenario/)  
[Computation expressions: Introduction](http://fsharpforfunandprofit.com/posts/computation-expressions-intro/)

