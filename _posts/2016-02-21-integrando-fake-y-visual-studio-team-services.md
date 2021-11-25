---
title: Integrando FAKE y Visual Studio Team Services
---
**FAKE** (F# Make) es un DSL escrito en F# con el que podemos definir diferentes tareas para compilar y desplegar cualquier tipo de proyecto. Es un sistema de automatización de _builds_ similar a [Make](http://www.gnu.org/software/make/) o [Rake](https://github.com/ruby/rake), es _open-source_ y cuenta con una comunidad, con más de 200 _contributors_, muy activa.

**FAKE** nos permite aprovechar toda la potencia de .NET con la programación funcional para crear nuestros scripts de automatización para cualquier plataforma. No debe confundirnos que esté escrito en F#, ya que esto no implica que solo se pueda utilizar con proyectos F#, sino todo lo contrario, **FAKE** se puede utilizar para automatizar el proceso de compilación de, potencialmente, cualquier tipo de proyecto. También es importante destacar que no es necesario tener conocimientos previos de F# para utilizarlo, ya que las tareas básicas son fáciles de utilizar sin conocimiento alguno del lenguaje.

En este post vamos a ver cómo utilizar **FAKE** para crear un script que genere la _build_ de un proyecto ASP.NET MVC estándard, ejecute los tests unitarios y, por último, veremos cómo integrarlo muy fácilmente en el nuevo sistema de _builds_ de **Visual Studio Team Services**.

### Añadir FAKE a un proyecto ASP.NET MVC 

Para comenzar vamos a añadir FAKE a un proyecto web existente. Como ejemplo utilizaremos un proyecto creado con la plantilla ASP.NET MVC al que se le ha agregado un proyecto de test. Antes que nada, necesitamos agregar a nuestra solución la utilizad de línea de comandos de NuGet. Esto es necesario porque durante el proceso de compilación es necesario descargar todas las dependencias, y esto lo haremos mediante NuGet. Podríamos hacerlo utilizando Paket, pero como la solución por defecto de ASP.NET MVC no lo utiliza, en esta ocasión lo omitiremos.

Para agregar NuGet tenemos que bajarnos la última versión de la línea de comandos que está disponible en este [enlace](http://dist.nuget.org/win-x86-commandline/latest/nuget.exe) y copiarlo en el directorio **.nuget**. La estructura del proyecto quedará como se muestra a continuación.

    C:.
    |   DemoWebApp.sln
    |   
    +---.nuget
    |       nuget.exe
    |       
    +---DemoWebApp
    |   |   DemoWebApp.csproj
    |   |   packages.config
    |   |   ...
    |   |   
    |               
    \---DemoWebApp.Tests
        |   DemoWebApp.Tests.csproj
        |   packages.config
        |   ...
        |
    

El siguiente paso es crear un fichero con el que lanzar el script de compilación. Para tal efecto, creamos un fichero con el nombre `build.cmd` en el directorio raíz de la solución con el siguiente contenido.

    @echo off
    cls
    ".nuget\NuGet.exe" "Install" "FAKE" "-OutputDirectory" "packages" "-ExcludeVersion"
    "packages\FAKE\tools\Fake.exe" build.fsx
    pause
    

Al ejecutar este script se descargará la última versión de **FAKE** utilizando la utilidad de línea de comandos de NuGet que hemos descargado anteriormente y ejecutará el script de compilación de **FAKE**. Antes de ejecutar vamos a crear el script mínimo de **FAKE** creando un fichero con el nombre `build.fsx`, también en el directorio raíz.

    // include Fake lib
    #r @"packages/FAKE/tools/FakeLib.dll"
    open Fake
    
    // Targets
    Target "Default" (fun _ ->
    	trace "Hello FAKE!"
    )
    
    // start build
    RunTargetOrDefault "Default"
    

Este script es bastante sencillo de entender incluso si esta es la primera vez que vemos código F#. Con las dos primeras líneas añadimos la referencia a la librería y espacio de nombres de **FAKE**. En el segundo bloque de código definimos los distintos _Targets_, o conjunto de tareas. En este caso, estamos definiendo el _target_ “Default” que mostrará el mensaje “Hello FAKE!” en la consola. Por último, la última línea define el _Target_ predeterminado.

Si ejecutamos el fichero `build.cmd` obtendremos el siguiente resultado.

![Hello FAKE!](/img/hello-fake.png)

Aunque no hemos conseguido un resultado realmente sorprendende, esta primera introducción nos ha servido para conocer la estructura básica de los scripts de FAKE. Vamos a ver ahora cómo modificar el _script_ para realizar las tareas típicas de un proceso de _build_.

## Compilando un proyecto con MSBuild 

El paso más importante en un proceso de _build_ es sin duda la compilación del proyecto. **FAKE** contiene _helpers_ que contienen tareas que nos permiten utilizar MSBuild (o xBuild en Linux/Unit) para compilar los ficheros de proyectos o de solución de cualquier proyecto .NET. Estas tareas las encontramos en el [Helper MSBuildHelper](http://fsharp.github.io/FAKE/apidocs/fake-msbuildhelper.html). Pero además de estas, FAKE dispone de multitud de tareas de las que se puede consultar su modo de uso en la [documentación de la API](http://fsharp.github.io/FAKE/apidocs/index.html).

Con el siguiente código vemos cómo definir un **Target** para compilar el proyecto web.

    // Targets
    let buildDir = "./build/"
    
    Target "BuildApp" (fun _ ->
      !! "DemoWebApp/**/*.csproj"
        |> MSBuildRelease buildDir "Build"
        |> Log "AppBuild-Output: "
    )
    
    Target "Clean" (fun _ ->
      CleanDir buildDir
    )
    
    

Vamos a hacer algunas aclaraciones al código anterior. El operador **!!** obtiene e incluye todos los ficheros `.csproj` que se encuentren en el subdirectorio “DemoWebApp”. La tarea **MSBuildRelease** compila los proyectos utilizando el target “Build” y el directorio de salida definido en el valor `buildDir`.

En este ejemplo vemos también que se define el _target_ “Clean”. Aquí se utiliza la tarea **CleanDir** que limpia un el directorio eliminando todos los ficheros y subdirectorios que contenga.

Aun nos queda un último detalle para poder ejecutar el _script_. Antes de compilar el proyecto necesitamos descargar todas las dependencias. En FAKE tenemos varias funciones para poder descargar las dependencias de NuGet o Paket. En nuestro caso, como tenemos el fichero `packages.config` utilizaremos la función **RestorePackages** que busca el fichero en cualquier subdirectorio y restaura todos los paquetes al directorio “packages”. Además como la función **RestorePackages** no requiere de nigún parámetro podemos simplificar la forma en la que declaramos el _Target_.

    Target "RestorePackages" 
         RestorePackages  
    

Ahora ya tenemos los tres _Targets_ que necesitamos para ejecutar nuestra _build_ definidos, pero para establecer el orden de ejecución de los distintos _Targets_, **FAKE** nos proporciona una serie de funciones y operadores. El operador principal es el operador `==>` con el que definimos que el que el _Target_ a la derecha del operador es dependiente del que tengamos a la izquierda. El listado del resto de operadores para la gestión de dependencias entre _Targets_ los podemos consultar [aquí](http://fsharp.github.io/FAKE/apidocs/fake-additionalsyntax.html).

Esta sería la declaración de dependencias de nuestros _Targets_ y se leería de la siguiente forma: en primer lugar, limpiamos el directorio, después restauramos los paquetes y por último compilamos el proyecto.

    "Clean"
      ==> "RestorePackages"
      ==> "BuildApp"

t bbAl ejecutar y después de unos pocos segundos obtendremos el siguiente resultado.

![FAKE First Build](/img/fake-first-build.png)

## Ejecución de pruebas 

Otra de las tareas imprescindibles en una _build_ automatizada es la ejecución de tests. **FAKE** dispone de tareas para ejecutar tests de NUnit, XUnit y MSTest.

Para nuestro ejemplo vamos a crear dos _Targets_, uno para la compilación del proyecto o proyectos (en caso de que los hubiese) de tests y otro para la ejecución de los tests. Este es la aproximación que vamos a seguir, aunque podríamos modificar el _target_ BuildApp para que compilase todos los proyectos y ejecutase los tests sobre esa compilación. Es preferible tener compilaciones distintas y tener los distintos _Targets_ aislados.

    let testsDir  = "./tests/"
    
    Target "BuildTests" (fun _ ->
      !! "DemoWebApp.Tests/**/*.csproj"
        |> MSBuildRelease testsDir "Build"
        |> Log "TestsBuild-Output: "
    )
    
    Target "Test" (fun _ ->
        !! (testsDir + @"/**/*.Tests.dll") 
          |> MSTest (fun p -> p)
    )
    

Ahora solo tenemos que actualizar la declaración de dependencias entre _Targets_ de la siguiente forma:

    // Dependencies
    "Clean"
      ==> "RestorePackages"
      ==> "BuildApp"
      ==> "BuildTests"
      ==> "Test"
    

El resultado de la ejecución, en esta ocasión, contendrá el número y el resultado de la ejecución de los tests.

![FAKE First Test Build](/img/fake-first-test-build.png)

## Integrando FAKE con Visual Studio Team Services 

El nuevo sistema de Builds de **Visual Studio Team Services** (VSTS) permite integrar muy fácilmente cualquier _script_ de FAKE.

Comenzamos creando una nueva definición de _build_ vacía (sin ningún paso) en la que podremos seleccionar el repositorio de origen, ya sea un proyecto de VSTS o un repositorio Git remoto. Marcamos también la casilla para habilitar la integración continua, para que la build se ejecute cada vez que la rama se actualice.

![VSTS Create New Build Definition](/img/vsts-create-build-definition.png)

Una vez creada la definición de la _build_, añadimos una tarea para lanzar el script. De hecho, como nuestro script de FAKE realiza todas las acciones solo necesitaremos añadir esta tarea.

![VSTS Add Task Batch Script](/img/vsts-add-task-batch-script.png)

Al añadir el paso a la build tenemos que seleccionar el fichero `build.cmd` en la propiedad _Path_ y debemos marcar la casilla _Fail on Standard Error_.

![VSTS Add Task Batch Script Setup](/img/vsts-add-task-batch-script-setup.png)

Por último, para que la build pueda obtener y mostrar información sobre la ejecución de los tests, tenemos que añadir una tarea de tipo _Publish Result test_.

![vsts-add-task-test-results](/img/vsts-add-task-test-results.png)

En este paso tenemos que establecer el formato de test que utilizamos, en nuestro ejemplo VSTest, y modificar el nombre del fichero de los resultados a “_\*/_.trx”, que es el formato predeterminado.

Si ahora lanzamos una nueva _build_, ya sea manualmente o realizando un commit al repositorio, veremos el siguiente informe al finalizar.

![VSTS Build Results](/img/vsts-build-results.png)

## Conclusiones 

En esta entrada hemos visto cómo podemos utilizar **FAKE** para crear nuestros scripts de automatización de builds que se ejecutan de la misma forma en local que en cualquier servidor de _builds_. **FAKE** proporciona un EDSL funcional para definir las tareas propias de una build: limpiar directorios, compilar proyectos, ejecución de tests, etc.

Los ficheros de script de FAKE se escriben en F#, pero no es necesario tener conocimientos previos del lenguaje para ejecutar las tareas de build más sencillas. Además, al ser F# un lenguaje con tipado estático, el compilador nos mostrará cualquier error que haya en el script antes de ejecutarlo.

Otra ventaja es que podemos escribir los scripts con Visual Studio, con lo que tenemos soporte de Intellisense y podremos depurar los scripts como si de cualquier otra aplicación se tratase.

## Referencias 

[FAKE - F# Make](https://github.com/fsharp/FAKE)  
[Installing NuGet](http://docs.nuget.org/consume/installing-nuget)  
[Exploring FAKE, an F# Build System for all of .NET](http://www.hanselman.com/blog/ExploringFAKEAnFBuildSystemForAllOfNET.aspx)