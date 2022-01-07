---
title: Enlazar un EntityDataReader con un DataGrid
tags: [programming]
---
En todos los ejemplos que he utilizado para mostrar el funcionamiento del [proveedor EntityClient para EntityFramework](http://msdn.microsoft.com/es-es/library/bb738561.aspx), siempre he acabado mostrando los resultados de la consulta en una aplicación de consola mediante un sencillo _Console.WriteLine_. Nunca había hecho la implementación en una aplicación real y mucho menos había utilizado un _DataGrid_ para mostrar el contenido de un _EntityDataReader_. De hecho no había visto ninguna implementación de esto último hasta hace unos días, en la que se resolvía añadiendo los resultados del EntityDataReader a un _DataTable_ que se enlazaba directamente con el _DataGrid_. Esta no es la única forma de conseguirlo, podríamos, por ejemplo, utilizar un Dictionary y convertirlo a una lista de _KeyValuePair_ o crear un tipo en tiempo de ejecución y crear una lista de ese tipo. Hay unas cuantas formas de hacerlo.

En esta entrada vamos a ver una forma más de resolverlo. En lugar de crear un tipo en tiempo de ejecución, haremos uso de un [tipo anónimo](http://msdn.microsoft.com/es-es/library/bb397696.aspx). Así, además de la consulta EntitySQL a ejecutar, tendremos que definir el tipo de objeto que queramos que nos devuelva y al final lo que obtendremos será una lista genérica de nuestro tipo anónimo que podremos enlazar directamente con cualquier _DataGrid_.

Comenzamos definiendo un método genérico que acepte una cadena y un tipo por referencia y devuelva un _IEnumerable_ del tipo que se le pasa. En el parámetro cadena pasaremos la consulta EntitySQL que ejecutaremos contra el modelo conceptual y en el parámetro tipo pasaremos un tipo anónimo. La implementación inicial de este método queda de la siguiente forma:

```cs
public IEnumerable<T> Query<T>(string queryString, T cls) where T : class { var results = new List<T>();

    using (var connection = new EntityConnection(&quot;name=AdventureWorksLT2008Entities&quot;))
    {
        connection.Open();
    
        using (var command = new EntityCommand(queryString, connection))
        {
            var reader = command.ExecuteReader(CommandBehavior.SequentialAccess);
    
            while (reader.Read())
            {
                ...
            }
        }
    
        return results as IEnumerable&lt;T&gt;();
    } }
```

Vemos que en este código estamos definiendo una lista del tipo que hemos pasado, que será la que devolvemos como _IEnumerable_. Pero la diferencia fundamental entre trabajar con EntityClient en lugar de otras tecnologías (LINQ to Entities o Entity SQL), es que aquí tenemos que encargarnos nosotros del manejo de la conexión. Otra particularidad es que el objeto EntityCommand devueve la información como tipos primitivos en lugar de objetos de entidades y además como el objeto _EntityDataReader_ devuelve una fila cada vez, tenemos que utilizar el método _Read_ para poder tratar la siguiente fila en el _EntityDataReader_. Se trabaja de forma idéntica que con otros proveedores de datos ADO.NET.

Ahora lo que falta es el código para leer y procesar todas las filas. Pero antes de esto necesitaremos una cosa más, necesitamos conocer el nombre de las propiedades del tipo anónimo, para esto utilizamos una consulta LINQ que nos devuelve una lista genérica con el nombre de las propiedades que utilizaremos en el bucle.

```cs
var properties = from j in template.GetType().GetProperties().ToList()
                      select j.Name;
```

Y ahora sí que podemos implementar la lectura del _EntityDataReader_.

```cs
var values = new List<object>();

for (int i = 0; i < reader.FieldCount; i++)
{
    if (properties.Contains(reader.GetName(i)))
    {
        object value = reader[i];
        Type convert = reader.GetFieldType(i);
        values.Add(value is System.DBNull ? null : Convert.ChangeType(value, convert));
    }
}

T record = Activator.CreateInstance(cls.GetType(), values.ToArray()) as T;

results.Add(record);
```

Iteramos entre todos los campos devueltos del _EntityDataReader_, comprobamos si el tipo anónimo tiene una propiedad con el mismo nombre del campo y en caso afirmativo, añadimos el valor a la lista de objetos, previa conversión al tipo del campo. Una vez tenemos todos los valores en la lista _values_, creamos una instancia del tipo anónimo que recibe el método. Para crear la instancia utilizamos el método _CreateInstance_ de la clase _Activator_, al que le tenemos que pasar además del tipo a crear (nuestro tipo anónimo), el array de valores (la lista _values_). Este método lo que hace es llamar al constructor del tipo anónino que, por suerte para nosotros, tiene el mismo número de parámetros que elementos del array. Y esto lo repetimos para todas las filas del EntityDataReader.

La implementación del método completo es la siguiente:

```cs
public IEnumerable<T> Query<T>(string queryString, T cls) where T : class
{
    var results = new List<T>();

    using (var connection = new EntityConnection("name=AdventureWorksLT2008Entities"))
    {
        connection.Open();

        using (var command = new EntityCommand(queryString, connection))
        {
            var reader = command.ExecuteReader(CommandBehavior.SequentialAccess);

            var properties = from j in cls.GetType().GetProperties().ToList()
                             select j.Name;

            while (reader.Read())
            {
                var values = new List<object>();

                for (int i = 0; i < reader.FieldCount; i++)
                {
                    if (properties.Contains(reader.GetName(i)))
                    {
                        object value = reader\[i\];
                        Type convert = reader.GetFieldType(i);
                        values.Add(value is System.DBNull ? null : Convert.ChangeType(value, convert));
                    }
                }

                T record = Activator.CreateInstance(cls.GetType(), values.ToArray()) as T;

                results.Add(record);
            }
        }

        return results as IEnumerable<T>;
    }
}
```

y una forma de utilizar el método es esta:

```cs
this.dataGrid1.ItemsSource = this.Query("SELECT VALUE p FROM AdventureWorksLT2008Entities.Products as p", new
  {
      Name = (string)"",
      ProductNumber = (string)"",
      ListPrice = (decimal)1,
      Size = (string)"",
      SellEndDate = DateTime.Now
  });
```

En este caso estamos consultando la entidad completa, pero el tipo que queremos que nos devuelva el método solo tendrá cinco propiedades, aunque podríamos modificar esta consulta para que solo se seleccionase los campos que queremos que nos devuelva. Algo parecido a esto: «SELECT p.Name, p.ProductNumber, p.ListPrice, p.Size, p.SellEndDate FROM AdventureWorksLT2008Entities.Products as p».

Además, para utilizar este método tenemos que tener en cuenta una serie de requisitos. El primero es que no estamos procesando parámetros, así que la consulta EntitySQL no puede hacer uso de ellos. Esto lo podríamos solucionar agregando un nuevo parámetro en el método donde pasar, a su vez, los parámetros de la consulta. Y el segundo requerimiento es que el orden de las propiedades del tipo debe ser igual al orden de los campos de la consulta EntitySQL. Quizás en una nueva actualización del la solución de ejemplo mejore estos dos inconvenientes, pero creo que para fines didácticos queda más claro la implementación del método tal y como está, sin más complicaciones.

**Descarga código fuente:** 
[WPF-BindingEntityDataReader.zip](/files/WPF-BindingEntityDataReader.zip)

