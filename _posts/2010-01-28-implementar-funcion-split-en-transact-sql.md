---
title: Implementar la función split en T-SQL
tags: [programming]
reviewed: true
---
En la anterior entrada vimos cómo [concatenar datos de una columna en una fila](/concatenar-datos-de-una-columna-en-una-fila/). En esta entrada haremos justo lo contrario, dividir una cadena de texto en varios registros a partir de un carácter delimitador. Es decir, vamos a implementar en Transact-SQL la función _split_ de la que disponen la mayoría de los lenguajes de programación.

Si buscamos en [Google](http://www.google.es/search?q=split+function+sql), encontraremos multitud de variantes de esta función. Sin embargo, la peculiaridad de este ejemplo es que no utiliza bucles y por lo tanto es más eficiente. Para conseguir esto, tenemos que utilizar una tabla auxiliar, concretamente la tabla _spt\_values_ de la base de datos _master_. Esta tabla contiene, entre otras cosas, 2048 registros con los números consecutivos del 0 al 2047 que son de gran utilidad para nuestro propósito.

El siguiente código muestra cómo crear la función con valor de tabla para que admite tres parámetros: la cadena que queremos separar, el carácter delimitador y el número de resultados que queremos que nos devuelva. Este último parámetro es opcional, así que si le pasamos el valor NULL como tercer parámetro, la función nos devolverá todos los registros.

```sql
CREATE FUNCTION StringSplit ( @String AS VARCHAR(2048), @Separator AS CHAR(1), @Count AS INT ) RETURNS TABLE AS RETURN ( 
  SELECT TOP (ISNULL(@Count, 2147483647)) SUBSTRING( @String, Number, CHARINDEX(@Separator, @String + @Separator, Number) - Number ) AS \[Substring\] 
  FROM master..spt\_values 
  WHERE \[Type\]=’P’ AND Number BETWEEN 1 AND LEN(@String) + 1 AND SUBSTRING(@Separator + @String, Number, 1) = @Separator )
```

La forma de utilizar esta función es la siguiente:

```sql
SELECT Substring FROM StringSplit('Lunes,Martes,Miércoles,Jueves,Viernes,Sábado,Domingo', ',', null);
```

Con la que obtendremos el siguiente resultado:

```
Substring
------------------------------------
Lunes
Martes
Miércoles
Jueves
Viernes
Sábado
Domingo

(7 filas afectadas)
```

Por último, sólo queda comentar que la limitación de esta función está en la propia tabla auxiliar (_master..spt\_values_), ya que al contener sólo 2048 números consecutivos no puede tratar cadenas de texto más largas. Si tuviesemos que tratar tamaños superiores, deberíamos crear una tabla auxiliar con más números consecutivos.

**Actualización (20/06/2010):** Me he topado con otro [artículo](http://www.kodyaz.com/articles/t-sql-convert-split-delimeted-string-as-rows-using-xml.aspx "Split String using XML - How to Convert or Split a Delimited String Values to Rows using T-SQL XML Commands") en el que se utilizan los métodos XML para crear la función _split_. La principal ventaja respecto al método que expliqué en el post es que no tiene la limitación de los 2048 carácteres y puede tratar cadenas de cualquier longitud. Aquí dejo el código que modifica la función _StringSplit_.

```sql
ALTER FUNCTION StringSplit
(
  @String NVARCHAR(MAX),
  @Separator CHAR(1),
  @Count AS INT
) RETURNS @t TABLE (\[Substring\] NVARCHAR(max))
AS
  BEGIN
  DECLARE @xml xml = N'\*' + replace(@String,@Separator,'**') + '*'

  INSERT INTO @t(\[Substring\])
  SELECT TOP (ISNULL(@Count, 2147483647))
  r.value('.','varchar(5)') as Value
  FROM @xml.nodes('//root/i') as records(r)

  RETURN
END
```

