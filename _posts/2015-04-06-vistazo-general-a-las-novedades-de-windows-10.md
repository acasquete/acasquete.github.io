---
title: Vistazo general a las novedades de Windows 10
tags: [windows_store]
reviewed: true
---
Hace un par de semanas Microsoft liberó por fin el SDK para las aplicaciones de **Windows 10**. Este anuncio implica un importante cambio que nos va a marcar la nueva forma de desarrollar aplicaciones para todos los dispositivos con **Windows 10**. En este artículo voy a comentar las novedades más destacadas que nos vamos a encontrar. No voy a entrar en el detalle de cada una de ellas. Si queréis más información [Josue Yeray](http://geeks.ms/blogs/jyeray/archive/tags/win10dev/default.aspx) y [Javier Suárez](http://geeks.ms/blogs/jsuarez/archive/tags/Windows+10/default.aspx) están escribiendo una serie de posts en los irán profundizando en cada una de las novedades.

Lo que pretendo con este artículo es que sirva de actualización para aquellos que conocían el desarrollo con Windows 8.1 y quieren conocer que es lo que tenemos que tener en cuenta y qué nuevas funcionalidades vamos a poder dar a nuestras aplicaciones en **Windows 10** y si sobre todo merece la pena realizar la migración de nuestras aplicaciones Windows 8.1.

Comenzando
----------

Para poder utilizar el SDK necesitamos la versión más reciente de Visual Studio, **VS2015 CTP6**, que al igual que el SDK se puede descargar a través del programa [Windows Insiders](https://insider.windows.com/).

Además, tenemos varios recursos con documentación oficial que son imprescindibles por si queremos profundizar en las nuevas características:

* [What’s new in Windows 10 Developer Preview](https://dev.windows.com/en-us/whats-new-windows-10-dev-preview)
* [Ejemplos de aplicaciones Windows 10](http://microsoft.github.io/windows/)
* [A Developer’s Guide to Windows 10 Preview](http://www.microsoftvirtualacademy.com/training-courses/a-developers-guide-to-windows-10-preview) En este último enlace podemos acceder a una serie de 13 vídeos en los que podemos conocer las principales novedades de la plataforma de desarrollo, y son los puntos principales en los que me he basado para escribir este post.

Control SplitView
-----------------

Comenzamos con un nuevo control para navegar entre el contenido de nuestra app llamado **SplitView**. Este control proporciona una barra de menú lateral de navegación, conocido normalmente como “hamburguer menu” y un área donde mostrar contenido.

El uso de este control es muy sencillo. La propiedad **Pane** contiene el código del menú en sí. El contenido de la página va en el propio control. La propiedad **OpenPaneLength** establece el ancho del menú. Y, por último, la propiedad **PanePlacement** indica en qué lado de la página aparecerá el menú, limitado a izquierda y derecha. El menú se abre estableciendo la propiedad **IsPaneOpen** a true, y se cierra cuando la propiedad se establece en false o cuando el usuario hace pulsa fuera del menú.

El funcionamiento de este control lo podemos ver en la aplicación de mapas de Windows 10.

Mapas
-----

Podemos hacer que nuestra aplicación interactúe con mapas del modo que ya lo haciamos en Windows Phone.

Podemos lanzar la aplicación de mapas pasando parámetros por **QueryString** con la posibilidad de mostrar rutas indicando dirección origen y destino. También es posible lanzar la configuración de mapas del sistema mediante **Windows.Services.Maps.MapManager** para, por ejemplo, descargar mapas y disponer de ellos de forma _offline_.

```csharp
// The URI to launch 
string uri = @”bingmaps:?cp=51.501156~-0.141706&lvl=17”; await Windows.System.Launcher.LaunchUriAsync(new Uri(uri)); 
```

Las URI para mostrar rutas, como la que se muestra a continuación provoca un fallo en la aplicación haciendo que finalice, pero es de esperar que esté soportado en la versión final.

```csharp
string uri = @”ms-drive-to:?destination.latitude=47.6451413797194&destination.longitude=-122.141964733601&destination.name=Redmond, WA”;
await Windows.System.Launcher.LaunchUriAsync(new Uri(uri));
```

También podemos utilizar el control MapControl (MVVM _friendly_) para poder integrar mapas en nuestra app. Es el mismo control que teníamos en Windows Phone 8.1 pero ahora lo tenemos en el namespace **Windows.UI.Xaml.Maps**. Para utilizarlo es tan sencillo como añadir:

```xml
<maps:MapControl x:Name=”myMap” /> 
 ```

En este control podemos establecer propiedades básicas como **ZoomLevel**, **Heading**, **DesiredPitch** y para añadir elementos utilizamos un control hijo.

```xml
<maps:MapControl x:Name=”myMap”>
    <maps:MapItemsControl x:Name=”MapItems” ItemsSource=”{Binding}” /> 
</maps:MapControl>
```

InkCanvas
---------

Un nuevo control de dibujo con soporte para todos los dispositivos y que permite agregar contenido escrito a mano en una página.

```html
<a href="/img/windows10-inkcanvas.jpg">![windows10-inkcanvas](/img/windows10-inkcanvas-1024x576.jpg)</a>
```

El uso es muy sencillo aunque yo no lo he podido ver en funcionamiento ya que en las primeras pruebas no ha funcionado. Seguiremos informado...

```xml
<Grid>
    <InkCanvas x:Name="inkCanvas">
</Grid>
```

RelativePanel
-------------

El control **RelativePanel** es un control de diseño destinado a reemplazar al Grid. Lo utilizaremos junto con el sistema de triggers para crear UIs que se adapten a distintos factores de forma. La ventaja del RelativePanel es que podemos realizar alineaciones con el centro o el borde de cualquier elemento.

La forma de alinear es colocar el control dentro de un RelativePanel y luego asignar una *Attached Property* que indicará como se alineará con respecto a otro control. Además, los objetos pueden ser alineados en el contexto del panel o alineados con otro control.

El **RelativePanel** hace el diseño de interfaces adaptativas más simple ya que es posible cambiar las alineaciones utilizando el **Visual State Manager**.

```xml
<RelativePanel>
    <Rectangle x:Name="BlueRect" 
        Height="100" Width="100" Fill="Blue" />
    <Rectangle x:Name="RedRect" 
        Height="100" Width="100" Fill="Red"
        RelativePanel.Below="BlueRect"
        RelativePanel.AlignLeftWith="BlueRect" />
</RelativePanel>
```

Adaptive triggers
---

Los Adaptive Triggers son triggers en el Visual State Manager que podemos utilizar para definir cómo el layout cambia dependiendo de unas condiciones del estado visual.

La recomendación oficial es hacer la gestión de los estados visuales basadas en el tamaño de la pantalla. Sin embargo se pueden utilizar estados visuales para definir el diseño de pantalla según la plataforma utilizando el **PlatformAdaptiveTrigger**.

```xml
<VisualState x:Name="wideState">
    <VisualState.Setters>
                 <Setter Target="myPanel.Orientation" Value="Horizontal" />
    </VisualState.Setters>
    <VisualState.StateTriggers>
                <AdaptiveTrigger MinWindowWidth="600"/>
    </VisualState.StateTriggers>
</VisualState>
```

App-to-app communication
---

Sea añaden nuevas capacidades de comunicación app-to-app a las ya existentes en Windows 8.1. Como por ejemplo:

* **LaunchForResults** - para lanzar una app que devolverá resultados a la aplicación origen.
* Invocar a una aplicación específica cuando realizamos activación por protocolo.
* Almacenamiento compartido para aplicaciones del mismo publicador.

```xml
    <Package>
        <Extensions>
            <Extension Category="windows.publisherCacheFolder">
                <PublisherCacheFolder>
                    <Folder Name="Folder1">
                </PublisherCacheFolder>
            </Extension>
        </Extensions>
    </Package>
```

App services
------------

Otra forma interesante de comunicar aplicaciones. Esta nos permite crear servicios sin UI que las aplicaciones pueden llamar de la misma forma que llaman a un servicio web (excepto que estos servicios están en el dispositivo).

Action Center
-------------

Tenemos disponible una API para la gestión del Action Center para que, por ejemplo, la App, el **Action Center** y las notificaciones de la _tile_ muestren información consistente.

La API permite:

* Eliminar una o varias notificaciones.
* Etiquetar y agrupar notificaciones.
* Reemplazar una notificación con una nueva.
* Establecer un tiempo de expiración – para, por ejemplo, escenarios en los que la información sea sensible al tiempo.
* Enviar una notificación “Ghost Toast” (solo se muestra en el action center).

```csharp
    ToastNotification toasty = new ToastNotification(doc);
    toasty.Tag = "Windows 10 Toast #3";
    toasty.Group = "JumpStart";
    toasty.ExpirationTime = (DateTimeOffset.Now + TimeSpan.FromHours(2));
    toasty.SuppressPopup = true;
```

Más características
-------------------

Estas son las características principales, pero no las únicas. De entre todas las novedades también destacaría las siguientes:

* Nuevas propiedades para validación de datos del lado cliente para la entrada de usuario.
* Nuevo método para solicitar permiso al usuario para acceder a su ubicación.
* Capacidades de arrastrar y soltar entre distintas plataformas de aplicaciones. Esto permitirá por ejemplo, arrastrar un fichero desde el escritorio hasta una aplicación UAP.
* Poder enviar, recibir y filtrar anuncios sobre una conexión Bluetooth LE.

Cambios diseño y UX
-------------------

El cambio más importante a tener en cuenta para diseñar los layouts en nuevos desarrollos para **Windows 10** es que cuando el sistema operativo no está en modo Tablet, las aplicaciones funcionan en ventana en lugar de ventana completa, por lo que la interfaz se debe adaptar a distintos tamaños, ya no solo a distintos dispositivos. Básicamente el concepto es, todo lo que hemos utilizado en la web a nivel de layout lo aplicaremos al escritorio (scrolls verticales, layouts flexibles con tamaños relativos).

Otro cambio importante es la incorporación del menú lateral para la navegación (control **SplitView** comentado anteriormente).

Otro cambio a tener en cuenta es a nivel de contratos. Ahora las apps de Windows 10 no muestran el **Charm Bar** por lo que tenemos que añadir en el canvas de la app los botones que nos den acceso a compartir y a la configuración. La implementación subyacente de los contratos no cambia, es el mismo código que utilizábamos en Windows 8.1. También se puede seguir accediendo a los contratos mediante el menú de control de la aplicación, pero no es la opción recomendada.

Bien, estos son los cambios más importantes que vamos a encontrarnos en cuanto a desarrollo de aplicaciones en **Windows 10**. Es importante destacar que todavía estamos hablando de versiones CTP, así que la versión final seguramente tendrá cambios algunos cambios con respecto a lo que he puesto aquí. Intentaré mantener actualizada esta entrada con los nuevos cambios que se produzcan hasta la versión final.
