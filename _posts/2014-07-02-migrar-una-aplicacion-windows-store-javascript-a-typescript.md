---
title: Migrar una aplicación Windows Store JavaScript a TypeScript
tags: [typescript, windows_store, winjs]
reviewed: true
---
Con la [última actualización de Visual Studio 2013](http://www.microsoft.com/es-es/download/details.aspx?id=42666) se liberó la versión 1.0 de [TypeScript](http://www.typescriptlang.org/), la primera release oficial del lenguaje después de año y medio de desarrollo. Además, con esta actualización TypeScript pasa a ser un lenguaje totalmente soportado en Visual Studio y sin necesidad de ninguna extensión tenemos comprobación estática de código, navegación basada en símbolos, refactorización, etc.

A partir de ahora, si en un proyecto ASP.NET añadimos o renombramos un fichero TypeScript, se añaden automáticamente las referencias a los “targets” y propiedades de MSBuild para poder compilarlos. Además en el mismo momento que agregamos un fichero TS, nos pregunta si queremos añadir paquetes NuGet con las definiciones de tipos de las librerías JavaScript más comunes.

Sin embargo, no sucede lo mismo si realizamos la misma acción en un proyecto **Windows Store JavaScript**, es decir, al añadir un fichero TypeScript en una solución Windows Store, el proyecto no se actualiza y por lo tanto no podremos compilar ningún fichero .ts.

En esta entrada vamos a ver los cambios que tenemos que hacer manualmente en el proyecto para tener soporte de compilación para TypeScript.

Modificando el fichero .jsproj
------------------------------

Para mostrar cómo habilitar la compilación de TypeScript, voy a utilizar como ejemplo el código de una aplicación creada con la plantilla Hub y aprovecharemos para ver cómo migrar todo el código JavaScript a TypeScript.

El primer paso es añadir el **Import** de las propiedades predeterminadas. Recordad que para poder modificar el fichero .jsproj, tenemos que descargar el proyecto de la solución y luego seleccionar la opción Editar en el menú contextual. Una vez abierto, añadiremos justo antes del primer **ItemGroup** la siguiente línea:

```xml
<Import Project="$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.Default.props" Condition="Exists('$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.Default.props')" />
```

Y al final del fichero, justo después del último Import añadiremos la referencias a los tres targets.
    
```xml
<Import Project="$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.targets" 
        Condition="Exists('$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.targets')" />

<Import Project="$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.Microsoft.TypeScript.jsproj.targets" 
        Condition="Exists('$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.TypeScript.Microsoft.TypeScript.jsproj.targets')" />

<Import Project="$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.VisualStudio.WJProject.targets" 
            Condition="Exists('$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\TypeScript\Microsoft.VisualStudio.WJProject.targets')" />
```
    
Una vez realizados estos cambios podemos recargar el proyecto y comenzar a realizar la migración del código JavaScript a TypeScript.
    
Compilando TypeScript
---

Cuando afrontemos una migración de una aplicación JavaScript a TypeScript no vamos a tener que migrar todo el código de la aplicación de una sola vez, podemos migrar la solución fichero a fichero. Además tenemos que tener en cuenta que todo código JavaScript es también un código válido TypeScript, así que el primer paso para migrar un fichero es simplemente cambiar la extensión de js a ts y el código seguirá funcionando a no ser que tengamos referencias a librerías externas. En nuestro caso, el primer fichero que vamos a cambiar es data.js, ya que es el único que no tiene ninguna referencia a otro módulo.
    
Si abrimos el fichero **data.ts** y si tenemos instalada la extensión [Web Essentials](http://visualstudiogallery.msdn.microsoft.com/56633663-6799-41d7-9df7-0f2a504ca361), veremos la ventana de código partida en dos vistas, en el lado izquierdo veremos el código TypeScript y en el lado derecho el código JavaScript compilado, que en un primer mostrará el mensaje “Not compiled to disk yet”, ya que todavía no hemos compilado la aplicación. 
    
   
Para poder compilar el fichero, tenemos que seleccionar la opción “Reset to Default” en la propiedad **Package Action** y automáticamente cambiará a **TypeScriptCompile**. Con esto estamos indicando a VS que compile los ficheros TypeScript al generar el paquete.
      
Y ahora sí, si guardamos el fichero aparecerá al cabo de unos instantes el código JavaScript compilado. La compilación se realizar al guardar ya que una de las propiedades por defecto de **Web Essentials** es compilar al guardar. Podemos cambiar este comportamiento en **Opciones > Web Essentials > TypeScript**.
    
En este momento el código que tendremos en las dos vistas será exactamente el mismo y si abrimos el contenido de la carpeta js veremos que además del fichero **data.js** se ha generado el fichero data.map, que utiliza Visual Studio para poder depurar el código TypeScript directamente.
     
Agregar Type Definitions
---    
    
Si ejecutamos la aplicación, obtendremos varios errores de compilación "*Could not find symbol 'WinJS'*", lo que nos indica que el compilador no encuentra el símbolo WinJS. Este problema, como comentaba antes, nos sucederá siempre que utilicemos una librería JavaScript externa. Para solventar este problema recurriremos a las declaraciones de tipos, que básicamente consisten en un fichero de declaración (d.ts) que describe la firma de esa librería. 
    
Pero por suerte no tendremos que escribir nosotros ese fichero de declaración. El proyecto [DefinitelyTyped](https://github.com/DefinitelyTyped) contiene las definiciones para las principales librerías JavaScript, entre las que encontramos WinJS y WinRT. Además estas definiciones las tenemos disponibles en NuGet, así que para agregarlas al proyecto simplemente tenemos que añadir los paquetes **winjs.TypeScript.DefinitelyTyped** y **winrt.TypeScript.DefinitelyTyped** ejecutando en la Package Manager Console los dos comandos:
    
```xml
    Install-Package winjs.TypeScript.DefinitelyTyped
    Install-Package winrt.TypeScript.DefinitelyTyped
```
    
Después de agregarlos, podremos ver una nueva carpeta **typings** dentro de la carpeta **Scripts**, que contendrá los dos ficheros de declaraciones que tendremos que referenciar utilizando el tag reference al principio del fichero data.ts.
    
```js
/// <reference path="../Scripts/typings/winrt/winrt.d.ts"/>
/// <reference path="../Scripts/typings/winjs/winjs.d.ts"/>
```
    
Después de añadir esta referencia, desaparecerá el primer error de compilación y podremos continuar migrando nuestro código.
    
Migrando código a TypeScript
---    
    
El primer cambio que vamos a realizar es sustituir la declaración del *namespace* que se hace mediante la función **WinJS.Namespace.define** por un módulo, que es la forma que tenemos en TypeScript para organizar el código. Y como queremos que todas las funciones que antes se exponían en el namesapce sigan siendo visibles fuera del módulo, anteponemos a cada función la palabra clave **export**.
    
El código de momento queda de la siguiente forma:
    
```js
module Data {

    var list = new WinJS.Binding.List();

    var groupedItems = list.createGrouped(
        function groupKeySelector(item) { return item.group.key; },
        function groupDataSelector(item) { return item.group; },
        null
        );

    generateSampleData().forEach(function (item) {
        list.push(item);
    });

    export var groups = groupedItems.groups;
    
    export function getItemReference(item) {
        return [item.group.key, item.title];
    }

    export function getItemsFromGroup(group) {
        return list.createFiltered(function (item) { return item.group.key === group.key; });
    }

    export function resolveGroupReference(key) {
        return groupedItems.groups.getItemFromKey(key).data;
    }

    export function resolveItemReference(reference) {
        for (var i = 0; i &lt; groupedItems.length; i++) {
            var item = groupedItems.getAt(i);
            if (item.group.key === reference[0] && item.title === reference[1]) {
                return item;
            }
        }
    }

    function generateSampleData() {
        var itemContent = "&lt;p&gt;Curabitur …";
        var itemDescription = "Item Description…";
        var groupDescription = "Group Description: …";

        var darkGray = "data:image/png;base64, …";
        var lightGray = "data:image/png;base64, …";
        var mediumGray = "data:image/png;base64, …";

        var sampleGroups = [
            { key: "group1", title: "Group Title: 1", subtitle: "Group Subtitle: 1", backgroundImage: darkGray, description: groupDescription },
            …

        return sampleItems;
    }
}
```
    
El siguiente error que tenemos es “*The property 'group' does not exist on value of type '{}'*” provocado en la llamada a la función **createGrouped**.
    
```js
var groupedItems = list.createGrouped(
    function groupKeySelector(item) { return item.group.key; },
    function groupDataSelector(item) { return item.group; },
    null
    );
```

Esto es debido a que la lista **WinJS.Binding.List** no estamos explicitando el tipo. Una forma de solucionarlo sería utilizando el tipo Any.
    
```js
var list = new WinJS.Binding.List&lt;any&gt;();
```
    
El tipo Any nos puede ser de mucha utilidad cuando estemos realizamos migraciones de código JavaScript, porque nos permite introducir tipos de forma gradual y decidir en que momento queremos comprobación de tipos. Si no asignamos un tipo a una variable, se asigna el tipo Any y podremos establecer cualquier valor, ya sean objetos complejos o simples, es decir, actuará como una variable de tipado dinámico de JavaScript. Pero como podréis suponer, siempre deberemos optar por asignar un tipo especifico en lugar de utilizar el tipo Any.
    
Con TypeScript podemos definir un tipo de objeto mediante el uso de interfaces. El concepto de interfaz es muy común para los programadores de .NET, pero la interfaz de TypeScript tiene algunas diferencias fundamentales con las de .NET.
    

* Son una construcción solo de tiempo de diseño para proporcionar comprobación de tipos, intellisense y refactorización. Al compilar desaparecer y son sustituidas por los tipos de objetos que representan.
* No son heredadas por las clases. Son tipos de objetos para aplicar a variables, parámetros y tipos de retono.
* Son open-ended. Podriamos hacer la analogía a las clases parciales de .NET, que podemos definir en varios archivos y el tipo final es la combinación de todas las partes.
    
A continuación definimos dos interfaces para los tipos de objeto grupo (**ISampleGroup**) y elemento (**ISampleItem**)

```ts    
export interface ISampleGroup {
    key: string;
    title: string;
    subtitle: string;
    backgroundImage: string;
    description: string;
}

export interface ISampleItem {
    group: ISampleGroup;
    title: string;
    subtitle: string;
    description: string;
    content: string;
    backgroundImage: string;
}
```

Y utilizamos el tipo al crear la instancia de la **Binding.List**.

```ts    
var list = new WinJS.Binding.List<ISampleItem>();
```

Con estos cambios ya podemos compilar y ejecutar la aplicación de forma normal, pudiendo depurar el código TypeScript directamente.
    
El siguiente fichero con el que continuaremos la migración de código será **navigator.js**, siempre siguiendo la regla de migrar con los módulos que no tienen dependencias con otros módulos.
    
Al igual que con data.ts, lo primero que haremos será sustituir el **namespace** por un módulo. Una vez hecho esto nos encontraremos que en este caso tenemos una clase definida mediante **WinJS.Class.define**. En TypeScript podemos definir clases de forma muy similar a lo que lo hacemos en C#.

```ts
export class PageControlNavigator {
    
    public element = <HTMLElement>null;
    public home = "";
    \_lastNavigationPromise = WinJS.Promise.as(null);
    \_lastViewstate = 0;
    \_disposed = false;
    \_eventHandlerRemover = \[\];

    constructor(element: Element, options: { home: string } ) {
        this.element = <HTMLElement>(element || document.createElement("div"));
        this.element.appendChild(this.createPageElement());

        this.home = options.home;

        var that = this;

        function addRemovableEventListener(e, eventName, handler, capture) {
            e.addEventListener(eventName, handler, capture);
            that.\_eventHandlerRemover.push(function () {
                e.removeEventListener(eventName, handler);
            });
        };

        addRemovableEventListener(nav, 'navigating', this.navigating.bind(this), false);
        addRemovableEventListener(nav, 'navigated', this.navigated.bind(this), false);

        window.onresize = this.resized.bind(this);
        Application.navigator = this;
    }

    // Código omitido
}
```

La única diferencia evidente es que la función constructora está marcada con la palabra clave **constructor**.
    
El último detalle importante es que la clase **PageControlNavigator** se utiliza de forma declarativa en la página default.html, así que es necesario marcar la clase como compatible con el procesamiento declarativo, ya que en caso contrario obtendremos la excepción “_Value is not supported within a declarative processing context_”.

```ts    
WinJS.Utilities.markSupportedForProcessing(PageControlNavigator);
```   
    
Esto no era necesario en el código JavaScript por que al definir una clase con **WinJS.Class.define**, internamente se realiza una llamada a este método.

Una vez convertido el fichero navigator.js, continuaríamos con default.js y los controles de página (hum, section, ítem), siguiendo el mismo procedimiento que hemos seguido hasta ahora. Tenéis todo el código disponible en un repositorio de GitHub ([https://github.com/acasquete/TypeScriptStoreApps](https://github.com/acasquete/TypeScriptStoreApps))

Plantillas Windows Store con TypeScript
---------------------------------------

En este post hemos visto como habilitar la compilación y realizar la migración de un proyecto ya existente, pero si lo que quieres hacer es un nuevo proyecto, he creado una extensión de Visual Studio que añade las tres plantillas básicas de proyecto (blank, navigation y hub) de Windows Store con TypeScript. La extensión está disponible para descarga desde la [Visual Studio Gallery](http://visualstudiogallery.msdn.microsoft.com/bd97e47d-ed3a-4f5e-ace2-37bbcb545c9e).

Al instalarla tendremos disponible en la categoría **TypeScript** las tres nuevas plantillas con todo código en TypeScript y lista para subir a la Store.

Happy TypeScripting!

Referencias
-----------

[TypeScript Lang](http://www.typescriptlang.org/)  
[Store Apps Templates with TypeScript](http://visualstudiogallery.msdn.microsoft.com/bd97e47d-ed3a-4f5e-ace2-37bbcb545c9e)  
[Use TypeScript in Modern Apps](http://msdn.microsoft.com/en-us/magazine/dn201754.aspx)  
