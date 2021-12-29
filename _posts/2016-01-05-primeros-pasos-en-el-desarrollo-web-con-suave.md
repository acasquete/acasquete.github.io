---
title: Primeros pasos en el desarrollo web con Suave
tags: [fsharp, suaveio, functional_programming, web]
reviewed: true
header_fullview: suave.jpeg
---
En la entrada anterior vimos cómo implementar [Hypermedia en una API REST utilizando Suave](/building-an-hypermedia-rest-api-with-fsharp-and-suave-io), en la que partíamos de una pequeña solución y dábamos por conocidos algunos conceptos. En esta entrada damos a un pequeño paso atrás para introducir el funcionamiento y conceptos básicos de [Suave](https://suave.io/) para poder afrontar y crear un proyecto web. 

A través de varios posts, iremos conociendo las distintas características de Suave con los que cualquier desarrollador, incluso sin conocimientos profundos del lenguaje, podrá crear y desplegar una web realizada íntegramente en F#.

> “Suave es una librería de F# para desarrollo web que proporciona un servidor ligero y un conjunto de combinadores para manipular flujos de enrutamiento y composición de tareas.”

En esta primera introducción, partimos de cero. Crearemos la solución inicial y veremos cómo funciona el _routing_ en Suave haciendo uso de una fantástica característica de la programación funcional: la composición de funciones. En próximos posts trataremos la implementación de vistas, autenticación, despliegues en Azure o Heroku y, en definitiva, todo lo necesario para tener una web o Web API totalmente operativa.

Ayer mismo se publicó la [versión 1.0 de Suave](https://www.nuget.org/packages/Suave), así que todos los ejemplos que vamos a mostrar en este y sucesivos posts será utilizando, como mínimo, esta versión.

Iniciando un nuevo proyecto con Suave
-------------------------------------

Actualmente tenemos varios editores con los que crear una solución con F#, desde el ya clásico **Visual Studio** hasta el recién llegado **Visual Studio Code** y sus [extensiones](https://marketplace.visualstudio.com/items/Ionide.Ionide-fsharp), pasando por **Atom** o **Xamarin Studio**. En esta serie vamos a utilizar Visual Studio, pero para crear la solución inicial utilizaremos [Yeoman](http://yeoman.io/), la herramienta de node.js (multiplataforma en consecuencia) que ha adquirido mucha popularidad en el ecosistema Microsoft por ser la utilizada por el equipo de ASP.NET. Sin embargo, nada nos impide crear una solución vacía y agregar las dependencias manualmente.

Después de instalar **Yeoman** utilizando `npm install –g yo`, necesitamos instalar [yeoman-fsharp](https://github.com/fsprojects/generator-fsharp) que proporciona las plantillas para realizar el _scaffolding_ de proyectos web, consola y, el que nos interesa a nosotros, una aplicación web con Suave.

Para instalar generador-fsharp desde npm ejecutamos el siguiente comando en la línea de comandos:

    npm install –g generator-fsharp
    

Una vez instaladas estás plantillas, iniciamos el generador ejecutando `yo fsharp` en el directorio donde queramos crear la solución y, cuando nos pregunte, seleccionaremos las opciones _Create standalone project_ y _Suave Application_, daremos un nombre a nuestra aplicación y responderemos que sí cuando nos pregunte si queremos utilizar **Paket** como gestor de paquetes. Al completar estos pasos, el generador descargará los ficheros necesarios y al final obtenemos la estructura siguiente.

[![yo-fsharp-folder](/img/yo-fsharp-folder.png)](/img/yo-fsharp-folder.png)

Si abrimos el fichero del proyecto **fsproj**, veremos que el contenido es muy simple. Únicamente tenemos un fichero de script con el código mínimo para iniciar el servidor web de Suave.

```csharp
#r "packages/Suave/lib/net40/Suave.dll"  
    
open Suave // always open suave  
open Suave.Http.Successful // for OK-result  
open Suave.Web // for config  

startWebServer defaultConfig (OK "Hello World!")
```   

Esta sentencia iniciará un servidor web en el puerto por defecto. Si ejecutamos la solución y abrimos en cualquier navegador la dirección `http://localhost:8083` obtendremos una respuesta con el mensaje “_Hello World!_”.

Antes de continuar, una pequeña puntualización. La plantilla de **Yeoman** agrega la dependencia de Suave de una versión más antigua que la última estable disponible. Como norma general, es recomendable utilizar siempre la última versión estable, que actualmente es la 1.0 así que para actualizar la dependencia solo tenemos que modificar el fichero de dependencias de paket y actualizar el paquete ejecutando el siguiente comando desde la **Consola de Gestión de Paquetes** de Visual Studio.

    PM> .\.paket\paket.exe update
    

Al actualizar la versión, también estamos obligados a realizar un cambio en el código: El namespace **Suave.Http.Successful** en la versión 1.0 pasa a ser **Suave.Successful**. Y ahora sí, tras este cambio menor, si ejecutamos la solución tendremos el servidor web funcionando y utilizando la última versión estable de Suave.

Conociendo los fundamentos de Suave
-----------------------------------

Vamos a comenzar analizando la primera, y de momento única, expresión que tenemos en el código:

    startWebServer defaultConfig (OK "Hello World!")
    

La función `startWebServer`, la encargada de iniciar el servidor web, requiere un _record_ de tipo **SuaveConfig** con la configuración inicial del servidor y una **WebPart**. La configuración por defecto (`defaultConfig`) está definida en **Suave.Web** en el modulo **Web.fs**.

```csharp
let defaultConfig = { 
    bindings  = [ HttpBinding.defaults ]
    serverKey = Crypto.generateKey HttpRuntime.ServerKeyLength
    errorHandler  = defaultErrorHandler
    listenTimeout = TimeSpan.FromSeconds 2.
    cancellationToken = Async.DefaultCancellationToken
    bufferSize= 8192 // 8 KiB
    maxOps= 100
    mimeTypesMap  = Writers.defaultMimeTypesMap
    homeFolder= None
    compressedFilesFolder = None
    logger= Loggers.saneDefaultsFor LogLevel.Info
    tcpServerFactory  = new DefaultTcpServerFactory()
    cookieSerialiser  = new BinaryFormatterSerialiser()
    tlsProvider   = new DefaultTlsProvider()
    hideHeader= false 
    }
```   

En esta configuración podemos ver varias propiedades con valores predeterminados. La configuración por defecto inicia el servidor en el puerto 8083 y utiliza un manejador de errores predeterminado que devuelve un error 500 para todas las excepciones no controladas. Para cambiar, por ejemplo, el puerto por defecto tenemos que crear una nueva configuración con un nuevo enlace Http.

```csharp
#r "packages/Suave/lib/net40/Suave.dll"

open Suave // always open suave
open Suave.Successful  // for OK-result
open Suave.Web // for config
open System.Net

let newBinding = HttpBinding.mk HTTP IPAddress.Loopback 80us
let webConfig = { defaultConfig with bindings = [ newBinding ] }

startWebServer webConfig (OK "Hello World!")
```  

En este código, utilizamos la función **HttpBinding.mk** para crear el nuevo enlace con esquema HTTP en el puerto 80 (`us` es el sufijo que utilizamos para indicar el tipo _unsigned int_ de 16 bits). Con este nuevo enlace creamos una nueva configuración a partir de la configuración por defecto estableciendo únicamente la propiedad bindings.

Ahora centrémonos en el segundo argumento de **startWebServer**, en la WebPart. Una **WebPart** es una función que recibe un objeto de tipo **HttpContext** y devuelve un workflow asíncrono de tipo **HttpContext option** (`HttpContext -> Async<HttpContext option>`). Para más información sobre los workflows asíncronos podéis consultar un post anterior ([Workflows asíncronos con F#](/workflows-asincronos-con-f-sharp/)) en el que se explican los conceptos básicos.

Como decíamos al principio, la WebPart más simple es la que definimos con la función `OK (OK “Hello World!”)`, y que siempre devuelve un workflow con HttpContext con una respuesta HTTP 200 y la cadena que se le pasa como argumento en el cuerpo de la respuesta. **Podemos entender una WebPart como una promise que contendrá el HttpContext resultante dado por la lógica de la WebPart**.

Además de la función **OK**, en el namespace `Suave.Succesful` tenemos las funciones **CREATED**, **ACCEPTED** y **NO\_CONTENT**, que utilizaremos para devolver una respuesta con los códigos 201, 202 y 204 respectivamente. En los módulos **Intermediate**, **Redirection**, **RequestErrors \*\* y \*\*ServerErrors** tenemos las funciones que nos devuelven códigos HTTP 100, 300, 400 y 500.

Registrando múltiples rutas
---------------------------

Tal y como tenemos el código ahora mismo, da igual la ruta que pidamos, ya sea `localhost` o `localhost/hello`, que siempre recibiremos la misma respuesta. Esto es porque no estamos añadiendo ninguna restricción, ni estamos definiendo más rutas en nuestro código. Vamos a ver cómo podemos restringir una WebPart a una ruta determinada.

```csharp
open Suave
open Suave.Successful
open Suave.Filters
open Suave.Operators

let webPart = path "/hello" >=> OK "Hello World!"

startWebServer defaultConfig webPart
``` 

Ahora, al ejecutar la solución, solo obtendremos una respuesta si accedemos a `localhost/hello`. En cualquier otra obtendremos una respuesta vacía.

De la expresión anterior podemos diferenciar dos partes. La primera es la función **path** que es de tipo `string -> WebPart`. Es decir, que devuelve una **WebPart** a partir de un **string**. La función path comprueba si la ruta de la petición coincide con la que pasamos cómo argumento y en caso afirmativo devuelve **Some** y en caso negativo devuelve **None**. La otra parte es el operador `>=>`. Este operador no es un operador incluido en F#, sino que está definido por Suave en el namespace **Suave.Operators**. Este operador compone dos **WebParts** en una, evaluando primero la de la izquierda y aplicando el segundo si el primero devuelve **Some**. En teoría de categorías esta operación es conocida como [composición Kleisli](https://en.wikipedia.org/wiki/Kleisli_category), con la que **si el resultado del primero de los dos workflows encadenados es None, el cálculo se cortocircuita y el segundo cálculo no se ejecuta nunca**. Tenéis un excelente tutorial del uso del operador `>=>` en [Railway oriented programming](http://fsharpforfunandprofit.com/posts/recipe-part2/).

Operadores personalizados
-------------------------

Una de las características que hace de F# un lenguaje perfecto para crear un DSL (_Domain Specific Languages_) es la posibilidad de poder sobrecargar los operadores estándar o crear nuevos operadores a partir de determinadas secuencias de caracteres. Todos los operadores en F#, incluso el operador “+” están definidos en **Microsoft.FSharp.Core.Operators**. Podemos definir o sobrecargar los operadores a nivel de clase, _record type_ o a nivel global. Por ejemplo, podemos sobrecargar el operador suma a nivel global, para cambiar radicalmente su comportamiento.

```csharp
    let (+) a b = a - b
```

A partir de este momento, si utilizamos el operador suma para realizar la operación “3 + 4” obtendremos “-1” como resultado. Además de los operadores matemáticos, en F# disponemos de otras definiciones de operadores. Quizá el más característico del lenguaje es el operador pipe `|>` que está definido de la siguiente forma:

```csharp
let inline (|>) x f = f x
```

De la misma forma, nosotros podemos definir nuestros propios operadores. Por ejemplo, podemos definir un operador que nos devuelta si una cadena coincide con una expresión regular de la siguiente manera:

```csharp
open System.Text.RegularExpressions

let (=~) input pattern =
    Regex.IsMatch(input, pattern)
```

Ahora podemos utilizar este operador con varios ejemplos de expresiones regulares con los siguientes resultados.

    > "P2ssw0rd" =~ "^[a-zA-Z0-9_-]{6,18}$";;
    val it : bool = true
    > "hello" =~ "hello|world";;
    val it : bool = true
    > "#dd22fy" =~ "/^#?([a-f0-9]{6}|[a-f0-9]{3})$/";;
    val it : bool = false
    

Es importante mencionar que los operadores definidos de esta forma son útiles cuando la definición no entra en conflicto con otras, o cuando el ámbito es pequeño, dentro de una función. **Introducir operadores como estos en nuestro código lo hace más difícil de entender**, ya que no hay forma de conocer previamente que es lo que hacen. Es una característica que debemos utilizar cuando tengamos una gran cantidad de operaciones repetidas y es una buena práctica definir los operadores como miembros estáticos para tipos personalizados.

Para terminar esta breve introducción a los operadores, mencionar que existen dos tipos de operadores de **prefijo** y de **infijo**. Los operadores de infijo son los operadores que se espera que se coloquen entre los dos operandos, es decir, son los operadores que hemos visto hasta ahora, “+”, “>”. Y los operadores de prefijo son los que se esperan que se coloquen delante de un operando. Los caracteres de operador permitidos son los que aparecen en la siguiente lista:

    !, %, &, *, +, -, . /, <, =, ?, @, ^, | y ~. 
    

Pero no podemos declarar cualquier operador como operador de prefijo. Por ejemplo, los operadores que comienzan por `!`, excepto `!=`, el operador `~` y secuencias repetidas de `~` actúan siempre como operadores de prefijo. Los operadores `+`, `-`, `+.`, `-.`, `&`, `&&`, `%` y `%%` pueden ser operadores de prefijo u operadores de infijo. En estos casos utilizamos el carácter `~` para convertirlo en un operador de prefijo y no formará parte de la secuencia de caracteres del operador. El resto de combinaciones siempre formaran caracteres de infijo.

Según la secuencia de caracteres exacta utilizada, el operador tendrá una prioridad y una asociatividad determinadas. Podéis leer sobre la precedencia y asociatividad de los operadores en este [magnifico post](http://www.readcopyupdate.com/blog/2014/09/10/custom-ops-associativity-precedence.html).

Combinadores, combinadores, combinadores
----------------------------------------

Y volviendo al punto en el que lo dejamos, gracias al operador `>=>` combinamos la WebPart que nos devuelve la función path con la WebPart que devuelve la función OK. Si ahora queremos definir diferentes rutas, tenemos que utilizar la función **choose**, que acepta una lista de WebParts y devuelve una sola WebPart.

```csharp
let webPart = 
    choose [  
        path "/"   >=> OK "Home"  
        path "/first"  >=> OK "First page"  
        path "/second" >=> OK "Second page"  
]
```

Como vemos, estamos constantemente utilizando la composición de funciones para obtener una **WebPart**. **En programación funcional, un combinador combina varias cosas de un mismo tipo en otra cosa del mismo tipo, o coge un valor y devuelve una nueva versión modificando ese valor**. En Suave existen dos tipos de combinadores, unos se utilizan para crear **WebParts** y combinarlos para producir nuevos WebParts y otros para combinar varios en un solo WebPart que se utiliza para inicializar el servidor web.

Pero podemos agregar un nuevo nivel de composición con otra serie de combinadores. En este caso para poder diferenciar peticiones GET o POST, tenemos una serie de funciones, de combinadores, que podemos utilizar junto con las funciones choose y path que hemos visto. En el siguiente ejemplo tenemos seis rutas distintas, tres que responderán con peticiones GET y la otras tres que responderán con peticiones POST. Obviamente, además de estas dos funciones, tenemos disponibles para el resto de verbos HTTP (PUT, HEAD, CONNECT, PATCH, TRACE, OPTIONS).

```csharp
let webPart =
    choose [
        GET >=>
            choose [
            path "/"   >=> OK "Get Home"
            path "/first"  >=> OK "Get First page"
            path "/second" >=> OK "Get Second page"
        ]  
        POST >=>
            choose [  
            path "/"   >=> OK "Post Home"
            path "/first"  >=> OK "Post First page"
            path "/second" >=> OK "Post Second page"
        ]
]
```

Y para terminar este post, vamos a ver cómo obtener información de las rutas. Suave proporciona una característica denominada “typed routes” (rutas con tipo) que nos permite acceder a los argumentos de las rutas mediante el tipado estático. Para aprovechar esta característica tenemos que utilizar la función **pathScan** en lugar de **path** de la siguiente forma.

```csharp
pathScan "/hello/%s" (fun name -> OK (sprintf "Hello %s!" name))
```

Como vemos, estamos pasando la ruta y una función que tiene tantos argumentos de entrada como la cadena. Podemos utilizar tantos parámetros como queramos. Por ejemplo, el siguiente caso también es válido.

```csharp
pathScan "/hello/%s/%d" (fun (name, year) -> OK (sprintf "Hello %s! Happy new year %d!" name year))
```    

En esta ocasión si el parámetro no es un entero, nos devolverá una respuesta vacía.

Y hasta aquí esta primera entrada dedicada al desarrollo con Suave. En la siguiente veremos como implementar las vistas con distintos motores de renderizado.

Resumen
-------

En este artículo hemos realizado un primer acercamiento al desarrollo web con Suave y nos hemos centrado en el enfoque que utiliza Suave para llevar a cabo el _routing_. En lugar de utilizar atributos como utilizamos en la mayoría de framework de .NET, Suave utiliza la composición de funciones que utilizamos para definir rutas, extraer información y devolver una respuesta.

Referencias
-----------

[Custom Operators, Associativity and Precedence in F#](http://www.readcopyupdate.com/blog/2014/09/10/custom-ops-associativity-precedence.html)  
[Operadores de prefijo e infijo](https://msdn.microsoft.com/es-es/library/dd233204.aspx#prefix)  
[Railway oriented programming](http://fsharpforfunandprofit.com/posts/recipe-part2/)  
[Suave.IO introduction and example - Part 1: Intro](http://blog.geist.no/suave-io-introduction-and-example-part-1-intro/)  
[The F# Operators and Basic Functions](http://blogs.msdn.com/b/dsyme/archive/2008/09/01/the-f-operators-and-basic-functions.aspx)

