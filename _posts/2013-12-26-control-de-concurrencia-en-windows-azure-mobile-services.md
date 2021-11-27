---
title: Control de concurrencia en Windows Azure Mobile Services
tags: [windows_store, azure]
---
Desde hace unas semanas tenemos de serie en **Windows Azure Mobile Services** un mecanismo de detección de conflictos basado en un control optimista de concurrencia. Este mecanismo nos permite detectar conflictos cuando se realizan cambios sobre la misma entidad al mismo tiempo. Sin este control, el último cambio que se hace siempre sobrescribe cualquier cambio anterior.

En esta entrada vamos a ver cómo funciona el control de concurrencia y cómo podemos detectar los conflictos tanto en una aplicación cliente como en el servidor y qué acciones podemos realizar en caso de conflicto. Para mostrar los distintos ejemplos haré uso de una aplicación para la Windows Store que permite realizar el mantenimiento básico de una entidad.

Nuevas propiedades de sistema
-----------------------------

El control de concurrencia optimista permite verificar, al realizar una transacción, que ninguna otra transacción haya modificado los datos. Si se han realizado modificaciones, la transacción es rechazada. **Mobile Services** hace el seguimiento de cambios de cada fila utilizando la [propiedad de sistema](http://msdn.microsoft.com/en-us/library/windowsazure/jj193162.aspx) **\_\_version**, que contiene un _timestamp_ que se actualiza cada vez que se realiza un cambio en la fila. Este campo, junto con **\_\_createdAt** y **\_\_updateAt**, son los nuevos campos que se agregan cuando creamos una nueva tabla.

El funcionamiento es bien sencillo, cuando realizamos una actualización y el valor del campo **\_\_version** no coincide con el valor de servidor, Mobile Services lanza una excepción del tipo **MobileServicePreconditionFailedException** que podemos capturar para poder decidir qué acción realizar.

Para poder aprovecharnos de esta nueva característica es obvio que tenemos que agregar el campo version en nuestra entidad. En el caso de que estemos utilizando tablas tipadas tenemos que añadir directamente el campo **\_\_version** o utilizar el atributo **JsonProperty**.

En nuestro ejemplo, agregamos el nuevo campo en la clase _Person_.

    public class Person
    {
        public String Id { get; set; }
    
        public String Name { get; set; }
    
        public String Phone { get; set; }
    
        public String Comments { get; set; }
    
        [JsonProperty(PropertyName = "__version")]
        public string Version { set; get; }
    }
    </pre>
    
    A partir de la versión 1.1 del SDK podemos utilizar el atributo **Version** del namespace **Miscrosoft.WindowsAzure.MobileServices**. Esto significa que si agregamos la referencia a través de la opción **Agregar referencia a servicio** de Visual Studio no podremos utilizar este atributo, sino que tenemos que añadir manualmente la referencia al paquete Nuget.
    
    <pre class="brush:csharp">
    public class Person
    {
        public String Id { get; set; }
    
        public String Name { get; set; }
    
        public String Phone { get; set; }
    
        public String Comments { get; set; }
    
        [Version]
        public String Version { get; set; }
    }
    </pre>
    
    
    
    ## Capturando MobileServicePreconditionFailedException
    
    
    
    Al capturar la excepción en cliente podremos decidir qué acción realizar: sobrescribir los datos de servidor, no realizar ningún cambio, o combinar los datos. En el caso de que queramos sobrescribir los datos o combinarlos tendremos que actualizar el valor del campo **__version** con el valor actual del servidor. Esto lo podemos realizar utilizando el valor de la propiedad **Item** de la excepción, que contiene los valores de servidor.
    
    <pre class="brush:csharp">
    private async Task InsertOrUpdatePerson(Person person)
    {
        Exception exception = null;
    
        try
        {
            if (String.IsNullOrEmpty(person.Id))
            {
                await personTable.InsertAsync(person);
            }
            else
            {
                await personTable.UpdateAsync(person);
            }
    
            await new MessageDialog("Person saved succesfully!").ShowAsync();
    
        }
        catch (Exception ex)
        {
            exception = ex;
        }
    
        if (exception != null)
        {
            if (exception is MobileServicePreconditionFailedException)
            {
                var serverRecord = ((MobileServicePreconditionFailedException<Person>)exception).Item;
    
                await ResolveConflict(currentPerson, serverRecord, exception.Message);
            }
            else
            {
                await new MessageDialog(exception.Message).ShowAsync();
            }
        }
    }
    
    private async Task ResolveConflict(Person localItem, Person serverItem, string message)
    {
        MessageDialog msgDialog = new MessageDialog(message, "Resolve conflict");
    
        UICommand localBtn = new UICommand("Commit Local Text");
        UICommand serverBtn = new UICommand("Leave Server Text");
    
        msgDialog.Commands.Add(localBtn);
        msgDialog.Commands.Add(serverBtn);
    
        localBtn.Invoked = async (IUICommand command) =>
        {
            // Get server value
            localItem.Version = serverItem.Version;
    
            await InsertOrUpdatePerson(localItem);
        };
    
        serverBtn.Invoked = async (IUICommand command) =>
        {
            await RefreshPeople();
        };
    
        await msgDialog.ShowAsync();
    }
    </pre>
    
    Naturalmente, es posible que nos encontremos ante un nuevo conflicto de concurrencia cuando guardemos de nuevo la entidad, así que tenemos que comprobar que no se produzca ningún conflicto, por eso estamos llamando al mismo método (*InsertOrUpdatePerson*) para guardar la entidad.
    
    
    
    ## Detectar conflictos en servidor
    
    
    
    También es posible detectar el conflicto desde el lado de servidor y poder llevar a cabo acciones sin tener que devolver un error al cliente y que sea el usuario quien tenga que tomar una decisión. 
    
    Por defecto, la función **execute** devuelve la respuesta automáticamente, pero podemos pasar parámetros opcionales para sobrescribir este comportamiento. Hasta ahora disponíamos de los parámetros **succes** y **error**. Ahora, además, tenemos el parámetro **conflict** que podemos utilizar para pasar una función *callback* que se ejecutará cuando ocurra un conflicto de concurrencia. Esta función nos permitirá modificar los resultados antes de escribir la respuesta.
    
    En nuestro ejemplo vamos poner una condición para que en caso de conflicto, se compruebe si no se han modificado el nombre y el teléfono y en caso afirmativo permitiremos la transacción, y en caso contrario devolveremos un error.
    
    <pre class="brush:js">
    function update(item, user, request) {
        request.execute({ 
            conflict: function (serverRecord) {
                // Only committing changes if name and phone are not changed.
                if (serverRecord.Name === item.Name && serverRecord.Phone === item.Phone) {
                    request.execute();
                }
                else {
                    request.respond(statusCodes.FORBIDDEN, 'The name or the phone have changed.');
                }
            }
        }); 
    }
    </pre>
    
    En este ejemplo si se produce un conflicto y el nombre o el teléfono cambian se devolverá un error 403 que se traduce en una excepción **MobileServiceInvalidOperationException**. Si queremos devolver un error de concurrencia, tenemos que devolver un error 412 *Precondition failed*. En este caso tenemos que utilizar el código de error ya que el objeto [statusCodes](http://msdn.microsoft.com/en-us/library/windowsazure/jj554225.aspx) no contiene ningún miembro para este código de error.
    
    <pre class="brush:js">
    function update(item, user, request) {
        request.execute({ 
            conflict: function (serverRecord) {
                // Only committing changes if name and phone are not changed.
                if (serverRecord.Name === item.Name && serverRecord.Phone === item.Phone) {
                    request.execute();
                }
                else {
                    request.respond(412, 'The name or the phone have changed. Please resolve the conflict.');
                }
            }
        }); 
    }
    </pre>
    
    Sin embargo, esta solución presenta un problema y es que si provocamos un conflicto e intentamos mantener los datos locales, al obtener el valor de la versión de servidor obtendremos un error de referencia nula ya que la excepción no contiene el elemento **Ítem** con los valores de servidor. 
    
    Si echamos un vistazo al código del método **UpdateSync** en la clase **MobileServiceTable** del SDK, vemos que el objeto que se utiliza para establecer el valor de la propiedad Ítem se obtiene directamente del contenido del mensaje. Lo vemos en la llamada al método **ParseContent**.   
    
    <pre class="brush:csharp;highlight: [31]">
    public async Task&lt;Token&gt; UpdateAsync(JObject instance, IDictionary&lt;String, String&gt; parameters)
    {
        JToken jTokens;
        if (instance == null)
        {
            throw new ArgumentNullException("instance");
        }
        MobileServiceInvalidOperationException mobileServiceInvalidOperationException = null;
        Object id = MobileServiceSerializer.GetId(instance, false, false);
        String str = null;
        if (!MobileServiceSerializer.IsIntegerId(id))
        {
            instance = MobileServiceTable.RemoveSystemProperties(instance, out str);
        }
        parameters = MobileServiceTable.AddSystemProperties(this.SystemProperties, parameters);
        try
        {
            JToken jTokens1 = await this.StorageContext.UpdateAsync(this.TableName, id, instance, str, parameters);
            jTokens = jTokens1;
            return jTokens;
        }
        catch (MobileServiceInvalidOperationException mobileServiceInvalidOperationException2)
        {
            MobileServiceInvalidOperationException mobileServiceInvalidOperationException1 = mobileServiceInvalidOperationException2;
            if (mobileServiceInvalidOperationException1.Response != null && mobileServiceInvalidOperationException1.Response.get_StatusCode() != 412)
            {
                throw;
            }
            mobileServiceInvalidOperationException = mobileServiceInvalidOperationException1;
        }
        JToken jTokens2 = await MobileServiceTable.ParseContent(mobileServiceInvalidOperationException.Response);
        throw new MobileServicePreconditionFailedException(mobileServiceInvalidOperationException, jTokens2);
        return jTokens;
    }
    </pre>
    
    Así que si queremos devolver el objeto de servidor, simplemente tenemos que pasar el objeto de servidor (*serverRecord*) como cuerpo del mensaje, en lugar del mensaje de error. El script de la función Update queda así.
    
    <pre class="brush:js">
    function update(item, user, request) {
          request.execute({ 
            conflict: function (serverRecord) {
                // Only committing changes if name and phone are not changed.
                if (serverRecord.Name === item.Name && serverRecord.Phone === item.Phone) {
                    request.execute();
                }
                else {
                    request.respond(412, serverRecord);
                }
            }
        }); 
    }
    </pre>
    
    
    
    ## Probar control de concurrencia con Windows Store apps
    
    
    
    Para probar el control de concurrencia con aplicaciones para la Windows Store, podemos seguir las instrucciones que aparecen en la [documentación de MSDN](http://www.windowsazure.com/en-us/develop/mobile/tutorials/handle-database-write-conflicts-dotnet/), en la que se nos indica cómo crear el paquete e instalarlo en otra máquina. Pero si no disponemos de otra máquina donde hacer el despliegue, una alternativa es hacer una copia de la solución y modificar el **Package Name** del *manifest* de la aplicación. Otra forma de probarlo es modificar directamente el valor de la propiedad **__version**. En el ejemplo que he utilizado para esta entrada he dejado el campo versión visible y editable para que se pueda modificar y simular un conflicto de concurrencia.
    
    
    
    ## Tablas sin propiedades de sistema
    
    
    
    Para finalizar, quiero hacer un último apunte en referencia a las nuevas propiedades de sistema. Ahora todas las tablas que creamos en Mobile Services incluyen los tres nuevos campos, si no vamos a hacer uso el control de concurrencia ni necesitamos los otros dos campos (*createdAt* y *updatedAt*), podemos crear la tabla sin estas columnas utilizando [la línea de comandos](http://www.windowsazure.com/en-us/downloads/#cmd-line-tools).
    
    <pre>
    >azure account download
    
    >azure account import &lt;path-to-settings-file&gt;.publishsettings
    
    >azure mobile table create --integerId &lt;service-name&gt; &lt;table-name&gt;
    

Este comando además de no agregar las columnas **\_\_createdAt**, **\_\_updateAt**, y **\_\_version**, generará la columna **id** de tipo entero en lugar de string.

Descarga código fuente
----------------------

El código de la aplicación lo tenéis disponible para descarga en el siguiente enlace.

[WAMSConflictDetection.zip](https://skydrive.live.com/redir?resid=483C407ED85318FE!19643&authkey=!AM09bckjITvOF20&ithint=file%2c.zip)

Referencias
-----------

[Handling Database Write Conflicts](http://www.windowsazure.com/en-us/develop/mobile/tutorials/handle-database-write-conflicts-dotnet/) 
[Mobile Services Concepts: Create a table](http://msdn.microsoft.com/en-us/library/windowsazure/jj193162.aspx) 
[Accessing optimistic concurrency features in Azure Mobile Services client SDKs](http://blogs.msdn.com/b/carlosfigueira/archive/2013/12/02/accessing-optimistic-concurrency-features-in-azure-mobile-services-client-sdks.aspx) 
[Mobile Services server script reference](http://msdn.microsoft.com/en-us/library/windowsazure/jj554226.aspx) 
[Automate mobile services with command-line tools](http://www.windowsazure.com/en-us/develop/mobile/tutorials/command-line-administration/)
