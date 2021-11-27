---
title: Comprobar si una cadena es un GUID
tags: []
---
Los GUIDs (_Globally Unique Identifier_) son un tipo especial de identificador y se escriben normalmente como una secuencia de dígitos hexadecimales separados en cinco bloques mediante guiones «-». Si tenemos la necesidad de saber si una cadena de texto tiene el formato de un [GUID](http://es.wikipedia.org/wiki/Globally_Unique_Identifier) podemos realizar la comprobación de varias maneras, pero la más eficiente es mediante el uso de expresiones regulares.

En el siguiente ejemplo podemos ver como se realiza la comprobación mediante el método _IsMatch_ de la clase _RegEx_. Si la cadena no es nula y coincide con el patrón de un GUID, el método _IsGuid_ devuelve _True_; en caso contrario devuelve _False_. He añadido los caracteres «^» y «$» al patrón para indicar que toda la cadena, y no sólo una parte de ella, debe cumplir la expresión regular. Por último, al constructor se le pasa el parámetro _RegexOptions.IgnoreCase_ para indicar que no se debe distinguir entre mayúsculas y minúsculas.

Imports System.Text.RegularExpressions

Class Program Private Shared Sub Main() Dim guid As String = “95cd9c38-cedd-4f11-8105-5a4d100f2472” Dim noguid As String = “no guid”

        Console.WriteLine("Is Guid: {0} - {1}", guid, IsGuid(guid))
        Console.WriteLine("Is Guid: {0} - {1}", noguid, IsGuid(noguid))
        Console.ReadKey()
    End Sub
    
    Public Shared Function IsGuid(ByVal exp As String) As Boolean
        If exp IsNot Nothing Then
            Dim GuidRegEx As New Regex("^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$",RegexOptions.IgnoreCase)
            Return GuidRegEx.IsMatch(exp)
        Else
            Return False
        End If
    End Function End Class
    

</pre>

y en C#:

using System;
using System.Text.RegularExpressions;

class Program
{
    static void Main()
    {
        string guid = "95cd9c38-cedd-4f11-8105-5a4d100f2472";
        string noguid = "no guid";

        Console.WriteLine("Is Guid: {0} - {1}", guid, IsGuid(guid));
        Console.WriteLine("Is Guid: {0} - {1}", noguid, IsGuid(noguid));
        Console.ReadKey();
    }

    static public bool IsGuid(string exp)
    {
        if (exp != null)
        {
            Regex GuidRegEx = new Regex(@"^\[0-9A-F\]{8}-\[0-9A-F\]{4}-\[0-9A-F\]{4}-\[0-9A-F\]{4}-\[0-9A-F\]{12}$", RegexOptions.IgnoreCase);
            return GuidRegEx.IsMatch(exp);
        }
        else
        {
            return false;
        }
    }
}

