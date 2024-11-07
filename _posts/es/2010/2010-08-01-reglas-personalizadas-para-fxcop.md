---
title: Reglas personalizadas para FxCop
tags: [programming]
reviewed: true
---
En una entrada anterior vimos [cómo integrar **FxCop** con Visual Studio](/integrando-fxcop-10-en-visual-studio), el siguiente paso lógico que debemos dar es crear nuestras propias reglas de análisis de código. Vamos a ver que la dificultad no está en cómo crear estas reglas, sino en averiguar cuáles son las que necesitamos y cómo de complejo queremos hacer el análisis de esas reglas.

En esta entrada vamos a crear una sencilla regla con la que podremos verificar que las clases de un ensamblado tienen una única responsabilidad. Para los que no sepáis a qué me estoy refiriendo con esto, lo aclaro brevemente: existe un principio de diseño de la programación orientada a objetos, y en concreto sobre el diseño de clases, que dice que una clase debe tener una única responsabilidad. Este principio, como no podría ser de otra forma, se llama [SOLID](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod).

¿Cómo conseguir esto con una regla de análisis de código? Pues la verdad es que no resulta sencillo, pero podemos tener un indicador bastante fiable si comprobamos la cantidad de métodos públicos y protegidos que exponen nuestras clases. Si una clase tiene, por ejemplo, 20 o más métodos públicos es casi seguro que estamos dando a esta clase más responsabilidades de las necesarias; la clase hace demasiadas cosas. Tengo que destacar el “casi seguro”, ya que he elegido 20 arbitrariamente, no hay un número concreto que indique que a partir de ahí, la clase hace mucho. Es posible (aunque poco probable) que nos encontremos clases con 20 métodos que tengan una única responsabilidad y otras con 5 métodos que tengan más de una responsabilidad. De todas formas, creo que es un buen indicador y un buen ejemplo para introducir las reglas personalizadas para **FxCop**.

Para crear un conjunto de reglas debemos crear un proyecto de **Biblioteca de clases** (_Class Library_) y añadir las referencias **FxCopSdk.dll** y **Microsoft.Cci.dll** que se encuentran en el directorio de **FxCop**. En el proyecto añadiremos una clase que herede de **BaseIntrospectionRule** por cada regla que queramos añadir y un fichero XML con la descripción de las reglas.

El código mínimo de la clase de una regla es el siguiente:

```csharp
using Microsoft.FxCop.Sdk;

namespace SolidRules { 
  public class SingleResponsibilityCheck : BaseIntrospectionRule { 
    public SingleResponsibilityCheck() : base(“SingleResponsibility”, “SolidRules.Rules”, typeof(SingleResponsibilityCheck).Assembly) 
    { } 
  } 
}
```

En el constructor hay que llamar al constructor de la clase base **BaseIntrospectionRule** pasando 3 parámetros: el nombre de la regla, el nombre del fichero XML de documentación, incluyendo el _namespace_, y el ensamblado al que pertenece la clase.

El siguiente paso es añadir un nuevo fichero XML a nuestro proyecto y asignarle el valor **Recurso incrustado** (_Embebbed resource_) a la propiedad **Acción de compilación** (_Action Build_), para que se incruste dentro del ensamblado del proyecto. El contenido de este fichero debe ser el siguiente:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Rules FriendlyName="SOLID Rules">
    <Rule TypeName="SingleResponsibility" Category="Design" CheckId="IB001">
        <Name>Single Responsibility Principle</Name>
        <Description>Every object should have a single responsibility, and that responsibility should be entirely encapsulated by the class.</Description>
        <Owner>IdleBit</Owner>
        <Url>http://www.idlebit.es/2010/08/01/reglas-personalizadas-para-fxcop</Url>
        <Resolution>'{0}' has {1} public or protected methods. A class or module should have one, and only one, reason to change. Refactor into new classes.</Resolution>
        <Email></Email>
        <MessageLevel Certainty="99">Warning</MessageLevel>
        <FixCategories>NonBreaking</FixCategories>
    </Rule>
</Rules>
```

De este fichero, sólo habría que destacar varios detalles que hay que tener en cuenta. El elemento _Resolution_ acepta elementos de formato, que podemos utilizar para mostrar el valor de cualquier objeto. El _MessageLevel_ describe el porcentaje de exactitud que creemos que tiene la regla y la gravedad del mensaje (_CriticalError_, _Error_, _CriticalWarning_, _Warning *, *Information_). Y por último, aunque parece evidente, que en un mismo fichero XML podemos añadir tantos elementos _Rules_ como queramos.

A continuación, vamos a añadir el código que verifique el número de métodos de cada clase. Esto lo hacemos utilizando la sobrecarga del método **Check** que acepta un parámetro de tipo **TypeNode**. En este método añadimos a una lista todos los métodos de la clase públicos o protegidos. Si al final de procesar todos los métodos de la clase obtenemos un número superior a 20, añadimos un nuevo elemento a la colección _Problems_. La implementación queda como sigue:

```csharp
public override ProblemCollection Check(TypeNode type)
{
  var methods = new List<string>();

  var cls = type as ClassNode;

  if (cls != null)
  {
    foreach (var methodName in from method in cls.Members
                               let methodName = method.Name.ToString()
                               where !methods.Contains(methodName) && (method.IsPublic || method.IsFamily)
                               select methodName)
    {
      methods.Add(methodName);
    }

    if (methods.Count > 20)
    {
      var resolution = GetResolution(new\[\] { cls.Name.ToString(), methods.Count.ToString() });
      Problems.Add(new Problem(resolution));
    }
  }

  return Problems;
}
```

Sólo queda compilar y agregar el *assembly* al directorio Rules de FxCop. Al ejecutar nos aparecerá el nuevo grupo (*SOLID rules*) con una sola regla. En el proyecto que os podéis descargar al final de la entrada, he incluido un proyecto con una clase para probar la nueva regla. Si analizamos este ensamblado mediante la aplicación de FxCop obtendremos un resultado parecido al siguiente:

Y si ejecutáis el análisis en Visual Studio mediante los *Build Events*, la pantalla de errores mostrará el siguiente aspecto:


Y ahora, ¿quién se anima a mejorar esta y añadir el resto de reglas para principios SOLID?

**Descargar código fuente**  
[SOLIDRules.zip](/files/SOLIDRules.zip) 
