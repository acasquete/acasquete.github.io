---
title: Insertar dinámicamente un tag script en el head
tags: []
---
Hoy, entre otras cosas, he estado buscando la forma elegante de añadir dinámicamente un tag _script_ en la cabecera de un ASPX. Pensaba que existía un control análogo al [HtmlMeta](http://msdn.microsoft.com/es-es/library/system.web.ui.htmlcontrols.htmlmeta(VS.80).aspx) (algo así como HtmlScript) o que se haría mediante algún misterioso método de la clase ClientScript, pero no, sólo tenemos que crear un control Html genérico y añadirlo a la colección de controles de la cabecera.

HtmlGenericControl script = new HtmlGenericControl(“script”);

script.Attributes.Add(“type”, “text/javascript”); script.Attributes.Add(“src”, “jquery.js”);

this.Page.Header.Controls.Add(script); </pre> Este código añade el nuevo control script al final de todos los del HEAD, si queremos ponerlo al principio tenemos que utilizar el método AddAt indicando en que posición lo queremos añadir.

this.Page.Header.Controls.AddAt(0, script);



En definitiva, nada espectacular, pero muy instructivo.

