---
title: Workflows asíncronos con F#
tags: [fsharp, functional_programming]
reviewed: true
header_fullview: beasync.png
---
Continuamos con este post la serie introductoria a los conceptos básicos de programación funcional con F#. En esta ocasión trataremos los flujos de trabajos asíncronos o, en inglés, _asynchronous workflows_.

Uno de los aspectos más importantes del paradigma de la programación funcional es que facilita la creación de procesos asíncronos, gracias sobre todo al uso de la inmutabilidad y de la programación declarativa. En F#, además de poder hacer uso, como en cualquier lenguaje .NET, de la _Task Parallel Library_ (TPL) para implementar paralelismo a nivel de datos y tareas, podemos utilizar una característica propia del lenguaje denominada _asynchronous workflows_. Me voy a referir a este termino de aquí en adelante con su denominación inglesa, ya que me parece mucho más natural que su traducción al español, flujos de trabajo asíncronos.

**La ventaja de los _workflows_ asíncronos respecto a la TPL es que podemos crear operaciones asíncronas con una sintaxis que se ajusta mejor al paradigma de programación funcional, permitiéndonos escribir un código mucho más legible.**

Veamos el primer ejemplo con la sintaxis básica de una expresión asíncrona, en la que queremos obtener el contenido de una página web a partir de una URI.

```csharp
async {
    let client = new System.Web.WebClient()
    return! client.AsyncDownloadString(System.Uri("http://www.casquete.es"))
}
```

Los _workflows_ asíncronos se basan en el tipo **Microsoft.FSharp.Control.Async<‘T>**, pero, como vemos en el código, en lugar de crear instancias de este tipo directamente, las expresiones se crean mediante la palabra clave **async**, de forma parecida a cuando creamos una secuencia con **seq** o una consulta con **query**. De hecho, tanto **las expresiones de consulta y las expresiones asíncronas son casos de una construcción más general llamada expresiones de cálculo (_computation expressions_)** de las que hablaremos en otro post.

Todo el código incluido dentro de las llaves { }, son las expresiones que queremos que se ejecuten de forma asíncrona, pero es importante destacar que con este código no estamos ejecutando la petición, solo estamos creando una instancia de Async<string> que representa la petición. Es decir, un valor de tipo **Async<‘T>** representa una porción de código que generará un valor de tipo **‘T** en algún momento futuro. Para ver exactamente lo que significa esto, solo tenemos que ejecutar el código anterior en la consola interactiva de F#, en la que obtendremos el siguiente resultado:

```csharp
val it : Async&lt;string> = Microsoft.FSharp.Control.FSharpAsync`1[System.String]
``` 

Como vemos, no se ha ejecutado la petición web, únicamente hemos obtenido una instancia de Async de tipo **String**. Solo cuando iniciemos el _workflow_ y se complete con éxito, obtendremos una cadena como resultado. Veremos un poco más adelante los métodos que tenemos para invocar los _workflows_, pero antes examinemos otra característica de la sintaxis que hemos introducido en este primer ejemplo.

Si nos fijamos en la última línea, vemos que hemos utilizado la palabra clave **return** seguida del operador ! (pronunciado _bang_). Esto indica a la expresión de cálculo (_computation expression_) que se está realizando otra operación asíncrona y que se debe esperar a sus resultados. De esta forma, **podemos invocar a otros _workflows_ desde un _workflow_ asíncrono y esperar resultados sin bloquear el hilo de ejecución**. En el ejemplo estamos llamando al método **AsyncDownloadString**, método extensor de la clase WebClient, que devuelve un cálculo asíncrono (un objeto async) que esperará la descarga de la URI especificada. En este caso usamos la palabra **return!** para invocar el _workflow_ y devolver directamente el resultado, pero podemos utilizar el operador ! con las palabras clave let, do y use.

En el caso de **let!**, nos permite invocar un _workflow_ asíncrono y para enlazar el resultado a un nombre. Y de forma similar, con **use!** invocamos un _workflow_ asíncrono que devuelve como resultado un objeto **IDisposable**, que se enlaza a un nombre y lo libera al salir del ámbito. Por ejemplo, si en lugar de devolver el resultado de la petición web directamente, quisiéramos devolver solo una lista con los enlaces que contiene, podríamos crear el siguiente _workflow_:

```csharp
async {
    let client = new WebClient()
    let! content = client.AsyncDownloadString(System.Uri("http://casquete.es"))
    let pattern = "href=\s*\"[^\"h]*(http://[^&\"]*)\""
    return [ for m in Regex.Matches(content, pattern) -> m.Groups.Item(1).Value ]
}
```

En este código, utilizamos **let!** Para invocar **AsyncDownloadString** y enlazar el resultado al valor **content**. Después de buscar las coincidencias mediante una expresión regular, generamos y devolvemos una lista con el valor de cada enlace, utilizando en este caso la palabra clave **return**. Si quisiéramos invocar un _workflow_ asíncrono que no devuelve ningún valor, podríamos utilizar **do!** o su forma equivalente utilizando **let!**

```csharp
do! AsyncNoReturnValue()  
let! _ = AsyncNoReturnValue()  // Forma equivalente usando let!
```

Y para mostrar un ejemplo de **use!** veamos cómo podemos crear la misma petición web de la siguiente forma:

```csharp
async {
    let req = WebRequest.Create "http://www.casquete.es"
    use! response = req.AsyncGetResponse()
    use stream = response.GetResponseStream()
    use reader = new StreamReader(stream)
    return reader.ReadToEnd()
}
```

Con este código, estamos llamando al método extensor **AsyncGetResponse** que esperará la respuesta de la petición web y devolverá un objeto **WebResponse** que se liberará al salir del ámbito, en este caso, al final del _workflow_.

Iniciar un _workflow_ asíncrono
-------------------------------

Hemos comentado antes que es necesario invocar los _workflows_ explícitamente ya que no se inician automáticamente al declararlos. Los métodos que podemos utilizar para iniciar un _workflow_ asíncrono son los siguientes:

**Start** – Inicia un _workflow_ asíncrono, pero no espera un resultado. **RunSynchronously** – Inicia un _workflow_ asíncrono y espera su resultado. **StartImmediate** – Inicia el _workflow_ asíncrono utilizando el hilo actual. **StartWithContinuations** – Inicia el _workflow_ utilizando el hilo actual e invocando tres funciones de continuación (success, exception o cancelation) dependiendo de si la operación tiene éxito o no.

Además del comportamiento de cada uno de estos métodos, existe una diferencia añadida. Los métodos **Start** y **StartInmediate** requieren que se pase como parámetro un _workflow_ asíncrono que no devuelva ningún valor, mientras que **RunSynchronously** y **StartWithContinuations** permiten cualquier _workflow_, independientemente del tipo de valor devuelto. Esto significa que si intentamos iniciar el _workflow_ del primer ejemplo mediante el método **Start** como se muestra a continuación.

```csharp
async {
    let client = new System.Web.WebClient()
    return! client.AsyncDownloadString(System.Uri("http://www.casquete.es")) 
}
|> Async.Start
```

Obtendremos el siguiente error de compilación:

```bash
Script.fsx(10,4): error FS0193: Type constraint mismatch. The type  Async<string> is not compatible with type Async<unit> The type 'unit' does not match the type 'string'
``` 

Como el objetivo del _workflow_ es obtener el contenido de la web y no ignorarlo, vamos a tener que encapsular este _workflow_ en una función y crear otro _workflow_ que realice la llamada al primero y muestre el resultado en la consola. Tenemos el ejemplo con el siguiente código:

```csharp
let getContent =
    async {
        let client = new System.Net.WebClient()
        return! client.AsyncDownloadString(System.Uri("http://localhost"))
    }

async {
    let! content = getContent
    content |> printf "%s" }
|> Async.Start
```

Las llamadas a los métodos **StartInmediate**, **RunSynchronously** se realizan de la misma forma, pero veamos cómo es la sintaxis utilizando continuaciones.

Funciones de continuación
-------------------------

El método **StartWithContinuations** requiere que pasemos un _workflow_ y tres funciones que se ejecutarán dependiendo de si el _workflow_ se completa con éxito, lanza una excepción o es cancelado.

```csharp
Async.StartWithContinuations(
    getContent,
    (printfn "%s"),
    (printfn "Exception: %O"), 
    (printfn "Cancelled")
    )
```

En este ejemplo, si la ejecución de la llamada al método **getContent** se completa con éxito se mostrará el contenido, si se produce una excepción (que, por ejemplo, podemos provocar utilizando una URI inválida) se mostrará el mensaje de la excepción y, por último, si se cancela se ejecutará la continuación de cancelación y se mostrará el mensaje “Cancelled”.

El método **StartWithContinuations** permite un quinto parámetro que nos permitirá pasar un _Token_ de cancelación. En casos sencillos, en los que solo iniciamos un _workflow_, no es necesario utilizar un token personalizado y podemos hacer uso del token de cancelación por defecto de la clase **Async** para controlar la cancelación. Para cancelar el _workflow_ más reciente sin un token de cancelación específico, tenemos utilizaremos el método **CancelDefaultToken**.

```csharp
Async.StartWithContinuations(
    getContent,
    (printfn "%s"),
    (printfn "Exception: %O"), 
    (printfn "Cancelled")
    )

Async.CancelDefaultToken
```

Control de excepciones
----------------------

Si solo queremos manejar las excepciones lanzadas en un _workflow_, podemos utilizar el método **Catch** de la clase **Async**, que nos ofrece un enfoque más funcional.

**Catch** devuelve un valor de tipo **Choice<’T, exn>**, donde **‘T** es el tipo de retorno del _workflow_ asíncrono y **exn** es la excepción que se ha lanzado desde el _workflow_. Lo interesante de este tipo, es que es una unión discriminada (tipo de dato que vimos [en el post anterior](/uniones-discriminadas-y-jerarquia-de-objetos/)) con solo 2 casos de unión: **Choice1Of2** y **Choice2Of2**. El primero, **Choice1Of2**, representa la operación completada con éxito y contiene el resultado del _workflow_ y el segundo, **Choice2Of2**, representa la operación completada con errores y contiene la excepción lanzada dentro del _workflow_.

Por ejemplo, el siguiente código muestra cómo podemos crear y ejecutar una operación asíncrona, manejando las posibles excepciones que puedan ocurrir.

```csharp
open System
open System.Net

let getContent =
    async {
        let client = new WebClient()
        return! client.AsyncDownloadString(System.Uri("http://www.casquete.es"))
    }

getContent
|> Async.Catch
|> Async.RunSynchronously
|> function
    | Choice1Of2 result -> Some result
    | Choice2Of2 ex ->
        match ex with
        | :? System.Net.WebException ->
                ex.Message |> printf "Caught WebException: %s" 
        | ex ->
                ex.Message |> printf "Exception: %s"
        None
```

En este ejemplo se llama a la función **getContent** para crear un _workflow_ asíncrono que se canaliza a **Async.Catch** para crear otro _workflow_ que se canalizará a su vez a **Async.RunSynchronously** para ejecutarlo y esperar su resultado. Finalmente, utilizando _pattern-matching_ devolvemos el resultado con **Some** si la operación se ha podido completar y **None** en caso contrario.

Resumen
-------

En este post hemos visto cómo crear procesos asíncronos mediante una característica propia de F# denominada _workflows_ asíncronos. Hemos visto los distintos métodos que tenemos para iniciarlos y cómo manejar excepciones mediante funciones continuación y mediante el método Catch que devuelve una unión discriminada y nos permite implementar la gestión de excepciones con un código más comprensible y funcional.