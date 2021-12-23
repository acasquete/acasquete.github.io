---
title: Expresiones de consulta en F#
tags: [fsharp, functional_programming]
reviewed: true
header_fullview: query-expressions.png
---
En un post anterior vimos cómo podemos [crear operaciones asíncronas](/workflows-asincronos-con-f-sharp "Workflows asíncronos con F#") utilizando una característica denominada _workflows_ asíncronos, que nos permite escribir un código mucho más legible y que se adecúa mejor al paradigma de la programación funcional. Este tipo de construcción junto con las expresiones de secuencia, son casos de una construcción más general denominada **expresiones de cálculo**.

En esta entrada veremos otro tipo de expresiones de cálculo, las **expresiones de consulta**, que nos permiten **describir una consulta de forma declarativa** y conoceremos los operadores que nos van a permitir transformar, filtrar, ordenar y agrupar secuencias de objetos.

Si conoces C#, seguro que la siguiente construcción te recordará a la forma en que se escriben las consultas con LINQ.

```csharp
type customer = { id : int; name : string; }

let customers =
    [ { id = 10; name = "Global Associates";  }
        { id = 20; name = "AGS Group"; }
        { id = 30; name = "OIA Global Logistics";  }
        { id = 40; name = "World Transport Agency ";  }
        { id = 50; name = "Tigers Limited";  } ]

query {
    for c in customers do
    sortBy c.name 
    select c.name
    }
```

Para crear una expresión de consulta utilizamos la misma sintaxis que en una expresión de secuencia, pero utilizando **query** en lugar de **seq** y en el cuerpo de la expresión escribimos las transformaciones que queramos realizar sobre la secuencia utilizando los operadores **where**, **select**, **sortBy**, etc. Este tipo de construcción nos va a permitir simplificar muchísimo nuestro código, y es tremendamente potente ya que **dentro de una expresión de consulta vamos a poder utilizar cualquier código F#, a excepción de utilizar valores mutables y declarar nuevos tipos**, limitaciones, por otro lado, comunes a cualquier expresión de cálculo.

También podemos escribir el código anterior utilizando secuencias combinadas con el operador _pipe_ y las funciones de lista **sortBy** y **map**, más o menos, de la siguiente forma:

```csharp
customers
    |> List.sortBy (fun c->c.id)
    |> List.map(fun c->c.name)
```

Sin embargo, a pesar de que este ejemplo es totalmente declarativo y funcional, utilizando las expresiones de consulta obtendremos un código mucho más claro, mucho más cercano a la sintaxis SQL. Además, la ventaja más importante de las expresiones de consulta es que el código se puede convertir (utilizando *Type Providers*) en una consulta SQL que podemos ejecutar sobre cualquier origen de datos, por ejemplo una base de datos, evitando el tener que recuperar un gran conjunto de resultados y filtrarlos en cliente.

Los tipos de operadores permitidos dentro de las expresiones de consulta son similares a los métodos existentes en el [módulo Seq](http://msdn.microsoft.com/en-us/library/ee353635.aspx). Vamos a repasar a continuación los operadores más importantes. De entre todos los operadores disponibles, destacaremos aquellos en los que su uso no es tan evidente.

Operadores de selección
-----------------------

El operador de selección más común y que ya hemos visto en el primer ejemplo es **select**, análogo a **Seq.map**. Este operador proyecta cada elemento seleccionado en la consulta y además es posible utilizarlo para devolver otros tipos complejos. En el siguiente ejemplo se devuelve una secuencia de un nuevo tipo.

```csharp
type newcustomer = { name : string; }

query {
    for c in customers do
    select { name = c.name }
    }
```

El operador **contains** nos permite comprobar si la consulta resultante contiene al menos un elemento que satisfaga el predicado, de la misma forma que lo hace la función **Seq.exists**. En el siguiente ejemplo la consulta devolverá **true** o **false**, según si la lista de clientes contiene el nombre seleccionado.

```csharp
query {
    for c in customers do
    select c.name
    contains "AGS Group"
    }
```

El operador **count** devuelve el número de elementos que devuelve la consulta, al igual que **Seq.length**.

```csharp
query {
    for c in customers do
    select c
    count
    }
```

En este caso, en el que estamos devolviendo cada uno de los elementos sin realizar ninguna operación de transformación, operación **select** se puede omitir de la consulta. El siguiente ejemplo es equivalente al anterior:

```csharp
query {
    for c in customers do
    count
    }
```

El operador **nth** nos permite obtener un ítem según su índice. Por ejemplo, si queremos obtener el cuarto elemento de la lista de clientes, crearemos la siguiente consulta:

```csharp
query { for c in customers do nth 4 }
```

En este caso la consulta no nos devuelve una secuencia de elementos, sino que solo nos devolverá un objeto de tipo customer.

Mediante los operadores **skip**, **skipWhile**, **take** y **takeWhile** podemos paginar los resultados devueltos por una expresión de consulta. Mientras que con **skip** y **take** indicamos el número de elemento que queremos seleccionar o saltar, con **skipWhile** y **takeWhile** tenemos que indicar una condición. En el siguiente ejemplo obtenemos 2 elementos de la lista de clientes saltando los 2 primeros.

```csharp
query { for c in customers do
        skip 2
        take 2 }
```

Operadores de filtrado
----------------------

El primer tipo de operador que podemos utilizar para filtrar es **distinct**, con la que filtraremos los elementos duplicados de la secuencia.

```csharp
    query { for f in QuerySource.films do
    select f.releaseYear
    distinct }
```

El otro operador de filtro es **where**, basado en un predicado, en los que especificamos un criterio que tienen que satisfacer todos los elementos para que se incluyan en la secuencia. Para crear filtro incluimos el operador **where** seguido del predicado, una expresión booleana, que siempre colocaremos entre paréntesis.

```csharp
query { for c in customers do 
        where (c.id > 40) }
```

Tenemos que tener en cuenta que si obtenemos los datos de una base de datos con un campo que permite valores nulos, los datos se devolverán como tipo **Nullable\<int>** en lugar de **int**. Esto es importante, ya que los operadores de comparación no pueden trabajar con tipos “_nulables_”. Supongamos que tenemos la siguiente lista de clientes en la que hemos añadido un nuevo campo _orders_ que nos indica el número de pedidos de cada cliente.

```csharp
let customers =
    [ { id = 10; name = "Global Associates"; orders = Nullable<int>() }
        { id = 20; name = "AGS Group"; orders = Nullable<int&>() }
        { id = 30; name = "OIA Global Logistics"; orders = Nullable 5 }
        { id = 40; name = "World Transport Agency "; orders = Nullable 10 }
        { id = 50; name = "Tigers Limited"; orders = Nullable 33 } ]
```

Vemos además que en los 2 primeros casos no tenemos ningún valor asignado en este campo. Si intentamos realizar una consulta para mostrar los clientes con más de 5 pedidos de la forma que ya conocemos.

```csharp
query { for c in customers do 
        where (c.orders > 5) }
```

Obtendremos el siguiente error del compilador: “_The type ‘Nullable\<int>’ does not support the ‘comparison’ constraint. For example, it does not support the ‘System.IComparable’ interface_”. Para poder trabajar con tipos que acepten nulos, tendremos que utilizar los operadores definidos en el módulo **NullableOperators** del namespace **Microsoft.FSharp.Linq**.

```csharp
open Microsoft.FSharp.Linq.NullableOperators

query { for c in customers do 
        where (c.orders ?> 5) }
```

Ahora la expresión de consulta se compilará sin errores y nos devolverá los clientes que cumplen con el criterio. Los operadores “nulables” son los mismos que utilizamos con tipos no nulos, pero se indica con el signo ? el lado donde está el campo con un posible valor nulo.

El operador **find** es similar al **where** excepto que solo devuelve un solo elemento. Para obtener el primer cliente que tiene pedidos utilizaremos la siguiente consulta.

```csharp
query { for c in customers do 
        find (c.orders ?> 0) }
```

En este caso nos devuelve el primero, pero puede que no sea el único resultado. Si necesitamos obtener el primer resultado y además asegurarnos de que sea el único tenemos que utilizar el operador **exactlyOne**.

```csharp
query { for c in customers do 
        where (c.orders ?> 10) 
        exactlyOne }
```

Si el resultado de la consulta contuviese más de un elemento o no devolviese ningún elemento, el operador **exactlyOne** lanzaría una excepción **InvalidOperationException**. Para evitar una excepción en el caso de que no devuelva elementos podemos utilizar el operador **exactlyOneOrDefault**, sin embargo este operador seguirá lanzando excepción la secuencia a devolver contiene más de un elemento.

Operadores de ordenación
------------------------

Disponemos de operadores ordenación para definir el orden de la consulta. Los operadores para definir el primer campo de ordenación son **sortBy** y **sortByDescending**, y para añadir nuevos valores de ordenación utilizaremos **thenBy** y **thenByDescencding**. También tenemos variaciones de estos operadores para soportar campos “nulables”.

En el siguiente ejemplo estamos ordenando la lista de clientes por número de pedidos, utilizando el operador **sortByNullable**, ya que el campo **orders** es de tipo **Nullable\<int>** y como segundo campo de ordenación indicamos **name**.

```csharp
query { for c in customers do 
        sortByNullable c.orders 
        thenBy c.name
        }
```

Operadores de agrupación
------------------------

Las expresiones de consulta nos proporcionan dos operadores de agrupación. Estos operadores producen una secuencia intermedia de tipo **IGrouping<_,_\>** que podemos utilizar dento de la consulta.

Con **groupBy** indicamos el valor de clave por el cual queremos agrupar y la secuencia intermedia con la palabra clave **into**. Cada grupo incluye el valor clave y una secuencia hija que contiene todos los elementos de la secuencia origen que coinciden con la clave. En el siguiente ejemplo hemos creado un nuevo conjunto de datos en el que hemos incluido un nuevo campo **city**.

```csharp
let customers =
    [ { id = 10; name = "Global Associates"; orders = Nullable<int&>(); city = "Barcelona" }
        { id = 20; name = "AGS Group"; orders = Nullable 5; city = "Barcelona" }
        { id = 30; name = "OIA Global Logistics"; orders = Nullable 5; city = "Madrid" }
        { id = 40; name = "World Transport Agency "; orders = Nullable 10; city = "Madrid" }
        { id = 50; name = "Tigers Limited"; orders = Nullable 33; city = "Madrid" } ]


query { for c in customers do
        groupBy c.city into g 
        select (g.Key, g) }
```

El resultado de esta consulta será el siguiente:

```csharp
val it : seq<string * Linq.IGrouping<string,customer>> =
    seq
    [("Barcelona", seq [{id = 10;
                            name = "Global Associates";
                            orders = null;
                            city = "Barcelona";}; {id = 20;
                                                name = "AGS Group";
                                                orders = 5;
                                                city = "Barcelona";}]);
        ("Madrid",
        seq [{id = 30;
            name = "OIA Global Logistics";
            orders = 5;
            city = "Madrid";}; {id = 40;
                                name = "World Transport Agency ";
                                orders = 10;
                                city = "Madrid";}; {id = 50;
                                                    name = "Tigers Limited";
                                                    orders = 33;
                                                    city = "Madrid";}])]
```

Como vemos, el resultado es una secuencia de tuplas de **string** (que contiene la clave de agrupación) y **IGrouping** (que contiene la secuencia de elementos que cumplen con la clave).

En lugar de devolver toda la secuencia origen, podemos utilizar el operador **groupValBy** para especificar los campos que queremos incluir en el resultado. Este operador acepta dos argumentos, el valor a incluir en el resultado y el valor clave. En este ejemplo agrupamos, al igual que en el ejemplo anterior, por el valor city, pero seleccionamos solo los campos name y orders, que son los que aparecerán en la secuencia hija.

```csharp
query { for c in customers do
        groupValBy (c.name, c.orders) c.city into g 
        select (g.Key, g) }
```

El resultado en este caso será el siguiente:

```csharp
val it : seq<string * Linq.IGrouping<string,(string * Nullable<int>)>> =
    seq
    [("Barcelona", seq [("Global Associates", null); ("AGS Group", 5)]);
        ("Madrid",
        seq
        [("OIA Global Logistics", 5); ("World Transport Agency ", 10);
            ("Tigers Limited", 33)])]
```

Con los operadores **sumBy**, **averageBy**, **minBy**, **maxBy** podemos totalizar valores, obtener la media y los valores mínimo y máximo. A estos operadores tenemos que añadir las variantes para trabajar con valores nulables.

En el siguiente ejemplo se muestra como obtener la suma de pedidos de todos los clientes:

```csharp
query { for c in customers do
        sumByNullable c.orders
        }
```

Y la siguiente muestra la media de pedidos por cliente. En este caso tenemos que realizar el cast a **Nullable.float** ya que no es posible utilizar el operador **averageByNullable** con tipos enteros.

```csharp
open Microsoft.FSharp.Linq

query { for c in customers do
        averageByNullable (Nullable.float c.orders)
        }
```

“join” y “joinGroup”
--------------------

Los últimos operadores que vamos a ver son los que nos permiten enlazar múltiples orígenes.

El primer operador es **join** que nos permite correlacionar valores de una secuencia con los de otra. Tenemos que incluir una expresión **join** para cada secuencia e identificar la relación existente entre ellas. Para mostrar los próximos casos, hemos ampliado el código con una lista de pedidos y cada una de los pedidos tiene un campo **id\_customer** que lo relación con el cliente. Este campo es el que utilizamos para enlazar con el id de pedido de la lista de clientes.

```csharp
type customer = { id : int; name : string; city: string }
type order = { id : int; id_customer: int; status : string; total: float }

let customers =
    [ { id = 10; name = "Global Associates"; city = "Barcelona" }
        { id = 20; name = "AGS Group"; city = "Barcelona" }
        { id = 30; name = "OIA Global Logistics"; city = "Madrid" }
        { id = 40; name = "World Transport Agency "; city = "Madrid" }
        { id = 50; name = "Tigers Limited"; city = "Madrid" } ]

let orders =
    [ { id = 1; id_customer = 10; status = "PND"; total = 1995.0 }
        { id = 2; id_customer = 10; status = "PND"; total = 10995.0 }
        { id = 3; id_customer = 20; status = "PND"; total = 13990.0 }
        { id = 4; id_customer = 20; status = "PND"; total = 30400.5 }
        { id = 5; id_customer = 20; status = "PND"; total = 1995.0 }
        { id = 6; id_customer = 40; status = "PND"; total = 995.0 }
        { id = 7; id_customer = 40; status = "PND"; total = 55000.0 }
        { id = 8; id_customer = 50; status = "PND"; total = 1000.0 }
        ]

query { for c in customers do
        join o in orders on (c.id = o.id_customer)
        select (c.name, o.id, o.total) }
```

El operador **groupJoin** nos permite unir dos secuencias pero en lugar de seleccionar los elementos que satisfacen el criterio de unión individualmente, se proyecta cada ítem que satisface el criterio de unión en otra secuencia que podemos utilizar dentro de la consulta.

```csharp
query { for c in customers do
        groupJoin o in orders on (c.id = o.id_customer) into result
        select (c.name, result) }
```

El resultado de esta consulta es el siguiente

```csharp
val it : seq<string * seq<order>> =
    seq
    [("Global Associates", 
        seq [{id = 1; id_customer = 10; status = "PND"; total = 1995.0;}; 
            {id = 2; id_customer = 10; status = "PND"; total = 10995.0;}]);
        ("AGS Group",
        seq [{id = 3; id_customer = 20; status = "PND"; total = 13990.0;}; 
            {id = 4; id_customer = 20; status = "PND"; total = 30400.5;}; 
            {id = 5; id_customer = 20; status = "PND"; total = 1995.0;}]);
        ("OIA Global Logistics", [||]);
        ("World Transport Agency ", 
        seq [{id = 6; id_customer = 40; status = "PND"; total = 995.0;}; 
            {id = 7; id_customer = 40; status = "PND"; total = 55000.0;}]);
```

Si en lugar de devolver la secuencia de pedidos por cliente con todos los campos, queremos devolver solo algunos campos, podemos realizar otra consulta dentro de la selección. En el siguiente ejemplo para mostrar el estado y el total de cada pedido.

```csharp
query { for c in customers do
        groupJoin o in orders on (c.id = o.id_customer) into result
        select (c.name, query { for r in result do select (r.status, r.total) } ) }
```

En este caso el resultado será el siguiente:

```csharp
val it : seq<string * seq<string * float>> =
    seq
    [("Global Associates", seq [("PND", 1995.0); ("PND", 10995.0)]);
        ("AGS Group", seq [("PND", 13990.0); ("PND", 30400.5); ("PND", 1995.0)]);
        ("OIA Global Logistics", seq []);
        ("World Transport Agency ", seq [("PND", 995.0); ("PND", 55000.0)]); ...]
```

En este ejemplo vemos que la secuencia de pedidos del cliente que no tiene pedidos está vacía. Si utilizamos el operador **leftOuterJoin** la secuencia contendrá un valor predeterminado, en este caso null.

```csharp
query { for c in customers do
        leftOuterJoin o in orders on (c.id = o.id_customer) into result
        select (c.name, result) }

val it : seq<string * seq<order>> =
    seq
    [("Global Associates", 
        seq [{id = 1; id_customer = 10; status = "PND"; total = 1995.0;}; 
            {id = 2; id_customer = 10; status = "PND"; total = 10995.0;}]);
        ("AGS Group",
        seq [{id = 3; id_customer = 20; status = "PND"; total = 13990.0;}; 
            {id = 4; id_customer = 20; status = "PND"; total = 30400.5;}; 
            {id = 5; id_customer = 20; status = "PND"; total = 1995.0;}]);
        ("OIA Global Logistics", seq { null });
        ("World Transport Agency ", 
        seq [{id = 6; id_customer = 40; status = "PND"; total = 995.0;}; 
            {id = 7; id_customer = 40; status = "PND"; total = 55000.0;}]);
```

En este caso al tener un valor nulo, no podemos iterar como lo hemos hecho en el ejemplo anterior ya que obtendríamos un error de referencia nula.

Resumen
-------

En esta entrada hemos visto como construir expresiones de consulta con los operadores principales para filtrar, ordenar y agrupar.
