---
title: Pattern matching con F#
tags: [fsharp, functional_programming]
reviewed: true
---
![Query Expressions](/img/pattern-matching.png){:.fullview}

Continuamos la serie dedicada a F# con una característica del lenguaje tremendamente potente, _pattern matching_ o su traducción en español, coincidencia de patrones. La lista de todas las entradas de la serie se puede consultar en este [link](http://www.casquete.es/category/fsharp). Además, [Juan Manuel Gómez](https://twitter.com/_jmgomez_), está escribiendo otra serie que puedes consultar [aquí](http://geeks.ms/blogs/jmgomez/archive/tags/FSharp/default.aspx).

Muchas veces se compara _pattern matching_ con la sentencia switch de C#, yo mismo utilizo esta analogía en muchas ocasiones para introducir el concepto, pero esa comparación es muy injusta ya que con _pattern matching_ no solo podemos añadir construcciones de control sino que también lo podemos utilizar para descomponer información de entrada a partir de distintas operaciones especificadas a través de un patrón. A lo largo del post veremos algunos posibles de uso de _pattern matching_ y descubriremos como en muchas ocasiones ya lo estamos utilizando sin darnos cuenta.

_Pattern matching_ consiste en una serie de reglas o funciones que se ejecutarán solo cuando la expresión de entrada coincide con un determinado patrón. La expresión de _pattern matching_ devuelve el resultado de la función que ha coincidido, de tal forma que el tipo de valor devuelto de todas las funciones debe ser el mismo.

Para crear un _pattern matching_, utilizamos la palabra clave **match** seguida de la expresión de entrada y **with** y mediante la barra vertical | declaramos la lista de reglas. El esquema más simple de _pattern matching_ tiene el siguiente aspecto.

```csharp
match expr with
| pattern1 -> result1
| pattern2 -> result2
| _ -> defaultResult
```

La sintaxis de las reglas nos será familiar debido a la flecha ->, ya que es la misma que utilizamos en la definición de funciones anónimas. En _pattern matching_ se comprueba si el patrón, el parámetro de la función lambda, coincide con la expresión de entrada y en caso afirmativo, se devuelve el resultado de la expresión lambda. El guion bajo \_, el comodín, se utiliza para definir el patrón predeterminado, en el caso de que la expresión de entrada no coincida con ningún patrón se devolverá este valor.

Las reglas se comprueban en el orden en que se declaran, así que si declaramos el comodín como primera regla, las siguientes no se comprobarán. En esta situación obtendremos una advertencia del compilador, lo veremos más adelante cuando hablemos de la coincidencia exhaustiva.

Pero veamos el primer ejemplo, en el código siguiente se muestra cómo utilizar _pattern matching_ contra la expresión x.

```csharp
let x = 2

let y = 
    match x with 
    | 1 -> "a"
    | 2 -> "b"  
    | _ -> "z" 
```

Después de ejecutar estas expresiones, y contendrá el valor “a” ya que es el resultado que coincide con el parámetro 2. Este código tan sencillo es equivalente a escribir una secuencia de condicionales if/then/elif/else.

```csharp
let y = 
    if x = 1 then "a"
    elif x = 2 then "b"
    else "z"
```

Utilizando la sentencia **match..with** el compilador genera una sentencia switch mientras que en este último caso se generan los ifs anidados. En este primer ejemplo, hemos utilizado un patrón constante, en este caso un número, pero podemos utilizar un carácter, cadenas de texto o enumeraciones. En el siguiente ejemplo, vemos cómo utilizar _pattern matching_ con una enumeración.

```csharp
type Position =
    | First = 1
    | Second = 2
    | Third = 3

let printPosition (position) =
    match position with
    | Position.First -> "first"
    | Position.Second -> "second"
    | Position.Third -> "third"
    | _ -> "Invalid Position"
```

Patrones soportados
-------------------

En estos dos ejemplos anteriores, hemos utilizado un solo valor constante como expresión de patrón, pero es posible utilizar otros. La lista completa de los patrones soportados es la siguiente:

Patrón | Ejemplo
---|---
Constante|1.0, "test", 30, Color.Red|Identificador|Some(x) Failure(msg)|
Variable|a
as|(a, b) as tuple1
OR|(\[h\] \| \[h; \_\])
AND|(a, b) & (\_, "test")
cons|h :: t
Lista|\[ a; b; c \]
Matriz|\[\| a; b; c \|\]
Entre paréntesis|( a )
Tupla|( a, b )
Registro|{ Name = name; }
Carácter comodín|\_
Con anotación de tipo|a : int
Prueba de tipo|:? System.DateTime as dt
NULL|null

El siguiente ejemplo muestra cómo utilizar _pattern matching_ con un patrón de una tupla, para obtener la tabla de verdad de una operación OR.

```csharp
let Or a b =
    match a, b with
        | true, true -> true
        | true, false -> true
        | false, true -> true
        | false, false -> false
```

Podemos escribir una versión simplificada de esta función utilizando el patrón comodín.

```csharp
let Or a b =
    match a, b with
        | false, false -> false
        | _ , _ -> true
```

Coincidencia exhaustiva
-----------------------

Todos los ejemplos que hemos visto hasta ahora, tienen un caso en el que utilizamos el patrón comodín. Esto es así porque si no pusiésemos esta última regla, el compilador se nos quejaría ya que puede que haya algún caso que no estemos contemplando. El siguiente es el código de ejemplo de un _pattern matching_ incompleto:

```csharp
let x = 2

let y = 
    match x with 
    | 1 -> "a"
    | 2 -> "b"  
```

Si ejecutamos este código, el compilador nos devuelve la siguiente advertencia, informándonos de que existe al menos un caso no contemplado.

```csharp
Script.fsx(12,11): warning FS0025: Incomplete pattern matches on this expression. For example, the value '0' may indicate a case not covered by the pattern(s).
```

Si echamos un vistazo al código IL generado de un _pattern matching_ no exhaustivo, veremos que se ha agregado un caso por defecto en el que se lanza la excepción **MatchFailureException**. En el caso opuesto, cuando existen reglas redundantes, el compilador también nos lo indicará mediante una advertencia, pero en este caso no se generará ningún código para ese caso, simplemente el compilador lo ignora.

Patrones con nombre
-------------------

Hasta ahora sólo hemos utilizado valores constantes como patrón, pero es posible utilizar patrones con nombre para extraer los datos y enlazarlos a un nuevo valor.

```csharp
let greetings name =
    match name with
        | "Mercedes" -> "Hello, Merche"
        | x -> sprintf "Hello, %s" x 
```

En este ejemplo, el primer caso estamos utilizando un patrón de cadena constante, pero en la segunda estamos utilizando el parámetro x. Este último caso funciona como el patrón comodín, pero en lugar de ignorar el valor, podemos utilizarlo en la expresión lambda.

En lugar de utilizar un valor constante “Mercedes”, es posible utilizar como patrón un valor existente marcándolo con el atributo [\<Literal>\]. Cualquier valor literal (entero, punto flotante, carácter, cadena, o booleano) que comience con una mayúscula y esté marcado con este atributo se puede utilizar como patrón dentro de _pattern matching_.

```csharp
[<Literal>]
let Mercedes = "Mercedes"

let greet name =
    match name with
    | Mercedes -> "Hello, Merche"
    | x -> sprintf "Hello, %s" x
```

Si en lugar de un tipo simple queremos utilizar tipos complejos como patrón, tendremos que utilizar la claúsula **when**.

Agrupación de patrones
----------------------

Es posible combinar patrones realizando operaciones lógicas AND, utilizando el operador &, y OR, utilizando la línea vertical |. En el primer caso la coincidencia si el dato de entrada coincide con todos los patrones agrupados y en el segundo si alguno coincide.

```csharp
type Colors =
    | Red = 1
    | Violet = 2
    | Blue = 3
    | Green = 4
    | Yellow = 5
    | Orange = 6

let isWarm color =
    match color with
    | Colors.Red | Colors.Orange | Colors.Yellow -> true
    | Colors.Violet | Colors.Blue | Colors.Green -> false
```

Restricciones en los patrones con **when**
------------------------------------------

Muchas veces la combinación de múltiples patrones no es suficiente y necesitamos añadir condiciones adicionales para comprobar si una regla debe coincidir o no. Mediante la cláusula **when**, conocida como protección, podemos establecer estas condiciones adicionales.

El siguiente ejemplo implementa el algoritmo para resolver la kata FizzBuzz.

```csharp
let fizzbuzz x =
    match x with
    | x when x % 5 = 0 && x % 3 = 0 -> "FizzBuzz"
    | x when x % 3 = 0 -> "Fizz"
    | x when x % 5 = 0 -> "Buzz"
    | x -> string x
```

_Pattern matching everywhere_
-----------------------------

Hasta aquí hemos visto la sintaxis básicos de _pattern matching_, pero lo interesante es que pattern maching no se utiliza exclusivamente en las expresiones **match..with**, está presente sin que lo veamos en todo el lenguaje. Por ejemplo, los enlaces con let o los parámetros de funciones son realmente reglas de _pattern matching_. Si escribimos el siguiente código para el asignar los valores de una tupla:

```csharp
let (a,b) = (100,200)
```  

Podemos pensar en que es una construcción _pattern matching_ con esta forma.

```csharp
let a,b = match (100, 200) with
            | x, y -> x, y
```  

Sintaxis alternativa con **function**
-------------------------------------

Por último vamos a ver una sintaxis alternativa de _pattern matching_. Es muy habitual que cuando definimos una función pasemos el parámetro de la función a la expresión **match..with** como hemos visto ya en un ejemplo anterior:

```csharp
let Or a b =
    match a, b with
        | false, false -> false
        | _ , _ -> true
```

La forma simplificada de escribir este mismo código es haciendo uso de la palabra clave function, que actúa muy parecido a la palabra clave fun para la creación de lambdas, excepto que la function solo acepta un parámetro que se utilizará en el _pattern matching_. Este es el mismo ejemplo de antes, pero utilizando la sintaxis simplificada:

```csharp
let Or a b =
    function
        | false, false -> false
        | _ , _ -> true
```

Resumen
-------

_Pattern matching_ es una característica muy potente, de la que hemos visto las posibilidades y sintaxis básica, que podemos utilizar para descomponer y transformar datos. El uso más sencillo es utilizando patrones de constante, pero se soportan un gran tipo de patrones, desde listas o matrices hasta comprobaciones de tipo. Además, cuando la combinación de varios patrones no nos es suficiente, podemos añadir condiciones adicionales con las protecciones **when**.
