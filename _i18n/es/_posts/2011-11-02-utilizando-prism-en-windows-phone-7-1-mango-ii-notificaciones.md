---
title: Utilizando Prism en Windows Phone 7.1 Mango (II), Notificaciones
tags: [programming, windows_phone]
reviewed: true
---
En el primer post dedicado a [Prism para Windows Phone 7](/utilizando-prism-en-windows-phone-7-1-mango-i/) vimos las clases que nos permitían ejecutar comandos desde la barra de aplicación. En esta segunda entrada veremos las clases del espacio de nombres **Microsoft.Practices.Prism.Interactivity.InteractionRequest** que nos van a permitir mostrar diferentes notificaciones en la interfaz de usuario.

De entre todas las notificaciones que necesitamos mostrar al usuario podemos distinguir dos tipos: las **informativas** y las de **error**. La principal diferencia entre los dos tipos es que que las notificaciones informativas no deben interrumpir la tarea que el usuario está realizando mientras que las de error sí lo deben hacer, es decir, que el usuario no debería poder seguir trabajando cuando se muestre este tipo de notificación. Además, a partir de un mensaje informativo el usuario no debe realizar ninguna acción concreta, sin embargo a partir de un mensaje de error, el usuario tendrá que realizar una serie de acciones para evitar la situación de error. Normalmente utilizaremos las notificaciones informativas para informar que una determinada acción se ha completado.

Para mostrar cómo utilizar las notificaciones he añadido dos botones en la vista principal de la solución de ejemplo que utilicé en la anterior entrada. Al pulsar cada uno de estos dos botones se muestran los dos tipos de notificaciones. Es obvio que este no es el escenario real que nos encontraremos en la mayoría de los casos, pero como fines demostratitos nos sirve.

Comenzamos con el tipo de notificación más sencillo: la notificación de error. Lo primero que debemos hacer es exponer en el _View-Model_ un objeto de solicitud de interacción ([InteractionRequest](http://msdn.microsoft.com/en-us/library/gg431432(v=PandP.39).aspx)).

```cs
private readonly InteractionRequest<Notification> submitErrorInteractionRequest;

public MainViewModel() 
{ 
    … 
    this.submitErrorInteractionRequest = new InteractionRequest<Notification>(); 
}

public IInteractionRequest SubmitErrorInteractionRequest 
{ 
    get 
    { 
        return this.submitErrorInteractionRequest; 
    } 
}
```
Cuando deseemos hacer efectiva la interacción de usuario tenemos que llamar al método **Raise** pasando como argumento el contexto el objeto [Notification](http://msdn.microsoft.com/en-us/library/microsoft.practices.prism.interactivity.interactionrequest.notification(v=pandp.39).aspx), y adicionalmente el método función de _callback_ que se ejecutará cuando la interacción se haya completado.

```cs
private void ShowErrorExecute(string text)
{
    this.submitErrorInteractionRequest.Raise(
               new Notification { Title = "Error Message", Content = "Este es un mensaje que bloquea la acción del usuario." },
               n => { });
}
```

Ahora solo tenemos que declarar el _trigger_ en el XAML de la vista, y la acción que se queremos que se ejecute cuando se el _trigger_ se dispare. En el caso de las notificaciones de error utilizaremos **MessageBoxAction**, que muestra el mensaje con el contenido de la notificación.

```xml
<Custom:EventTrigger SourceObject="{Binding SubmitErrorInteractionRequest}" EventName="Raised">
    <prismInteractionRequest:MessageBoxAction />
</Custom:EventTrigger>
```

En el caso de la notificación informativa es prácticamente igual, definimos la solicitud de interacción en el View-Model de la siguiente forma:

private readonly InteractionRequest<Notification> submitNotificationInteractionRequest;

```cs
public MainViewModel()
{
    ...
    this.submitNotificationInteractionRequest = new InteractionRequest<Notification>();
}

public IInteractionRequest SubmitNotificationInteractionRequest
{
    get { return this.submitNotificationInteractionRequest; }
}
```

Y en el momento que queremos lanzar la notificación, llamamos al metodo **Raise**.

```cs
private void ShowNotificationExecute(string text)
{
    this.submitNotificationInteractionRequest.Raise(
               new Notification { Title = "Notification message", Content = "Este es un mensaje que no bloquea la acción del usuario y desaparece a los 6 segundos." },
               n => { });
}
```

Lo único que tenemos que cambiar, como ya habréis supuesto, es la **TriggerAction** por la **ToastPopupAction**. Al utilizar esta acción tenemos que definir, además, la propiedad **PopupElementName** a la que asignaremos el nombre de un control **Popup** que será el que se muestre cuando se reciba la solicitud de interacción.

```xml
<Custom:Interaction.Triggers>
    <Custom:EventTrigger SourceObject="{Binding SubmitNotificationInteractionRequest}" EventName="Raised">
        <prismInteractionRequest:ToastPopupAction PopupElementName="SynchronizationToast" />
    </Custom:EventTrigger>

</Custom:Interaction.Triggers>
```

En nuestro ejemplo, el objeto **Popup** contiene un StackPanel con dos bloques de texto que muestran el título y el contenido de la notificación.

```xml
<Popup x:Name="SynchronizationToast">
    <StackPanel Background="{StaticResource PhoneAccentBrush}" Width="480">
            <TextBlock Text="{Binding Title}" FontFamily="{StaticResource PhoneFontFamilySemiBold}" Foreground="{StaticResource PhoneForegroundBrush}" TextWrapping="Wrap" Margin="15,5,15,5" />
            <TextBlock Text="{Binding Content}" Foreground="{StaticResource PhoneForegroundBrush}" TextWrapping="Wrap" Margin="15,5,15,5" />
    </StackPanel>
</Popup>
```

Y hasta aquí esta entrada en la que hemos visto una serie de clases que nos proporciona Prism para mostrar notificaciones. En próximas entradas seguiremos viendo otras clases que podemos utilizar en nuestras aplicaciones para **Windows Phone 7**.

Enlaces relacionados:
---
[Guia del desarrollador de Windows Phone 7](http://msdn.microsoft.com/es-es/library/gg490765.aspx) 
[Notificaciones de la interfaz de usuario](http://msdn.microsoft.com/es-es/library/gg490771.aspx#sec16) 


