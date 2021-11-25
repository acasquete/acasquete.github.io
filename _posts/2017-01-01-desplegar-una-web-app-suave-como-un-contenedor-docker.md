---
title: Desplegar una Web App Suave como un contenedor Docker
tags: docker, fsharp, functional_programming, suaveio
---
¿Has oído hablar de Docker? Seguramente sí, a no ser que te hayas pasado los últimos meses, o años podríamos decir a estas alturas, encerrado en una cueva. Para contribuir un poco más al _hype_ creado en torno a esta tecnología, voy a dedicar una serie de entradas al uso, creación y despliegue de contenedores **Docker**. Si eres de los que no sabes de qué va todo esto y has caído en este blog, aquí encontrarás una guía introductoria a **Docker**, con los pasos necesarios para empaquetar y desplegar una aplicación web.

Una muy breve introducción a Docker
-----------------------------------

**Docker** es un proyecto _open source_ que nos permite empaquetar el código de la aplicación y sus dependencias en un **contenedor aislado**, que comparte el núcleo del sistema operativo host. Esta última parte de la definición de contenedor es la diferencia fundamental con las máquinas virtuales, en las que la aplicaciones se ejecutan sobre un sistema operativo invitado.

![VMvsContainers.png](/img/VMvsContainers.png)

Los contenedores **Docker** se pueden ejecutar en cualquier plataforma en la que podamos tener funcionando el **Docker Engine**, el núcleo de Docker: Linux, macOS, Windows y, por supuesto, entornos Cloud.

Mientras que **Docker** se ejecuta de forma nativa en Linux, en macOS y Windows necesita apoyarse en un sistema para virtualizar las características específicas del kernel de Linux y el entorno de ejecución de **Docker Engine**. En el caso de macOS se utiliza [xhyve](https://github.com/mist64/xhyve/) y en Windows se utiliza Hyper-V. Además, desde septiembre del año pasado, tenemos disponibles las características de contanerización mediante Docker en todas las versiones de Windows Server 2016 y Windows 10 con _Anniversary Update_, con las que podemos crear y ejecutar contenedores Windows de la misma forma que utilizamos los contenedores Linux.

Imágenes y contenedores
-----------------------

En el mundo Docker trabajaremos con dos conceptos principales y estrechamente relacionados: **imágenes** y **contenedores**. Las imágenes de Docker son la base de cualquier contenedor y las podemos definir como una plantilla inmutable con un estado que nosotros describimos. Utilizando el símil de la programación, podemos entender una imagen como una clase y un contenedor como una instancia de esa clase, de la que podremos tener varias instancias, o lo que es lo mismo, es posible tener varios contenedores creados a partir de la misma imagen.

> Podemos entender una imagen Docker como una clase y un contenedor como una instancia de esa clase.

Las imágenes Docker deben contener el código de aplicación, sus dependencias y la configuración necesaria para que la aplicación pueda iniciarse correctamente. Una imagen puede contener, por ejemplo, un servidor Tomcat y nuestra aplicación web, o puede contener la última versión de Mono y F# que es la que utilizaremos en nuestro primer ejemplo.

El enfoque que propone **Docker** es partir siempre de una imagen base y extenderla añadiendo las dependencias que necesitemos. El lugar donde encontrar estás imágenes es el repositorio de **[Docker Hub](https://hub.docker.com/)**, desde donde tendremos acceso a multitud de imágenes, tanto compartidas por la comunidad, como a la [lista oficial de repositorios](https://hub.docker.com/explore/), un conjunto curado de repositorios básicos que sirven de punto de partida para la mayoría de usuarios.

Podemos buscar desde el sitio web de Docker Hub o podemos utilizar la herramienta de línea de comandos y ejecutar el comando de búsqueda. Por ejemplo, podemos ejecutar el siguiente comando para buscar una imagen con Mono:

    docker search mono
    

Esto nos mostrará una lista de las imágenes disponibles en Docker Hub que coinciden con el término de búsqueda.

La aplicación a contenerizar
----------------------------

Una vez vistos los conceptos esenciales, vamos a crear nuestro primer ejemplo con **Docker**. Lo primero que vamos a hacer es generar una aplicación utilizando el [generador de Yeoman](https://github.com/fsprojects/generator-fsharp). En un post anterior hice una [introducción al desarrollo con Suave](/primeros-pasos-en-el-desarrollo-web-con-suave/) en el que explicaba cómo hacerlo mediante línea de comandos.

Una vez creada la aplicación utilizando FAKE y PAKET tendremos una estructura similar a esta.

    .
    ├── build.cmd
    ├── build.fsx
    ├── build.sh
    ├── packages
    ├── paket.dependencies
    ├── paket.lock
    ├── paket.references
    ├── suavedocker.fsproj
    └── suavedocker.fsx
    

Vamos a reemplazar el contenido del fichero `suavedocker.fsx` por el siguiente código:

    #r "packages/Suave/lib/net40/Suave.dll"
    #r "packages/Newtonsoft.Json/lib/net40/Newtonsoft.Json.dll"
    
    open System
    open System.Net
    open Suave
    open Suave.Successful
    open Suave.Web
    open Suave.Filters
    open Suave.Operators
    open Suave.Writers
    open Newtonsoft.Json
    
    type TodoItem = { Id: int; Name: string; IsComplete: bool }
    
    let todoItems = [ { Id = 1; Name = "Complete Suave Project"; IsComplete = false} ]
    
    let toJson data = 
        (JsonConvert.SerializeObject data |> OK) 
        >=> setMimeType "application/json; charset=utf-8"
    
    let webPart =
        choose [
            GET  >=> path "/api/todoitems" >=> (todoItems |> toJson)
        ]
    
    let newBinding = HttpBinding.mk HTTP (IPAddress.Parse "0.0.0.0") 8083us
    let webConfig = { defaultConfig with bindings = [ newBinding ] }
    
    startWebServer webConfig webPart
    

Es un código, que aunque no deja de ser muy sencillo, es algo más que el “Hola Mundo” y nos permitirá ir completando la funcionalidad en las siguientes entradas. La parte más importante de este código es en la que establecemos un nuevo binding con la IP 0.0.0.0 ya que sino lo hiciésemos sería imposible acceder a la web.

Dockerfile
----------

Las imágenes Docker se crean a partir de un fichero `Dockerfile`. Este fichero contendrá una lista de instrucciones en la que iremos indicando que acciones realizar para crear el contenedor e iniciar la aplicación.

> La imagen que generemos contendrá todas las dependencias necesarias para ejecutar la aplicación.

El primer paso es decidir qué imagen base vamos a utilizar para crear nuestro contenedor. Comenzamos creando el fichero `Dockerfile` en el directorio raíz de nuestra aplicación al que le añadiremos la siguiente línea.

    FROM fsharp/fsharp
    

La primera línea del `Dockerfile` debe ser siempre la instrucción FROM para indicar la imagen base queremos utilizar. En este caso elegimos la [imagen oficial de F#](https://hub.docker.com/r/fsharp/fsharp/) que contiene la última instalación de Mono y F#, suficientes para ejecutar nuestra aplicación de ejemplo.

El siguiente paso es definir las dependencias y acciones que hay que realizar para que la aplicación pueda iniciarse.

    RUN         mkdir -p /src
    WORKDIR     /src
    
    COPY        . .
    RUN         mono ./.paket/paket.bootstrapper.exe
    RUN         mono ./.paket/paket.exe restore
    

La instrucción `RUN` ejecuta el comando especificado. Es similar a lanzarlo desde la línea de comandos. La instrucción `WORKDIR` define el directorio de trabajo donde los comandos se ejecutarán. La instrucción `COPY` copia los ficheros y directorios desde el directorio a la imagen del contenedor. Se utiliza para copiar el código fuente en la imagen, permitiendo que se compile dentro de la imagen.

Una vez tenemos las dependencias vamos a incluir cómo construir y ejecutar la aplicación.

    COPY 		. /src
    EXPOSE      8083
    CMD         ["fsharpi", "suavedocker.fsx"]
    

La instrucción `EXPOSE` define que puertos la aplicación está escuchando. Esto ayuda a saber cómo debe iniciarse la aplicación. Se puede considerar como parte de la documentación, metadatos sobre la imagen o aplicación.

Por último, la instrucción `CMD` define el comando por defecto que se ejecutará cuando el contenedor se inice. Este comando puede sobrescribirse en el momento de iniciar el contenedor.

Crear la imagen Docker
----------------------

Una vez tenemos el fichero `Dockerfile` creado podemos crear la imagen utilizando el CLI de Docker.

    docker build -t suave-todoapi:0.1 .
    

Cuando creamos una imagen también definimos un nombre y un _tag_. El _tag_ es un string que se utiliza normalmente para definir el número de versión. En este caso utilizamos el valor 0.1.

Al ejecutar el comando _build_, todos las instrucciones definidas en el `Dockerfile` se ejecutan en orden. Docker crea el container, ejecuta las instrucciones y, por último, guarda la imagen.

Para ver la imagen recién creada podemos utilizar el siguiente comando:

    docker images | head -n2
    

Con el que obtendremos un listado similar a este:

    REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
    suave-todoapi       0.1                 1206ffdbf1b9        About a minute ago   958.5 MB
    

Ejecutar la imagen Docker
-------------------------

Una vez que hemos generado la imagen de Docker podemos lanzarla como cualquier otra imagen utilizando el comando `docker run`.

    docker run -d -p 8083:8083 --name todoapi suave-todoapi:0.1
    

Con este comando estamos indicando a docker que debe ejecutar la imagen `suave-todoapi:0.1` que hemos creado en el punto anterior y, mediante el parámetro `-name`, estamos danto el nombre `todoapi` al contenedor. Cuando ejecutamos el contenedor podemos decidir si lo queremos ejecutar en segundo plano (_detached_) o primer plano, la configuración por defecto. Para iniciar un contenedor en modo _detached_, tenemos que utilizar el argumento `-d`. Por último, mediante el argumento `-p` indicamos que exponemos el puerto 8083 para que podamos acceder a la aplicación.

Para probar que el contenedor está funcionando correctamente podemos acceder a la aplicación desde cualquier navegador [http://localhost:8083/api/todoitems](http://localhost:8083/api/todoitems) o utilizar curl.

    curl http://localhost:8083/api/todoitems 
    

Con esto último terminamos esta primera entrada dedicada a **Docker** en el que hemos visto cómo crear una aplicación Suave F# como una imagen Docker.

Resumen
-------

**Docker** hace más sencillo la forma en la que podemos desplegar y ejecutar aplicaciones distribuidas y, en poco tiempo, se ha convertido en uno de los proyectos _open source_ más importantes, haciendo que muchas empresas estén pensando en cómo contenerizar sus aplicaciones.

En esta entrada hemos visto los conceptos básicos para poder generar una imagen **Docker** con una aplicación Suave con F#.

Referencias
-----------

[Introducing Docker For Windows Server 2016](https://blog.docker.com/2016/09/dockerforws2016/)  
[Docker.com: What is Docker?](https://www.docker.com/what-docker)  
[Github.com: Docker Labs](https://github.com/docker/labs)  
[How to Use Docker on OS X: The Missing Guide](https://www.viget.com/articles/how-to-use-docker-on-os-x-the-missing-guide)