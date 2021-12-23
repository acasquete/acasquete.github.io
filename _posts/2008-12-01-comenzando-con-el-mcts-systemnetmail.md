---
title: Comenzando con el MCTS, System.Net.Mail
tags: [certification]
reviewed: true
---
Hoy, con esta entrada, comienzo mi camino hacia la certificación MCTS. Estoy preparando desde hace unos días el examen 70-536 con el «Self-paced training kit». En realidad llevo preparando este examen desde hace unos cuantos meses, y si cuento desde que comencé a preparar el 70-315 podría decir que llevo varios años detrás de una certificación, que por muy diversos motivos nunca he podido conseguir. En los próximos días elegiré el centro y el día del examen para marcarme unos hitos en el estudio y aprovecharé este humilde blog para crear un resumen sobre cada tema que finalice.

Hoy comienzo con el resumen del capítulo 15 (porque por alguno tengo que comenzar) dedicado a la creación y envío de e-mails utilizando el espacio de nombres _System.Net.Mail_.

El e-mail más sencillo es un mensaje que tiene un remitente, un destinatario, un asunto y un cuerpo de mensaje. Este tipo de e-mail se puede crear con una simple línea de código. Los mensajes más complejos pueden tener tipos de codificación (_encoding_) personalizados, múltiples vistas para texto plano y HTML, ficheros adjuntos e imágenes incrustadas dentro del código HTML.

Para crear un e-mail tenemos que crear un objeto _MailMessage_, utilizando alguno de sus cuatro constructores.

```csharp
MailMessage m0 = new MailMessage(); 
MailMessage m1 = new MailMessage(“email@remitente”, “email@destinatario”); 
MailMessage m2 = new MailMessage(“email@remitente”, “email@destinatario”, “Asunto”, “Cuerpo”); 
MailMessage m3 = new MailMessage(new MailAddress(“email@remitente”, “Nombre Remitente”), new MailAddress (“email@destinatario”, “Nombre Destinatario”);
```

Como vemos podemos especificar las direcciones de origen y destino como cadenas de texto o como un objeto _MailAddress_, que permite especificar una dirección, un nombre y un tipo de codificación aunque esto último es necesario en muy pocas ocasiones.

Si necesitamos enviar un mensaje a varios destinatarios tenemos que hacer uso del constructor vacío y añadir objetos _MailAddress_ al _MailMessage_ y especificar las propiedades _MailMessage.From_, _MailMessage.Subject_ y _MailMessage.Body_. Adicionalmente podemos añadir destinatarios CC y BCC, exactamente igual que añadimos destinatarios en _MailMessage.To_.

```csharp
MailMessage m = new MailMessage();
m.From = new MailAddress("email@origen.com", "Nombre Origen");
m.To.Add(new MailAddress("email@destinoA", "Destino A"));
m.To.Add(new MailAddress("email@destinoB", "Destino B"));
m.Subject = "Asunto";
m.Body = "Cuerpo";
```

_MailMessage_ tiene estas otras propiedades que se utilizan menos pero que en ocasiones pueden sernos de utilidad: **DeliveryNotificationOptions** - indica al servidor SMTP que debe enviar un mensaje a la dirección especificada en _MailMessage.From_ si el mensaje ha sido entregado, ha fallado o ha sido retrasado. La enumeración es del tipo DeliveryNotificationOptions y puede tomar los valores _Delay_, _OnFailure_, _None_, _OnSuccess_, _Never_. **ReplyTo** - Indica la dirección donde se enviaran las respuestas de un e-mail. **Priority** - Indica, como se deduce, la prioridad del mensaje. Puede tomar los valores siguientes de la enumeración _MailPriority_: _High_, _Low_ y _Normal_.

Para añadir un fichero adjunto tenemos que utilizar el metodo _Add_ de la colección _MailMessage.Attachments_ para añadir un nuevo objeto _Attachment_. La manera más sencilla es especificando el nombre del fichero.

```csharp
MailMessage m = new MailMessage();
m.Attachment.Add(@"c:fichero.ext");
```

Se puede especificar un tipo de contenido MIME utilizando la enumeración _System.Net.Mime.MediaTypeNames_ para texto e imágenes, pero lo normal es especificar _Application.Octet_.

```csharp
m.Attachments.Add(new Attachment(@"fichero.ext", System.Net.Mime.MediaTypeNames.Application.Octet)
```

En lugar de especificar un nombre de fichero, también se puede especificar un objeto Stream.

```csharp
MailMessage m = new MailMessage();
Stream sr = new FileStream(@"fichero.ext", FileMode.Open, FileAccess.Read);
m.Attachments.Add(new Attachment(sr, "fichero.ext", MediaTypeNames.Application.Octet));
```

Para crear un mensaje HTML hay que poner la propiedad _IsBodyHtml_ a Verdadero e informar un contenido html en _MailMessage.Body_.

```csharp
m.Body = "Mensaje HTML."
m.IsBodyHtml = True
```

Hay que tener en cuenta que el Asunto (_MailMessage.Subject_) siempre es texto plano y que podemos definir el cuerpo como una página web, pero que la mayoria de clientes de correo ignoran la sección head, scripts y no descargan imágenes desde direcciones sitios web.

Para incrustar imagenes dentro del mensaje HTML hay que utilizar las clases _AlternateView_ y _LinkedResource_. Hay crear una vista alternativa indicando el fichero, o un objeto stream y el _System.Net.Mime_, informar el ContentID y referenciarlo en el HTML.

```csharp
string htmlBody = "![](cid:Img1)";

AlternateView avHtml = AlternateView.CreateAlternateViewFromString (htmlBody, null, MediaTypeNames.Text.Html);

LinkedResource pic1 = new LinkedResource("imagen.jpg", MediaTypeNames.Image.Jpeg);
pic1.ContentId = "Img1";

avHtml.LinkedResources.Add(pic1);

string textBody = "Tu cliente de correo no soporta mensajes HTML";
AlternateView avText = AlternateView.CreateAlternateViewFromString (textBody, null, MediaTypeNames.Text.Plain);
MailMessage m = new MailMessage();
m.AlternateViews.Add(avHtml);
m.AlternateViews.Add(avText);
```

El objeto *MailMessage* incluye la lógica para validar las direcciones de correo, en algunas circunstancias puede ser necesario tener dos niveles de validación. Si introducimos una dirección en blanco *MailMessage* lanzará una excepción *ArgumentException* y si introducimos una dirección erronea, se lanzará una excepción *FormatException*

Con esto termino este resumen de la lección dedicada a la creación de e-mails mediante el objeto *MailMessage*. En una próxima entrada trataré la siguiente lección, el envío de e-mails.

