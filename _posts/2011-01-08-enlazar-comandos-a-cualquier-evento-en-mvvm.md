---
title: Enlazar comandos a cualquier evento en MVVM
tags: []
---
En la [primera entrada dedicada a MVVM](/otra-implementacion-basica-del-patron-mvvm) vimos que en este patrón no utilizamos eventos, en su lugar nos valemos de los comandos para asociar una acción con un determinado control. El problema es que los controles WPF no tienen propiedades para enlazar todos los eventos con comandos. Por ejemplo, en un botón podemos utilizar la propiedad _Command_ para ejecutar una acción al pulsar el botón. Pero, ¿qué sucede si queremos asignar un comando a otro evento? ¿Cómo hacemos, por ejemplo, para ejecutar un comando al pasar por encima de un control? ¿Y al escribir en un TextBox? ¿Y al cargar una vista?

En esta entrada vamos a ver dos métodos para responder a estas preguntas: el primero es mediante la implementación del patrón **Attached Behavior** y el segundo es haciendo uso de los comportamientos que nos proporcionan las clases de **System.Windows.Interactivity**.

### Patrón _Attached Behavior_

Básicamente el patrón _Attached Behavior_ consiste en una clase estática en la que se definen una o varias propiedades asociadas (_attached properties_), un tipo especial de propiedad de dependencia (_dependency property_). En nuestra solución de ejemplo vamos a definir la clase _MouseBehavior_ dentro del namespace **BasicMVVM.Behaviors** y dentro de esta clase definiremos la propiedad asociada _MouseEnter_. A diferencia de las _dependency properties_, no definimos un _wrapper_ para las propiedades sino que tenemos que crear el par de métodos estáticos _GetMouseEnter_ y _SetMouseEnter_. En el método controlador _MouseEnterCallback_, que se llamará cada vez se cambie la propiedad, asignamos al evento _MouseEnter_ el código para ejecutar el comando. La implementación completa de la clase queda de la siguiente forma:

namespace BasicMVVM.Behaviors { public static class MouseBehavior { public static readonly DependencyProperty MouseEnterProperty;

    static MouseBehavior()
    {
      MouseEnterProperty = DependencyProperty.RegisterAttached("MouseEnter",
      typeof(ICommand), typeof(MouseBehavior), new PropertyMetadata(MouseEnterCallback));
    }
    
    public static ICommand GetMouseEnter(UIElement element)
    {
      return (ICommand)element.GetValue(MouseEnterProperty);
    }
    
    public static void SetMouseEnter(UIElement element, ICommand value)
    {
      element.SetValue(MouseEnterProperty, value);
    }
    
    private static void MouseEnterCallback(object obj, DependencyPropertyChangedEventArgs e)
    {
      var element = obj as UIElement;
    
      element.MouseEnter += (sender, ev) =&gt;
      {
        var el = sender as UIElement;
        var command = GetMouseEnter(el);
    
        if (command.CanExecute(null))
        {
          command.Execute(el);
        }
      };
    }   } }
    

</pre>

Para poder utilizar este comportamiento en la vista, que en nuestro ejemplo es la vista _Basic_, solo tenemos que declarar el espacio de nombres _BasicMVVM.Behaviors_ en la etiqueta Window.

<Window x:Class="BasicMVVM.Views.Basic"
...
xmlns:b="clr-namespace:BasicMVVM.Behaviors"
...>

Y para comprobar el funcionamiento, añadimos un nuevo botón al que enlazamos el comando deseado, en este caso que el comando _ChangeColorCommand_.

<Button Content="Attached behavior" b:MouseBehavior.MouseEnter="{Binding ChangeColorCommand}" />

Esta solución puede llegar a ser bastante tediosa porque tenemos que implementar todas las clases con los comportamientos que queremos controlar. Así que una alternativa a este método es utilizar los comportamientos incluidos en las clases de **System.Windows.Interactivity** que veremos a continuación.

    ### Comportamientos en System.Windows.Interactivity
    

**System.Windows.Interactivity.dll** es un ensamblado que tenemos disponible a través del SDK de Microsoft Expression Blend, y que podemos descargar en el [Centro de descargas de Microsoft](http://www.microsoft.com/downloads/en/details.aspx?displaylang=en&FamilyID=75e13d71-7c53-4382-9592-6c07c6a00207). Esencialmente este ensamblado lo que intenta es formalizar de alguna forma el patrón _attached behavior_ que hemos visto en el punto anterior.

Una vez hemos instalado el SDK, podemos utilizar el ensamblado añadiendo en el proyecto la referencia a _System.Windows.Interactivity.dll_ que se encuentra en la carpeta _{Program Files}Microsoft SDKsExpressionBlend.NETFrameworkv4.0Libraries_ y declarando el espacio de nombres correspondiente en la vista.

<Window x:Class="BasicMVVM.Views.Basic"
...
xmlns:i="http://schemas.microsoft.com/expression/2010/interactivity"
...>

Para añadir el mismo comportamiento que en el primer ejemplo anterior añadimos el botón con el siguiente código.

<Button Content="System.Windows.Interactivity">
  <i:Interaction.Triggers>
    <i:EventTrigger EventName="MouseEnter">
      <i:InvokeCommandAction Command="{Binding ChangeColorCommand}"/>
    </i:EventTrigger>
  </i:Interaction.Triggers>
</Button>

En este código definimos un desencadenador (_trigger_) que está escuchando el evento _MouseEnter_ y que al activarse invocará el comando _ChangeColorCommand_. Podemos definir estos desencadenadores en cualquier elemento. Por ejemplo, si queremos lanzar un comando cuando la vista se haya cargado, podemos utilizar el siguiente código XAML:

<Window x:Class="BasicMVVM.Views.Basic"
...
xmlns:i="http://schemas.microsoft.com/expression/2010/interactivity">

<Window.DataContext>
<vm:Basic />
</Window.DataContext>

<i:Interaction.Triggers>
  <i:EventTrigger EventName="Loaded">
    <i:InvokeCommandAction Command="{Binding ShowWelcomeMsgCommand}"/>
  </i:EventTrigger>
</i:Interaction.Triggers>
...
</Window>



\*\*Enlaces relacionados\*\*
\[Descarga Microsoft Expression Blend Software Development Kit (SDK) for .NET 4\](http://www.microsoft.com/downloads/en/details.aspx?displaylang=en&FamilyID=75e13d71-7c53-4382-9592-6c07c6a00207)
\[Información general sobre propiedades asociadas\](http://msdn.microsoft.com/es-es/library/ms749011.aspx)
\[Espacio de nombres System.Windows.Interactivity\](http://msdn.microsoft.com/es-es/library/system.windows.interactivity(v=expression.40).aspx)

**Descarga código fuente:**
[BasicMVVM-Behaviors.zip\](http://sdrv.ms/12KND9X)

