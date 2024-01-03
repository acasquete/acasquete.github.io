---
title: Sincronizar bases de datos IndexedDB y CouchDB con PouchDB
tags: [windows_store]
reviewed: true
---
Cuando desarrollamos una aplicación para la **Windows Store** y queremos ofrecer navegación offline tenemos que hacer uso de algún sistema para guardar información en local. Podemos utilizar como almacén de información el sistema de archivos, el _local storage_ o podemos recurrir a sistemas de terceros como [SQLite](http://www.sqlite.org/). Pero si estamos utilizando JavaScript, podemos utilizar además el motor de **IndexedDB** que nos permite almacenar pares clave/valor en una base de datos local.

El uso de **IndexedDB** es la opción recomendada cuando tenemos que manipular gran cantidad de información estructurada, ya que el uso de otros sistemas implicaría la necesidad de implementar nuestros propios mecanismos de búsqueda, ordenación, etc. Sin embargo, la API de **IndexedDB** tiene un gran pero y es que no nos proporciona una forma para poder sincronizar los datos con un servidor externo.

En esta entrada vamos a ver cómo sincronizar una base de datos **IndexedDB** con un servidor **CouchDB** haciendo uso de la librería JavaScript [PouchDB](http://pouchdb.com/). Trataremos en futuras entradas el cómo realizar la sincronización de datos con otros tipos de bases de datos.

**PouchDB** es una implementación de [Apache CouchDB](http://couchdb.apache.org/) que funciona de forma nativa en cualquier navegador utilizando **IndexedDB** como sistema de almacenamiento. Tiene el mismo modelo de datos, la misma API y la misma resolución de conflictos que CouchDB. Pero lo más importante es que permite sincronizar los datos con una base de datos **CouchDB** externa cuando la aplicación está online.

Para mostrar el uso de **PouchDB** vamos crear una aplicación con una grid en la que podremos editar una la información de una lista de clientes y que podremos sincronizar entre varios dispositivos.

Partimos de un proyecto Windows Store app vacío al que le añadimos las librerías de [Knockout](http://knockoutjs.com/) y [PouchDB](http://pouchdb.com/). La referencia a Knockout la podemos añadir mediante Nuget, pero la librería de PouchDB debemos agregarla manualmente. El uso de la librería de Knockout es para simplificar la vista mediante bindings, pero podríamos prescindir de ella o utilizar cualquier otra.

Guardando datos en local
------------------------

Para comenzar a utilizar **PouchDB** tenemos que crear la base de datos. Para esto, simplemente tenemos que crear una instancia de **PouchDB** indicando el nombre de la base de datos.

```js
var db = new PouchDB(‘customers’);
```

Una vez creada podemos comenzar a añadir documentos a la base de datos.

```js
self.addCustomer = function() {
  var customer = { 
    \_id: new Date().toISOString(), 
    firstname: "", 
    lastname: "", 
    email: "", 
    telephone: "", 
    city: "" 
  };
  
  db.put(customer, function callback(err, result) {
    if (!err) {
      console.log('Customer added.');
    } else {
      console.log(err);
    }
  });
};
````

Es importante destacar que cada documento que queramos agregar a la base de datos necesita un campo _\_id_ único. En el ejemplo estamos utilizando la fecha para poder utilizarlo para ordenar los elementos, pero es posible utilizar el método **post** en lugar de **put** para que PouchDb genere un identificador aleatorio por nosotros.

La función _callback_ se llama cuando se ha completado la operación de escritura. Si se completa con éxito, el argumento _err_ contendrá un objeto detallando el error o en caso contrario, el argumento _result_ contendrá el resultado.

Para realizar la actualización de datos utilizaremos de la misma forma el método _put_. Sin embargo, tenemos que tener en cuenta que el objeto customer debe tener los campos _\_id_ y _\_rev_.

```js
self.updateCustomer = function(customer) {
  db.put(customer, function callback(err, result) {
    if (!err) {
      console.log('Customer updated.');
    } else {
      console.log(err);
    }
  });
};
````

Si el documento no contiene el campo _\_rev_ o no coincide, obtendremos el siguiente objeto de error:

```json
{ status: 409, error: "conflict", reason: "Document update conflict"} 
````

De forma similar podemos eliminar un documento de la base de datos. En este caso tenemos que llamar al método **remove** pasando un objeto con los campos _\_id_ y _\_rev_ informados. En nuestro ejemplo, pasamos directamente todo el objeto customer aunque no es necesario, podríamos crear en su lugar un objeto que tuviese solo estos dos campos.

```js
self.removeCustomer = function(customer) {
  db.remove(customer);
};
```

Ahora ya tenemos las tres operaciones básicas, pero no estamos actualizando el observableArray de Knockout para que se actualice la información de la vista. Lo que vamos a hacer para conseguirlo, en lugar de actualizar la colección en cada operación, es suscribirnos a cambios en la base de datos y cada vez que se produzca uno actualizar toda la grid.

Para suscribirnos a cambios utilizamos el método **changes**. Este método acepta una serie de opciones con las que podemos indicar, por ejemplo, el método _callback_ que se llamará después de cada actualización (**onChange**). Con la opción **continuous** indicamos que nos queremos suscribir a los cambios.

```js
db.changes({
  continuous: true,
  onChange: updateVM
});
```

En el método **updateVM** vamos a borrar la colección de customers y añadir todos los documentos de la base de datos. Aunque esto no es lo óptimo, nos servirá para refrescar las actualizaciones de documentos que nos lleguen durante la sincronización sin mayor complicación.

```js
function updateVM() {
  db.allDocs({include\_docs: true}, function(err, doc) {
    viewModel.customers.removeAll();
    doc.rows.forEach(function(row) {
      viewModel.customers.push(row.doc);
    });
  });
}
```

Para consultar todos los documentos de la base de datos utilizamos el método **allDocs**, indicando con la opción **include\_docs** que queremos que se incluyan el contenido de los documentos en cada fila.

El servidor CouchDB
---    

Ahora que ya tenemos funcionando los datos en local, es el momento de sincronizarlos con un servidor **CouchDB** externo. Para el entorno de desarrollo podemos instalar una instancia de CouchDB en local o podemos optar por un proveedor externo como [IrisCouch](http://www.iriscouch.com/) o [Cloudant](http://www.cloudant.com/).

Sea cual sea la opción que escojamos, antes de utilizar **CouchDB** es necesiario que activemos CORS añadiendo la siguiente configuración a CouchDB.

```bash
httpd/enable\_cors = true
cors/origins = \*
cors/credentials = true
cors/methods = GET, PUT, POST, HEAD, DELETE
cors/headers = accept, authorization, content-type, origin
````

La configuración de CouchDB la podemos establecer manualmente mediante la página de configuración ([http://idlebit.iriscouch.com/\_utils/config.html](http://idlebit.iriscouch.com/_utils/config.html)) o realizando las siguientes peticiones mediante Curl o PowerShell. Si tenemos instalado [Git for Windows](http://git-scm.com/downloads) podemos utilizar Curl desde la consola Bash y actualizar la configuración con los siguientes comandos.

```bash
$ export HOST=http://username:password@idlebit.iriscouch.com
$ curl -X PUT $HOST/\_config/httpd/enable\_cors -d '"true"'
$ curl -X PUT $HOST/\_config/cors/origins -d '"\*"'
$ curl -X PUT $HOST/\_config/cors/credentials -d '"true"'
$ curl -X PUT $HOST/\_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'
$ curl -X PUT $HOST/\_config/cors/headers -d '"accept, authorization, content-type, origin"'
````

Una vez tenemos configurado correctamente el servidor **CouchDB**, solo hay que crear la base de datos y podremos sincronizar los datos mediante **PouchDB** de una forma realmente sencilla.

Mediante los métodos **replicate.to** y **replicate.from** podemos indicar en que dirección queremos replicar los datos. Si queremos sincronizar datos en las dos direcciones, tendremos que llamar a los dos métodos.

```js
self.syncDb = function () {
  var remoteCouchDB = 'http://idlebit.iriscouch.com/customers';
  
  db.replicate.to(remoteCouchDB, options);
  db.replicate.from(remoteCouchDB, options);
}
```

En este caso indicamos que replique los datos hacia y desde nuestro servidor externo en **IrisCouch**. Además, estamos indicando el método *callback* cuando haya finalizado la sincronización. También podemos utilizar la opción **continuos** para indicar que se suscriba a cambios mediante un longpoll, pero en este caso lo he dejado para que la sincronización se tenga que hacer explícitamente.

Código fuente
---

El ejemplo en jsFiddle para hacer las pruebas de sincronización desde el mismo dispositivo y no tener que añadir los documentos en CouchDB a mano.

[jsFiddle - Customer Grid Sample with CouchDB](http://jsfiddle.net/acasquete/zCd7h/embedded/result/)

Resumen
---

En este artículo hemos visto como utilizando \*\*PouchDB\*\* podemos guardar la información en local de la misma forma que utilizamos \*\*CouchDB\*\* y además podemos sincronizar estos datos con un servidor externo muy fácilmente. Para terminar, quiero reiterar que si queremos guardar poca información podemos y debemos utilizar otros mecanismos. Desde las aplicaciones de la Windows Store podemos sincronizar configuración y archivos entre dispositivos mediante el almacén de datos en itinerancia (\*Roaming\*). 

En próximas entradas veremos que estrategias podemos seguir para sincronizar los datos locales con otros servidores de base de datos externos.


Recursos online
---

[PouchDB - Getting Started Guide](http://pouchdb.com/getting-started.html)  
[Storing and retrieving state efficiently](http://msdn.microsoft.com/en-us/library/windows/apps/hh781225.aspx)  
[Apache CouchDB Documentation](http://docs.couchdb.org/en/latest/)  
