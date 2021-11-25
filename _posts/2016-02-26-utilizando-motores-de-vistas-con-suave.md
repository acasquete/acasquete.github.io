---
title: Utilizando motores de vistas con Suave
tags: fsharp, suaveio, functional_programming
---
En el [post anterior](/primeros-pasos-en-el-desarrollo-web-con-suave) vimos cómo haciendo uso de la composición de funciones podíamos definir las rutas de nuestra aplicación web y devolver una respuesta con un código HTTP determinado y una cadena de texto en el cuerpo en cada una de esas respuestas. Esto lo conseguíamos fácilmente con las WebParts **OK**, **CREATED** y **ACCEPTED** que están definidas en el [módulo Succesful](https://github.com/SuaveIO/suave/blob/master/src/Suave/Combinators.fs). Pero además de devolver una cadena de texto, que nos puede ser muy útil e incluso suficiente para desarrollar una Web API, **Suave** también permite utilizar distintos motores de vistas para generar HTML y enviarlo al cliente.

> Los motores de vistas nos permiten utilizar ficheros de plantillas estáticos que contienen variables que son reemplazadas en tiempo de ejecución por los valores reales.

Suave permite generar las vistas haciendo uso de los motores **RazorEngine** o **DotLiquid** y generando el código HTML desde el servidor mediante código F#. En este post vamos a ver una introducción al uso de cada uno de estos métodos.

RazorEngine
-----------

Vamos a comenzar viendo posiblemente el motor de vistas que será más conocido, **RazorEngine**, un proyecto _open-source_ basado en el motor de parseo de Microsoft Razor.

Para poder utilizar vistas Razor necesitamos añadir la referencia al paquete Suave.Razor, añadiendo la dependencia en el fichero **paket.dependencies** y actualizando desde la consola de gestor de paquetes.

    PM> .\.paket\paket.exe install
    

Además del paquete **Suave.Razor**, veremos que **Paket** descarga RazorEngine y varias dependencias más.

A partir de este momento podremos añadir nuestra primera vista al proyecto. Solo necesitaremos agregar al proyecto el fichero `hello.cshtml` con el siguiente contenido.

    <html>
    <head>
        <title>Suave.Razor</title>
    </head>
    <body>
        <h1>Hello Razor!</h1>
    
        <!-- Single statement blocks  -->
        @{ var answer = 42; }
        @{ var message = "The answer to life the universe and everything"; }
    
        <!-- Inline expressions -->
        <p>@message is @answer </p>
    
        <!-- Multi-statement block -->
        @{
            var greeting = "Welcome to Suave.Razor!";
            var weekDay = DateTime.Now.DayOfWeek;
            var greetingMessage = greeting + " Today is: " + weekDay;
        }
        <p>The greeting is: @greetingMessage</p>
    
        <!-- Loop Code -->
        @{ var colors = new[] { "red", "blue", "green" }; }
    
        <p>The content of colors is:</p>
        <ul>
            @foreach (var color in colors)
            {
                <li style="color:@color">@color</li>
            }
        </ul>
    
    </body>
    </html>
    

Como la intención de este post no es entrar en detalle de todas las posibilidades que ofrece la sintaxis de Razor, esta vista contiene las estructuras más simples de Razor y podemos resumir la sintaxis en que los bloques de código Razor estan entre @{ … } y las expresiones en línea (variables y funciones) comienzan con @. Y, obviamente, el lenguaje utilizado en las expresiones es C#.

Al añadir el fichero al proyecto es importante revisar que las propiedades **Build Action** y **Copy to Output Directory** están establecidas en _Content_ y _Copy if never_, respectivamente. En caso de que no hagamos este cambio, la vista no se copiará en el directorio de destino. Por defecto, el motor de Razor buscará la vista en el directorio raíz y en el directorio Views, y en el caso de no encontrarla en ninguno de estos directorios, lanzará una excepción con el mensaje _Could not resolve requested view_.

Y una vez que tenemos la vista preparada, solo tenemos que modificar el código para poder devolverla para una determinada ruta. Añadimos la referencia al namespace Suave.Razor y cambiamos la webpart para que realice una llamada a **Razor.razor**. Esta función tienes dos parametros: el primero es la vista que hay que parsear y el segundo es el modelo, que para este primer ejemplo lo dejamos como una lista vacía.

    #r "packages/Suave/lib/net40/Suave.dll"
    #r "packages/Suave.Razor/lib/net40/Suave.Razor.dll"
    
    open Suave                 
    open Suave.Successful      
    open Suave.Web
    open Suave.Filters
    open Suave.Operators
    open Suave.Razor
    
    let webPart = path "/" >=> (Razor.razor "hello" [] )
    
    startWebServer defaultConfig webPart
    

Si ejecutamos la solución y accedemos a `localhost:8083`, veremos el resultado de la template una vez procesada. En lugar de pasar una lista vacía, podemos pasar cualquier tipo como segúndo parámetro de la función razor. En el siguiente ejemplo definimos un _Record Type_ y después declaramos una lista de este tipo y lo pasamos a la función razor.

    type OS = { Name: string; }
    
    let OSList =  [ { Name = "OSX"; }
                    { Name = "Android"} 
                    { Name = "Windows Phone"} ]
    
    let webPart = path "/" >=> Razor.razor "hello" OSList
    
    

Y en la vista podemos hacer referencia a este modelo mediante la variable `Model`.

    <p>Product list</p>
    <ul>
        @foreach (var product in Model)
        {
            <li>@product.Name @product.Description</li>
        }
    </ul>
    

Experimental
------------

Despues de ver el funcionamiento básico con **RazorEngine**, vamos a ver cómo generar las vistas con **Suave.Experimental**, un componente que nos permite generar las vistas utilizando código F#. Al igual que hicimos con Razor, para poder utilizar el Experimental tenemos que añadir la referencia al paquete al proyecto y al namespace **Suave.Html**.

Como la vista la vamos a generar con código F#, vamos a crear un nuevo fichero en el proyecto con el nombre `View.fs` en el proyecto con el siguiente contenido que examinaremos a continuación.

    module View
    
    open Suave.Html
    open System
    
    // Helpers
    let h1 = tag "h1" [] 
    let ul = tag "ul" [] (flatten xml)
    let li = tag "li" []
    let spanStyle style = spanAttr ["style", style]
    
    let answer = 42
    let message = "The answer to life the universe and everything"
    let greeting = "Welcome to Suave.Experimental!"
    let weekDay = DateTime.Now.DayOfWeek.ToString()
    let greetingMessage = greeting + " Today is: " + weekDay
    
    let colors = ["red";"blue";"green"]
    
    let index = 
      html [
          head [
              title "Suave.Experimental"
          ]
    
          body [
    
              h1 (text ("Hello Experimental!"))
              p [ (text (message + " is " + string answer))]
              p [ (text ("The greeting is:" + greetingMessage)) ]
              p [ (text ("The content of colors is:")) ]
              ul [ for color in colors -> li (spanStyle ("color:" + color) (text color)) ]
          ]
      ]
      |> xmlToString
    

Este sistema de plantillas es el que posiblemente se nos haga más raro de utilizar inicialmente, sobre todo porque tenemos que aprender una nueva sintaxis y en muchas ocasiones tendremos que crea funciones para facilitarnos a estructurar el código para que sea mucho más expresivo.

El modulo **Suave.Html** define cuatro tipos básicos: `Attribute`, `Element`, `Xml` y `Node`. La combinación de estos tipos nos va permitir generar toda la estructura de la página HTML. Con el tipo **Attribute** podemos definir una tupla de dos cadenas, **Element** es una unión discriminada para representar elementos que van dentro de un elemento HTML como un elemento que contiento el nombre, el namespace y un array de atributos, **Xml** es una lista de nodos y cada nodo es un Elemento y otro Xml. Además de estos tipos básicos tenemos una serie de funciones Helpers para crear distintos elementos HTML: input, br, img, span, p, div, body, script, link, title, head, html

Si examinamos el código anterior del fichero View.fs, vemos que declaramos un valor `index` que va a contenter una representación del código HTML completo. La función `html` es una función que recoge una lista de otros _tags_ como argumentos, en este caso `head` y `body`. La función `text` nos sirve para definir texto plano en un elemento HTML. También vemos que además de estas funciones _helper_ que están definidas en el módulo **Suave.Html**, en muchas ocasiones tendremos que definir nuestras funciones auxiliares que nos ayuden a declarar elementos. En este caso hemos definido una función `h1` que crea un _tag_ h1 sin atributos. De forma similar definimos la función `ul` en la que utilizamos como tercer parámetro la función `flatten` que concatena una lista de elementos, o la función `spanStyle` que crea un elemento span con el atributo style. Por último, la función `xmlToString` transforma el XML generado a partir de todo modelo en una cadena HTML.

Una vez tenemos la estructura de la vista definida, tenemos que modificar la WebPart para que devuelva el HTML en la respuesta de la forma siguiente.

    let webPart = path "/" >=> OK View.index
    

DotLiquid
---------

El último sistema de templates que vamos a ver es **DotLiquid**, un _port_ a .NET del sistema de plantillas de Ruby. Esta aproximación es muy similar a la que vimos con Razor, ya que con DotLiquid tenemos las plantillas en ficheros HTML con el único cambio es la sintaxis. Como en los dos casos anteriores, para utilizar el motor de _DotLiquid_ debemos añadir la referencia al paquete y al namespace de **Suave.DotLiquid**. A continuación vemos el mismo contenido de la plantilla que vimos en el primer ejemplo, pero con la sintaxis Liquid.

La sintaxis utilizada en las plantillas de DotLiquid es muy similar a la utilizada en **mustache** o **angularJS**. Se utiliza la doble llave para expresiones que se deben reemplazar por texto y dentro de `{% %}` para funciones especiales como en el caso del bucle `for` que vemos en el ejemplo. La documentación completa de la sintaxis completa se puede consultar aquí: [Liquid For Designers](https://github.com/Shopify/liquid/wiki/Liquid-for-Designers). También es posible definir nuestras propias variables dentro de la plantilla para poder utilizarlas posteriormente. La forma más fácil es utilizando el tag `assign` como vemos en el ejemplo para crear la variable `answer`.

En este caso, vamos a generar un tipo con todas las propiedades que necesita nuestro modelo y lo pasamos al motor de **DotLiquid** para generar la vista.

    type OS = { Name: string; }
    type Model = { message:string; weekday:string; colors: string list; products: OS list }
    
    let OSList =  [ { Name = "OSX"; }
                    { Name = "Android"} 
                    { Name = "Windows Phone"} ]
    
    let model = { message = "The answer to life the universe and everything";
                  weekday = System.DateTime.Now.DayOfWeek.ToString()
                  colors = ["red";"blue";"green"]
                  products = OSList }
    
    let webPart = path "/" >=> (DotLiquid.page "index.html" model )
    

En este caso pasamos a la función `page` el nombre de la página completo (index.html) y el modelo.

Contenido estático
------------------

Suave solo es capaz de servir los ficheros que están en algunas de las rutas definidas en las WebParts. Es decir, si hacemos una petición a `http://localhost:8083/styles.css`, el servidor nos devolverá un error ya que al no haber una WebPart que responda a esa ruta, no es capaz de manejar esa petición. Para poder servir contenido estático, tenemos que añadir otra alternativa a la función `choose`.

    pathRegex "(.*)\.css" >=> Files.browseHome
    

La WebPart `pathRegex` devuelve `Some` si el _path_ de una petición coincide con el patrón de la expresión regular. En caso afirmativo, se aplicará la WebPart **Files.browseHome**, que sirve ficheros los estáticos que está a partir del directorio raíz de la aplicación. Ahora podemos añadir un fichero CSS al proyecto, sin olvidar establecer el valor de la propiedad “Copy to Output Directory” a “Copy if never” y añadir la referencia en nuestro HTML. En el caso de **Suave.Experimental**, nos podemos crear una función para generar un elemento link.

    let cssLink href = linkAttr [ "href", href; " rel", "stylesheet"; " type", "text/css" ]
    

Y añadirlo en la cabecera de la siguiente forma:

    head [
            title "Demo"
            cssLink "/Styles.css"
         ]
    

Resumen
-------

En este artículo hemos visto el funcionamiento y sintaxis básica de **Suave** para definir las vistas de nuestra aplicación web tres motores de renderizado de vistas que soporta Suave: **Suave.Razor**, **Suave.Experimental** y **Suave.DotLiquid**.

Referencias
-----------

[Introduction to ASP.NET Web Programming Using the Razor Syntax (C#)](http://www.asp.net/web-pages/overview/getting-started/introducing-razor-syntax-c)  
[DotLiquid - Safe templating system for .NET](http://dotliquidmarkup.org/)  
[Liquid For Designers](https://github.com/Shopify/liquid/wiki/Liquid-for-Designers)  
[Suave.IO Source Code](https://github.com/SuaveIO/)
