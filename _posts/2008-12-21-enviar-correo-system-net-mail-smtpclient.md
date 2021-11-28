---
title: Enviar correo con System.Net.Mail.SmtpClient
tags: [certification]
---
Continúo con mis resúmenes del «MCTS Self-Placed Training Kit» que estoy utilizando para la preparación del examen 70-356.

Una vez tenemos creado el objeto MailMessage, la forma de código más sencilla para enviar el mensaje es la siguiente

SmtpClient smtp = new SmtpClient(“localhost”); smtp.Send(m); </pre> Esto es, como he dicho, lo más sencillo, pero muchas cosas pueden ir mal durante el envío: puede que el servidor de correo no esté disponible o no acepte las credenciales de usuario o puede que el servidor determine que alguno de los destinatarios no es válido. En cada una de estas circunstancias se lanzará una excepción que tendremos que capturar para evitar un error de aplicación. Las excepciones a capturar son estas:

**SmtpException** - no es un usuario válido o ha habido algun problema en la tansmisión. **SmtpFailedRecipientException** - Se está enviando un mensaje a un remitente que no existe. (Sólo en modo síncrono) **InvalidOperationException** - No se ha definido un nombre de servidor. **SmtpException con una WebException** - El servidor de correo no se puede encontrar.

Para especificar unas credenciales podemos utilizar las credenciales de red por defecto poniendo a True la propiedad _UseDefaultCredentials_ o asignado _CredentialCache.DefaultNetworkCredentials_ (del espacio de nombres _System.Net_) a _SmtpClient.Credentials_.

SmtpClient client = new SmtpClient("smtp.servidor.com");
client.Credentials = System.Net.CredentialCache.DefaultNetworkCredentials;

Si queremos especificar usuario y password y opcionalmente dominio tenemos que crear una instancia del _System.Net.NetworkCredentials_ y asignarla a _SmtpClient.Credentials_.

SmtpClient client = new SmtpClient("smtp.servidor.com");

client.Credentials = new NetworkCredential("usuario", "contraseña");

Si queremos encriptar la comunicación SMTP debemos poner a True la propiedad _EnableSsl_, teniendo en cuenta que no todos los servidores tienen soporte de SSL.

    ### Envío asíncrono con SmtpClient.SendAsync
    

El envío asíncrono de e-mails permite que nuestra aplicación siga respondiendo mientras se envía el mensaje. Si el servidor no responde, la aplicación esperará el valor indicado en _SmtpClient.Timeout_. Para enviar un mensaje de forma asíncrona tenemos crear un método para responder al evento _SmtpClient.SendCompleted_, llamar al método _SmtpClient.SendAsync_ y opcionalmente podremos cancelar el envío llamando al método _SmtpClient.SendAsyncCancel_.

sc = new SmtpClient("localhost");
sc.SendCompleted += new SendCompletedEventHandler(sc\_SendCompleted);
sc.SendAsync(mailmessage, null);
sc.SendAsyncCancel();

void sc\_SendCompleted(object sender, AsyncCompletedEventArgs e)
{
    if (e.Cancelled)
        Console.WriteLine("Envío cancelado");
    else if (e.Error != null)
        Console.WriteLine("Error: " + e.Error.ToString());
    else
        Console.WriteLine("Mensaje enviado");
}



Cuando usamos \*SmtpClient.SendAsync\*, los destinatarios no válidos y otros posibles errores no generan una excepción. Si el valor de \*AsyncCompletedEventArgs.Error\* no es nulo, significa que se ha producido algún error. El segundo parámetro del método SendAsync se puede utilizar para identificar el mensaje que se está enviando en el caso de que tengamos múltiples envíos asíncronos.

Hasta aquí el capítulo de \*System.Net.Mail\*. El siguiente tema al que dedicaré otra entrada es el tema relacionado con la reflexión.

