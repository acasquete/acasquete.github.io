---
title: Añadir un evento a un control creado en tiempo de ejecución
tags: [programming]
reviewed: true
---
Visual Basic no me gusta. Y no es que no le haya dado oportunidades, todo lo contrario, le he dado y le sigo dando demasiadas. He trabajado con VB desde la versión 4 hace ya unos cuantos años y ahora sigo trabajando día a día con VB.NET, y aún no me acostumbro. No es que crea que VB.NET sea malo —que no lo es—, simplemente es que no me acostumbro, se me olvidan las instrucciones. El ejemplo claro es lo que me ha pasado hoy. He estado intentando añadir un evento a un control creado dinámicamente y no lo he conseguido, simplemente porque se me había olvidado como se hacía.

En Visual Basic.NET se utiliza la instrucción _AddHandler_ para asociar un evento a un controlador de eventos en tiempo de ejecución. Esta instrucción espera dos argumentos: el evento y una referencia al delegado. Con el siguiente código se crea dinámicamente un control botón, se asocia el método _Button\_Command_ al evento _Command_ del control, y se añade a la colección de controles del formulario de la página.

```vb
Dim Button1 As New Button

Button1.Text = “Púlsame!” 
Button1.CommandArgument = “Argumento”

AddHandler Button1.Command, AddressOf Me.Button_Command

Me.Form.Controls.Add(Button1)
```

He utilizado el evento _Command_ en lugar del evento _Click_ ya que permite pasar información adicional mediante la propiedad _CommandArgument_. Esto es útil si queremos asociar varios controles al mismo delegado. Este evento solo existe en los controles _Button_, _ImageButton_ y _LinkButton_. Si no necesitamos pasar más información, podemos utilizar el evento _Click_.

Lo único que queda ahora es crear el método que será invocado cuando pulsemos el botón:

```vb
Public Sub Button_Command(ByVal sender As Object, ByVal e As System.Web.UI.WebControls.CommandEventArgs)
   Response.Write(e.CommandName)
End Sub
```

Este método requiere dos objetos como parámetros, que serán enviados cuando se invoque. El primer objeto es el «sender» que identifica al objeto que lo ha llamado, y el segundo objeto es el «CommandEventArgs», que contiene la información adicional del control.

Bien sencillo que es y lo que me ha costado por no recordar la instrucción *AddHandler*. Creo que esto ya no lo olvidaré jamás.

