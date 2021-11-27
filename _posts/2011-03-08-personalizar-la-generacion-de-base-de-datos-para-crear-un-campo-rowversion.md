---
title: Personalizar la generación de base de datos para crear un campo rowversion
tags: []
---
_Model-First_ es como denominamos a uno de los enfoques que tenemos disponibles con Visual Studio 2010 y Entity Framework 4 para diseñar nuestro **Entity Data Model** y del que ya he hablado en alguna ocasión. Este enfoque nos permite crear nuestro EDM desde un modelo vacío y después, a partir de este, generar la base de datos, las asignaciones y las clases. En esta entrada nos vamos a centrar en conocer cómo el asistente genera el script de base de datos y de qué forma podemos modificarlo para adaptarlo a nuestras necesidades o a las reglas que tengamos impuestas.

Uno de los problemas con el que nos podemos encontrar al diseñar nuestro modelo desde cero es que no tenemos forma de definir un campo como [rowversion](http://msdn.microsoft.com/es-es/library/ms182776.aspx) o [timestamp](http://msdn.microsoft.com/es-es/library/ms182776(v=sql.90).aspx), teniendo que modificar manualmente el script generado. Así que lo que vamos a hacer para salvar este inconveniente es modificar la plantilla T4 que el asistente utiliza para generar los scripts, modificando el tipo de dato generado según el nombre de la propiedad. Veamos cómo…

El asistente de generación de base de datos utiliza flujos de trabajo (_workflows_) y plantillas de texto para generar el código DDL (_Data Description Language_). El nombre del fichero del _workflow_ lo podemos ver la propiedad del modelo conceptual **Database Generation Workflow** y el nombre del fichero de la plantilla de texto en la propiedad **DDL Generation Template**. Los valores predeterminados de estas propiedades son «TablePerTypeStrategy.xaml» y «SSDLToSQL10.tt», dos ficheros que se encuentran en el directorio “%programfiles(x86)%Microsoft Visual Studio 10.0Common7IDEExtensionsMicrosoftEntity Framework ToolsDBGen”. Y aunque podemos modificar cualquiera de los dos ficheros para cambiar el comportamiento, es recomendable crear una copia del fichero y realizar las modificaciones que queramos sobre esa copia. Para el propósito que buscamos, que es cambiar el tipo de datos de un campo según su nombre, solo tendremos que adaptar la plantilla de texto.

Comenzamos creando una copia del fichero **SSDLToSQL10.tt** en el mismo directorio y le cambiamos el nombre, por ejemplo, a **SSDLToSQL10-RowVersion.tt**. Una vez tenemos la copia editamos el fichero con Visual Studio y modificamos el contenido de la línea 165 según aparece en el siguiente código:

* * *

– Creating all tables – ————————————————–

<# foreach (EntitySet entitySet in Store.GetAllEntitySets()) { string schemaName = Id(entitySet.GetSchemaName()); string tableName = Id(entitySet.GetTableName()); #> – Creating table ‘<#=tableName#>’ CREATE TABLE <# if (!IsSQLCE) {#>\[<#=schemaName#>\].<#}#>\[<#=tableName#>\] ( <# for (int p = 0; p < entitySet.ElementType.Properties.Count; p++) { EdmProperty prop = entitySet.ElementType.Properties\[p\]; #> \[<#=Id(prop.Name)#>\] <#if (prop.Name==”RowVersion”) { #>rowversion<# } else { #><#=prop.ToStoreType()#><# } #> <#=WriteIdentity(prop, targetVersion)#> <#=WriteNullable(prop.Nullable)#><#=(p < entitySet.ElementType.Properties.Count - 1) ? “,” : “”#> <# } #> ); GO

<# } #> </pre>

Lo que hemos hecho es añadir una condición para que se cambie el tipo de datos generado para las propiedades que tengan el nombre **RowVersion**. Un detalle que quiero destacar es que he utilizado el tipo de datos _rowversion_ ya que el tipo _timestamp_ está obsoleto y posiblemente desaparezca en alguna próxima versión de SQL Server, así que es recomendable utilizar _rowversion_ siempre que sea posible.

Para probar esta plantilla simplemente tenemos que añadir una entidad en nuestro modelo conceptual con una propiedad con el nombre **RowVersion**. Esta propiedad, además, debe tener los valores siguientes en estos atributos:

**Type** - Binary **Nullable** - False **StoreGeneratedPattern** - Computed

Ahora solo queda seleccionar la nueva plantilla que acabamos de crear en la propiedad **DDL Generation Template** del EDM y ejecutar el asistente de generación de base de datos. El resultado debería contener un código similar a este:

\-- Creating table 'MiEntidad'
CREATE TABLE \[dbo\].\[MiEntidad\] (
  \[Id\] int IDENTITY(1,1) NOT NULL,
  \[RowVersion\] rowversion NOT NULL
)



**Descarga Plantilla T4:**
[SSDLToSQL10-RowVersion.zip](http://sdrv.ms/1aiQMmw)

**Enlaces relacionados**
[MSDN: rowversion (Transact-SQL)](http://msdn.microsoft.com/es-es/library/ms182776.aspx) 
[Cómo: Personalizar la generación de bases de datos (Asistente para generar base de datos)](http://msdn.microsoft.com/es-es/library/dd560887.aspx) 

