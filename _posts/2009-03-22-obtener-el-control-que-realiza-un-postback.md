---
title: Obtener el control que realiza un Postback
tags: [programming]
reviewed: true
---
Al realizar una instrumentación de una aplicación es importante saber que acciones ha realizado el usuario en un determinado momento. Una de estas acciones es saber que botón o control se ha pulsado, es decir que control es el que provoca el _postback_, y naturalmente tenemos que obtenerlo modificando el menor código posible, por ejemplo, modificando el método _Page\_Load_ de una clase base de la que hereden todas las páginas de la aplicación.

Creía que con consultar la propiedad «__EVENTTARGET» tendría suficiente, pero mi sorpresa ha venido porque los botones no informan esta propiedad, y de hecho tiene una explicación lógica en la que a estas alturas aún no había caído. Únicamente tenemos esta propiedad en los controles que, para realizar el postback, llaman a la función «__doPostBack», es decir, en todos los controles menos en los _Button_ y los _ImageButton_.

Lo primero que se debe hacer en estos casos es buscar, y he tardado 0,27 segundos en encontrar la solución a mi problema en una entrada del año 2006 del blog de [Mahesh Singh](http://geekswithblogs.net/mahesh/archive/2006/06/27/83264.aspx). Como necesitaba el código en VB.NET me he tomado la libertad de realizar una conversión literal.

La solución se basa en que si tenemos dos botones y pulsamos sobre el segundo sólo este último estará disponible en la colección _Page.Request.Form_. Así que si queremos saber quien ha provocado el _postback_ y no lo tenemos en el «\_\_EVENTTARGET», podemos suponer correctamente que el que lo ha provocado ha sido un botón (_Button_ o _ImageButton_), y sólo debemos comprobar que control de la colección _Page.Request.Form_ es un botón y habremos dado con él. Una única condición a tener en cuenta es que los identificadores de los ImageButton terminan con las cadenas «.x» y «.y», que identifican las coordenadas del ratón.

He aquí el código completo del método que comprueba toda la colección de controles del formulario y la llamada desde el _Page\_Load_ de la página:

```vb
Protected Sub Page_Load(ByVal sender As Object, ByVal e As System.EventArgs) Handles Me.Load 

    If IsPostBack Then
        Response.Write(getPostBackControlName) 
    End If 

End Sub

Private Function getPostBackControlName() As String 
    Dim control As Control = Nothing
    Dim ctrlname As String = Page.Request.Params(“__EVENTTARGET”)

    If ctrlname IsNot Nothing AndAlso ctrlname <> String.Empty Then
        control = Page.FindControl(ctrlname)
    Else
        ' Si __EVENTTARGET es nulo, el control es de tipo botón y tenemos
        ' que iterar sobre la colección del formulario para encontrarlo
        Dim ctrlStr As String = String.Empty
        Dim c As Control = Nothing
        For Each ctl As String In Page.Request.Form
            If ctl.EndsWith(".x") OrElse ctl.EndsWith(".y") Then
                ctrlStr = ctl.Substring(0, ctl.Length - 2)
                c = Page.FindControl(ctrlStr)
            Else
                c = Page.FindControl(ctl)
            End If
            If TypeOf c Is System.Web.UI.WebControls.Button OrElse _
                TypeOf c Is System.Web.UI.WebControls.ImageButton Then
                control = c
                Exit For
            End If
        Next
    End If
    
    Return control.ID End Function
```
