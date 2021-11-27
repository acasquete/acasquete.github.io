---
title: Explorando ensamblados con System.Reflection
tags: []
---
De nuevo una nueva entrada dedicada a mi resumen del «MCTS Self-Placed Training Kit». En esta ocasión es del capítulo dedicado al espacio de nombres _System.Reflection_. Comienzo con la primera de las cinco entradas que dedicaré, al igual que el libro, a la reflexión con .NET.

Uno de los pilares del _Framework .NET_ y una de las mayores ventajas del CLR es la gran cantidad de información que tenemos disponible en tiempo de ejecución. El sistema de reflexión permite interrogar esta información y crear código al vuelo, permitiendo crear fácilmente sistemas basados en plug-ins.

Aunque siempre pensamos que es un fichero, un ensamblado es realmente un contenedor lógico de las distintas partes de datos que el CLR necesita para ejecutar código: metadatos de ensamblado, metadatos de tipo, código (IL) y recursos.

El Metadata o _manifest_ incluye información que define el ensamblado, como el nombre, versión, _strongname_ e información de la cultura. Los metadatos de tipos es toda la información que describe, incluyendo el espacio de nombres, los nombres de las clases (tipos) y miembros de una clase (métodos, propiedades y constructores). El código es el código de lenguaje intermedio (IL) que se compila a código máquina cuando el ensamblado se ejecuta. Los recursos son objetos (cadenas, imágenes o ficheros) que se utilizan desde el código.

La mayoría de veces, todas estas partes de un ensamblado se compilan en un único fichero, aunque esto no debe ser siempre necesariamente así. Los metadatos de ensamblado sí que necesitan estar en el ensamblado principal, pero los metadatos de tipos, código y recursos se pueden referenciar desde otros ficheros.

Los módulos son contenedores de tipos en un ensamblado. En general, utilizaremos múltiples módulos por ensamblado sólo en casos muy especiales. Visual Studio no soporta múltiples módulos por ensamblado, así que si queremos crear ensamblados multi-módulo necesitaremos hacerlo mediante la línea de comandos o mediante otras herramientas, como por ejemplo MSBuild.

Para examinar un ensamblado tenemos que instanciar un objeto de la clase _Assembly_ mediante alguno de los nueve siguientes métodos estáticos: _GetAssembly_, _GetCallingAssembly_, _GetEntryAssembly_, _GetExecutingAssembly_, _Load_, _LoadFile_, _LoadFrom_, _ReflectionOnlyLoad_, _ReflectionOnlyLoadFrom_.

string fullName = “System.Drawing, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a”; Assembly a= Assembly.ReflectionOnlyLoad(fullName); Console.Write(“Location: {0}”, a.Location);

// Lanza una excepción porque se carga sólo para reflexión object o = a.CreateInstance(“System.Drawing.Bitmap”); </pre>

Una vez tenemos una instancia de clase _Assembly_, podemos interrogar las propiedades del ensamblado mediante los siguientes métodos y propiedades.

**Propiedades:** _EntryPoint_, _FullName_, _GlobalAssemblyCache_,\* Location_, \*ReflectionOnly_. **Métodos:** _CreateInstance_, _GetCustomAttributes_, _GetExportedTypes_, _GetFile_, _GetFiles_, _GetLoadedModules_, _GetModule_, _GetModules_, _GetName_, _GetSatelliteAssembly_, _GetTypes_, _IsDefined_.

El siguiente código muestra el nombre todos los módulos del ensamblado que está en ejecución.

Assembly a = Assembly.GetExecutingAssembly();

Console.WriteLine("Nombre completo: {0}", a.FullName);
Console.WriteLine("Ubicación: {0}", a.Location);
Console.WriteLine("¿Sólo reflexión?: {0}", a.ReflectionOnly);

Module\[\] mods = a.GetModules();
foreach (Module m in mods)
{
    Console.WriteLine("Module Name: {0}", m.Name);
}



Y como podemos suponer, la clase \*Module\* se puede utilizar para recuperar o buscar tipos contenidos dentro de un módulo especifico. Estos son los métodos y las propiedades de la clase \*Module\* que nos ayudarán en esta tarea:

\*\*Propiedades:\*\* \*Assembly\*, \*FullyQualifiedName\*, \*Name\*.
\*\*Métodos:\*\* \*FindTypes\*, \*GetCustomAttributes\*, \*GetField\*, \*GetFields\*, \*GetMethod\*, \*GetMethods\*, \*GetTypes\*, \*IsResource\*.

La siguiente entrada tratará de los atributos de los ensamblados, es decir de aquella información de un ensamblado que no está disponible mediante la clase \*Assembly\*.

