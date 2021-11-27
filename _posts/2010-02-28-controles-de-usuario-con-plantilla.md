---
title: Controles de usuario con plantilla
tags: []
---
Una característica de ASP.NET que no he utilizado en ningún proyecto y que he redescubierto durante la preparación del segundo examen para el MCTS, es la posibilidad de crear un control de usuario que permita separar la información del control de su presentación. Como vamos a ver en esta entrada, podemos conseguir esto sin mayores dificultades mediante la implementación de [controles de usuario con plantilla](http://msdn.microsoft.com/es-es/library/36574bf6.aspx) (_Templated User Controls_).

Imaginemos que queremos crear un control de usuario que debe mostrar una información concreta, por ejemplo, el campo nivel del usuario, pero en el que la interfaz de usuario variará dependiendo de la página. Creando un control de usuario con plantilla no vamos a exponer ningún diseño predeterminado, de esta manera, será el programador quien defina la interfaz del control en la página en la que se utilice.

El primer paso para crear un control de usuario con plantilla es, obviamente, añadir un nuevo control de usuario a nuestro sitio web. En ese control añadiremos un control _Placeholder_ que definirá la posición donde aparecerá la plantilla. El código del control de usuario será el siguiente:

<%@ Control Language="C#" AutoEventWireup="true" CodeFile="UCSample.ascx.cs" Inherits="UCSample" %> <asp:PlaceHolder ID="PlaceHolderContent" runat="server"></asp:PlaceHolder> </pre>

En el _code-behind_ del control crearemos las propiedades que necesitemos y una propiedad de tipo _ITemplate_ con la que los usuarios de nuestro control podrán definir su código dentro de esta plantilla. El nombre que demos a esta propiedad será el mismo que tenga el _tag_ en el marcado de la página. Para nuestro ejemplo sólo hemos creado una propiedad de tipo entero que utilizaremos para establecer el nivel del ususario.

public partial class UCSample : System.Web.UI.UserControl
{
    public ITemplate Template { get; set; }

    public int Level { get; set; }
}

A continuación crearemos una clase contenedora que herede de la clase _Control_ y que implemente la interfaz [_INamingContainer_](http://msdn.microsoft.com/es-es/library/system.web.ui.inamingcontainer.aspx). Además, crearemos las propiedades públicas de los elementos de información que debe contener. En nuestro ejemplo, sólo creamos la propiedad _Level_.

public class UCContainer : Control, INamingContainer
{
    public int Level { get; set; }

    internal UCContainer(int level)
    {
        this.Level = level;
    }
}

Una vez creada la clase, aplicaremos el atributo [_TemplateContainer_](http://msdn.microsoft.com/es-es/library/system.web.ui.mobilecontrols.templatecontainer(VS.80).aspx) a la propiedad _ITemplate_. A este atributo le pasaremos como parámetro el tipo de la clase contenedora, _UCContainer_.

public partial class UCSample : System.Web.UI.UserControl
{
    \[PersistenceMode(PersistenceMode.InnerProperty)\]
    \[TemplateContainer(typeof(UCContainer))\]
    public ITemplate Template { get; set; }

    public int Level { get; set; }
}

Lo único que queda por hacer es añadir el código necesario en el manejador del evento _DataBind_ del control. Si la propiedad _ITemplate_ está establecida, crearemos una instancia de la clase contenedora, la instanciaremos dentro de la plantilla mediante el método [_InstantiateIn_](http://msdn.microsoft.com/es-es/library/system.web.ui.itemplate.instantiatein.aspx) y la añadiremos a la colección de controles del _Placeholder_. Si por el contrario la propiedad _ITemplate_ no está establecida, mostraremos un mensaje indicando que no se ha definido ninguna plantilla.

protected void Page\_DataBind(object sender, EventArgs e)
{
    PlaceHolderContent.Controls.Clear();

    if (Template == null)
    {
        PlaceHolderContent.Controls.Add(new LiteralControl("Plantilla no definida"));
    }
    else
    {
        UCContainer container = new UCContainer(Level);
        Template.InstantiateIn(container);
        PlaceHolderContent.Controls.Add(container);
    }
}

Para utilizar el control, como con cualquier control de usuario, lo debemos hacer dentro del mismo proyecto y lo añadimos a nuestra página web arrastrándolo desde el Explorador de soluciones. Una vez registrado, podemos definir la plantilla mediante el tag _<Template>_ que se ha definido con la propiedad _ITemplate_. Dentro de la plantilla podemos hacer referencia a la información llamando al objeto _Container_, que es una instancia de la clase _UCContainer_. El siguiente código muestra el código completo del _Web form_ con el control de usuario y la plantilla definida.

<%@ Page Language="C#" AutoEventWireup="true"  CodeFile="Default.aspx.cs" Inherits="\_Default" %>
<%@ Register src="UCSample.ascx" tagname="UCSample" tagprefix="uc1" %>
<html>
<head runat="server">
    <title>TemplatedUserControl Sample</title>
</head>
<body>
    <form id="form1" runat="server">
        <uc1:UCSample ID="UCSample1" runat="server">
            <Template>
                Nivel de Usuario: <%#Container.Level %> puntos
            </Template>
        </uc1:UCSample>
    </form>
</body>
</html>



Como hemos podido ver, los controles de usuario con plantilla incrementan la flexibilidad, manteniendo la encapsulación y la reutilización que ya proporcionan los controles de usuario.


