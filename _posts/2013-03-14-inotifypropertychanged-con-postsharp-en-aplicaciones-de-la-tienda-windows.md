---
title: INotifyPropertyChanged con PostSharp en aplicaciones de la Tienda Windows
tags: [aop, windows_store, winrt]
---
He hablado alguna vez de la [programación orientada a aspectos](/tags/aop), y muchos sabéis de mi debilidad por [PostSharp](http://www.postsharp.net/), el que considero el mejor Framework para implementar aspectos. Hoy traigo de nuevo este tema, porque la versión RTM de **PostSharp 3** está muy próxima a ser liberada y como gran novedad, en esta última versión, se ha añadido soporte completo para Windows 8 y Windows Phone, así que ya no tenemos excusa para no utilizar aspectos en nuestras aplicaciones. De hecho, con esta versión vamos a poder crear aspectos portables, que vamos a poder utilizar en las dos plataformas.

Para mostrar la utilidad de los aspectos vamos a ver cómo implementar automáticamente **INotifyPropertyChanged** en una aplicación para la Windows Store. Creo que todo el que haya trabajado con MVVM ha sufrido y sabe que el crear los _bindings_ de un objeto con los elementos de la vista, además de ser sumamente aburrido, nos ensucia el código y es foco de no pocos errores. Si queréis leer más información sobre implementación de MVVM, [@jvinyes](https://twitter.com/jvinyes) tiene una [serie de posts introducciorios bastante aclaratorios](http://blog.techdencias.net/blog/2013/03/12/capitulo-2-breve-introduccion-a-mvvm/). La forma más básica de implementar **INotifyPropertyChanged**es con un código similar a este (¡manos a la cabeza!):

public class EmployeeViewModel : ViewModelBase { private string street; private string city;

    public string Street
    {
        get { return street; }
        set
        {
            street = value;
            OnPropertyChanged("Street");
            OnPropertyChanged("FullAddress");
        }
    }
    
    public string City
    {
        get { return city; }
        set
        {
            city = value;
            OnPropertyChanged("City");
            OnPropertyChanged("FullAddress");
        }
    }
    
    public string FullAddress
    {
        get
        {
            return GetFullAddress();
        }
    }
    
    private string GetFullAddress()
    {
        var sb = new StringBuilder();
        sb.AppendLine(Street);
        sb.AppendLine(City);
    
        return sb.ToString();
    } }</pre> Como vemos, tenemos que escribir mucho código repetido y además, al estar pasando una cadena como parámetro en **OnPropertyChanged**, estamos convirtiendo nuestro código en una mina de errores. La verdad es que este tipo de implementación ya se ve bien poco, quien más, quien menos, hace uso del algún Framework de MVVM y la cadena se sustituye por una expresión lambda, que nos aporta comprobación en tiempo de compilación. Algo así:
    

public string City
{
    get { return city; }
    set
    {
        city = value;
        OnPropertyChanged(()=>City);
        OnPropertyChanged(()=>FullAddress);
    }
}

Mejoramos, pero el problema de raíz persiste. Y es ahora cuando llegamos a las aplicaciones de la **Windows Store** y a las novedades del Framework .NET 4.5. Aquí nos encontramos con un nuevo invento en forma de atributo [**CallerMemberName**](http://msdn.microsoft.com/es-es/library/system.runtime.compilerservices.callermembernameattribute.aspx). Podéis ver su uso en la clase BindableBase que se utiliza como clase base para los ViewModel. Básicamente lo que nos permite este atributo es aplicarlo a un parámetro opcional de un método y si no pasamos nada obtiene el nombre del método que lo llama. Un atributo hecho a medida para una implementación básica de **INotifyPropertyChanged**. Utilizando este atributo, nuestro código pasaría a tener esta forma:

public string City
{
    get { return city; }
    set
    {
        city = value;
        OnPropertyChanged();
        OnPropertyChanged(()=>FullAddress);
    }
}

Nos ahorramos un poco de código, pero el problema sigue estando ahí, bien presente. El problema lo tenemos, sobre todo, cuando tenemos dependencias de propiedades, es decir, que cuando al establecer el valor a una propiedad, tengamos que actualizar otra. En nuestro ejemplo, cuando actualizamos la propiedad _City_, queremos actualizar la propiedad _FullAddress_, ya que la última depende del valor de la primera. Así que, código duplicado aparte, tenemos que gestionar las dependencias entre propiedades. Algo falla, ¿no?. Sí, pero seguimos y seguimos haciendo este tipo de código como si no tuviésemos alternativa, ¡y tenemos unas cuantas! Vamos a ver una de ellas.

    ## Simplificando nuestro código con PostSharp
    

Después de toda esta parrafada, este es el momento en el que entra en escena la última versión de **PostSharp**. Lo primero que tenemos que hacer es descargar la última versión mediante NuGet. Como he dicho al principio de la entrada, la versión 3 todavía está en _Preview_, así que tenemos que marcar la opción “Include PreRelease” para que nos aparezca en los resultados.

[![postsharp-nuget](/img/postsharp-nuget.png)](/img/postsharp-nuget.png)

Una vez tenemos **PostSharp** referenciado en nuestro proyecto, solo tenemos que ir a cualquier ViewModel, pulsar sobre el **Smart Tag** del nombre de la clase y seleccionar en el menú la opción “Implement INotifyPropertyChanged”.

[![postsharp-smarttag](/img/postsharp-smarttag.png)](/img/postsharp-smarttag.png)

La primera vez que lo hagamos, nos aparecerá un asistente para agregar la **Model Pattern Library**. Esta librería es la encargada de hacer toda la magia, la que se encarga, entre otras cosas, de analizar las dependencia entre propiedades, métodos y campos del código fuente. Al pulsar “Continuar”, se descargará y agregará automáticamente a nuestro proyecto la referencia a **PostSharp.Patterns.Model**.

Además de esto, veremos que ahora nuestra clase tiene aplicado el atributo **NotifyPropertyChanged**. Esté atributo añadirá automáticamente la implementación de **INotifyPropertyChanged** y el código necesario para notificar el cambio de cada una de las propiedades. Por lo tanto, a partir de este momento podemos dejar de heredar de **BindableBase**y limpiar nuestro código utilizando propiedades autoimplementadas. Después de la limpieza nuestro código debería quedar mucho más claro:

\[NotifyPropertyChanged\]
public class EmployeeViewModel
{
    public string Street { get; set; }

    public string City { get; set; }

    public string Province { get; set; }

    public string PostalCode { get; set; }

    public string FullAddress
    {
        get { return GetFullAddress(); }
    }

    private string GetFullAddress()
    {
        var sb = new StringBuilder();
        sb.AppendLine(Street);
        sb.AppendLine(City);
        sb.AppendLine(Province);
        sb.AppendLine(PostalCode);

        return sb.ToString();
    }
}

¡Y lo mejor de todo es que todo seguirá funcionando igual! Para terminar, en lugar de aplicar el atributo a todas las clases de los ViewModel o entidades de nuestra aplicación, podemos hacer uso del atributo **Multicast** de PostSharp. Para utilizarlo tenemos que abrir el fichero AssemblyInfo.cs de nuestro proyecto y añadir la siguiente línea:

\[assembly: NotifyPropertyChanged(AttributeTargetTypes = "AOPNotification.ViewModels.\*")\]

Esta línea es equivalente a añadir el atributo a todas las clases del namespace AOPNotification.ViewModels. Y hasta aquí esta entrada en la que hemos visto cómo podemos simplificar el código de nuestros ViewModel eliminando código repetitivo y dejando la responsabilidad de la notificación y gestión de dependencias de propiedades a \*\*PostSharp\*\*.


Referencias
---

[http://www.postsharp.net/model](http://www.postsharp.net/model)
[Automatically implementing INotifyPropertyChanged](http://www.postsharp.net/model/inotifypropertychanged)

