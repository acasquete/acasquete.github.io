---
title: Routing con ASP.NET 4 Web Forms
tags: []
---
Con la salida del Framework .NET 3.5 SP1, se introdujo el enrutamiento de URL (_URL Routing_) como parte de ASP.NET MVC. Los programadores de ASP.NET _Web Forms_ también [podíamos utilizar routing](http://haacked.com/archive/2008/03/11/using-routing-with-webforms.aspx), pero no de una forma directa y siempre mediante la implementación de una clase _[IRouteHandler](http://msdn.microsoft.com/es-es/library/system.web.routing.iroutehandler.aspx)_ para procesar las solicitudes. Lo importante, al fin y al cabo, era que ya no teníamos que utilizar la reescritura de direcciones URL, y eso fue una gran noticia.

Ahora, con ASP.NET 4 WebForms, podemos implementar de una forma muy sencilla el enrutamiento de direcciones URL. En las siguientes líneas, vamos a ver ejemplos de cómo definir rutas, establecer unos valores predeterminados a los parámetros de la ruta y, por último, veremos cómo aplicar restricciones utilizando expresiones regulares y objetos que implementan la interfaz [_IRouteConstraint_](http://msdn.microsoft.com/es-es/library/system.web.routing.irouteconstraint.aspx).

Para definir una ruta, utilizaremos el método _MapPageRoute_ de la clase _RouteCollection_. La sobrecarga más sencilla de este método tiene tres parámetros: el identificador, el modelo de ruta y la URL física.

En el siguiente ejemplo, creamos una ruta con dos parámetros (_language_ y _year_, encerrados entre llaves). Aunque en el código no aparece de forma explícita, las rutas se definen, normalmente, en el _Application\_Start_ del Global.asax.

RouteTable.Routes.MapPageRoute("Ruta", "{language}/{year}", "~/default.aspx"); </pre>

Este código es equivalente a crear un objeto _Route_ mediante un _PageRouteHandler_ (para definir el fichero que procesará la solicitud) y añadirlo a la colección _RouteCollection_. Como es evidente, utilizar el método _MapPageRoute_ hará nuestro código mucho más inteligible.

Route def = new Route("{language}/{year}", new PageRouteHandler("~/default.aspx"));
RouteTable.Routes.Add("Ruta", def);

En los dos ejemplos anteriores, la página _default.aspx_ será la encargada de procesar la solicitudes que coincidan con el modelo de ruta, como, por ejemplo, «spanish/2010» o «english/10». En algunos casos, podemos necesitar que ciertos parámetros no sean obligatorios, es decir, que la ruta se procese aunque falte algún parámetro en la petición. Esto se consigue insertando un asterisco en el parámetro que queramos indicar como opcional. En el siguiente ejemplo, el parámetro _month_ es opcional, por lo tanto, las peticiones «spanish/2010/04» y «spanish/2010» se procesarán por la misma ruta.

RouteTable.Routes.MapPageRoute("", "{language}/{year}/{\*month}", "~/default.aspx");

En lugar de utilizar parámetros opcionales, también podemos asignar un valor por defecto a un determinado parámetro. De esta forma, aunque la URL no incluya el parámetro, siempre recibiremos un valor. La definición de los valores predeterminados de una ruta se realiza mediante una colección [_RouteValueDictionary_](http://msdn.microsoft.com/es-es/library/system.web.routing.routevaluedictionary.aspx) que pasamos en la llamada al método _MapPageRoute_.

routes.MapPageRoute("", "{language}/{year}/{month}", "~/default.aspx", false,
    new RouteValueDictionary
    {
        { "year", DateTime.Now.Year},
        { "month", DateTime.Now.Month}
    }
);

Aún más interesantes son las restricciones (_constraints_), con las que podemos delimitar los valores aceptados en los parámetros. Podemos crear estas restricciones utilizando expresiones regulares y objetos que implementen la interfaz _IRouteConstraint_. Al igual que para agregar valores por defecto, las restricciones se agregan mediante una colección _RouteValueDictionary_. En el siguiente ejemplo, se define una ruta sin valores por defecto y con restricciones en todos los parámetros.

routes.MapPageRoute("", "{language}/{year}/{month}/{day}", "~/default.aspx", false, null,
    new RouteValueDictionary
    {
        { "language", "\[a-z\]{2}-\[a-z\]{2}" },
        { "year", @"d{4}" },
        { "month", @"d{2}" },
        { "day", @"d{2}" }
    }
);

Si las comprobaciones que queremos hacer son más complejas, tendremos que utilizar un objeto _IRouteConstraint_. Siguiendo con el ejemplo anterior, a continuación definimos una clase (_DateRouteConstraint_) que implementa la interfaz _IRouteConstraint_ y en el método _Match_, comprobamos que la fecha sea una valida y que esté entre unos valores máximo y mínimo (que no sea superior a hoy y no sea anterior al año 2000).

public class DateRouteConstraint : IRouteConstraint
{
    bool IRouteConstraint.Match(HttpContextBase httpContext,
        Route route, string parameterName,
        RouteValueDictionary values, RouteDirection routeDirection)
    {
        bool valid = false;
        DateTime dt = new DateTime();

        string s = String.Format("{0}/{1}/{2}", values\["day"\], values\["month"\], values\["year"\]);

        if (DateTime.TryParse(s, out dt))
        {
            if (dt >= new DateTime(2000, 1, 1) && dt <= DateTime.Now)
            {
                valid = true;
            }
        }

        return valid;
    }
}

Para definir la ruta, procederemos igual que con las restricciones con expresiones regulares, pero como valor proporcionaremos en la colección _RouteValueDictionary_ una instancia de nuestra clase _DateRouteConstraint_. Además, podemos combinar los dos tipos de restricciones en la misma colección.

routes.MapPageRoute("", "{year}/{month}/{day}", "~/default.aspx", false,
  null,
   new RouteValueDictionary
   {
       { "check", new DateRouteConstraint() },
       { "year", @"d{4}" },
       { "month", @"d{2}" },
       { "day", @"d{2}" }
   }
   );

Después de repasar lo más destacado en cuanto a enrutamiento, es importante recordar algo que nos puede librar de más de un dolor de cabeza: las rutas se evalúan por el orden en que se encuentran en la colección, y sólo hasta encontrar la primera coincidencia; si definimos dos rutas: «{year}/{month}» y «{year}», la segunda ruta nunca controlará una solicitud. Una situación común —y ya voy terminando— con la que nos encontraremos, es cómo definir las mejores rutas en aplicaciones existentes. Supongamos, por ejemplo, que tenemos una tienda en la que se realizan las siguientes peticiones para ver los distintos tipos de detalle de un producto:

    > **tienda.es/producto.aspx?id=1 tienda.es/productoDetalle.aspx?id=1&amp;pagina=1 tienda.es/productoAccesorios.aspx?id=1&amp;pagina=1**
    

En un principio, podríamos pensar en definir tres rutas (una para cada página física), pero con una sola ruta podemos abarcar muchas más situaciones, podemos utilizar los parámetros para componer el nombre de la URL física de la ruta. En el ejemplo siguiente, se utiliza el parámetro «detalle» como nombre de la página ASPX.

 RouteTable.Routes.MapPageRoute("", "{detalle}/{id}/{\*pagina}", "~/{detalle}.aspx");



Así, nuestra aplicación responderá correctamente ante peticiones «/producto/100», «/productodetalle/500» o «/productoaccesorios/600/3». Podríamos mejorar bastante este ejemplo. Quizás, la mejora más evidente sería añadir restricciones para que sólo se aceptasen determinados valores en el parámetro «detalle», pero lo que quería mostrar con este código son las capacidades de enrutamiento que tenemos a partir de ahora en ASP.NET \*WebForms\*.

