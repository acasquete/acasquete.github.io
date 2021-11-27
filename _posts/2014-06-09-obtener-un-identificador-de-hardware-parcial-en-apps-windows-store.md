---
title: Obtener un identificador de hardware parcial en apps Windows Store
tags: [windows_store, winrt]
---
Un requisito habitual en las aplicaciones que ofrecen contenido bajo un sistema de licenciamiento es poder limitar el uso que se hace de una cuenta de usuario en un número determinado de dispositivos. Para poder implementar esta restricción, tenemos que obtener y asociar el identificador de dispositivo con la cuenta de usuario para poder después autentificar todas las llamadas de los servicios mediante este identificador.

La forma de obtener el identificador varía según la plataforma, por ejemplo, en Windows Phone 8.1 obtenemos el identificador de dispositivo mediante la propiedad **HostInformation.PublisherHostId**. Este identificador es único por dispositivo y por cuenta de publicador, es decir, dos aplicaciones publicadas con distintas cuentas que se ejecuten en un mismo dispositivo, obtendrán distintos identificadores.

En las aplicaciones Windows 8, sin embargo, se utiliza el identificador de hardware específico de aplicaciones (ASHWID) que varía de una aplicación a otra. Esto provoca que si tenemos un _back-end_ compartido por varias aplicaciones, no será posible utilizar un solo ID de dispositivo, sino que tendremos que asociar la cuenta de usuario con cada uno de los ASHWID de dispositivo generados en cada una de las aplicaciones. Otra característica del ASHWID es que se genera a partir de varios componentes de hardware del dispositivo y varía si el usuario hace cambios de hardware, esto es conocido como desfase de hardware. Por ejemplo, el ASHWID generado por una aplicación será distinto si un usuario deshabilita una conexión WiFi o un adaptador BlueTooth.

Los componentes de hardware que se evalúan para generar el ASHWID son los siguientes:

*   CPU del procesador
*   Tamaño de la memoria
*   Número de serie del dispositivo de disco
*   Adaptador de red
*   Adaptador de audio
*   Estación de acoplamiento
*   Dirección de Bluetooth
*   Identificador de dispositivo de banda ancha móvil
*   BIOS

La secuencia de bytes del ASHWID esta formada por grupos de cuatro bytes en donde los dos primeros bytes contienen el tipo de componente y los dos bytes siguientes contienen el valor. Si un dispositivo no dispone un componente concreto, este no formará parte del ASHWID. Y si el dispositivo tiene varios componentes del mismo tipo, por ejemplo, tiene varios adaptadores de red o varias unidades de disco físicos, el ASHWID contendrá un valor para cada uno de ellos, aunque tampoco se garantiza que aparezcan de forma secuencial.

Debido al desfase de hardware, no deberíamos utilizar el ASHWID directamente en nuestras aplicaciones. Si pasamos el ASHWID completo a un servicio web para realizar la autentificación, podríamos identificar incorrectamente el dispositivo si el usuario cambia o desconecta algún componente. Para salvar este problema, la mejor forma es implementar un nivel de tolerancia a cambios de hardware. La forma de calcular esta tolerancia en un servicio de _back-end_ está descrita en el artículo de la MSDN [“Componente de nube Identificador de hardware específico de aplicaciones”](http://msdn.microsoft.com/es-es/library/windows/apps/jj835815.aspx).

Sin embargo, si tenemos que utilizar un servicio de terceros que nos solicita un ID de dispositivo, o no podemos implementar la verificación de tolerancia en servidor, tendremos que obtener un identificador de dispositivo parcial a partir de ciertos componentes de hardware en lugar del ASHWID completo.

Para comenzar, creamos una enumeración con los distintos tipos de hardware que se evalúan para generar el ID.

    public enum HardwareIdType
    {
        Invalid = 0,
        Processor = 1,
        Memory = 2,
        DiskDevice = 3,
        NetworkAdapter = 4,
        DockingStation = 6,
        MobileBroadband = 7,
        Bluetooth = 8,
        Bios = 9
    };
    </pre>
    
    A continuación creamos un método al que le pasamos un array de la enumeración que acabamos de definir, para pasar los elementos que queremos que se tenga en cuenta para generar el ID. Este método obtiene el ASHWID mediante el método **GetPackageSpecificToken** de la clase **HardwareIdentification**. 
    
    <pre class="brush:csharp">
    public static string GetPartialHardwareId(params HardwareIdType[] components)
    {
        var hwToken = HardwareIdentification.GetPackageSpecificToken(null);
        var hwId = hwToken.Id;
        var hwIdBytes = hwId.ToArray();
    
        var filteredHwIdBytes = GetFilteredHardwareIdArray(hwIdBytes, components);
    
        return Convert.ToBase64String(filteredHwIdBytes);
    }
    </pre>
    
    El siguiente método es el que descompone la secuencia de bytes del identificador, comprobando si los dos primeros bytes de cada grupo de 4 corresponde con algún tipo de hardware que hemos indicado en el array y en caso afirmativo se va agregando el valor de cada en una lista de bytes.
    
    <pre class="brush:csharp">
    internal static byte[] GetFilteredHardwareIdArray(byte[] hwId, params HardwareIdType[] components)
    {
        if (hwId.Length % 4 != 0)
        {
            throw new ArgumentException("Invalid Hardware Id", "hwId");
        }
    
        var hardwareId = new List&lt;byte&gt;();
    
        for (int i = 0; i < hwId.Length / 4; i++)
        {
            if (components.Contains((HardwareIdType)BitConverter.ToUInt16(hwId, i * 4)))
            {
                hardwareId.AddRange(hwId.Skip(i * 4).Take(4));
            }
        }
    
        return hardwareId.ToArray();
    }
    </pre>
    
    Para utilizar, crearemos un array con los tipos de componentes que queremos utilizar para la generación del identificador y llamamos al método **GetPartialHardwareId**. En el siguiente ejemplo se está utilizando el identificador del procesador, unidades de disco, adaptador de red, memoria y BIOS, componentes que tienen una menor probabilidad menor de cambiar.  
    
    <pre class="brush:csharp">
    public string GetInstallationId()
    {
        var hardwareIdTypes = new[] { 
            DeviceIdentification.HardwareIdType.Processor, 
            DeviceIdentification.HardwareIdType.DiskDevice, 
            DeviceIdentification.HardwareIdType.NetworkAdapter, 
            DeviceIdentification.HardwareIdType.Memory, 
            DeviceIdentification.HardwareIdType.SmBios, };
    
        var deviceId = GetPartialHardwareId(hardwareIdTypes);
    
        return deviceId;
    }
    

El código que aparece en este artículo está disponible como parte del paquete Nuget **[Business Apps WinRT Toolkit](https://www.nuget.org/packages/BusinessAppsWinRTToolkit)**, un conjunto de helpers, behaviors y extensiones para crear aplicaciones empresariales con Windows Runtime. El código también está disponible en un [repositorio GitHub](https://github.com/acasquete/BusinessAppsWinRTToolkit).

Referencias
-----------

[Instrucciones sobre el uso del identificador de hardware específico de aplicaciones (ASHWID) para la implementación de lógica de aplicaciones por dispositivo](http://msdn.microsoft.com/es-es/library/windows/apps/jj553431.aspx) 
[Componente de nube Identificador de hardware específico de aplicaciones (ASHWID)](http://msdn.microsoft.com/es-es/library/windows/apps/jj835815.aspx) 
[Business Apps WinRT Toolkit Nuget Package](https://www.nuget.org/packages/BusinessAppsWinRTToolkit) 
[Business Apps WinRT Toolkit GitHub repository](https://github.com/acasquete/BusinessAppsWinRTToolkit)

