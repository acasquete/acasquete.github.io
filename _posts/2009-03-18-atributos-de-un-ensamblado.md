---
title: Atributos de un ensamblado
tags: [certification]
---
De nuevo vuelvo a retomar, dos meses después, los resúmenes del [MCTS](/tag/certification). En la última entrada vimos como consultar la información que contiene un ensamblado mediante la clase _Assembly_. Es importante saber que no toda la información de un _Assembly_ está disponible mediante esta clase, o no podemos acceder a toda mediante esta clase. Hay información como el _copyright_, información de la empresa o información de la cultura que se capturan como parte del ensamblado como atributos, esto quiere decir que los atributos de los ensamblados dan información adicional sobre el ensamblado.

Normalmente se añaden los atributos del ensamblado en el fichero AssemblyInfo (AssemblyInfo.cs para C# o AssemblyInfo.vb para VB.NET), y se añaden especificando que es un atributo utilizando el prefijo (assembly: en C# y Assembly: en Visual Basic.NET). Este código corresponde a la definición de un atributo en C#:

\[assembly: AssemblyCompany(“IdleBit WebLog”)\] </pre> El nombre atributo es el mismo que el de la clase del atributo pero omitiendo la palabra _Attibute_. Por ejemplo, la clase _AssemblyCopyrightAttribute_ representa el atributo _AssemblyCopyright_.

Esta es la relación de los atributos más comunes: _AssemblyAlgorithmId_, _AssemblyCompany_, _AssemblyConfiguration_, _AssemblyCopyright_, _AssemblyCulture_, _AssemblyDefaultAlias_, _AssemblyDelaySign_, _AssemblyDescription_, _AssemblyFileVersion_, _AssemblyFlags_, _AssemblyInformationalVersion_, _AssemblyKeyFile_, _AssemblyTitle_, _AssemblyTrademark_, _AssemblyVersion_.

Para obtener los atributos de un _assembly_ tenemos que utilizar el método _GetCustomAttributes_ de la clase _Assembly_. Este método acepta un parámetro booleano que indica si debe obtener los atributos heredados.

Para obtener los atributos del ensamblado podemos utilizar el siguiente código:

Assembly a = Assembly.GetExecutingAssembly();

object\[\] attrs = a.GetCustomAttributes(false);
foreach (Attribute attr in attrs)
{
    Console.WriteLine("Attribute: {0}", attr.GetType().Name);
}

Si lo que queremos es obtener un atributo específico, podemos llamar al mismo método _GetCustomAttributes_ especificando el tipo del atributo. Este es un ejemplo para obtener el atributo AssemblyDescription:

Assembly a = Assembly.GetExecutingAssembly();

Type attrType = typeof(AssemblyDescriptionAttribute);
object\[\] versionAttrs = a.GetCustomAttributes(attrType, false);

if (versionAttrs.Length > 0)
{
    AssemblyDescriptionAttribute desc =
        (AssemblyDescriptionAttribute)versionAttrs\[0\];
    Console.WriteLine("Found Description!");
    Console.WriteLine("Desc: {0}", desc.Description);
}



Hasta aquí esta entrada sobre un nuevo aspecto de \*System.Reflection\*. Quedan aún tres entradas más para terminar este tema que intentaré publicar ASAP. Después seguiremos con otros dos grandes temas: «globalización» e «instrumentalización».

