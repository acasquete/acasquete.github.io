---
title: Acceder a variables de servidor con ASP.NET desde Javascript
tags: []
---
Estos días estoy escribiendo una documentación sobre _jQuery_ y buenas prácticas de programación con JavaScript para intentar evitar y corregir los errores más frecuentes en la aplicación que desarrollamos. Una de las malas prácticas más recurrentes y que más preocupa es como resolver el uso exagerado e indiscriminado de _ClientScript.RegisterStartupScript_, normalmente utilizado para definir un comportamiento en cliente dependiendo del valor de una variable de servidor.

La mayoría de los casos a resolver tienen la forma siguiente:

If ServerVariable.Value = False Then ClientScript.RegisterStartupScript(Me.GetType(), “Script”, “HideMenuOption(‘160’);refreshTree();”, True) Else ClientScript.RegisterStartupScript(Me.GetType(), “Script”, “ShowMenuOption(‘160’);refreshTree();”, True) End If </pre> Como vemos, según el valor que tenga la variable ServerVariable se registra un código javascript distinto. Este ejemplo es un claro caso de mala práctica por distintos motivos, el más evidente es que podríamos encapsular las llamadas a las funciones Javascript _ShowMenuOption_, _HideMenuOption_, _refressTree_ en una sola. Dejando este detalle aparte, el gran problema de este código es que si necesitamos modificar el comportamiento en cliente, tenemos que modificar el código de servidor, obligándonos a recompilar el proyecto. Otra gran desventaja es que utilizar este tipo de código provoca que tengamos que recurrir al uso de setTimeout para controlar el estado de carga de la página dentro de la función JavaScript, más o menos de la manera siguiente:

function HideMenuOption (opciones) {
   if (document.readyState=="complete") {
      if (hideMenubar) {
         hideMenubar(opciones, true);
      } else {
         setTimeout('HideMenuOption("'+opciones+'");',500);
      }
   } else {
      setTimeout('HideMenuOption("'+opciones+'");',500);
   }
} 

Y posiblemente, dependiendo de su funcionalidad, tengamos que repetir esta comprobación para todas las demás funciones. Para evitar todo esto hay varias opciones. Una alternativa, recomendable en algunos casos, es crear un control oculto que contenga el valor que queremos pasar. Pero la opción más sencilla es pasar la variable de servidor a JavaScript, es decir utilizar _ClientScript.RegisterStartupScript_ sólo para registar la variable en JavaScript.

Dim clientVar As String = "var ServerVariable=" & ServerVariable.Value

ClientScript.RegisterStartupScript(Me.GetType(), "Script", clientVar, True)

Utilizando jQuery, esperamos a que el DOM esté disponible (no todo el contenido de la página) y comprobamos que existe la variable.

$(document).ready(function() {
   if (window.ServerVariable) {
      if (ServerVariable==true) {
         HideMenuOption('160');
      } else {
         ShowMenuOption('160');
      }
   }
}); 


De esta forma si tenemos que modificar el código de cliente, únicamente tendremos que modificar el fichero con el código JavaScript.

