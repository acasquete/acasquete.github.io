---
title: Gestión del estado de las apps con Prism for Windows Runtime
tags: [windows_store]
reviewed: true
---
Hace justo un mes, el equipo de patterns & practises publicó [Prism for Windows Runtime](http://blogs.msdn.com/b/blaine/archive/2013/04/24/kona-guidance-is-now-prism-for-windows-runtime.aspx), proyecto que hasta entonces era conocido con el nombre Kona y que surge como una guía para facilitar la implementación de escenarios comunes en las **aplicaciones de negocio para la Windows Store** (_Windows Store business apps_). Esta es la denominación que veremos a partir de ahora para hacer referencia a aplicaciones destinadas a las operaciones de negocio de una empresa y que veniamos conociendo por el término _Line-of-business app (_LOB apps_), algo más genérico.

**Prism for Windows Runtime**, a parte de ser la enésima librería que nos enseña como implementar **MVVM** (tranquilos, no voy a tratar este tema), **delegate commands** y comunicación desacoplada mediante el patrón [Event Agregattor](http://martinfowler.com/eaaDev/EventAggregator.html), funcionalidades todas ellas heredadas del Prism de WPF, también nos proporciona las clases para facilitarnos la implementación de la gestión de estado de la aplicación, navegación, búsqueda, validación, autenticación, tiles, etc. No es mi intención comenzar con el hola mundo de las aplicaciones con **Prism for WinRT**, para esto ya hay grandes posts como el de [Brian Noyes](https://twitter.com/briannoyes) ([WinRT Business Apps with Prism: Getting Started](http://www.silverlightshow.net/items/Windows-Store-LOB-Apps-with-Kona-Getting-Started.aspx)), vídeos como el de presentación en Channel 9: [Prism for Windows Store Apps](http://channel9.msdn.com/Shows/Visual-Studio-Toolbox/Prism-for-Windows-Store-Apps) y para los que tengáis suscripción en Pluralsight, el [nuevo curso](http://pluralsight.com/courses/building-windows-store-business-applications-prism) impartido por el mismo Brian Noyes.

En las próximas líneas vamos a ver cómo resuelve **Prism** la administración del tiempo de vida del proceso para guardar y restaurar el estado de la aplicación. Este es un tema que en las aplicaciones de negocio cobra, si cabe, más importancia, ya que normalmente se trabaja profusamente con formularios de entrada de datos y la correcta administración de los datos de sesión redundará en una mejor experiencia para los siempre exigentes usuarios. No queremos que nuestros usuarios tengan que volver a rellenar todo un formulario de campos, únicamente porque ha leído el correo o ha visitado otra página y el sistema a finalizado la aplicación.

En una aplicación para la Windows Store generada a partir de las plantillas estándar de Visual Studio (y sin utilizar ningún framework), la forma normal de guardar el estado de la aplicación es haciendo uso de **SuspensionManager**. Básicamente tenemos que guardar el estado al suspender y recuperarlo si el estado anterior es finalizado (_Terminated_). Esto lo vemos en el App de una aplicación cualquiera en la que se llama a los métodos SaveAsync y RestoreAsync.

```csharp
private async void OnSuspending(object sender, SuspendingEventArgs e) 
{ 
    var deferral = e.SuspendingOperation.GetDeferral(); 
    await SuspensionManager.SaveAsync(); 
    deferral.Complete(); 
}

protected override async void OnLaunched(LaunchActivatedEventArgs args) 
{ 
    …

    if (args.PreviousExecutionState == ApplicationExecutionState.Terminated) { 
        // Restore the saved session state only when appropriate 
        try 
        { 
            await SuspensionManager.RestoreAsync(); 
        } 
        catch (SuspensionManagerException) { 
            //Something went wrong restoring state. 
            //Assume there is no state and continue 
        } 
    }

    … 
}
```

Esto se encarga de serializar, guardar, leer y deserializar los datos que previamente hemos indicado en el m&eacute;todo **SaveState** de la p&aacute;gina que hereda de&nbsp;**LayoutAwarePage**. Y somos nosotros los responsables de recuperar estos datos en el m&eacute;todo **LoadState**&nbsp;de cada p&aacute;gina. El siguiente c&oacute;digo es que necesitamos para recuperar el elemento seleccionado de una p&aacute;gina ItemDetailPage de la plantilla Grid.
    
```csharp
protected override void SaveState(Dictionary<String, Objec> pageState)
{
    var selectedItem = (SampleDataItem)this.flipView.SelectedItem;
    pageState\["SelectedItem"\] = selectedItem.UniqueId;
}
        
protected override void LoadState(Object navigationParameter, Dictionary<String, Object> pageState)
{
    // Allow saved page state to override the initial item to display
    if (pageState != null && pageState.ContainsKey("SelectedItem"))
    {
        navigationParameter = pageState\["SelectedItem"\];
    }
}
```

No está de más que recuerde que tanto la clase **SuspensionManager** como **LayoutAwarePage** no son de WinRT, son clases generadas por Visual Studio y que se encuentran en la carpeta Common de la solución. El problema evidente es que tenemos que guardar y recuperar cada uno de los datos que querramos mantener.
       
**Con Prism para WinRT** tenemos un mecanismo interno muy similar al que he mostrado, pero nos es totalmente transparente como desarrolladores. Partiendo de la idea de que todos los campos que tenemos en la vista est&aacute;n enlazados con una propiedad del ViewModel, Prism nos presenta el nuevo atributo **RestorableState** con el que podemos decorar cualquier propiedad.

```csharp
[RestorableState]
public string UserName
{
    get { return userName; }
    set { SetProperty(ref userName, value); }
}
```

Desde este momento, cuando el sistema suspenda la aplicaci&oacute;n (podemos simularlo mediante la barra de herramientas Debug Location) o cuando se navegue a otra p&aacute;gina, Prism recuperar&aacute; mediante reflection el valor de todas las propiedades que tengan el atributo **RestorableState,**&nbsp;los guardar&aacute; en el almacenamiento local y los recuperar&aacute; cuando la aplicaci&oacute;n se restaure. En el ejemplo anterior lo hemos utilizado en una propiedad de tipo string, pero se puede utilizar con tipos complejos.&nbsp;
    
```csharp
[RestorableState]
public ObservableCollection<user> SelectedUsers 
{ 
    get { return selectedUsers; } 
    set { SetProperty(ref selectedUsers, value); } 
}

[RestorableState] 
public User SelectedUser 
{ 
    get { return selectedUser; } 
    set { SetProperty(ref selectedUser, value); } 
} 
```

Y al igual que sucede con&nbsp;**SuspensionManager**,Prism utiliza la clase **DataContractSerializer** con lo que tenemos que indicar todos los tipos que vamos a serializar. Para esto tenemos que sobrescribir el m&eacute;todo OnRegisterKnownTypesForSerialization de la clase MvvmAppBase y registrar el tipo mediante el m&eacute;todo RegisterKnownType de la clase **SessionStateService**.
    
```csharp
protected override void OnRegisterKnownTypesForSerialization() 
{ 
    base.OnRegisterKnownTypesForSerialization(); 

    SessionStateService.RegisterKnownType(typeof(User)); 
    SessionStateService.RegisterKnownType(typeof(ObservableCollection<user>)); 
}
```

La clase **SessionStateService** nos sirve tambi&eacute;n para guardar datos que no tenemos en el ViewModel, agregando al diccionario SessionState cualquier objeto que queramos mantener durante la sesi&oacute;n.
    
```csharp
sessionStateService.SessionState\["users"\] = users.ToArray();
```

Y para cargar el contenido:
    
```csharp
if (sessionStateService.SessionState.ContainsKey("users"))
{
    IEnumerable<user> users = sessionStateService.SessionState\["users"\] as IEnumerable<user>; 
    
    if (users != null) 
    { 
        foreach (User user in users) 
        { 
            SelectedUsers.Add(user); 
        } 
    } 
}
```

Como vemos, esta última forma poco cambio nos aporta con la que ya veníamos utilizando. El aporte principal que nos da Prism en este aspecto es el uso del atributo **RestorableState** para no tener guardar y recuperar una a una las propiedades del ViewModel.

## Plantillas de proyecto Prism for Windows Runtime


Antes he dicho que no quería hacer una introducción, pero no puedo terminar esta entrada sin recomendar (sobre todo para los que no hayáis utilizado nunca Prism) que os bajéis de la Visual Studio Gallery [la colección de plantillas para Visual Studio](http://visualstudiogallery.msdn.microsoft.com/e86649de-2b5e-45bb-bc65-5c6499b92b34) que ha creado David Britch (autor también toda la documentación de Prism) y que están disponibles desde hoy mismo.

Estás plantillas están pensadas para poder crear proyectos rápidamente y no tener que crear toda la estructura a mano. Las plantillas nos permiten crear dos tipos de aplicaciones: **Prism App** y **Prism App using Unity**. La diferencia, como resulta evidente, es que a parte de agregar la referencia a la librería **Prism.StoreApps**, la segunda utiliza Unity como contenedor de inyección de dependencias.

Además de las plantillas de proyecto, tenemos plantillas de elementos que podemos añadir a la aplicación: Page View, UserControl, View Model, Model con soporte para validación, PubSubEvent, Flyout y SearchContract para mostrar resultados de búsqueda.

En próximas entradas iré desgranando lo más interesante de esta librería.

## Referencias

[Manage app lifecycle and state](http://msdn.microsoft.com/en-us/library/windows/apps/hh986968.aspx)  
[Channel 9: Prism for Windows Store Apps](http://channel9.msdn.com/Shows/Visual-Studio-Toolbox/Prism-for-Windows-Store-Apps)  
[Guidelines for form layouts](http://msdn.microsoft.com/en-us/library/windows/apps/jj839734.aspx)

