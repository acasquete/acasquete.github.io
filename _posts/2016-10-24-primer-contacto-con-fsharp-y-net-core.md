---
title: Primer contacto con F# y .NET Core
tags: [fsharp, functional_programming, netcore]
---
En este post veremos cómo comenzar a utilizar F# con .NET Core. Comenzaremos creando un proyecto F# mediante las herramientas de línea de comandos (.NET CLI). Aprovecharemos, además, este primer post para introducir el funcionamiento del servicio **Configuration** de [.NET Core](https://dotnet.github.io/) para cargar la configuración de nuestra aplicación desde distintos orígenes, utilizando una colección en memoria, los clásicos ficheros externos y la versátil línea de comandos.

Hola Mundo .NET Core
--------------------

La mejor forma para poder comenzar a utilizar .NET Core es [instalar el SDK de .NET Core](https://www.microsoft.com/net/core) y una vez lo tengamos disponible en el sistema, inicializar un proyecto de tipo consola escribiendo desde la línea de comandos lo siguiente:

    md netcorefsharpapp
    cd netcorefsharpapp
    dotnet new --lang fsharp
    

Si miramos el directorio veremos que el último comando ha inicializado el directorio añadiendo los ficheros `Program.fs` y `project.json`.

Para poder ejecutar la aplicación necesitamos restaurar los paquetes definidos en el `project.json`. Esto lo podemos hacer mediante el comando _dotnet restore_.

    dotnet restore
    dotnet run
    

El último commando compila el código fuente, genera el programa y, por último, lo ejecuta.

Después de la compilación aparecerá el mensaje “Hello World!” en la consola, con lo que daremos por completado el primer ejemplo utilizando **F#** y **.NET Core** desde el **CLI**.

Configuration
-------------

Una vez tenemos la primera app, vamos a ver los principales servicios de .NET Core que podemos utilizar. El primero en el que nos detendremos es **Configuration**.

**Configuration** es un _framework_ para acceder a configuraciones basadas en clave valor. Por defecto, .NET Core incluye proveedores para manejar configuraciones desde ficheros **JSON**, **XML** y **INI**, variables de entorno y argumentos de la línea de comandos.

A grandes rasgos, este nuevo framework de configuración tiene dos componentes fundamentales **IConfigurationRoot** y **IConfigurationBuilder**. El primero, **IConfigurationRoot**, es el objeto con el que podremos acceder a las configuraciones mediante clave/valor y **IConfigurationBuilder** es en encargado de cargar los proveedores de configuración y de crear el objeto **Root** con el que accederemos a las distintas configuraciones.

El nuevo modelo de **.NET Core** permite recuperar la configuración desde una gran variedad de orígenes y para poder utilizarlo necesitamos configurar al menos un orígen de configuración. El siguiente ejemplo muestra cómo trabajar con Configuration utilizando el proveedor de memoria.

Es importante no olvidar que antes de poder hacer referencia a cualquiera de los objetos mencionados anteriormente, es necesario añadir la dependencia al paquete `Microsoft.Extensions.Configuration`.

    open System
    open Microsoft.Extensions.Configuration
    
    [<EntryPoint>]
    let main argv = 
    
        let builder = new ConfigurationBuilder();
        builder.AddInMemoryCollection() |> ignore
        let config = builder.Build()
    
        config.["firstkey"] <- "firstkeyvalue"
    
        printfn "Setting value: %s" config.["firstkey"]
        0 // return an integer exit code
    

Con este ejemplo hemos aprendido a ver el funcionamiento básico de Configuración con .NET Core, sin embargo, lo habitual no es utilizar una colección en memoria para guardar la configuración, sino que en su lugar utilizamos ficheros externos (JSON, XML o incluso INI) y donde además no guardamos propiedades simples sino que tendemos a agrupar las propiedades dentro de otras mediante una estructura jerárquica, que nos ayuda a tener organizadas las distintas secciones de la configuración.

Por ejemplo, el siguiente fichero `appsettings.json` es el que se añade en un proyecto ASP.NET que contiene la cadena de conexión y la configuración de niveles de registro de la aplicación.

    {
      "ConnectionStrings": {
        "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=aspnet-WebApplication1-26e8893e-d7c0-4fc6-8aab-29b59971d622;Trusted_Connection=True;MultipleActiveResultSets=true"
      },
      "Logging": {
        "IncludeScopes": false,
        "LogLevel": {
          "Default": "Debug",
          "System": "Information",
          "Microsoft": "Information"
        }
      }
    }
    

Para poder leer esta configuración desde un fichero JSON tenemos que añadir el paquete `Microsoft.Extensions.Configuration.Json`.

    open System
    open System.IO
    open Microsoft.Extensions.Configuration
    open Microsoft.Extensions.Configuration.Json
    
    [<EntryPoint>]
    let main argv = 
    
        let builder = new ConfigurationBuilder();
        builder.SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json") |> ignore
        
        let config = builder.Build()    
    
        printfn "Connection: %s" config.["ConnectionStrings:DefaultConnection"]
        
        0 // return an integer exit code
    

En este codigo podemos ver que en el paquete de configuración de JSON nos proporciona el método extensor **AddJsonFile**. Esta es la forma habitual en la que utilizaremos los distintos proveedores de configuración y en la la que implementaremos nuestros proveedores personalizados.

El otro punto a destacar es la forma en la que se recupera el valor de configuración. En este caso, se utiliza una clave separada por `:` comanzando a partir de la propiedad raíz de la jerarquía.

Cargar configuración desde la línea de comandos
-----------------------------------------------

Como hemos visto, el framework de configuración tiene incluído soporte para cargar ficheros JSON, XML INI, así como soporte para poder establecer esta configuración desde código utilizando una colección en memoria.

Además de estos tiene la posibilidad de obtener valores de configuración desde las variables de entorno y parámetros de línea de comandos.

Para utilizar esta configuración desde la línea de comandos tenemos que añadir la referencia a `Microsoft.Extensions.Configuration.CommandLine`. Una vez añadida esta referencia tenemos que generar el _builder_ llamando al método extensor **AddCommandLine** al que le pasaremos los argumentos que, en este caso, recibe el método **Main**. Lo podemos ver en el siguiente código:

    let builder = new ConfigurationBuilder();
    builder.SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json") 
            .AddCommandLine(argv) |> ignore
        
    let config = builder.Build()    
    

A partir de ahora podremos acceder a cualquier argumento que pasemos por la línea de comandos de la misma forma que accedemos a una propiedad de una colección en memoria o en el fichero de configuración.

Por ejemplo, para probar podemos ejecutar la aplicación desde la línea de comandos utilizando el siguiente comando:

    dotnet run --ConnectionStrings:DefaultConnection "test"
    

El valor del argumento que estamos pasando en la línea de comandos sobrescribirá el valor cargado desde el fichero JSON y la aplicación mostrará la cadena “test” en lugar de la cadena de conexión que tenemos establecida en el fichero **appsettings.json**.

Resumen
-------

En este primer post dedicado a **.NET Core** hemos visto cómo crear un proyecto F# utilizando el CLI de .NET Core. Además hemos visto el funcionamiento principal de unos de los servicios principales de **.NET Core** que nos permite leer la configuración para nuestra aplicación desde distintos orígenes.

En las siguientes entradas seguiremos introduciéndonos en la programación con F# y .NET Core.

Referencias
-----------

[Getting Started with F# on .NET Core](https://channel9.msdn.com/Events/Build/2016/T661)  
[.NET Core](https://www.microsoft.com/net/core)  
[Docs Fundamentals Configuration](https://docs.asp.net/en/latest/fundamentals/configuration.html)  
[Ionide - Crossplatform F# Editor](http://ionide.io/)

