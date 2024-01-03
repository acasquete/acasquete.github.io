---
title: Utilizando Prism en Windows Phone 7.1 Mango (I)
tags: [programming, windows_phone]
reviewed: true
---
**Prism** es un conjunto de librerías que nos facilitan el desarrollo de aplicaciones **WPF** y **Silverlight** de una forma modular, permitiéndonos dividir la funcionalidad de una aplicación compleja en módulos más simples. Uno de los beneficios de utilizar Prism es que estos módulos pueden ser implementados y mantenidos de manera independiente y puede haber una comunicación poco acoplada entre ellos. Esta vendría a ser una definición bastante sencilla y simple de lo que es y nos permite hacer **Prism**.

Hace aproximadamente un año se incorporaron a Prism una serie de librerías para ayudar a desarrollar aplicaciones para **Windows Phone 7**. Para los que conozcáis Prism, puede que en un primer momento sorprenda que se aplique el modelo de desarrollo a la plataforma móvil, porque lo cierto es que Prism surgió para el desarrollo de aplicaciones compuestas (de una Shell y módulos) y este escenario raramente lo vamos a encontrar en las aplicaciones Windows Phone 7, así que… ¿para qué podemos utilizar Prism en Windows Phone 7? Pues para aprovecharnos de una serie de clases que nos permiten desarrollar con el el patrón MVVM e implementar comandos, navegación, notificaciones de objetos observables, interacción con notificaciones y con la barra de la aplicación. Y es por esto último por lo que vamos comenzar. En este primer artículo, que nos servirá de introducción, vamos a ver tres clases que tenemos disponibles para agregar comportamientos a los botones de la barra de la aplicación.

Para comenzar a utilizar **Prism** tenemos que descargar la última release de [http://compositewpf.codeplex.com/](https://web.archive.org/web/20210123141005/http://compositewpf.codeplex.com/ "Patterns & practices: Prism "), pero aquí ya tengo que hacer el primer inciso, ya que a día de hoy esta release no funciona con la última versión de Windows Phone 7. Sin embargo, hay una actualización de las librerías con soporte para Mango que podemos descargar en [según el equipo de Prism](https://web.archive.org/web/20210123141005/http://compositewpf.codeplex.com/discussions/273668) que en un mes aproximadamente se publiquen las librerías firmadas con soporte para Mango. Los ejemplos de código que mostraré y el código que se puede descargar en este artículo funcionan exclusivamente para la versión 7.1, así que será necesario descargar y compilar esta solución.

En esta primera aproximación vamos a ver varias clases del espacio de nombres **Microsoft.Practices.Prism.Interactivity** y para seguir el ejemplo suponemos que tenemos creado un proyecto utilizando MVVM con sus respectivas carpetas para las vistas, vistas modelo, etc, así que no me detendré en como implementar esto. Una vez hayamos compilado las solución _PrismLibrary.Phone_, tenemos que agregar en nuestro proyecto referencias a las librerías _Microsoft.Practices.Prism_, _Microsoft.Practices.Prism.Interactivity_ y _System.Windows.Interactivity_, así como añadir la siguiente declaración de namespaces en el XAML de nuestra vista.

```xml
<xmlns:Custom="clr-namespace:System.Windows.Interactivity;assembly=System.Windows.Interactivity" xmlns:prismInteractivity="clr-namespace:Microsoft.Practices.Prism.Interactivity;assembly=Microsoft.Practices.Prism.Interactivity">
```

Una vez declarados los namespaces, definimos una barra de aplicación con tres botones a los que le asignamos el texto _Option1_, _Option2_ y _Option3_ respectivamente.

```xml
<phone:PhoneApplicationPage.ApplicationBar>
    <shell:ApplicationBar IsVisible="True" IsMenuEnabled="True">
        <shell:ApplicationBarIconButton IconUri="/Images/appbar\_button1.png" Text="Option1"/>
        <shell:ApplicationBarIconButton IconUri="/Images/appbar\_button2.png" Text="Option2"/>
        <shell:ApplicationBarIconButton IconUri="/Images/appbar\_button2.png" Text="Option3"/>
    </shell:ApplicationBar>
</phone:PhoneApplicationPage.ApplicationBar>
```

Ahora lo que queremos hacer es asociar un comando al botón «Option1», para esto tenemos que definir un comportamiento utilizando la clase **ApplicationBarButtonCommand** que implementa permite asociar un comando a un botón de la barra de aplicación. En el siguiente código tenemos definido el XAML que tenemos que incluir en nuestra vista después de la definición de la _ApplicationBar_.

```xml
    <Custom:Interaction.Behaviors>
        <prismInteractivity:ApplicationBarButtonCommand ButtonText="Option1" CommandBinding="{Binding Option1Command}" />
    </Custom:Interaction.Behaviors>
```

Aquí estamos añadiendo el comportamiento (_ApplicationBarButtonCommand_) indicando el botón al que afecta (Option1) y el comando que se debe ejecutar (Option1Command). Así que ahora solo tenemos que definir el comando en el _View Model_ de la vista de la siguiente manera:

```csharp
using System;
using System.Windows;
using System.Windows.Input;
using Microsoft.Practices.Prism.Commands;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using System.Windows.Interactivity;
using Microsoft.Practices.Prism.Interactivity;

namespace WP7Prism.ViewModels
{
    public class MainViewModel
    {
        ICommand option1Command;

        public MainViewModel()
        {
            option1Command = new DelegateCommand<string>(Option1Execute, CanOption1);
        }

        public ICommand Option1Command
        {
            get { return option1Command; }
        }

        private void Option1Execute(string text)
        {
            MessageBox.Show("Option 1 Clicked!");
        }

        private bool CanOption1(string text)
        {
            return true;
        }
    }
}
```

En este código, podemos ver que he utilizado la clase [DelegateCommand](https://web.archive.org/web/20210123141005/http://msdn.microsoft.com/en-us/library/gg405494(v=PandP.40).aspx), una implementación de **ICommand** de la librerías de Prism que nos permite adjuntar los delegados para los métodos _CanExecute_ y _Execute_.

Si ejecutamos la aplicación y pulsamos el primer botón de la barra de la aplicación, aparecerá el mensaje informativo. Muy sencillo.

En el siguiente ejemplo vamos a añadir un comportamiento al segundo botón para navegar a una página específica y al tercer botón para navegar hacia atrás. Vamos a hacer uso de la clase **ApplicationBarButtonNavigation** que implementa este tipo de comportamiento. En este caso, el código XAML tampoco puede ser más sencillo:

```xml
<Custom:Interaction.Behaviors>
    ...
    <prismInteractivity:ApplicationBarButtonNavigation ButtonText="Option2" NavigateTo="/Views/View2.xaml" />
    <prismInteractivity:ApplicationBarButtonNavigation ButtonText="Option3" NavigateTo="#GoBack" />
</Custom:Interaction.Behaviors>
```

En el primer caso estamos definiendo la Uri (/Views/View2.xaml), y en el segundo caso estamos indicando que navegue hacia atrás mediante una convención interna (#GoBack) de la clase **ApplicationBarButtonNavigation**. Tenemos que tener en cuenta que si no es posible navegar hacia atrás, el comportamiento devolverá una excepción y la aplicación fallará.

Para finalizar solo quedaría comentar que la clase **ApplicationBarExtensions** nos proporciona el método extensor **FindButton** que utilizan los dos comportamientos anteriores que hemos visto y con el que podremos implementar nuestros propios comportamientos asociados a los botones de la barra de la aplicación. Si quereis ver como utilizar este método podéis echar un vistazo a los ficheros [ApplicationBarButtonNavigation.cs](https://prism.svn.codeplex.com/svn/V4/PrismLibrary/Phone/Prism.Interactivity/ApplicationBarButtonNavigation.cs) y [ApplicationBarButtonCommand.cs](https://prism.svn.codeplex.com/svn/V4/PrismLibrary/Phone/Prism.Interactivity/ApplicationBarButtonCommand.cs).

Y hasta aquí este primer contacto con las librerías de Prism en WP7. En próximas entradas veremos otras clases que tenemos disponibles y como podemos sacarles partido desde nuestras aplicaciones para Windows Phone 7.

Referencias
---

[Guia del desarrollador de Windows Phone 7: Biblioteca de Prism para Windows Phone 7](http://msdn.microsoft.com/es-es/library/gg490766.aspx)  
[Developer's Guide to Microsoft Prism](http://msdn.microsoft.com/en-us/library/gg406140.aspx)
