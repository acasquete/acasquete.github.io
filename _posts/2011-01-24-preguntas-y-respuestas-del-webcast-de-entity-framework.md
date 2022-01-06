---
title: Preguntas y respuestas del webcast de Entity Framework
tags: [event]
reviewed: true
---
El pasado 18 de enero tuve el placer de presentar mi primer [webcast de introducción a Entity Framework](https://msevents.microsoft.com/CUI/WebCastEventDetails.aspx?culture=es-ES&EventID=1032474104&CountryCode=ES) organizado por el grupo de usuarios [UOC DotNetClub](http://uoc.dotnetclubs.com/). La experiencia fue fantástica, con una gran asistencia y participación, así que quiero agradecer a [Jesús Bosch](http://geeks.ms/blogs/jbosch) que lo hiciese posible y a todos lo que asistieron por aguantarme la charla.

Al final del _webcast_ se hicieron bastantes preguntas y algunas no las pude contestar en el momento, así que he hecho una recopilación de las que he creído más interesantes. He intentado responder de una forma breve y he añadido enlaces en algunas respuestas para ampliar información.

Podéis [ver la grabación del webcast](https://msevents.microsoft.com/CUI/WebCastEventDetails.aspx?culture=es-ES&EventID=1032474104&CountryCode=ES) en la misma dirección de registro y la presentación que utilicé se puede descargar desde [SlideShare](http://www.slideshare.net/alexcasquete/entity-framework-4-desde-cero).

**_Roberto_: ¿Cómo logramos que los índices clúster se creen en un campo específico, diferente al ID?**  
El asistente de generación de base de datos genera un índice clúster en las claves primarias (_Primary Key_), y un índice no clúster en las claves foráneas (_Foreign Keys_). De momento, no es posible definir ningún índice explícitamente en el [Reglas de generación de bases de datos (Asistente para generar base de datos)](http://msdn.microsoft.com/es-es/library/dd456825.aspx)

**Jimmy: Si deseo utilizar Entity Framework en un servicio ASP.NET, ¿necesito algún requerimiento adicional para implementarlo en el servidor?**  
No se necesita ningún componente adicional para utilizar Entity Framework en un servicio, pero hay que tener en cuenta que en escenarios donde no está disponible el contexto de objetos, como puede ser el caso de los servicios web, puede ser necesario implementar soluciones para realizar el seguimiento de cambios de las entidades. _Más información:_ [Crear aplicaciones de n niveles (Entity Framework)](http://msdn.microsoft.com/es-es/library/bb896304.aspx)

**JBosch: El _ObjectContext_, ¿cómo se mantendría en una aplicación ASP.NET?**  
El _ObjectContext_ no perdura entre postbacks en una aplicación ASP.NET y esto impide realizar realizar el seguimiento de cambios de las entidades. Sin embargo, disponemos del control _EntityDataSource_ que nos puede ser de ayuda en aplicaciones pequeñas, donde no hay separación de la UI de la lógica de negocio o de acceso a datos. En aplicaciones de n niveles las _self-tracking entities_ ayudan a realizar el seguimiento de cambios, y los métodos _ApplyCurrentValues_ o _ApplyOriginalValues_ del ObjectContext se pueden utilizar para comparar una entidad conectada al contexto con otra desconectada. _Más información:_ [Asociar y desasociar objetos (Entity Framework)](http://msdn.microsoft.com/es-es/library/bb896271)

**Emili: ¿Se pueden crear entidades desde el diseñador con claves compuestas? ¿Sería sólo con tipos complejos?**  
Solo se puede definir una clave a partir de una o varias propiedades escalares, no se puede definir una propiedad de tipo complejo como clave de una entidad. _Más información:_ [Trabajar con claves de entidad (Entity Framework)](http://msdn.microsoft.com/es-es/library/dd283139.aspx).

**Carlos González: ¿Qué motores de datos se pueden utilizar actualmente con EF? ¿Soporta algún SGBD que no sea SQLServer?**  
Entity Framework utiliza proveedores ADO.NET para comunicarse con la base de datos. Actualmente hay varios proveedores de terceros para acceder a bases de datos Oracle, DB2, MySQL, etc. Puedes ver una lista de todos los proveedores disponibles aquí: [ADO.NET Data Providers](http://msdn.microsoft.com/en-us/data/dd363565.aspx)

**Rubén López: En caso de mapear dos tablas a una entidad, ¿cómo funcionan los updates?**  
En el código de nuestra aplicación, actualizamos la entidad sin preocuparnos por el número de tablas con las que está mapeada y Entity Framework genera las consultas necesarias para actualizar todas las tablas. En el caso de que el mapeo fuese contra dos tablas, Entity Framework generaría dos sentencias UPDATE. Más información: [Tutorial: Asignar una entidad a varias tablas (Herramientas de Entity Data Model)](http://msdn.microsoft.com/es-es/library/cc716698.aspx).

**Jonathan: Crear una entidad como has creado “Student”, ¿crea por detrás un INSERT parametrizado?**  
Sí, Entity Framework siempre intentará crear sentencias SQL parametrizadas.

**Gabriel Gonzalez: ¿Cómo trabaja EF en una aplicación multicapas, seria utilizando los Self-Tracking? Y si es así, ¿cómo los puedo utilizar?**  
Efectivamente, en la mayoría de aplicaciones de n niveles, en los que no tenemos disponible el contexto de los objetos, podemos hacer uso de las entidades self-tracking para realizar el seguimiento de cambios. _Más información:_ [Trabajar con entidades de seguimiento propio (Entity Framework)](http://msdn.microsoft.com/es-es/library/ff407090.aspx)

**Carlos González: Una entidad Entity Framework, entiendo que no debería ser expuesta en un servicio web por motivos de serialización, lo normal sería crear DTO, ¿no es así?**  
Aunque depende la interoperabilidad que se requiera, creo que DTO debería ser la última opción a considerar ya que en Entity Framework 4 disponemos de las clases _self-tracking entities_ que simplifica la creación de aplicaciones n-tier, y nos evita el tener que construir una nueva capa. _Más información:_ [Creación de aplicaciones de N niveles con EF4](http://msdn.microsoft.com/es-es/magazine/ee335715.aspx)

**JFrancisco Ibarra: Conozco LINQ, y después de ver algunas demos que has hecho, mi pregunta es: ¿por qué usar Entity SQL cuando puedo usar LINQ para llegar a las entidades?**  
Entity SQL es útil si necesitamos crear consultas dinámicamente en tiempo de ejecución. Otra ventaja es que no existen diferencias en la sintaxis de las consultas entre C# y VB.NET, además Entity SQL puede ser más fácil de aprender si dominas T-SQL. _Más información:_ [Consultar un modelo conceptual (Entity Framework)](http://msdn.microsoft.com/es-es/library/bb738642.aspx).

**Virgili: Ante un nuevo proyecto inminente (no muy grande en VS2010 y SQL Server y sin experiencia previa en Entity Framework) vale la pena el esfuerzo de aprendizaje e implementarlo en EF4 o cree que es mejor utilizar LINQ to SQL y entrar poco a poco en EF4?**  
Aconsejo utilizar Entity Framework en nuevos proyectos, pero naturalmente depende del proyecto y de las horas que dispongas para formación. Quizás un proyecto no muy complejo es el ideal para iniciarse con Entity Framework. Además Entity Framework 4 es la solución recomendada por Microsoft para acceso a datos en escenarios relacionales. _Más información:_ [Update on LINQ to SQL and LINQ to Entities Roadmap](http://blogs.msdn.com/b/adonet/archive/2008/10/29/update-on-linq-to-sql-and-linq-to-entities-roadmap.aspx)

**Carlos González: Podrías enumerar una serie de ventajas de Entity Framework con respecto a otros ORM como NHibernate, o incluso LINQ to SQL?**   
No conozco NHibernate, así que lo que mejor puedo hacer es remitir a un excelente post de Alberto Díaz: [¿EF vs NHibernate? ¿Esa es la pregunta?](http://geeks.ms/blogs/adiazmartin/archive/2010/03/21/191-ef-vs-nhibernate-191-esa-es-la-pregunta.aspx). Y entre LINQ to SQL o Entity Framework, creo que se responde con la anterior pregunta.

**Juan: Como podemos cambiar en tiempo de ejecución el origen de los datos? Por ejemplo: si nuestro Datamodel representa cada uno de nuestros clientes pero cada cliente tiene su propia base de datos. Entonces cuando autentifique el cliente se asigna dinámicamente el modelo a su base de datos. Se puede hacer una clase estática con un EntityConnectionStringBuilder pero al ser estática tiene que estar definida desde el inicio y no asigna la base de datos de cada cliente. ¿Qué aconsejas para solucionar un caso así?**  
Aunque no lo he probado, parece que la solución pasa por crear la cadena de conexión y pasarla al instanciar el contexto. El código está extraído de [este hilo de los foros MSDN](http://social.msdn.microsoft.com/Forums/en/adodotnetentityframework/thread/8a89a728-6c8d-4734-98cb-11b196ba11fd "EF and change of server (connection string)").

```cs
SqlConnectionStringBuilder sqlBuilder = new SqlConnectionStringBuilder(); sqlBuilder.DataSource = @”Server1MySERVER”; sqlBuilder.InitialCatalog = “MyNewDatabase”; sqlBuilder.IntegratedSecurity = true; sqlBuilder.MultipleActiveResultSets = true;

EntityConnectionStringBuilder entityBuilder = new EntityConnectionStringBuilder(); entityBuilder.Provider = “System.Data.SqlClient”; entityBuilder.ProviderConnectionString = sqlBuilder.ToString(); entityBuilder.Metadata = @”res://_/Model1.csdl|res://_/Model1.ssdl|res://\*/Model1.msl”;

EntityConnection conn = new EntityConnection(entityBuilder.ToString());

MyNewDatabaseEntities context = new MyNewDatabaseEntities(conn);
```

**MarcLafita: ¿Desde dónde podemos descargar la generación de codigo ADO.NET POCO? ¿Tengo que descargar algún CTP?**  
No hace falta descargar la CTP, las plantillas de generación de las clases POCO están disponibles para descarga en la [Galería de Visual Studio](http://visualstudiogallery.msdn.microsoft.com/). Están disponibles las plantillas en C# y VB.NET y también hay unas plantillas personalizadas para proyectos de Sitio Web. Estos son los enlaces a cada una de ellas:

[ADO.NET C# POCO Entity Generator](http://visualstudiogallery.msdn.microsoft.com/en-us/23df0450-5677-4926-96cc-173d02752313)  
[ADO.NET C# WebSite POCO Entity Generator](http://visualstudiogallery.msdn.microsoft.com/en-us/fe568da5-aa1a-4178-a2a5-48813c707a7f)  
[ADO.NET VB POCO Entity Generator](http://visualstudiogallery.msdn.microsoft.com/en-us/53ecbded-8936-4299-ab04-1e44e5489752)  
[ADO.NET VB WebSite POCO Entity Generator](http://visualstudiogallery.msdn.microsoft.com/en-us/463c5aca-05ad-4cdb-910b-2e4f83269e34)  

En el blog del equipo de ADO.NET podéis encontrar un tutorial para utilizar estas plantillas: [Walkthrough: POCO Template for the Entity Framework](http://blogs.msdn.com/b/adonet/archive/2010/01/25/walkthrough-poco-template-for-the-entity-framework.aspx).

**David: ¿Se puede utilizar Entity Framework con el Visual Studio Express, o necesitamos la versión completa de Visual Studio 2010?**  
Sí se puede, Visual Studio 2010 Express tiene soporte completo para Entity Framework.

**Roberto: ¿Se puede asignar a una propiedad de una Entidad los tipos Filestream y HierarchyID nuevos en SQL?**  
Propiamente dicho, Filestream no es un tipo de dato, podríamos decir que es un atributo que aplicamos a un campo varbinary(max). Entity Framework representa este tipo de campo como un campo de tipo byte\[\] y podemos acceder sin problema a su contenido. Sin embargo, Entity Framework no soporta el tipo [HierarchyID](http://msdn.microsoft.com/es-es/library/bb677290.aspx), aunque existe una solución temporal hasta que haya soporte oficial: [How to use HierarchyID in LinqToSQL or Entity-Framework // MSSQL Server 2008](http://nibblersrevenge.cluss.de/archive/2009/05/31/how-to-use-hierarchyid-in-linqtosql-or-entity-framework-mssql.aspx).

**Pedro Luís: ¿Podríamos sustituir la entidad de negocio por Entity Framework?**  
Sí, podemos extender los objetos de entidades para que contengan el comportamiento necesario de nuestra aplicación, o podemos crear nuestros objetos de negocio a partir de las entidades y almacenar la lógica en esos objetos de negocio. _Más información:_ [Implementar lógica de negocios (escenarios de Entity Framework)](http://msdn.microsoft.com/es-es/library/cc716789.aspx)

**Luís: ¿Cómo trabajaría con Entity Framework si quisiera utilizar el patrón MVC?**  
En MVC, el modelo debe contener toda la lógica de negocio de la aplicación, la lógica de validación y la lógica de acceso a bases de datos. En un proyecto ASP.NET MVC, deberíamos crear el Entity Data Model en la carpeta Models. En este [tutorial](http://www.asp.net/mvc/tutorials/creating-model-classes-with-the-entity-framework-cs "Creating Model Classes with the Entity Framework"), se muestra como utilizar Entity Framework en una aplicación ASP.NET MVC en la que se realizan operaciones CRUD.

**Jorge: ¿Futuro de Entity Framework?**  
Lo más cercano en el tiempo es la liberación en febrero o en marzo de la versión con soporte completo de Code-First. Además en el [PDC](http://player.microsoftpdc.com/session) se anunciaron varias características en las que se está trabajando, entre las que se incluyen: soporte para _Enums_, _Spatial_, funciones con valores de tabla y claves alternativas. También se anunciaron mejoras en el diseñador de entidades que permitirán tener múltiples diagramas por modelo, así como mejoras en la generación de SQL, en las consultas LINQ y en la migración y despliegue. _Más información:_ [PDC 2010 - Code First Development with Entity Framework](http://bit.ly/cbMOBm)

