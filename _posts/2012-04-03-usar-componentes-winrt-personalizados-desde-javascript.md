---
title: Usar componentes WinRT personalizados desde JavaScript
tags: [windows_store, winjs, winrt]
---
Desde nuestras **aplicaciones Windows Metro style** creadas con JavaScript podemos acceder a todas las APIs de **Windows Runtime** de la misma forma que lo hacemos desde las aplicaciones Metro creadas con XAML. Lo que no tenemos desde JavaScript es la posibilidad de acceder a toda la funcionalidad que nos proporcionan las librerías de clases del Framework .NET, ni podemos aprovechar el código que ya tengamos en C# o Visual Basic. Sin embargo, en estas situaciones podemos crear un **componente Windows Runtime personalizado**.

Mediante un componente WinRT podemos exponer nuestras propias APIs en C#, Visual Basic o C++ y utilizarlas desde una aplicación Metro con JavaScript. Esto significa que cuando escribamos una aplicación metro JavaScript podremos acceder a la misma funcionalidad que una aplicación XAML, no vamos a tener ninguna limitación. En esta entrada vamos a ver cómo podemos crear nuestros propios tipos en C#, empaquetarlos en un componente WinRT y referenciarlo desde JavaScript.

Comenzamos creando un nuevo proyecto de tipo _Class Library_ para aplicaciones Windows Metro Style. Hay que tener en cuenta que en Visual Studio 11 tenemos dos tipos de proyecto _Class Library_, uno para aplicaciones Metro o componentes Windows Runtime y otro para aplicaciones .NET clásicas.

Una vez tengamos generado el proyecto añadimos la siguiente clase:

using System; using System.Collections.Generic; using System.Linq; namespace Calculator { public sealed class Calc { public static int Suma(int a, int b) { return a + b; } } }</pre> Lo primero que vemos en este código es que la clase está marcada como sellada (_sealed_), esto es así porque desde un **componente WinRT** sólo podemos exportar las clases que estén así marcadas. Por lo tanto, todas las clases que queramos exponer (las clases públicas) deberán estar marcadas con el modificador _sealed_. Si no lo hacemos de esta forma, obtendremos un error de compilación con un mensaje muy esclarecedor: «_Exporting unsealed type is not currently supported. Please mark it as sealed_». Sobra comentarlo, pero obviamente el componente debe tener como mínimo una clase pública.

Por último, tenemos que cambiar la opción _Output type_ de las propiedades del proyecto, de _Class Library_, que es la opción por defecto, a _WinMD File_. Al hacer esto, estamos indicando al compilador que en lugar de generar el componente en una DLL, que sería suficiente si lo fuésemos a utilizar desde un lenguaje manejado, nos genere un fichero **WinMD**, que contiene la versión, metadatos y la implementación. Con esto ya tendremos listo el **componente WinRT** para ser consumido por cualquier aplicación Metro JavaScript.

Lo siguiente es añadir un nuevo proyecto a la solución eligiendo JavaScript como lenguaje y la plantilla de aplicación Metro style en blanco. Después de que se cree, añadimos una referencia al proyecto del componente WinRT y modificamos el fichero _default.js_ para realizar la llamada al componente. Para esta prueba podemos eliminar todo el código generado del fichero JS y escribir lo siguiente:

var result = Calculator.Calc.suma(2, 3);
console.log(result);

Si ejecutamos la aplicación podremos comprobar que la variable _result_ contiene el valor esperado, un 5. Así de simple. Añadiendo la referencia al componente WinRT, hemos realizado desde JavaScript una llamada a nuestro código en C#. Naturalmente este ejemplo no justifica la creación de un componente WinRT, pero como demostración rápida nos vale.

Hay un detalle en el código que los más observadores habréis notado y es que el nombre del método en la llamada ha sufrido una ligera modificación. El método _suma_ no empieza con mayúscula. Esto es debido a una convención para hacer más natural la programación desde JavaScript. Todos los caracteres iniciales del nombre del método que estén mayúsculas se pasan a minúsculas.

En este primer ejemplo hemos utilizado únicamente un tipo de dato básico, el tipo _int_. Pero, ¿qué sucedería si quisiésemos utilizar un tipo distinto? Por ejemplo, ¿Un tipo lista? Probemos añadiendo el siguiente método.

public static int SumaLista(List lista) { return lista.Sum(); }

Si intentamos compilar el código obtendremos el siguiente mensaje (también muy esclarecedor):

    >«*Method 'Calculator.Calc.SumaLista(System.Collections.Generic.List)' has a parameter of type 'System.Collections.Generic.List' in its signature. Although this type is not a valid Windows Runtime type, it implements interfaces which are valid Windows Runtime types. Consider changing the method signature to instead use one of the following types: 'System.Collections.Generic.IList, System.Collections.Generic.IReadOnlyList, System.Collections.Generic.IEnumerable, System.Collections.IList, System.Collections.IEnumerable'.*»
    

Básicamente nos está diciendo que el tipo **List** no se puede utilizar en una clase que queramos exportar, y que en su lugar debemos utilicemos una interfaz (**IList**). No olvidemos que Windows Runtime es un sistema basado en interfaces. Siguiendo las instrucciones del mensaje, cambiamos la firma del método de la siguiente forma.

public static int SumaLista(IList lista) { return lista.Sum(); }

Ahora sí, el código compila y podemos utilizarlo desde JavaScript. Si nos fijamos en el tipo del parámetro en JavaScript, veremos que no es del tipo IList, en su lugar veremos la proyección del tipo, un objeto de tipo [IVector](http://msdn.microsoft.com/en-us/library/windows/desktop/br206631.aspx), que representa una colección de objetos a los que podemos acceder por el índice. Mediante el siguiente código podemos realizar llamada al método _sumaLista_pasando una lista de enteros.

var result2 = Calculator.Calc.sumaLista(\[2,3,5\]);
console.log(result2);

En esta tabla aparecen las principales interfaces genéricas de Windows Runtime y los tipos equivalentes en .NET.

Windows Runtime

.NET Framework

IIterable

IEnumerable

IIterator

IEnumerator

IVector

IList

IVectorView

IReadOnlyList

IMap<k, v="">

IDictionary<tkey, tvalue="">

IMapView<k, v="">

IReadOnlyDictionary

Para finalizar esta entrada, un aspecto que tenemos que tener en cuenta al utilizar componentes WinRT es que no es posible depurar al mismo tiempo el código JavaScript y el código .NET. Eso significa que si depuramos la aplicación Javascript no podremos depurar el componente. Si queremos cambiar este comportamiento predeterminado, tenemos que acceder a las propiedades de la aplicación Metro y cambiar la opción \*Debugger Type\* del apartado \*Debugging\* seleccionando \*Managed Only\* en lugar de \*Script Only\*. De esta forma podremos poner puntos de ruptura y depurar el código de nuestro componente WinRT. Hasta aquí esta primera aproximación a los componentes WinRT personalizados donde hemos visto cómo crear un componente WinRT muy básico utilizando C# y consumirlo desde una aplicación Windows Metro utilizando JavaScript. En próximas entradas seguiremos viendo otros escenarios donde utilizar nuestros componentes WinRT.

Referencias:
---

[Creating a simple component in C# or Visual Basic and calling it from JavaScript](http://msdn.microsoft.com/en-us/library/windows/apps/hh779077(v=vs.110).aspx) 
[Using the Windows Runtime from JavaScript](http://channel9.msdn.com/Events/BUILD/BUILD2011/TOOL-533T) 
