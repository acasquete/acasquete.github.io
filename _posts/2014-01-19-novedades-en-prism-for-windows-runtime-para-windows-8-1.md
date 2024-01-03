---
title: Novedades en Prism for Windows Runtime para Windows 8.1
tags: [winrt, windows_store]
reviewed: true
---
Aunque desde diciembre teníamos disponible la última versión de [Prism for Windows Runtime](https://prismwindowsruntime.codeplex.com/), fue a principios de mes cuando el equipo de **Patterns & Practices** liberó de forma oficial la versión que da soporte a las novedades de Windows 8.1.

Para poder comenzar a utilizar esta actualización podemos agregar una referencia al [paquete Prism.StoreApps de NuGet](https://www.nuget.org/packages/Prism.StoreApps/1.1.0) o si ya tenemos una aplicación creada, simplemente tendremos que actualizarla.

Además de cambios en la librería **Prism.StoreApps**, se ha actualizado tanto la documentación en la MSDN, los ejemplos y la implementación de referencia. Lo único que todavía no tenemos actualizado es el PDF, para el que tendremos que esperar hasta final de mes. Podéis echar un vistazo general de todos los cambios en el post que anuncia el lanzamiento en el [blog de Blain Wastell](http://blogs.msdn.com/b/blaine/archive/2014/01/03/just-released-prism-for-the-windows-runtime-on-windows-8-1.aspx).

¿Y qué es lo que trae de nuevo esta nueva versión? Pues si nos ceñimos a los cambios hechos en la librería **Prism.StoreApps**, podemos hablar de tres “grandes” cambios, son estos:

*   Eliminación de las clases asociadas al panel de búsqueda y _flyouts_.
*   Soporte para pantallas de inicio extendidas (_Extended Splash screen_).
*   Actualización de la clase **VisualStateAwarePage** para detectar el tamaño de página y la orientación.

Clases eliminadas
-----------------

El primer cambio, la eliminación de las clases **FlyoutService** y **FlyoutView**, era más que evidente ya que ahora (por fin) en Windows 8.1 tenemos disponible el control [SettingsFlyout](http://msdn.microsoft.com/es-es/library/windows/apps/windows.ui.xaml.controls.settingsflyout.aspx) con el que podemos crear los paneles de configuración.

Si tenemos un proyecto que esté utilizando **FlyoutService**, al actualizar a 8.1 tendremos que cambiar todas las referencias a **FlyoutView** por **SettingsFlyout**. Lo que sí se mantiene es la interfaz **IFlyoutViewModel**, aunque con alguna ligera modificación, ya que ahora esta interfaz no tiene ni la propiedad **GoBack** ni el método **Open**.

Otra de las clases eliminadas ha sido **SettingsCharmActionItem** que se utilizaba para crear la lista de comandos de configuración. Ahora haremos uso de la clase **SettingsCommand** y en lugar de sobrescribir el método **GetSettingsCharmActionItems** de la clase **App**, tenemos que utilizar el método **GetSettingsCommands**.

```csharp
protected override IList&lt;SettingsCommand&gt; GetSettingsCommands()
{
    return new List&lt;SettingsCommand&gt;
            {
                new SettingsCommand("About", "About", (c) => new AboutFlyout().Show())
            };
}
```

Por último, las otras clases que se han eliminado han sido **SearchPaneService** y **SearchQueryArguments**. **SearchPaneService** era una abstracción de la clase **SearchPane** que se utilizaba para hacer la aplicación testeable, al no poder realizar llamadas a **SearchPane** desde los ViewModel. Tanto este servicio como el soporte de activación de búsqueda ha sido eliminado de la clase **MvvmAppBase** y de la implementación de referencia. Esto significa que la [nueva experiencia de búsqueda](http://msdn.microsoft.com/es-es/library/windows/apps/hh465233.aspx) tenemos que integrarla en nuestras aplicaciones utilizando únicamente el control **SearchBox**. 

Pantalla de inicio extendida
---    
 
Otra de las novedades incluidas en la librería **Prism.StoreApps** es el soporte para añadir una pantalla de inicio extendida (*ExtendedSplashScreen*). En la clase **MvvmAppBase** se ha añadido una propiedad para poder establecer la factoría que crea la página de inicio extendida.
    
```csharp
protected Func<SplashScreen, Page> ExtendedSplashScreenFactory { get; set; }
```    

Para utilizarla, lo primero que tenemos que hacer es crear la página extendida, una página que tenga como mínimo la imagen y un indicador de progreso. Para poder ubicar la nueva imagen en la misma posición que en la pantalla de inicio podemos crear está página con un constructor que acepte el objeto **SplashScreen**. 
    
Una vez tenemos la página, simplemente tenemos que establecer el valor de la propiedad **ExtendedSplashScreenFactory** en el constructor de la clase **App**. Esta propiedad requiere que asignemos una función a la que le pasamos el objeto **SplashScreen** y devuelva una nueva instancia de la página extendida. 
    
```csharp
public App()
{
    this.InitializeComponent();

    this.ExtendedSplashScreenFactory = (splashscreen) => new ExtendedSplashScreen(splashscreen);
}
```

Si esta breve explicación os deja con alguna duda, podéis acudir a los _QuickStarts_ de Prism, en los que se ha incluido un proyecto de ejemplo para demostrar el uso de esta nueva propiedad.

Soporte para los nuevos estados de vista
----------------------------------------

Y el último cambio a comentar es el realizado en la clase **VisualStateAwarePage**. Está clase es de la que heredan todas las vistas en **Prism**, y nos proporciona soporte para navegación, gestión de estado y cambios en el _layout_. Esta clase se ha actualizado para detectar el tamaño de página y la orientación con los nuevos estados de vista (_DefaultLayout_, _PortraitLayout_, and _MinimalLayout_). Además, ahora la clase **VisualStateAwarePage** contiene el comando **GoBackCommand** que permite navegar al elemento más reciente del historial de navegación.

Resumiendo, pocos cambios
-------------------------

Aunque se han realizado otros cambios menores, los cambios introducidos en la librería **Prism.StoreApps** son bien pocos. Donde sí vamos a ver más cambios es en la implementación de referencia, que se ha adaptado completamente a las novedades introducidas en Windows 8.1. Entre estos cambios destacaría el cambio del uso de la clase **System.Net.Http.HttpClient** por **Windows.Web.Http.HttpClient**, el uso de los controles **CommandBar** y **AppBarButton** en la barra de aplicación, el uso de [IncrementalUpdateBehavior](http://msdn.microsoft.com/en-us/library/windows/apps/dn440752.aspx) para mejorar la carga en los controles **ListView** y **GridView** y el nuevo control **AutoRotatingGridView** que actualiza el _layout_ cambiando entre _Landscape_, _Portrait_ y _Minimal_ dependiendo del tamaño y de la orientación.

Y aunque no forma parte de la _release_ oficial de Prism, es importante destacar que también tenemos disponibles la [actualización de la extensión](http://www.davidbritch.com/p/prism-for-windows-runtime.html) que añade las plantillas de Visual Studio para la creación de proyectos con la nueva versión de Prism. Podemos tener instaladas estas plantillas junto con las de la versión anterior, con lo que podremos crear proyectos para Windows 8 y 8.1 desde Visual Studio 2013.

Referencias
---

[CodePlex: Prism for the Windows Runtime](http://prismwindowsruntime.codeplex.com/)  
[Nuevos controles y actualizaciones de controles](http://msdn.microsoft.com/es-es/library/windows/apps/bg182878.aspx)  
[Directrices sobre búsqueda](http://msdn.microsoft.com/es-es/library/windows/apps/hh465233.aspx)  
[Prism for the Windows Runtime Templates (Win 8.1)](http://visualstudiogallery.msdn.microsoft.com/2a6c37e4-fe9a-4a93-baae-a9bce4cf60c7)  

