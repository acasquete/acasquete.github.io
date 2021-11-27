---
title: Tests unitarios con MessageBox en MVVM
tags: [mvvm]
---
Existen una serie de buenas prácticas que debemos seguir para hacer nuestras aplicaciones más testeables. Tres de estas prácticas son: hacer uso de patrones de diseño (MVVM, IoC, DI, etc.), utilizar un _framework_ de testing unitario para automatizar la ejecución de pruebas y, por último, hacer _mocking_ de nuestras bases de datos y _web services_ para evitar realizar llamadas remotas. Naturalmente no es necesario aplicar todas estas buenas prácticas en todos nuestros proyectos, sino que tenemos que identificar las situaciones en las que son necesarias.

En la entrada de hoy veremos una de estas situaciones, veremos los problemas que nos podemos encontrar al crear pruebas unitarias en una aplicación [«Otra implementación básica del patrón MVVM»](/otra-implementacion-basica-del-patron-mvvm), en la que introducía el patrón.

Comenzamos añadiendo dos nuevos controles a la vista: un control _Button_ y un _TextBlock_. La idea es que al pulsar el botón se muestre un _MessageBox_ y que se muestre un mensaje en la etiqueta según la respuesta del usuario.

<Button Command=”{Binding ShowYesNoQuestionCommand}” Content=”Show Question” /> <TextBlock Text=”{Binding Answer}” /></pre> Enlazamos la propiedad _Command_ del botón y la propiedad _Text_ del cuadro de texto con el comando **ShowYesNoQuestionCommand** y la propiedad **Answer** que tenemos que crear en el **ViewModel** con el código siguiente.

public string Answer
{
  get
  {
      return \_answer;
  }

  set
  {
      \_answer = value;
      NotifyPropertyChanged("Answer");
  }
}

public ICommand ShowYesNoQuestionCommand
{
  get
  {
      this.showYesNoQuestionCommand = new RelayCommand()
      {
          CanExecuteDelegate = p => true,
          ExecuteDelegate = p => { ShowYesNoQuestion("Are you sure?"); }
      };
      return this.showYesNoQuestionCommand;
  }
}

private bool ShowYesNoQuestion(string message)
{
  MessageBoxResult result = MessageBox.Show(
      message,
      "Question",
      MessageBoxButton.YesNo,
      MessageBoxImage.Question);

  switch (result)
  {
      case MessageBoxResult.Yes:
          this.Answer = "Your answer is Yes";
          return true;

      default:
          this.Answer = "Your answer is No";
          return false;
  }
}

Este código no brilla por su originalidad, pero si lo ejecutamos, funcionará perfectamente. Entonces, ¿cuál es el problema? Fundamentalmente el error está en que no deberíamos mostrar el _MessageBox_ desde el _ViewModel_, nos deberían doler los ojos al ver algo así. Pero, ¿por qué? Pues porque esta implementación nos impide probar correctamente nuestro _ViewModel_. Supongamos que queremos crear un test unitario para probar el funcionamiento de nuestro _Command_ y hacemos algo parecido a esto:

\[TestMethod\]
public void BadTestExecuteShowQuestionAndAnswerYes()
{
    ICommand command = vm.BadShowYesNoQuestionCommand;

    command.Execute(null);

    Assert.AreEqual("Your answer is Yes", vm.Answer);
}

¿Qué sucederá? Efectivamente, al ejecutar nuestro test, se mostrará el mensaje esperando que pulsemos algún botón, y esto no debe suceder nunca si queremos seguir llamando a nuestros tests, automatizados.

Para solucionar este problema tenemos que evitar la llamada al _MessageBox_ en el _ViewModel_ y substituirla por una llamada a un nuevo servicio, que será el que llame al _MessageBox_. En el test unitario falsearemos este servicio de mensajes por otro que no muestre el mensaje, pero que nos indique que se ha llamado. La forma más sencilla de implementar esta solución es mediante el uso del patrón [Service Locator](http://msdn.microsoft.com/en-us/library/cc304894.aspx), una versión especializada del patrón **Inversion of Control**.

Creamos un nuevo proyecto en el que añadiremos la clase _ServiceLocator_ y _MsgBoxService_. Podéis ver la implementación de la clase _ServiceLocator_ en el código fuente disponible para descarga al final de la entrada. La clase **MsgBoxService** no tiene ningún secreto, tiene un método _Show_ con 4 parámetros que son análogos a los del mismo método de la clase _MessageBox_.

public class MsgBoxService : IMsgBoxService
{
    public MessageBoxResult Show(string messageBoxText, string caption, MessageBoxButton button, MessageBoxImage icon)
    {
        return MessageBox.Show(messageBoxText, caption, button, icon);
    }
}

Ahora debemos agregar una referencia al _Service Locator_ en nuestro _ViewModel_, mediante una propiedad que nos devolverá siempre la misma instancia y añadiremos el método _GetService_ que nos devolverá el objeto que se haya registrado.

private ServiceLocator serviceLocator = ServiceLocator.Instance;

public ServiceLocator ServiceLocator
{
    get
    {
        return this.serviceLocator;
    }
}

public T GetService<T>()
{
    return this.serviceLocator.Resolve<T>();
}

Ahora tenemos que cambiar el _Command_ del _ViewModel_ para que utilice el nuevo servicio. El cambio es bastante sencillo:

private void ShowYesNoQuestion(string message)
{
    IMsgBoxService msgbox = GetService<IMsgBoxService>();

    MessageBoxResult result = msgbox.Show(
        message, 
        "Question", 
        MessageBoxButton.YesNo, 
        MessageBoxImage.Question);

    switch (result)
    {
        case MessageBoxResult.Yes:
            this.Answer = "Your answer is Yes";
            break;

        default:
            this.Answer = "Your answer is No";
            break;
    }
}

¿Qué es lo que falta? Registrar el servicio para que lo pueda devolver el _ServiceLocator_. Esto lo podemos hacer desde la clase _App_.

ServiceLocator.Instance.Register<IMsgBoxService>(new MsgBoxService());

Si ejecutamos la aplicación, funcionará de la misma forma que antes, con la ventaja de que ahora el _ViewModel_ no tiene ninguna llamada al _MessageBox_ y ahora sí estamos en condiciones de testearlo correctamente. Veamos cómo.

En nuestro proyecto de Test creamos un servicio falso que implemente la interfaz **IMsgBoxService**. Esta clase también tendrá un método _Show_, pero esta nos devolverá el valor que hayamos establecido en una nueva propiedad (**ShowReturnValue**) e incrementará un contador (**ShowCallCount**) que podremos consultar para comprobar las veces que se ha llamado al método.

class MockMsgBoxService : IMsgBoxService
{
    public MessageBoxResult ShowReturnValue;

    public int ShowCallCount;

    public MessageBoxResult Show(string messageBoxText, string caption, MessageBoxButton button, MessageBoxImage icon)
    {
        ShowCallCount++;
        return this.ShowReturnValue;
    }
}

El test unitario lo modificamos de la siguiente forma. Vemos que antes de llamar a _Execute_, establecemos el valor que queremos que nos devuelva el servicio, y que al final comprobamos que el método se haya ejecutado sólo una vez.

\[TestMethod\]
public void GoodTestExecuteShowQuestionAndAnswerYes()
{
    ICommand command = vm.ShowYesNoQuestionCommand;
    var msgBox = vm.GetService<IMsgBoxService>() as MockMsgBoxService;
    msgBox.ShowReturnValue = MessageBoxResult.Yes;
    msgBox.ShowCallCount = 0;

    command.Execute(null);

    Assert.AreEqual("Your answer is Yes", vm.Answer);
    Assert.AreEqual(1, msgBox.ShowCallCount);
}

Lo único que queda es registrar el servicio en la clase de test desde un método que marcamos con el atributo _AssemblyInitialize_, indicando que se ejecutará antes de todos los tests dentro del ensamblado.

\[AssemblyInitialize\]
public static void RegisterServices(TestContext context)
{
    ServiceLocator.Instance.Register<IMsgBoxService>(new MockMsgBoxService());
}

**Enlaces relacionados:**
[Service Locator (MSDN)](http://msdn.microsoft.com/en-us/library/cc304894.aspx)
[Dependency Injection (MSDN)](http://msdn.microsoft.com/en-us/library/ff648334.aspx)
[Inversion of Control (MSDN)](http://msdn.microsoft.com/en-us/library/ff648478.aspx)
[Dependency Injection (MSDN Magazine)](http://msdn.microsoft.com/en-us/magazine/cc163739.aspx)

**Descarga código fuente:**
[BasicMVVM-ServiceLocator.zip](http://sdrv.ms/159vPHz)** 

