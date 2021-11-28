---
title: Datetime sin hora
tags: []
---
Supongamos, puestos a suponer, que tenemos una tabla de bonificaciones con dos campos fecha que nos indican la fecha de vigencia de cada bonificación y queremos ejecutar una consulta que nos devuelva todas las bonificaciones que están vigentes en la fecha actual. La forma de proceder sería mediante la siguiente consulta:

SELECT BonificationID FROM Bonification WHERE (GETDATE() BETWEEN date\_start AND date\_end) </pre>

Esta consulta funciona correctamente excepto si estamos en el último día de vigencia. Supongamos que en la tabla tenemos una bonificación que finaliza el 17/11/2008, al ser un campo _datetime_ se guarda 17/11/2008 00:00:00. Si consultamos la fecha actual mediante la función _getdate_, también va a devolver la hora, y suponiendo que hoy es dia 17 a las 23 de la noche, la consulta no devolvería esta bonificación porque es menor que la fecha actual (siempre teniendo en cuenta la hora).

Lo que debemos hacer es realizar la consulta solamente con la fecha. Para realizar esto convertimos la fecha a un número flotante y cogemos la parte entera, luego solo tenemos que pasar el resultado a tipo fecha. La consulta anterior queda de esta forma:

SELECT BonificationID
FROM Bonification
WHERE (CAST(FLOOR(CAST(GETDATE() AS FLOAT)) AS Datetime) BETWEEN date\_start AND date\_end)

