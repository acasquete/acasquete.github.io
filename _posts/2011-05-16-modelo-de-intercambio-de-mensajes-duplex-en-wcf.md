---
title: Modelo de intercambio de mensajes dúplex en WCF
tags: []
---
Retomo el blog dos meses después de mi último post y justo también cuando se acaban de cumplir tres años desde que inicié mi andadura bloguera con **IdleBit**.

Estos últimos meses han sido bastante movidos profesionalmente, y entre la preparación de varios exámenes de certificación y proyectos personales, no he podido dedicar la debida atención al blog y al DotNetClub. Además, tanto ajetreo ha coincidido con el inicio de una nueva etapa profesional en [Pasiona Consulting](http://www.pasiona.es/), así que voy a tomarme este parón como algo muy positivo y espero que este cuarto año del blog que iniciamos ahora sea mucho mejor que los que tres que hemos dejado atrás. ¡No será por falta de ganas!

Uno de mis objetivos principales para esta etapa es aumentar el número publicaciones, así que después de esta breve puesta al día no os entretengo más. Comenzamos esta nueva etapa con una entrada sobre WCF (aprovechando que me presento de aquí a unas pocas semanas al examen) y sobre un modelo de intercambio de mensajes no muy utilizado: **contrato de servicios dúplex**.

En **Windows Communication Foundation** (WCF) hay disponibles tres modelos de intercambio de mensajes (_Message Exchange Patterns_ o MEPs): unidireccional (_one way_), solicitud-respuesta (_request/response_) y dúplex. Los MEP describen el protocolo que los clientes que consumen el servicio deben utilizar para comunicarse con él correctamente. Por ejemplo, si utilizamos el modelo unidireccional, el cliente debe saber que no tiene que esperar un mensaje de respuesta, o por el contrario, si utilizamos el modelo _Request/Response_ el cliente necesita saber que si habrá un mensaje de respuesta.

Para aclarar un poco estos conceptos pongo un par de ejemplos de contratos. Un **contrato unidireccional** se declara simplemente estableciendo el valor de la propiedad _IsOneWay_ del atributo _OperationContract_ a true.

public interface IMyService { \[OperationContract(IsOneWay=true)\] string Close(); } </pre>

En este ejemplo cuando se llame al método _Close_ no se recibirá ningún mensaje de respuesta. Aunque tenemos que tener en cuenta que aunque este tipo de comunicación parece asíncrona no lo es realmente. La forma que tiene WCF hace que el cliente bloquee después de que se haya enviado hasta que el servicio lo recibe de la cola interna y lo procesa. Por otro lado, tenemos que tener en cuenta que en el modo _OneWay_ no permite utilizar FaultContract ya que para que el servicio soporte faults debe tener una canal de dos sentidos.

El **contrato solicitud-respuesta** es el más común, de hecho, como el valor por defecto de la propiedad _IsOneWay_ es false, todas nuestras _OperationContract_ están en modo solicitud-respuesta incluso cuando no devuelve ningún valor.

public interface IMyService
{
   \[OperationContract\]
   void Close();
}

Por ultimo, tenemos el modelo de **intercambio de mensajes dúplex** que es un contrato de servicios con un canal de dos sentidos en el que cada punto de la comunicación puede enviar mensajes. Este tipo de contrato nos puede ser útil en alguna de las siguientes dos situaciones:

1.  El cliente envía un mensaje al servicio para iniciar un proceso largo y queremos ser notificados cuando el proceso termine.
2.  Queremos que el servicio pueda enviar mensajes no solicitados.

En el modelo de intercambio dúplex hay dos contratos (contrato de servicio y contrato de _callback_). La definición de la relación entre los dos contratos se realiza mediante la propiedad _CallbackContract_ del atributo _ServiceContract_ del contrato de servicio. En el siguiente ejemplo vamos a definir el contrato principal del servicio y el contrato de _callback_.

\[ServiceContract(CallbackContract = typeof(IMyServiceDuplexCallback))\]
public interface IMyServiceDuplex
{
   \[OperationContract(IsOneWay = true)\]
   void OperationHello(string name);

}

\[ServiceContract\]
public interface IMyServiceDuplexCallback
{
   \[OperationContract(IsOneWay = true)\]
   void Response(string message);
}

Una implementación simple de este servicio sería esta:

public class MyServiceDuplex : IMyServiceDuplex
{
   public void OperationHello(string name)
   {
      IMyServiceDuplexCallback callback = OperationContext.Current.GetCallbackChannel<IMyServiceDuplexCallback>();
      callback.Response(String.Format("Hi {0}! Hello world from a duplex service!", name));
   }
}

Ahora solo queda implementar el cliente que tiene que consumir este servicio. Como ejemplo creamos una aplicación de consola a la que tenemos que añadir la referencia a nuestro servicio. Si intentamos añadirla sin más obtendremos el error «El contrato requiere Duplex, pero el enlace ‘BasicHttpBinding’ no lo admite o no está configurado correctamente para admitirlo», o su equivalente en la lengua shakesperiana «Contract requires Duplex, but Binding ‘BasicHttpBinding’ doesn’t support it or isn’t configured properly to support it». Esto significa que debemos cambiar la configuración del binding de nuestro servicio ya que por defecto está configurado con _BasicHttpBinding_ y el único que soporta comunicaciones dúplex es _wsDualHttpBinding_. Así que modificamos el archivo de configuración añadiendo la configuración del _endpoint_ de la siguiente forma:

<services>
   <service name="WcfServiceDuplex.MyServiceDuplex">
      <endpoint address="" binding="wsDualHttpBinding" bindingConfiguration="" contract="WcfServiceDuplex.IMyServiceDuplex" />
   </service>
</services>

Una vez hecho esto, podremos añadir la referencia al servicio desde nuestra aplicación de consola. El siguiente paso es crear una clase que implemente el servicio _callback_. En nuestro caso creamos la clase _MyServiceDuplexCallbackHandler_ que implementa _IMyServiceDuplexCallback_. El método _Response_ escribe en la consola la cadena.

public class MyServiceDuplexCallbackHandler : IMyServiceDuplexCallback
{
  public void Response(string result)
  {
    Console.WriteLine(result);
  }
}

y por último implementamos la llamada. El constructor del cliente WCF de un contrato dúplex requiere que se pase una instancia de _InstanceContext_ para manejar los mensajes que lleguen desde el servicio. Cremos una instancia de InstanceConstext pasando la implementación, es decir una instancia de la clase MyServiceDuplexCallbackHandler y después creamos una instancia del cliente pasando la instancia de InstanceContext. Después solo queda realizar la llamada al método _OperationHello_.

static void Main(string\[\] args)
{
  var instanceContext = new InstanceContext(new MyServiceDuplexCallbackHandler());

  var client = new MyServiceDuplexClient(instanceContext);

  client.OperationHello("Alex");

  Console.ReadKey();
}



El modelo de intercambio de mensajes dúplex tiene varios problemas de aplicación en la mayoría de escenarios de la Vida Real™. El servicio necesita conectar con el cliente y muchas veces esto es imposible debido a problemas de seguridad o de configuración. Otro de los problemas es que los servicios dúplex no escalan bien porque su uso depende de la existencia de una sesión mantenida entre el cliente y el servicio. Y por último utilizando contratos dúplex perdemos interoperabilidad ya que no hay posibilidad de interoperar con clientes en otras plataformas que no sean .NET.

A pesar de estos inconvenientes, puede que para alguna implementación en un entorno Intranet os sea útil.

Descarga código fuente: 
[WcfDuplex.zip](http://sdrv.ms/18cxK0C)

**Referencias**

[Servicios dúplex](http://msdn.microsoft.com/es-es/library/ms731184.aspx) 
[Creación de un contrato dúplex](http://msdn.microsoft.com/es-es/library/ms731064.aspx) 
[Cómo: Obtener acceso a los servicios con un contrato dúplex](http://msdn.microsoft.com/es-es/library/ms731935.aspx)

