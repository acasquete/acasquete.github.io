---
title: Concatenar datos de una columna en una fila
tags: []
---
Me he topado en varias ocasiones con la necesidad de crear una vista en la que un campo contiene concatenados el valor de varios registros de otra tabla. Casi siempre he acabado recurriendo a _Google_ para recordar cómo hacerlo, porque, por alguna razón que desconozco, esta información no queda registrada en mi hipocampo.

En este artículo vamos a ver cómo conseguirlo con un ejemplo muy sencillo. Partimos de 3 tablas: _autor_, _libro_ y _libro\_autor_, que contienen, como podemos suponer, una relación de autores, libros y libro-autor. La estructura de estas tres tablas es la que se muestra en el siguiente diagrama.

Ahora supongamos que queremos mostrar el listado de todos los libros y que en una columna queremos que aparezcan concatenados el nombre de todos los autores del libro. El resultado que queremos obtener es el siguiente:

id\_libro titulo autores ———– ————– —————– 1 libro1 autor1, autor2 2 libro2 autor2, autor1 3 libro3 autor3 </pre>

La forma más sencilla de obtener este resultado es creando una función que devuelva el nombre de todos los autores, pasando como parámetro el identificador del libro. Esto lo podemos hacer fácilmente haciendo uso de las funciones [ISNULL](http://msdn.microsoft.com/es-es/library/ms184325.aspx) o [COALESCE](http://msdn.microsoft.com/es-es/library/ms190349(SQL.90).aspx). En este ejemplo, lo conseguimos mediante la función COALESCE.

CREATE FUNCTION dbo.DevuelveActores ( @id\_libro int )
RETURNS VARCHAR(40)
AS
BEGIN
   DECLARE @autores VARCHAR(40)

   SELECT @autores = COALESCE(@autores + ', ' + nombre, nombre)
   FROM libro\_autor la
   LEFT JOIN autor a ON la.id\_autor = a.id\_autor
   WHERE id\_libro=@id\_libro

   RETURN @autores
END

Ahora podemos, mediante la siguiente consulta, obtener el resultado deseado:

SELECT id\_libro, titulo, autores = dbo.DevuelveActores(id\_libro)
FROM libro

Otra opción es hacer uso del [modo PATH](http://msdn.microsoft.com/es-es/library/bb510462.aspx) de la cláusula [FOR XML](http://msdn.microsoft.com/es-es/library/ms178107.aspx). Este modo permite definir, mediante los nombres o alias de la columnas, la manera cómo se asignan los valores en el XML, así como el nombre del elemento, pudiendo sobrescribir el valor _<row>_ predeterminado. Por ejemplo, la siguiente consulta devuelve una cadena con todos los autores concatenados.

SELECT nombre as \[data()\] FROM autor FOR XML PATH ('')

Haciendo uso de esta característica, es posible montar una consulta con una subconsulta que devuelva todos los autores de un libro y reemplazar el espacio entre autores por el separador que queramos. Con la siguiente consulta obtenemos exactamente el mismo resultado que hemos conseguido antes con la función.

SELECT id\_libro, titulo, autores = CAST( REPLACE( (
   SELECT nombre as \[data()\]
   FROM libro\_autor la
   LEFT JOIN autor a ON la.id\_autor = a.id\_autor
   WHERE id\_libro = l.id\_libro
   FOR XML PATH ('')
   ), ' ', ', ') AS NVARCHAR(40) )
FROM libro l



Dejo un enlace para descargar el \*script\* que contiene las consultas de los dos métodos explicados y la creación de todos los elementos de base de datos (tablas y funciones) que he utilizado en este ejemplo.

