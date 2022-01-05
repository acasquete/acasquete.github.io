---
title: Mejorar el tiempo de carga eliminando espacios en blanco
tags: [programming]
---
Hace unos meses Microsoft publicó [Visual Round Trip Analyzer (VRTA)](http://www.microsoft.com/Downloads/details.aspx?FamilyID=119f3477-dced-41e3-a0e7-d8b5cae893a3&displaylang=en), una herramienta que permite visualizar y evaluar el rendimiento de un sitio web. Por su lado, Google presentó la semana pasada [Page Speed](http://code.google.com/speed/page-speed/), un complemento _open-source_ para FireFox / FireBug con una funcionalidad muy similar a VRTA. Ambas herramientas realizan un análisis de rendimiento y ofrecen sugerencias para mejorar la utilización del ancho de banda, el tiempo del viaje de ida y vuelta al servidor y el tiempo de renderizado del navegador.

Esta entrada la voy a dedicar a una de las optimizaciones más fáciles de implementar y con la que podemos reducir al máximo la cantidad de información que se envía al cliente. Esta optimización consiste en eliminar del código HTML los espacios, saltos de línea y tabuladores que normalmente utilizamos para facilitar la lectura, pero que son innecesarios para que el navegador genere la página correctamente. Según algunos estudios —que omito por ser parte interesada—, la media de espacios en blanco en una página Web está entre el 20 y el 30%. Y según las herramientas de Google y Microsoft, una cantidad por encima del 10% de espacios en blanco es un aspecto a corregir ya que, aunque no parezca mucho, al hacerlo se apreciará una mejora en el tiempo de carga de la página. En las siguientes líneas, vamos a intentar saber si este nivel de mejora se corresponde con la realidad, que ventajas se obtienen (si es que se obtienen) si se combina con la [compresión HTTP](http://www.microsoft.com/technet/prodtechnol/WindowsServer2003/Library/IIS/d52ff289-94d3-4085-bc4e-24eb4f312e0e.mspx?mfr=true "Using HTTP Compression in IIS 6.0"), que consumo de CPU se requiere y si, en definitiva, es recomendable implementar esta optimización.

Para tener una referencia he comprobado cuanto mejoraría la transferencia de la página principal de diez sitios web que sigo habitualmente. Puede parecer que diez no es una muestra significativa, pero no pretendo hacer un estudio exhaustivo, sino simplemente quiero saber si el beneficio que se obtendría es similar al que los estudios afirman.

La prueba que he realizado ha sido entrar en cada una de las páginas, guardar el código HTML generado y quitar mediante [expresiones regulares](http://msdn.microsoft.com/es-es/library/xbyh1eyc(VS.80).aspx "Expresiones regulares como lenguaje") los espacios en blanco entre etiquetas y todos los saltos de línea. He utilizado el siguiente código, donde _path_ es la ruta del archivo que contiene el código HTML de la página a optimizar:

StreamReader sr = new StreamReader(path); // Lee el fichero html string html = sr.ReadToEnd(); // y lo asignamos a la variable html

html = new Regex(@”>s+<”).Replace(html, “><”); // Reemplaza los espacios entre etiquetas html = new Regex(@”rn”).Replace(html, string.Empty); // Reemplaza los saltos de línea </pre>

En la siguiente tabla se muestra la comparación entre el tamaño de la página original y el tamaño de la página después de ser optimizada.

Comparación entre el tamaño del código HTML original y el optimizado sin espacios

|Sitio Web | Original (bytes) | Optimizado (bytes)| Diferencia (bytes) | Diferencia (%)
|---|---:|---:|---:|---:|
|www.encosia.com|30.847|29.192|1.655|5,37
|msdn.microsoft.com/es-es|55.196|52.307|2.889|5,23
|www.c-sharpcorner.com|353.178|219.019|134.159|37,99
|www.west-wind.com/weblog|182.094|175.258|6.836|3,75
|thinkingindotnet.wordpress.com|54.553|53.013|1.540|2,82
|blogs.msdn.com/somasegar|272.797|262.801|9.996|3,66
|stephenwalther.com/blog|21.491|18.533|2.958|13,76
|www.genbeta.com|79.554|66.472|13.082|16,44|
|channel9.msdn.com|102.595|96.393|6.202|6,05
|blogs.msdn.com/vbteam|124.264|121.574|2.690|2,16

Como podemos comprobar el índice de optimización se sitúa entre el 2 y el 16% del tamaño original. Sólo en el caso de «C# Corner» se obtiene un beneficio del 38%. Estos son unos resultados absolutos, esto significa que esta sería la mejora de transferencia si no se aplicase ninguna otra optimización. Pero lo cierto es que la mayoría de los sitios web que he consultado tienen habilitada la compresión HTTP y es de suponer que este beneficio será menor ya que los espacios en blanco ya se están comprimiendo. ¿Cuál es la mejora al eliminar los espacios en blanco en este caso? Lo vemos en la siguiente tabla:

Comparación utilizando compresión HTTP entre el tamaño del código HTML original y el optimizado sin espacios

|Sitio Web | Original (bytes) | Optimizado (bytes)| Diferencia (bytes) | Diferencia (%)
|---|---:|---:|---:|---:|
|www.encosia.com|8.458|72,58|8.229|229|2,71
|msdn.microsoft.com/es-es|12.436|77,47|11.894|542|4,36
|www.c-sharpcorner.com|29.331|91,70|25.992|3.339|11,38
|www.west-wind.com/weblog|44.764|75,42|43.897|867|1,94
|thinkingindotnet.wordpress.com|11.642|78,66|11.411|231|1,98
|blogs.msdn.com/somasegar|42.602|84,38|42.021|581|1,36
|stephenwalther.com/blog|4.599|78,60|4.340|259|5,63
|www.genbeta.com|15.882|80,04|14.993|889|5,60
|channel9.msdn.com|18.681|81,79|18.036|645|3,45
|blogs.msdn.com/vbteam|25.613|79,39|25.221|392|1,53

Viendo estos resultados, está de más comentar que la compresión HTTP debe ser una característica que debe estar activada en cualquier sitio web si en algo nos preocupa, ya no sólo la experiencia de usuario sino también el uso que hacemos de nuestro ancho de banda, ya que mediante la compresión HTTP se obtiene desde un 73 hasta más de un 90% de reducción del código transferido. Sin embargo, el beneficio que obtenemos al eliminar los espacios en blanco es mucho menos espectacular, varia de un 1,5 hasta un poco más del 5,5%. Como era de esperar, en la página de «C# Corner» la mejora es sensiblemente mayor, de más de un 11%. Estos resultados indican que si se aplicase está optimización, se estarían ahorrando unos 110 Mb por cada gigabyte de transferencia, y en los casos no tan extremos se estarían ahorrando únicamente entre 15 y 55 Mb por gigabyte.

Entonces y resumiendo: ¿es aconsejable implementar esta optimización?

Es muy recomendable en los casos en los que la cantidad de espacios del código transferido supere el 10% (medido con la compresión HTTP deshabilitada), en el resto de situaciones no le daría la misma prioridad, aunque personalmente me obsesiona mucho la optimización, y creo que cualquier mejora en el rendimiento, por pequeña que sea, debe ser implementada a no ser que existan otros factores que lo desaconsejen, como puede ser un elevado coste de procesador o de desarrollo. El coste de CPU de esta optimización es mínimo y no tendrá impacto en el rendimiento general de la aplicación, pero si además tenemos la posibilidad de cachear las páginas, este coste lo podemos despreciar. En cuanto al desarrollo, creo que en la mayoría de casos se puede implementar está solución con muy poco impacto en el código.

No me resisto a poner un ejemplo de código para realizar optimización básica que he utilizado para hacer este análisis. El código es una clase base de la que heredarán todas las páginas de la aplicación. En esta clase únicamente se sobrecarga el método _Render_ en el que se eliminan los espacios y saltos de línea, de la misma forma que he comentado antes.

```csharp
using System.Web.UI;
using System.Text.RegularExpressions;

public class BasePage : System.Web.UI.Page
{
    protected override void Render(HtmlTextWriter writer) 
    {
        using (HtmlTextWriter htmlwriter = new HtmlTextWriter(new System.IO.StringWriter())) 
        { 
          base.Render(htmlwriter);
          string html = htmlwriter.InnerWriter.ToString();

          html = new Regex(@">s+<", RegexOptions.Compiled).Replace(html, "><");
          html = new Regex(@"rn", RegexOptions.Compiled).Replace(html, string.Empty);

          writer.Write(html.Trim()); 
        } 
    }
}
```

Esta propuesta es muy básica, pero da idea de lo que se puede conseguir con tan poco código. No obstante, aún se podría eliminar más información innecesaria como, por ejemplo, los comentarios (ya sean en JavaScript o en HTML), espacios en el código JavaScript y entre atributos, etc., consiguiendo así que viaje al cliente exclusivamente el código imprescindible. Por último, hay que tener en cuenta que este código no funcionará correctamente si tenemos código JavaScript con comentarios de una sola línea iniciados con la doble barra (//) o si existen líneas sin terminar en punto y coma (;).

Dejo para otra ocasión la explicación de cómo realizar esta misma optimización en los ficheros estáticos (JS, CSS y HTML), que aunque se basa en el mismo principio, se puede llevar a cabo a través de varios métodos.

