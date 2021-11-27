---
title: Windows Store apps y F#
tags: [windows_store, fsharp]
---
Cuando hablamos de desarrollo de aplicaciones para la Windows Store, **F#** es el gran ausente en los diagramas que presentan la plataforma de **Windows 8**. El motivo es evidente: C#, Visual Basic, C++ y JavaScript son los únicos lenguajes con los que podemos crear proyectos de aplicación completos. Destacando especialmente los dos últimos, porque por primera vez podemos desarrollar aplicaciones nativas para Windows 8 utilizando C++ con XAML y JavaScript con HTML. Sin embargo, con F# no sucede lo mismo, en Visual Studio 2012 no disponemos de unas plantillas que nos permitan crear una aplicación para Windows 8 utilizando F#.

Esto es así porque, a pesar de ser un lenguaje totalmente soportado en la plataforma .NET, la filosofía de Microsoft en cuanto al rol de **F#** no ha sido la de proporcionar otro lenguaje como C# o VB, sino que ha enfocado el lenguaje exclusivamente a las áreas de programación donde proporciona una mayor productividad.

La programación funcional tradicionalmente siempre ha estado relacionada con el análisis y codificación de algoritmos. Ahora con **F# 3.0**, las mejoras se han orientado más al acceso a datos, así que, hasta el momento (ya veremos lo que sucede en el futuro), el _front-end_ queda relegado a los proyectos de C#, C++, VB, HTML5 y Javascript. Sin embargo, en esta entrada vamos a ver cómo podemos reaprovechar el código que tengamos escrito en F# para utilizarlo en una aplicación para Windows 8 y veremos algunas sugerencias de diseño por si alguno se aventura a crear componentes escritos desde cero.

Si queremos utilizar nuestro código **F#** en una aplicación para Windows 8, tendremos que incluirlo en una [librería portable](http://msdn.microsoft.com/es-es/library/gg597391.aspx). Esto comporta otra limitación más, y es que tampoco podremos utilizarlo directamente en proyectos JavaScript, ya que en estos solo se permite referenciar SDKs o componentes **Windows Runtime** y no librerías portables. Veremos luego de qué forma podemos salvar esta limitación.

Al crear un nuevo proyecto de librería portable (_F# Portable Library_) se genera automáticamente un fichero (_PortableLibrary1.fs_) con la definición de una clase _Class1_ con un solo miembro al que se le asigna el valor “F#”.

namespace FSharpLibrary type Class1() = member this.X = “F#”</pre> Antes de referenciar esta librería en un proyecto de una aplicación para la Windows Store, vamos a modificar este código autogenerado por una funcionalidad un poco más compleja (aunque no mucho más). Vamos a crear un método que nos devuelva una secuencia “infinita” de números primos. Primero creamos el tipo _PrimeNumbers_ con un método estático (_isPrime_), que determina si un número es primo o no, y una propiedad estática (_Primes_) que devuelve la secuencia de números primos. No es el objetivo de esta entrada tratar la síntaxis y el uso de las [funciones recursivas](http://msdn.microsoft.com/es-es/library/dd233229.aspx) y [secuencias](http://msdn.microsoft.com/es-es/library/dd233209.aspx), así que podéis consultar los enlaces de la MSDN en el caso de que queráis más información.

namespace FSharpLibrary

type PrimeNumbers =
    static member isPrime n =
        let rec check i =
            i > n/2 || (n % i <> 0 && check (i + 1))
        check 2

    static member Primes =
        Seq.initInfinite (fun i -> i + 2)
        |> Seq.filter PrimeNumbers.isPrime

Quiero remarcar, llegados a este punto, que cuando diseñemos librerías en **F#** que se van a usar desde otros lenguajes .NET es importante que sigamos las guías de diseño descritas en el documento [F# component design guidelines](http://research.microsoft.com/en-us/um/cambridge/projects/fsharp/manual/fsharp-component-design-guidelines.pdf). Una de las recomendaciones que aparece en este documento es que debemos proporcionar una API familiar y consistente con el resto del Framework .NET, minimizando el uso de construcciones específicas de F# en la API pública. En el código anterior, por ejemplo, en lugar de haber definido un tipo con miembros estáticos, podríamos utilizar la definición de un módulo de la siguiente forma:

namespace FSharpLibrary

module PrimeNumbers =
    let isPrime n =
        let rec check i =
            i > n/2 || (n % i <> 0 && check (i + 1))
        check 2

    let Primes =
        Seq.initInfinite (fun i -> i + 2)
        |> Seq.filter isPrime

Sin embargo, es preferible utilizar tipos estáticos en lugar de módulos, ya que permiten la evolución futura de la API para utilizar sobrecarga y otros conceptos de diseño que no pueden ser utilizados en los módulos de **F#**. El uso de módulos quedaría para contener tipos y funciones de utilidad.

Una vez tenemos la librería portable creada y compilada, podemos agregar a la solución un proyecto Windows Store utilizando C# o VB y añadir la referencia al proyecto de la librería portable. A partir de este momento podremos hacer referencia a los métodos definidos en\*\* F#\*\* como si se tratase de cualquier otro tipo de librería. Por ejemplo, en el siguiente código se crea un _Work item_ con un bucle foreach que obtiene en cada iteración un elemento de la colección _FSharpLibrary.PrimeNumbers.Primes_ y lo establece como texto en un control TextBlock.

ThreadPool.RunAsync((source) =>
{
    foreach (var primeNumber in FSharpLibrary.PrimeNumbers.Primes)
    {
        Dispatcher.RunAsync(CoreDispatcherPriority.High,
                            () =>
                                {
                                    PrimeNumber.Text = primeNumber.ToString();
                                });
    }
});

Antes he comentado que las librerías portables solo se pueden referenciar desde aplicaciones C# o VB. Si intentamos añadir una referencia a una librería portable desde una aplicación JavaScript, obtendremos el mensaje “_One or more of the selected items is not a valid reference for this type of project_”. Sin embargo, en aplicaciones JS sí que podemos añadir una referencia a un [componente Windows Runtime](/usar-componentes-winrt-personalizados-desde-javascript). Así que bastará con crear uno y añadirle la referencia a la librería portable de F#. Con el siguiente código definimos la clase de un componente Windows Runtime que encapsula llamadas a la clase de la librería portable.

using System.Collections.Generic;
using FS = FSharpLibrary;

namespace WinRTAdapter
{
    public sealed class PrimeNumbers
    {
        public static bool IsPrime(int number)
        {
            return FS.PrimeNumbers.isPrime(number);
        }

        public static IEnumerable<int> Primes 
        { 
            get { return FS.PrimeNumbers.Primes; }
        }
    }
}

Con la referencia de este componente añadida a un proyecto JavaScript para Windows 8, podremos ser capaces de ejecutar el código F# directamente desde el código JavaScript de la siguiente forma:

var primes = WinRTAdapter.PrimeNumbers.primes.first();

do {
    console.log(primes.current);
} while (primes.moveNext())

Hasta aquí esta entrada en la que hemos visto cómo crear nuestra primera aplicación para la Windows Store en la que aprovechamos código \*\*F# \*\*incluyéndolo en una librería portable y que para la interfaz de usuario nos seguimos apoyando en un proyecto C# o JavaScript.

Para los que todavía no conozcáis F# y queráis comenzar a introduciros en el mundo de la programación funcional y conocer todas las posibilidades que proporciona, os dejo a continuación varios enlaces que ofrecen una gran cantidad de recursos.

[Visual F# Development Portal](http://msdn.microsoft.com/en-us/library/ff730280.aspx) 
[F# 3.0 Sample Pack](http://fsharp3sample.codeplex.com) 
[Try F# Beta](http://preview.tryfsharp.org/) 
[F# component design guidelines](http://research.microsoft.com/en-us/um/cambridge/projects/fsharp/manual/fsharp-component-design-guidelines.pdf) 
