---
title: Programación basada en agentes
tags: [fsharp, functional_programming]
---
![Agents](/img/agents.png){:.fullview}

F# tiene incorporado un mecanismo de procesamiento de mensajes que consiste básicamente en un **sistema de colas que permite enrutar mensajes de forma asíncrona utilizando memoria compartida**. Este sistema, muy parecido a los agentes de Erlang, es especialmente útil cuando tenemos múltiples clientes que tienen que realizar una petición a un único servidor.

Para poder procesar las colas de mensajes, vamos a crear distintos agentes que escanearán las colas en busca de mensajes que cumplan con un determinado criterio y que estén relacionados con la funcionalidad que hayamos designado a cada agente.

La clase con la que implementaremos los agentes es **MailboxProcessor<’T>**, pero como vamos a referirnos constantemente a las instancias de esta clase como agentes, es una práctica habitual crear un alias de esta clase como **Agent<\`T>** de la forma siguiente:

```csharp
type Agent<'T> = MailboxProcessor<'T>
```

En la práctica, podremos trabajar con miles de instancias de esta clase, los llamados agentes o “actores”, ya que su huella en memoria es muy pequeña.

El primer ejemplo que vamos a ver es cómo trabajar de forma aislada con un agente. Comenzaremos creando un agente que se encargará de procesar un mensaje de un tipo en determinado y veremos cómo enviar un mensaje a ese agente. Más adelante nos ocuparemos de cómo trabajar con los agentes de forma coordinada.

La forma de crear un agente es mediante el método **Start**, al que pasaremos una función que se encargará de procesar los mensajes. El parámetro de esta función recibe por convención el nombre de _inbox_ ya que es donde recibiremos los nuevos mensajes.

```csharp
let agent = Agent.Start(fun inbox -> …)
```

Con el fin de poder leer todos los nuevos mensajes de forma continua e indefinida, crearemos una función recursiva para obtener el contenido del mensaje.

```csharp
let agent = Agent.Start(fun inbox -> 
    let rec loop () = async { 
        let! message = inbox.Receive() 
        printfn "Hello %s!" message
        return! loop()
    }
    loop()
)
```

En este código, la función **loop** es un _workflow_ asíncrono que, en primer lugar, obtiene el mensaje de la cola llamando al método **Receive** y muestra el contenido del mensaje en la consola. Justo después, realizamos la llamada recursiva a la función **loop** para leer el siguiente mensaje. El último loop es para iniciar el bucle de lectura de mensajes.

Podemos ejecutar el código anterior directamente en una sesión de F# _Interactive_, con lo que crearemos e iniciaremos el agente que esperará de forma asíncrona hasta que se reciba un mensaje.

Mientras la cola esté vacía, el método **Receive** bloqueará la ejecución del _workflow_ asíncrono, aunque sin bloquear ningún hilo, hasta que llegue el siguiente mensaje.

Para enviar un mensaje, podemos utilizar el método **Post** del agente de la forma siguiente:

```csharp
"World" |> agent.Post
```

Cuando se reciba el mensaje, se llamará a la función **loop** que recuperará y mostrará el mensaje de bienvenida por la consola y esperará a recibir el siguiente mensaje. Podemos enviar múltiples mensajes utilizando, por ejemplo, una lista y la función **List.iter** para realizar una llamada a **agent.Post** por cada uno de los elementos de la lista.

```csharp
["World"; "Agent"; "Async"] 
|> List.iter(agent.Post)
```

En este primer ejemplo, el tipo genérico **string** que devuelve el método **Receive** se está infiriendo del primer uso que hemos hecho del valor. Como un agente tan solo puede procesar mensajes de un tipo, normalmente utilizaremos una unión discriminada para declarar todos los tipos de mensajes que puede procesar el agente.

```csharp
type Message = 
    | MessageA of string
    | MessageB of int
```

En este caso hemos creado una unión discriminada con dos casos que aceptan un valor de tipo cadena y otro de tipo entero. Ahora podemos modificar la definición del agente que hemos creado antes para que procese estos tipos de mensaje.

```csharp
let messageAgent = Agent<Message>.Start(fun inbox -> 
    let rec loop () = async { 
        let! message = inbox.Receive() 
        match message with
        | MessageA x -> printfn "This is a string: %s" x 
        | MessageB x -> printfn "This is an integer: %d" x 
        return! loop()
    }
    loop()
)
```

Aquí mediante _pattern matching_ estamos obteniendo el tipo de mensaje que hemos recibido y mostramos un mensaje distinto para cada uno. Para probar el correcto funcionamiento del agente podemos enviar mensajes de distintos tipos, de la misma forma que lo hemos hecho en el ejemplo anterior.

```csharp
    > MessageA "asdfg" |> messageAgent.Post
    MessageB 1234567 |> messageAgent.Post;;
    This is a string: asdfg
    This is an integer: 1234567
```

Filtrar mensajes
----------------

En los ejemplos vistos hasta este momento, hemos utilizado el método **Receive** para obtener el contenido de los mensajes. En el momento que hacemos esto, el mensaje se elimina de la cola. Aunque este comportamiento es el que utilizaremos habitualmente en la mayoría de escenarios, la clase **MailboxProcessor** nos proporciona el método **Scan** para poder filtrar los mensajes antes de procesarlos. Siguiendo con el mismo ejemplo que hemos iniciado en el apartado anterior, el siguiente código muestra como podemos filtrar los mensajes según su tipo.

```csharp
let filterAgent =  Agent<Message>.Start(fun inbox ->
    let rec loop () = 
        inbox.Scan(
        fun (x) -> 
        match x with
        | MessageB y -> Some (async { 
            printfn "Filtered message: %d" y 
            return! loop() 
            })
        | _ -> None)
    loop())
``` 

En este ejemplo, la función recursiva **loop** llama al método **Scan** al que le pasamos la función que se utiliza para filtrar el mensaje. Cuando el mensaje es del tipo **MessageB**, es decir, del tipo que queremos procesar, tenemos que devolver un **Some<Async<’T»** y en caso contrario **None**. En el primer caso, el método **Scan** recuperará el mensaje de la cola e invocará el _workflow_ asíncrono. Y en el caso de que devolvamos _None_, el método **Scan** continuará con otro mensaje.

Para probar este nuevo agente, simplemente tenemos que enviar varios mensajes y comprobaremos que solo aparecerán en consola los de tipo **MessageB**.

```csharp
[ MessageA "ABC"
    MessageB 123
    MessageB 456
    MessageA "CDB" ] |> List.iter(filterAgent.Post)
```

Todo los mensajes de tipo **MessageA** permanecerán en la cola de forma indefinida. Podemos conocer el número de mensajes que hay en la cola, accediendo a la propiedad **CurrentQueueLength** del agente. No obstante, no existe método para eliminar todos los mensajes de la cola, así que si queremos vaciar la cola, simplemente tendremos que invocar el método **Receive** para todos los mensajes de la cola. Sin embargo, si tenemos que hacer esto durante el ciclo de vida de nuestro programa, seguramente será indicador de algún problema de diseño.

Respondiendo mediante el canal de respuesta
-------------------------------------------

Los ejemplos de agentes vistos hasta ahora son muy simples, en los que procesan un mensaje de forma aislada, sin comunicación con el mundo exterior. Sacaremos toda la potencia de la programación basada en agentes cuando tengamos agentes que se comuniquen con otros agentes, cuando enviemos mensajes a otros agentes y procesemos sus respuestas, o cuando los agentes creen nuevos agentes para delegar alguna responsabilidad.

Siguiendo con el mismo ejemplo, vamos a crear un nuevo tipo de mensaje para que en lugar de que sea el mismo agente el encargado de mostrar el resultado por la consola, devuelva un valor a la función que envía el mensaje.

El primer cambio que realizaremos es declarar un nuevo caso de unión en el que tendremos un nuevo valor asociado de tipo **AsyncReplyChannel<int>** que se utilizará para tener acceso al canal de respuesta.

```csharp
type Message = 
    | MessageA of string
    | MessageB of int
    | MessageC of string * AsyncReplyChannel<int>
```

En el siguiente paso modificaremos la función **loop** para cubrir el nuevo caso de unión en el que extraemos el mensaje y el canal y llamamos al método **Reply** del canal para enviar el mensaje de respuesta. En este caso hemos declarado este tipo como entero, que utilizamos, a modo de ejemplo, para devolver la longitud del mensaje.

```csharp
let replyAgent = Agent.Start(fun inbox -> 
    let rec loop () = async { 
        let! message = inbox.Receive() 
        match message with
        | MessageA x -> printfn "This is a string: %s" x 
        | MessageB x -> printfn "This is an integer: %d" x 
        | MessageC (msg,channel) -> channel.Reply (msg.Length)
        return! loop() }
    loop())
```  

Ahora para enviar un mensaje al agente y esperar la respuesta tenemos que utilizar el método **PostAndReply** de la forma siguiente.

```csharp
replyAgent.PostAndReply(fun c -> MessageC("Hello World!", c)) 
|> printfn "Length string: %i"
```

El método **PostAndReply**, a diferencia del método **Post**, crea internamente un canal de respuesta y utiliza la función lambda para crear el mensaje pasando el canal. El mensaje se envía al agente y se bloquea el _workflow_ hasta que el agente invoca al método **Reply** del canal.

Si tuviésemos que utilizar **PostAndReply** desde un workflow asíncrono, disponemos del método análogo **AsyncPostAndReplay**, con el que obtendremos el resultado de forma asíncrona sin bloquear el _thread_.

Manteniendo el estado
---------------------

Ahora que hemos visto cómo crear agentes y cómo devolver una respuesta, vamos a ver en el cómo crear un agente que mantenga el estado. Para mostrar esto vamos a partir de un ejemplo típico en este tipo de escenario, vamos a implementar un agente que procese unas operaciones básicas sobre una cuenta bancaria: ingresar, retirar y obtener saldo.

Comenzamos definiendo los tipos de mensajes mediante una unión discriminada:

```csharp
type Operation = 
    | Deposit of decimal
    | Withdraw of decimal
    | Balance of AsyncReplyChannel<decimal>
```

Hemos definido 3 casos de unión que representan las operaciones básicas que se pueden realizar sobre una cuenta bancaria. El caso de unión **Balance**, nos permite preguntar al agente por su estado, por el saldo actual, utilizando un canal de respuesta asociado. Con estos datos, podemos crear el agente de la forma siguiente:

```csharp
let accountAgent = Agent.Start(fun inbox -> 
    let rec loop balance = async { 
        let! message = inbox.Receive() 
        let newBalance =
            match message with
            | Deposit q -> balance + q
            | Withdraw q -> balance - q 
            | Balance c -> c.Reply balance
                            balance
        return! loop newBalance }
    loop 0.0m)
``` 

La parte importante del código anterior es ver cómo el agente mantiene el estado, el saldo de la cuenta, pasando el valor **newBalance** como argumento de la función **loop**. Para ver al agente en funcionamiento solo tenemos que enviar algunos mensajes como ya hemos visto anteriormente.

```csharp
[
Deposit 1000.0m
Deposit 550.0m
Withdraw 69.5m
] 
|> List.iter (accountAgent.Post)
```

Podemos repetir este proceso las veces que queramos y una vez procesados todos los mensajes, podemos preguntar al agente por el valor actual.

```csharp
let balance = accountAgent.PostAndReply(Balance)
```

Resumen
-------

En esta entrada hemos visto una introducción a la programación basada en agentes o “actores” mediante la clase **MailboxProcessor** que F# lleva incorporada.

Hemos visto cómo implementar un agente que procese varios tipos de mensajes utilizando uniones discriminadas y _pattern matching_, cómo podemos enviar una respuesta al método que invoca la llamada mediante un canal de respuesta y, por último, hemos visto cómo mantener el estado en un agente pasando el valor en el bucle de mensajes.

Pero con todo esto no hemos hecho más que rascar la superficie de la programación con agentes. En próximas entradas veremos temas como la gestión de excepciones, agentes cancelables y diferencias entre el sistema de agentes de F# y el modelo de actores.

Referencias
-----------

[Messages and Agents - F# for fun and profit](http://fsharpforfunandprofit.com/posts/concurrency-actor-model/)  
Syme, Don; Granicz, Adam; Cisternino, Antonio. Expert F# 3.0. 3a edición. New York: Apress, 2012. ISBN 978-1-4302-4650-3  
Petricek, Tomas; Skeet, Jon. Real-World Functional Programming. New York: Manning Publications, 2009. ISBN 978-1933988924
