---
title: Caché de dependencia de SQL con ASP.NET
tags: []
---
Estos últimos días he estado peleándome con la clase [_SqlCacheDependency_](http://msdn.microsoft.com/es-es/library/system.web.caching.sqlcachedependency.aspx) y he aprovechado este tiempo para conocer el funcionamiento de la notificación de cambios con las distintas versiones de SQL Server. En esta entrada veremos algunos sencillos ejemplos de configuración y de funcionamiento de las notificaciones basadas en tablas, compatible con todas las versiones de SQL Server, y ejemplos de notificaciones basadas en la infraestructura de [_Service Broker_](http://msdn.microsoft.com/es-es/library/ms166043(v=SQL.90).aspx), disponible desde SQL Server 2005.

La clase _SqlCacheDependency_ nos permite establecer una dependencia entre un elemento de la caché de nuestra aplicación web y una tabla o consulta de SQL Server, consiguiendo que cuando el contenido de una tabla cambie, los elementos de la caché vinculados con esa tabla también cambien. Vamos a ver que esto se consigue supervisando la tabla o, a partir de SQL Server 2005, registrando la aplicación para recibir notificaciones cuando se producen cambios en los datos originales.

Para habilitar la notificación por tablas, debemos hacer uso de la herramienta [_aspnet\_regsql.exe_](http://msdn.microsoft.com/es-es/library/ms229862.aspx). En el ejemplo siguiente se muestra como habilitar la caché de dependencia de SQL en la base de datos _TestDB_ del servidor local utilizando las credenciales actuales de Windows.

aspnet\_regsql -S . -E -ed -d TestDB </pre> Esto crea la tabla _AspNet\_SqlCacheTablesForChangeNotification_ y cinco procedimientos almacenados de uso interno. Una vez tenemos habilitada la base de datos, debemos hacer lo mismo con la tabla en la que queremos establecer caché de dependencia. En este ejemplo se muestra como habilitarla en la tabla _Libro_.

aspnet\_regsql -S . -E -d TestDB -et -t Libro

Al ejecutar comando, se añade un _trigger_ en la tabla con el nombre _Libro\_AspNet\_SqlCacheNotification\_Trigger_ para las operaciones INSERT, UPDATE y DELETE. Si miramos lo que hace este _trigger_, vemos que sólo ejecuta el procedimiento _AspNet\_SqlCacheUpdateChangeIdStoredProcedure_ al que le pasa como parámetro el nombre de la tabla. Este procedimiento actualiza la tabla _AspNet\_SqlCacheTablesForChangeNotification_ incrementando el número de cambio (campo _changeId_). ¡Bien sencillo!

Una vez habilitadas la caché de dependencia en nuestra tabla, ya podemos utilizar _SqlDependency_ en nuestra aplicación web. La forma más fácil de ponerlo en práctica es añadiendo en nuestro _WebForm_ un control _GridView_ y un control _SqlDataSource_. En el ejemplo se utiliza una cadena de conexión guardada en el _web.config_ con el nombre _testConnectionString_.

<asp:GridView ID="GridView1" runat="server" AutoGenerateColumns="True" DataSourceID="SqlDataSource1">
</asp:GridView>
<asp:SqlDataSource ID="SqlDataSource1" runat="server" 
        ConnectionString="<%$ ConnectionStrings:testConnectionString %>" 
        ProviderName="<%$ ConnectionStrings:testConnectionString.ProviderName %>" 
        SelectCommand="SELECT \[id\], \[titulo\] FROM \[libro\]" >
</asp:SqlDataSource>

El segundo paso a realizar es modificar el _web.config_ añadiendo la sección _caching_ dentro de _system.web_. En este ejemplo habilitamos la caché de dependencia para la base de datos _testdb_.

<caching>
      <sqlCacheDependency enabled = "true" >
        <databases>
          <add name="testdb" connectionStringName="testConnectionString" pollTime="1000" />
        </databases>
   </sqlCacheDependency>
</caching>

Por último, sólo queda añadir directiva _OutputCache_ a la página, indicando en el atributo _SqlDependency_ el nombre de la base de datos que hemos asignado en el _web.config_ y el nombre de la tabla, así como el atributo _VaryByParam=”none”_ para que no se tenga en cuenta ningún parámetro.

<%@ OutputCache Duration="3600" SqlDependency="test:Libro" VaryByParam="none" %>

Para comprobar que la página que se nos devuelve es la guardada en caché vamos a incluir un control _Label_ en el que mostraremos la hora actual.

protected void Page\_Load(object sender, EventArgs e)
{
     Label1.Text = DateTime.Now.ToString();
}

¡Y ya está!, si ejecutamos la página podremos ver que la etiqueta muestra la misma hora en cada actualización de la página, y que si realizamos cualquier modificación en la tabla _Libro_ y actualizamos veremos que el contenido del _GridView_ y la etiqueta se actualizan con la nueva información y la hora actual. Fantástico, ¿no? Pues la verdad es que sí, pero no es tan bonito como parece. Si realizamos una traza con SQL Profiler veremos que cada segundo se está ejecutando el procedimiento _AspNet\_SqlCachePollingStoredProcedure_. Esto es así debido al valor 1000 que asignamos al atributo _pollTime_ en el _web.config_. Para evitarnos unas cuantas consultas podemos reducir la frecuencia con la que se sondea la base de datos a un minuto, de hecho, este es el valor por defecto si no establece el atributo. Como es evidente, nuestra página permanecerá cacheada hasta que se produzca el siguiente sondeo de la base de datos y se compruebe que la tabla se ha modificado.

A partir de SQL Server 2005 la cosa cambió a mejor. Sobre todo porque nos deshacemos de las tablas y de los _triggers_ de notificación y pasamos a utilizar _Service Broker_. Antes de continuar con los ejemplos, vamos a deshabilitar la dependencia de caché por tablas de la base de datos _TestDB_ mediante el ya conocido _Aspnet\_regsql.exe_:

aspnet\_regsql -S . -E -d TestDB -dd

Para poder recibir notificaciones, Service Broker debe estar habilitado en la base de datos y los usuarios deben tener permisos para recibir esas notificaciones. Podemos saber el estado de _Service Broker_ en todas las bases de datos con esta consulta:

SELECT name, is\_broker\_enabled FROM sys.databases

Si _Service Broker_ no está habilitado en nuestra base de datos (TestDB), debemos hacerlo mediante la siguiente instrucción:

ALTER DATABASE testdb SET ENABLE\_BROKER WITH ROLLBACK IMMEDIATE

Una vez hecho esto ya podemos utilizar la clase _SqlCacheDependency_ en nuestra aplicación para relacionar cualquier objeto de la caché. En el siguiente ejemplo podemos ver la implementación más sencilla.

protected void Page\_Load(object sender, EventArgs e)
{
    DataTable categories = (DataTable)Cache.Get("Libros");

    if (categories == null)
    {
        categories = GetBooks();
        Label1.Text = System.DateTime.Now.ToString();
    }

    GridView1.DataSource = categories.DefaultView;
    GridView1.DataBind();
}

private DataTable GetBooks()
{
    string connectionString = 
        ConfigurationManager.ConnectionStrings\["testConnectionString"\].ConnectionString;

    DataTable categories = new DataTable();

    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        SqlCommand command = new SqlCommand("SELECT id, titulo FROM dbo.libro", connection);
        SqlCacheDependency dependency = new SqlCacheDependency(command);
        SqlDataAdapter adapter = new SqlDataAdapter();
        adapter.SelectCommand = command;

        DataSet dataset = new DataSet();
        adapter.Fill(dataset);
        categories = dataset.Tables\[0\];
        Cache.Insert("Libros", categories, dependency);
    }

    return categories;
}

Aunque el código es bastante autoexplicativo, lo resumo en cuatro líneas. La primera vez que se carga la página, se comprueba si existe el objeto _Libros_ en la caché. Al no existir, se consulta en la base de datos y se crea el objeto _SqlCacheDependency_ pasando el _SqlCommand_ de la consulta. Una vez tenemos el resultado, lo guardamos en la caché de la aplicación estableciendo la dependencia pasando el objeto _SqlCacheDependency_ como tercer parámetro. Una posterior ejecución de la página obtendrá el objeto _Libros_ de la caché.

El último detalle que queda es que para poder recibir las notificaciones de cambios, la aplicación se debe registrar utilizando el método _Start_ de la clase _SqlDependency_. En el caso de una aplicación web, el lugar adecuado para hacerlo es en los eventos _Application\_Start_ y _Application\_End_ del _global.asax_.

void Application\_Start(object sender, EventArgs e)
{
    string connectionString = 
        ConfigurationManager.ConnectionStrings\["testConnectionString"\].ConnectionString;
    System.Data.SqlClient.SqlDependency.Start(connectionString);
}

void Application\_End(object sender, EventArgs e)
{
    string connectionString =
        ConfigurationManager.ConnectionStrings\["testConnectionString"\].ConnectionString;
    System.Data.SqlClient.SqlDependency.Stop(connectionString);
}

Al ejecutar la aplicación comprobaremos que la primera vez se muestra la hora actual y el _GridView_ con los datos. Si recargamos la página, mostrará los mismos datos (recogidos de la caché), pero no mostrará la hora actual.

La pregunta que os estaréis haciendo (si habéis llegado hasta aquí), es si es posible utilizar _LinQ_ con _SqlCacheDependency_. La respuesta es que sí que se puede, pero no de una forma directa y con un inconveniente. La forma de hacerlo es idéntica al ejemplo anterior, pero para obtener la consulta SQL debemos recurrir al método _GetCommand_ del objeto _DataContext_. El siguiente código muestra la forma de hacerlo.

protected void Page\_Load(object sender, EventArgs e)
{
    List<libro> books = (List<libro>)Cache.Get("LibrosLinQ");

    if (books == null)
    {
        books = GetBooks();
        Label1.Text = System.DateTime.Now.ToString();
    }

    GridView1.DataSource = books;
    GridView1.DataBind();
}

private List<libro> GetBooks()
{
    DataClasses1DataContext dc = new DataClasses1DataContext();

    var q = from libro in dc.libros select libro;
  
    List<libro> libros;

    using (SqlConnection connection = new SqlConnection(dc.Connection.ConnectionString))
    {
        connection.Open();
        SqlCommand command = new SqlCommand(dc.GetCommand(q).CommandText, connection);
        SqlCacheDependency dependency = new SqlCacheDependency(command);
        command.ExecuteNonQuery();
        
        libros = q.ToList();
        Cache.Insert("LibrosLinQ", libros, dependency);
    }

    return libros;
}


Este código presenta un inconveniente y es que cada vez que realizamos el poceso de cacheo de una consulta, esta se tiene que ejecutar dos veces: la primera al llamar al método \*ExecuteNonQuery\* y la segunda al llamar al método \*ToList\*. Esto podría convertirse en un problema en el caso de consultas con un elevado tiempo de ejecución. Para evitar esta situación, podríamos almacenar el resultado en un objeto \*DataTable\* (como en el ejemplo de SQL), en lugar de en un \*List<T>\*, pero entonces perderíamos todas las ventajas de utilizar la lista genérica.

**Descarga código fuente:**
[SQLCacheDependency.zip](http://sdrv.ms/14OU9Q2)

