---
title: Code Quotations en F#
tags: [fsharp, functional_programming]
---
Las [expresiones de cálculo que vimos en un post anterior](/expresiones-de-calculo-personalizadas "Expresiones de cálculo personalizadas") se pueden utilizar para dar un significado distinto al código; sin embargo, tienen ciertas limitaciones. Por poner un ejemplo, no podemos manipular el código y ejecutarlo en un entorno diferente, al igual que hace **LINQ to SQL**. Si queremos hacer algo parecido en F#, podemos lograrlo utilizando una característica del lenguaje llamada _Code Quotations_ o expresiones de código delimitadas, que permite generar y usar expresiones de código F# de forma programática, de forma que es posible acceder a la información de tipo de un bloque de código y además ver cómo está estructurado, conocido normalmente como árbol de sintaxis abstracto (_Abstract-Syntax Tree_ o AST).

Una vez hemos obtenido el árbol de un bloque de código, lo podemos recorrer y procesar según nuestras necesidades. Podemos, por ejemplo, utilizar el árbol para generar código en F# o en algún otro lenguaje, realizar inspección y análisis del código o diferir el cálculo a otras plataformas como SQL, GPU. etc.

Las _Code Quotations_ son equivalentes a los objetos **Expression<>** de C#, en el que podemos crear una expresión convirtiendo de forma implícita una expresión lambda en un objeto **Expression** de la siguiente forma.

```csharp
Expression<Func<int, int>> expr = x => x + 1;
```

En F# podemos obtener una _Code Quotation_ poniendo los símbolos **<@ @>** o **<@@ @@>** alrededor de una expresión. La prueba más sencilla que podemos hacer es abrir la ventana _F# Interactive_ y escribir el siguiente código:

```csharp
    <@ 2 + 3 @>;;
```

El compilador no calculará el valor de la expresión, en su lugar generará el siguiente resultado:

```csharp
val it : Quotations.Expr<int> =
    Call (None, op_Addition, [Value (2), Value (3)])
    {CustomAttributes = [NewTuple (Value ("DebugRange"),
            NewTuple (Value ("stdin"), Value (1), Value (3), Value (1), Value (8)))];
        Raw = ...;
        Type = System.Int32;}
```

Como vemos, nos devuelve un objeto **Expr\<int>** que está definido en el namespace **Microsoft.FSharp.Quotations** y en el que el tipo de **Expr** se infiere del resultado de la expresión. En nuestro ejemplo, devuelve un entero porque la expresión **2 + 3** se evalúa como tal.

Si utilizamos los símbolos **<@@ @@>** estaremos declarando una _Code Quotation_ sin tipo, es decir obtendremos una instancia de **Expr** sin el tipo que devuelve la expresión. En cualquier caso, podemos obtener un objeto de tipo **Expr** a partir de uno genérico **Expr<\_>** accediendo a la propiedad **Raw**.

```csharp
let exprtype = <@ 2 + 3 @>
let expr = expr.Raw
```

Dentro de una _Code Quotation_ no solo podemos escribir expresiones simples, si no que podemos escribir prácticamente cualquier código F#. Por ejemplo, el siguiente código es válido:

```csharp
let expr = <@
        let a = 1 + 3 
        10 * a
            @>
```

En esta ocasión al ejecutar el código, **expr** tendrá el siguiente valor:

```csharp
val expr : Quotations.Expr<int> =
    Let (a, Call (None, op_Addition, [Value (1), Value (3)]),
        Call (None, op_Multiply, [Value (10), a]))
```

Podemos ver en este resultado que la expresión es una serie de llamadas a funciones (**Let**, **Call**, **Value**) que podemos representar en un árbol:

![031915_0032_CodeQuotati1.png](/img/031915_0032_CodeQuotati1.png)

El compilador solo genera esta estructura, nosotros somos los responsables de decidir qué hacer con este árbol. De hecho, podemos evaluar el código de distintas formas según el propósito de nuestra aplicación.

También es importante ver que en este último ejemplo estamos declarando un enlace **let** y después lo estamos utilizando, esto es así porque una _Code Quotation_ debe incluir una expresión completa. Es decir, con expresiones como las siguientes obtendríamos un error de compilación ya que el bloque de código no está terminado.

```csharp
let expr = <@ let a = 1 + 2 @>

let expr = <@ let a x = 1 + x in let b x = a + x @>
```

Cuando utilizar Expr<’T> y Expr
-------------------------------

Hemos visto que podemos declarar las _Code Quotations_ con o sin tipo, para obtener un tipo genérico **Expr<’T>** o un tipo no genérico **Expr**. Se recomienda de forma general utilizar las _Code Quotations_ con tipo ya que nos fuerza a tener en cuenta las restricciones de tipo que de otra forma provocarían errores en tiempo de ejecución. Por ejemplo, podríamos hacer lo siguiente utilizando _Code Quotations_ sin tipo:

```csharp
let exprA = <@@ 1 @@>

let exprB = <@@ "hello " + %%exprA @@> // excepción en tiempo de ejecución
```

Otro inconveniente es que si utilizamos _Code Quotations_ sin tipo tendremos que hacer uso en muchas ocasiones de las anotaciones de tipo.

```csharp
let expr = <@ ["a", "b"] @>
<@ List.map id %expr @>

// exception
let l = <@@ [1] @@>
let l2 = <@@ List.map id %%l @@>

// ok
let l = <@@ [1] @@>
let l2 = <@@ List.map (id:int->int) %%l @@>
```

Sin embargo, las _Code Quotations_ sin tipo nos dan más flexibilidad, sin contar que, además, un árbol grande de expresión sin información de tipo se puede recorrer más rápidamente.

Pero recordemos que podemos convertir entre sin tipo y con tipo según necesitemos. Como hemos dicho podemos realizar un _upcast_ de una **Expr<\_>** a **Expr** para obtener la instancia sin tipo y **Expr.Cast** para ir en el otro sentido.

```csharp
open Microsoft.FSharp.Quotations

let untyped = <@@ let a = 1 + 2 in a @@>
let typed = Expr.Cast<int>(untyped)
```

Otro detalle de este ejemplo es que hemos utilizado los operadores **%** y **%%**, estos son los llamados operadores de inserción y permiten insertar un objeto de expresión de F# en una _Code Quotation_. El operador **%** se utiliza para insertar un objeto de expresión con tipo en una _Code Quotation_ con tipo y el operador **%%** se utiliza para insertar en una _Code Quotation_ sin tipo.

Descomponer el AST
------------------

Una vez tenemos una _Code Quotation_ podemos descomponer el AST utilizando patrones activos. En los módulos **Microsoft.FSharp.Quotations.Patterns** y **Microsoft.FSharp.Quotations.DerivedPatterns**, tenemos a nuestra disposición varios patrones activos que podemos analizar los objetos de expresión.

A continuación vamos a ver un ejemplo de cómo descomponer una expresión. No vamos a utilizar todos los posibles patrones que podrían aparecer en una expresión de código, simplemente vamos a comenzar viendo un par de ejemplos sencillos que nos ayudarán a conocer el funcionamiento de las _Code Quotations_.

```csharp
let decomposeCode (expr) =
    match expr with
    | Bool(bool) -> sprintfn "Constant Boolean %b" bool
    | Int32(int32) -> sprintfn "Integer with value %i" int32
    | Value(obj) -> sprintfn "Constant value %O" obj
```

En este primer ejemplo estamos definiendo la función **decomposeCode** que acepta una _Code Quotation_ como parámetro y devuelve la descripción del código. En la expresión de _pattern maching_ estamos utilizando los patrones activos que nos permiten saber qué tipo de expresión representa el código así como los parámetros.

Podemos utilizar la función **decomposeCode** pasando en la ventana _F# Interactive_ y obtendremos los siguientes resultados:

```csharp
decomposeCode <@ 1024 @>;;
val it : string = "Integer with value 1024"

decomposeCode <@ true @>;;
val it : string = "Constant Boolean true"

decomposeCode <@ 12. @>;;
val it : string = "Constant value (12, System.Double)" 
```

Naturalmente no solo podemos descomponer valores constantes, en el siguiente ejemplo vemos cómo descomponer una expresión condicional:

```csharp
let rec decomposeCode (expr) =
    match expr with
    | IfThenElse(guard, thenExpr, elseExpr) -> 
        
        let guardDesc = decomposeCode guard
        let thenDesc = decomposeCode thenExpr
        let elseDesc = decomposeCode elseExpr

        sprintf "Conditional
        \tIf  : %s
        \tThen: %s
        \tElse: %s" guardDesc thenDesc elseDesc
    | Bool(bool) -> sprintf "Constant Boolean %b" bool
```

Y probamos la función escribiendo en la consola **F# Interactive** lo siguiente:

```csharp
decomposeCode <@ true && true @>;;
val it : string =
    "Conditional
            If  : Constant Boolean true
            Then: Constant Boolean true
            Else: Constant Boolean false"
```

Este caso nos sirve, además, para ver cómo la expresión “false && true” se transforma en una expresión equivalente: **if false then true else false**.

Diferencias entre Expression y Code Quotations
----------------------------------------------

Al principio del post comenté que las _Code Quotations_ y el tipo **Expression** de C# son similares, sin embargo, existen algunas diferencias que tenemos que tener en cuenta.

La diferencia principal es que las _Expression_, que se introdujeron en .NET 3.0, solo pueden representar expresiones de C#. Las _Code Quotations_, sin embargo, pueden capturar cualquier expresión F# incluyendo las imperativas y pueden representar construcciones que solo están disponibles en F#. Por ejemplo, para funciones recursivas tenemos el patrón **LetRecursive** que reconoce expresiones que representan enlaces **let** recursivos y que en caso de utilizar árboles de expresión no las veríamos.

Otra diferencia es que las _Code Quotations_ han sido diseñadas de una forma más funcional. Por ejemplo, una llamada **foo a b** se representará como una llamada **App(App(foo, a),b)**.

Y una última diferencia es que las **Quotations** fueron diseñadas para que sean fácilmente procesadas utilizando recursividad. El módulo **ExprShape** contiene patrones que nos permiten manejar todas las posibles **Quotations** con solo 4 casos. Este punto lo veremos en una próxima entrada.

Por último, recordad que podemos traducir una _Code Quotation_ de F# en un árbol de expresión de C# utilizando **FSharp.Quotations.Evaluator**. Esto nos puede resultar útil si estamos utilizando alguna API de .NET que espera una Expressión.

Resumen
-------

En esta entrada hemos realizado una primera aproximación a las Code Quotations que nos permiten generar y usar expresiones de código F# mediante código y a través de los patrones activos definidos en los módulos **Quotations.Patterns** y **Quotations.DerivedPatterns** podemos descomponer el AST fácilmente.

Referencias
-----------

[Traversing and transforming F# quotations: A guided tour](http://fortysix-and-two.blogspot.com.es/2009/06/traversing-and-transforming-f.html)  
[Homoiconicidad](http://es.wikipedia.org/wiki/Homoiconicidad)  
[When to favor untyped over typed quotations in F#?](http://stackoverflow.com/a/10641360)
