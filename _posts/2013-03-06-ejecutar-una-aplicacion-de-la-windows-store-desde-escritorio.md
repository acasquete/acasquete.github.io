---
title: Ejecutar una aplicación de la Windows Store desde escritorio
tags: [windows_store, winrt]
reviewed: true
---
Hago un paréntesis en la serie que estoy dedicando a los procesos en _background_ para tratar brevemente un tema de esos que llamo “raros”. Vamos a ver cómo **ejecutar una aplicación de la Windows Store desde un proceso de escritorio**. No es que sea un tema excesivamente complicado o “raro”, pero como hoy se me ha vuelto a plantear por segunda vez, aprovecho la oportunidad para escribir explicando cómo conseguirlo sin demasiadas complicaciones. También tengo que avisar que el código de esta entrada lo he extraído de un hilo de los foros de MSDN, ya que no he encontrado documentación oficial.

Lo primero a tener en cuenta (para no meternos en complicaciones innecesarias), es que si la aplicación que queremos lanzar tiene asociado un tipo de archivo o un protocolo por defecto, la forma más fácil será lanzando la url con ese protocolo o abrir el documento. Obviamente, si la aplicación está asociada a una aplicación de escritorio, esta solución no nos sirve.

Si queremos lanzar una aplicación directamente, tenemos que utilizar la interfaz **IApplicationActivationManager** que está definida en _%ProgramFiles(x86)%Windows Kits8.0includeumShObjIdl.h._ Esta interfaz nos proporciona métodos para activar una aplicación de la Tienda Windows a partir del **AppUserModelId** (luego veremos como obtenerlo), por protocolo o por extensión.

Comenzamos creando un nuevo proyecto en C# de librería de clases al que le añadimos la definición de la interfaz **IApplicationActivationManager** con el siguiente código**:**

```csharp
using System; using System.Runtime.InteropServices;

namespace StoreAppLauncher { public enum ActivateOptionsEnum { None = 0,  
DesignMode = 0x1, NoErrorUI = 0x2,  
NoSplashScreen = 0x4, }

    [ComImport]
    [Guid("2e941141-7f97-4756-ba1d-9decde894a3d")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IApplicationActivationManager
    {
        IntPtr ActivateApplication([In] String appUserModelId, [In] String arguments, [In] ActivateOptionsEnum options, [Out] out UInt32 processId);
    
        IntPtr ActivateForFile([In] String appUserModelId, [In] IntPtr itemArray, [In] String verb, [Out] out UInt32 processId);
    
        IntPtr ActivateForProtocol([In] String appUserModelId, [In] IntPtr itemArray, [Out] out UInt32 processId);
    }
    
    [ComImport]
    [Guid("45BA127D-10A8-46EA-8AB7-56EA9078943C")]
    public class ApplicationActivationManager : IApplicationActivationManager
    {
        [MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
        public extern IntPtr ActivateApplication([In] String appUserModelId, [In] String arguments, [In] ActivateOptionsEnum options, [Out] out UInt32 processId);
    
        [MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
        public extern IntPtr ActivateForFile([In] String appUserModelId, [In] IntPtr itemArray, [In] String verb, [Out] out UInt32 processId);
    
        [MethodImpl(MethodImplOptions.InternalCall, MethodCodeType = MethodCodeType.Runtime)]
        public extern IntPtr ActivateForProtocol([In] String appUserModelId, [In] IntPtr itemArray, [Out] out UInt32 processId);
    } }
```
    
Ahora podremos desde cualquier proyecto instanciar y llamar al método **ActivateApplication** para lanzar cualquier aplicación que tengamos instalada.
    
```js
var appActiveManager = new ApplicationActivationManager();

uint pid;
appActiveManager.ActivateApplication(appUserModelId, null, ActivateOptionsEnum.None, out pid);
```

Lo único que nos falta es obtener el **AppUserModelId**, el identificador de la aplicación de la Tienda Windows que queremos ejecutar. El único sitio donde lo podemos localizar es el registro, así que tenemos que abrir el editor del registro y buscar la clave **HKEY_CURRENT_USERSoftwareClassesActivatableClassesPackage**. Aquí encontraremos una lista con el nombre completo de todos los paquetes que tenemos instalados. Dentro de cada paquete encontraremos la clave **ServerApp.wwa** y dentro de esta valor de **AppUserModelId**. En la siguiente imagen se muestra el valor de la aplicación de Skype.

Así que si pasamos este valor (Microsoft.SkypeApp\_kzf8qxf38zg5c!App) al método **ActivateApplication**, la aplicación de Bing se lanzará o se pondrá en primer plano si ya la teníamos en ejecución.

Espero que os sea de utilidad si os encontráis con alguna de esas situaciones raras.


## Referencias

[IApplicationActivationManager interface (Windows)](IApplicationActivationManager%20interface%20(Windows))  
[Windows Desktop Development Forums](http://social.msdn.microsoft.com/Forums/en-US/windowsgeneraldevelopmentissues/thread/11e5a9ae-3497-4a0a-92ac-d409ccf3d2a3/)  

