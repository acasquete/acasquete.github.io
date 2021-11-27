---
title: Crear trigger en varias bases de datos
tags: []
---
Hace un par de días estuve enfrascado en la creación de un _trigger_ para auditar una tabla. Una vez tuve el _trigger_ preparado, necesitábamos replicarlo en todas las bases de datos —más de trescientas— del servidor de producción. La solución idónea parecía hacer todo este proceso mediante un _script_ Transact-SQL, pero me encontré con varios problemas que no esperaba. El primero de ellos fue en la creación del propio _trigger_, aunque este punto lo dejaré para explicarlo otro día. Lo que realmente me llevó más tiempo solucionar fue el poder crear el _trigger_ en distintas bases de datos, el problema fundamental que encontré fue que no podía hacer referencia a las bases de datos dinámicamente.

La primera prueba que hice, y creo que la que todo el mundo piensa la primera vez, fue utilizar el comando USE. En el código siguiente he omitido el código completo del _trigger_ por otro que no realiza ningúna acción ya que no aporta nada en el ejemplo.

DECLARE @dbname nvarchar(255), @script nvarchar(2000)

SET @dbname=’basededatos’ SET @script = ‘CREATE TRIGGER \[dbo\].\[MiTrigger\_Update\] ON \[dbo\].\[Tabla\] FOR UPDATE AS SET NOCOUNT ON;’ EXEC (‘USE ‘ + @dbname + ‘ ‘ + @script) </pre> En principio parece una buena solución, pero no funciona. Este _script_ devuelve el error «’CREATE TRIGGER’ debe ser la primera instrucción en un lote de consultas». Probé, después, a poner un GO después del USE e incluso a poner un salto de línea. Pero nada, sólo obtenía un error tras otro… Hasta que encontré (en no recuerdo que foro) la solución: utilizar el procedimiento almacenado _sp\_executesql_ indicando en que base de datos se tiene que ejecutar.

EXEC (@dbname + '..sp\_executesql N'''+ @script + '''')

Este que pongo a continuación es el _script_ completo que utilicé para crear el _trigger_ en todas las bases de datos del servidor. En este caso, he estado refiriéndome siempre a _triggers_, pero este mismo _script_ se puede utilizar para cualquier tipo de objeto de la base de datos (vistas, procedimientos, etc.).

DECLARE @sql nvarchar(2000), @dbname nvarchar(256)
DECLARE cur CURSOR
FOR 
SELECT name FROM master..sysdatabases
OPEN cur
FETCH next FROM cur INTO @dbname
WHILE @@fetch\_status = 0
BEGIN
SET @sql = 'CREATE TRIGGER \[...\]' -- Código del trigger omitido 

BEGIN TRY    
    EXEC (@dbname + '..sp\_executesql N'''+ @sql + '''')
    PRINT 'Trigger creado en BD ' + @dbname
END TRY
BEGIN CATCH
    PRINT 'Error al crear el trigger en BD ' + @dbname + '::' + ERROR\_MESSAGE()
END CATCH
FETCH next FROM cur INTO @dbname
END
CLOSE cur
DEALLOCATE cur

