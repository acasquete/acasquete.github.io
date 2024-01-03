---
title: Patrones activos en F#
tags: [fsharp, functional_programming]
reviewed: true
---
En una entrada anterior vimos cómo con [_pattern matching_](/pattern-matching-con-fsharp "Pattern matching con F#") podemos hacer nuestro código más expresivo cuando queremos comparar datos con estructuras lógicas. Cada patrón nos permite comparar los valores de entrada, descomponerlos y combinarlos con una estructura de datos. Sin embargo, con _pattern matching_ los patrones soportados están limitados a unos tipos determinados, como listas, tuplas o matrices y valores constantes de tipo cadena, numérico, enumeración, etc.

En esta entrada veremos que con el uso de los patrones activos aumentaremos la potencia de _pattern matching_ cuando los tipos de patrones incorporados no nos sean útiles para nuestro propósito, a la vez que añadiremos claridad a nuestro código, ya que podremos simplificar las construcciones eliminando el uso de las protecciones **when**.

Los patrones activos son un tipo especial de definición de función llamada reconocedor activo (_active recognizer_), donde definimos los casos que podemos utilizar en las expresiones de _pattern matching_. Los nombres de los casos están delimitados por los símbolos (\| y \|), llamados delimitadores de patrones activos o _banana clips_ y cada caso está separado por un separador vertical.

La sintaxis de la definición de patrones activos es la siguiente:

```csharp
let (|identificador1|identificador2|...|) [ argumentos ] = expresión
```

Las funciones de definición de un patrón activo deben incluir como mínimo un parámetro de entrada que debe ser el valor con el que se buscará coincidencias, pero además, como estas funciones son funciones parcializadas o _curried_, este valor deber ser el último de los argumentos. La función, además, debe devolver uno de los casos con nombre.

Podemos definir patrones activos de varias formas, según si definimos uno o varios casos, incluimos un comodín o utilizamos más de un argumento.

Vamos a ver a continuación el primer ejemplo en el que simplificaremos la sintaxis mediante los patrones activos de uno de los ejemplos que utilicé en el post de _pattern matching_. Se trata del siguiente ejemplo, con el que implementamos la Kata FizzBuzz, donde utilizábamos la protección **when** para establecer condiciones adicionales en cada uno de los casos:

```csharp
let fizzbuzz x =
    function
    | x when x % 5 = 0 && x % 3 = 0 -> "FizzBuzz"
    | x when x % 3 = 0 -> "Fizz"
    | x when x % 5 = 0 -> "Buzz"
    | x -> string x
```

Para simplificar la función, podemos crear un reconocedor activo de la siguiente forma:

```csharp
let (|Fizz|Buzz|FizzBuzz|Same|) x = 
    if x % 5 = 0 && x % 3 = 0 then FizzBuzz 
    elif x % 3 = 0 then Fizz 
    elif x % 5 = 0 then Buzz
    else Same x
```

En el que definimos cuatro casos con nombre (_Fizz_, _Buzz_, _FizzBuzz_ y _Same_) y devolvemos el caso correcto según las mismas condiciones que utilizábamos anteriormente. En este caso he utilizado la construcción **if..elif..else**, pero nada nos impediría utilizar también otra expresión **match..with**.

En cualquiera de los dos casos, ahora podemos escribir funciones _pattern matching_ de la siguiente forma, en la que utilizamos casos definidos en la función del reconocedor activo en lugar de los patrones predefinidos con las protecciones.

```csharp
let fizzBuzz =
    function
    | Fizz -> "Fizz"
    | Buzz -> "Buzz"
    | FizzBuzz -> "FizzBuzz"
    | Same x -> string x

seq {1..100}
|> Seq.map fizzBuzz
```

En el siguiente ejemplo vamos a definir un patrón activo que intentará parsear el valor de una cadena a entero, booleano y numérico flotante y devolverá el caso que haya tenido éxito si se ha podido realizar la conversión o por el contrario devolverá la cadena de entrada.

```csharp
open System

let (|Int32|Float|Boolean|String|) input =
    let sucess, res = Int32.TryParse input
    if sucess then Int32 res
    else 
        let sucess, res = Double.TryParse input
        if sucess then Float res
        else
            let sucess, res = Boolean.TryParse input
            if sucess then Boolean res
            else String input

let describeType input =
    match input with
    | Int32 i -> sprintf "Integer: %i" i
    | Boolean b -> sprintf "Boolean: %b" b
    | Float f -> sprintf "Floating point: %f" f
    | String s -> sprintf "String: %s" s


["1"; "True"; "2.5"; "Text"]
|> List.map describeType
```

La diferencia en este ejemplo es que el valor devuelto es el caso con nombre (_Int32_, _Float_, _Boolean_ o _String_) seguido de un valor que podemos utilizar en la expresión de la función de _pattern matching_.

Patrones activos parciales
--------------------------

Los patrones activos están limitados a siete casos con nombre. En el caso de que definamos una función con más de siete casos, obtendremos un error de compilación. Si nos encontremos con un escenario en el que tenemos que utilizar más de siete casos o necesitamos realizar un mapeo con cada posible entrada, tendremos que hacer uso de los patrones activos parciales.

La definición de los patrones activos parciales tiene la misma sintaxis que los completos, pero en lugar de una lista de casos con nombre, tenemos que incluir un solo caso seguido del carácter de comodín \_.

```csharp
let (|identificador1|_|) [parámetros] = expresión
```

Otra diferencia añadida es que el valor devuelto por un patrón activo parcial no es el mismo de uno completo. En lugar de devolver el caso directamente, los patrones parciales devuelven un tipo opción del tipo de patrón.

En el siguiente ejemplo creamos una función de _pattern matching_ que nos indica si un número es divisible por 3 y por 5. En este caso estamos haciendo uso de un patrón activo parcial en el que solo definimos un caso, si el numero cumple las 2 condiciones la función devuelve Some(x) y en caso contrario devuelve None.

```csharp
let (|DivisibleByThreeAndFive|_|) x = 
    if x % 3 = 0 && x % 5 = 0 then Some(x) else None

let describeNumber x =
    match x with
    | DivisibleByThreeAndFive x -> "Divisible by 3 and 5"
    | _ -> string x

seq {1..100}
|> Seq.map describeNumber
```

Patrones activos parametrizados
-------------------------------

En todos los ejemplos que hemos visto hasta ahora solo hemos definido funciones con un parámetro. Los últimos ejemplos que vamos a ver son la definición de funciones reconocedoras que aceptan varios argumentos de entrada. Este tipo de patrones activos son conocidos como patrones activos parametrizados.

Es importante recordar que **el último argumento será siempre el valor con el que queremos realizar la comparación de coincidencia**.

En este primer ejemplo creamos un función reconocedora que acepta el parámetro divisor además del valor a comparar y devuelve una tupla con el valor de entrada y el resto de la división.

```csharp
let (|DivisibleBy|_|) divisor n =
    Some (n, n % divisor)
```

En el caso de que el segundo valor de la tupla sea 0 indicará que el número de entrada es divisible por el divisor. De esta forma podemos crear una función de _pattern matching_ que nos devuelva el divisor de la siguiente forma:

```csharp
let printDivisor n =
    match n with
    | DivisibleBy 2 (n,0) -> 2
    | DivisibleBy 3 (n,0) -> 3
    | _ -> n

[1..100]
|> List.map printDivisor
```

Y como último ejemplo, vamos a definir un patrón activo parcial que nos indicará si una expresión regular coincide con el valor de entrada.

```csharp
open System.Text.RegularExpressions

let (|Regex|_|) regexPattern input =
    let regex = new Regex(regexPattern)
    let regexMatch = regex.Match(input)
    
    if regexMatch.Success then
        Some regexMatch.Value
    else
        None
```

Ahora podemos crear una función de _pattern matching_ en la que podemos pasar como argumento la expresión regular que queremos comprobar.

```csharp
let describeContactType input =
    match input with
    | Regex  @"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" s -> sprintf "Email: %s" s
    | Regex  @"^\d{9}$" s -> sprintf "Phone: %s" s
    | _ -> sprintf "Other: %s" input

["alex@mail.com";"Address Sample";"650018066"]
|> List.map describeContactType
```

El resultado será el siguiente:

```csharp
val it : string list =
    ["Email: alex@mail.com"; "Other: Address Sample"; "Phone: 611101010"]
```

Resumen
-------

Con el uso de los patrones activos completamos toda la potencia que nos ofrece _pattern matching_ en los casos en los que los patrones predefinidos no nos ofrecen la flexibilidad necesaria, además de mejorar la legibilidad del código.

Según el número de casos que definamos en el reconocedor activo tenemos cuatro variedades de patrones activos: de un solo caso, multi-caso, parciales y parametrizados. Los patrones de un solo caso se utilizan habitualmente para descomponer la entrada de una forma determinada. Los patrones parciales son aquellos en los que solo coincide una parte del valor de entrada. Y por último, los parametrizados realizan la misma función que los parciales pero admiten parámetros adicionales para que puedan ser reutilizados fácilmente.

Referencias
-----------

[Modelos activos (F#)](http://msdn.microsoft.com/es-es/library/dd233248.aspx)
