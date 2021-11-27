---
title: Reordenar registros de una tabla mediante un campo de posición
tags: []
---
Es una práctica muy habitual, por no decir imprescindible, hacer uso en una tabla de un campo que indique la posición o el orden en que deben aparecer los registros. Igual de habitual es el dar soporte para que se puedan insertar nuevos registros en una posición ya ocupada, teniendo que reasignar automáticamente el valor de la posición en todos los registros a partir del recién insertado.

En esta entrada voy a mostrar cómo realizar esta reasignación utilizando una tabla con tres campos (_id_, _position_, _value_) y cuatro registros. Hay que tener en cuenta que para poder realizar la reordenación correctamente necesitamos que en la tabla exista un campo que nos indique también el orden de inserción de los registros. Para este fin nos podemos valer de un campo auto numérico (_IDENTITY_), de un campo fecha o de un campo _[timestamp](http://msdn.microsoft.com/es-es/library/ms182776(SQL.90).aspx)_. En el ejemplo que voy a utilizar haré uso de un sencillo campo auto numérico.

Supongamos que el contenido inicial de la tabla ‘element’ es el siguiente:

Si insertamos un nuevo registro que queremos que aparezca en la posición 2 la tabla mostrará el siguiente aspecto:

Es esta situación podríamos mostrar los artículos en el orden correcto mediante esta simple consulta:

SELECT id, position, value FROM element ORDER BY position, id DESC</pre> En la que estamos ordenando el resultado por el campo _position_ de forma ascendente y por el campo _id_ de forma descendente. Es decir, mostraríamos los registros ordenados por la posición y en caso de coincidencia se ordenaría del más reciente al más antiguo.

Pero, ¿qué sucede si tenemos que añadir un nuevo artículo en la posición 3? Pues sencillamente no podemos, si le asignásemos la posición 3 nos aparecería en la posición 4, después del elemento «Dos». Y si le asignásemos la posición 2, nos aparecería una posición antes. Para poder llevar a cabo nuestro propósito, necesitamos tener el valor del campo _position_ ordenado de forma correlativa. Una forma de hacerlo es mediante la siguiente consulta:

UPDATE element
   SET position = SubQuery.newposition
   FROM ( SELECT Id, ROW\_NUMBER() OVER (ORDER BY position, id DESC) AS newposition FROM element ) SubQuery
   INNER JOIN element 
   ON SubQuery.Id = element.Id

Como vemos en la consulta, actualizamos el valor del campo _position_ a partir de una subconsulta en la que obtenemos el nuevo valor mediante la función [ROW\_NUMBER](http://msdn.microsoft.com/es-es/library/ms186734.aspx).

Esta consulta se puede optimizar actualizando sólo las filas a partir de la posición del registro insertado. Por ejemplo, si insertamos un registro en la posición 3, sólo tenemos que reorganizar los registros a partir de esa posición y no todos los de la tabla. La consulta a ejecutar en este caso sería la siguiente:

UPDATE element
   SET position = SubQuery.newposition
   FROM ( SELECT Id, ROW\_NUMBER() OVER (ORDER BY position, id DESC) AS newposition FROM element ) SubQuery
   INNER JOIN element ON SubQuery.Id = element.Id
   WHERE Orden>=4

Para terminar esta entrada, sólo queda comentar que esta misma operación se puede realizar mediante una consulta más sencilla, o al menos, más fácil de leer. Para evitar tener que recurrir al uso del INNER JOIN, podemos utilizar la cláusula [WITH](http://msdn.microsoft.com/es-es/library/ms175972(SQL.90).aspx) con la que podemos definir un conjunto de resultados temporal, conocido como [expresión de tabla común (CTE)](http://technet.microsoft.com/es-es/library/ms175972.aspx). Aquí os dejo el código T-SQL final:

WITH OrderedOrders AS (
SELECT position, ROW\_NUMBER() OVER (ORDER BY position, id DESC) AS 'newposition' FROM element
)
UPDATE OrderedOrders SET position=newposition WHERE position>=2

