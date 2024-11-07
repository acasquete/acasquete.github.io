---
title: Threading mediante aspectos con PostSharp
tags: [programming, aop]
reviewed: true
---
La primera toma de contacto que se suele hacer con la [programación orientada a aspectos](http://es.wikipedia.org/wiki/Programaci%C3%B3n_Orientada_a_Aspectos) (AOP) es, casi siempre, mediante algún ejemplo de _logging_. En todas las presentaciones a las que he asistido, siempre se termina con el mismo ejemplo: una aplicación de consola con un método en el que se aplica un aspecto de traza para registrar cuando se entra y se sale del mismo. Seguramente se elije este ejemplo porque tanto la implementación como el código IL generado son muy fáciles de entender. Sin embargo, mucha gente se queda desencantada viendo sólo este tipo de implementación, como diciendo: «¡Necesito más!, quiero saber qué más se puede hacer con AOP».

En esta ocasión vamos a ver como implementar _threading_ mediante aspectos utilizando, en mi opinión, el mejor framework de AOP para .NET: [_PostSharp_](http://www.sharpcrafters.com/). No es mucho más espectacular que implementar _logging_, pero lo interesante está en ver el cambio de paradigma de una programación convencional a una programación con aspectos, a la vez que obtenemos un código mucho más fácil de entender, de probar y, en definitiva, menos propenso a errores. ¿Comenzamos?

Tanto en WPF como en WinForms es habitual (y necesario) iniciar un _thread_ cuando lanzamos un proceso largo y no queremos bloquear la interfaz de usuario. En algún momento de nuestra vida se nos a planteado este problema y, más o menos todos, lo hemos resuelto mediante un delegado de la siguiente forma:

```csharp
private void buttonStart_Click(object sender, RoutedEventArgs e) { 
    ThreadPool.QueueUserWorkItem( delegate { // Do something a hundred times 
        for (int i = 0; i < 100; i++) 
        { 
            Thread.Sleep(20); 
        } 
    }); 
}
```

También es muy habitual que en estos mismos procesos, se muestre el progreso de la ejecución mediante, por ejemplo, un control _ProgressBar_. El problema que ya conocemos es que si intentamos acceder al control desde el _thread_, obtenemos una _InvalidOperationException_: «_The calling thread cannot access this object because a different thread owns it_», que viene a decir en la lengua de Cervantes, que el _thread_ no puede acceder al objeto de la interfaz de usuario porque en WPF y WinForms el subsistema gráfico es _single-threaded_.

Así que para salvar esta limitación tenemos que utilizar el método _Invoke_ de la clase _Dispatcher_ para ejecutar el delegado en el subproceso de la interfaz de usuario.

```csharp
private void buttonStart_Click(object sender, RoutedEventArgs e)
{
    ThreadPool.QueueUserWorkItem(
    delegate
    {
        // Do something a hundred times
        for (int i = 0; i < 100; i++)
        {
            Thread.Sleep(20);
            UpdateProgressBar(i);
        }
    });
}

private void UpdateProgressBar(int value)
{
    this.Dispatcher.Invoke(
        DispatcherPriority.Normal,
        new Action(() =>
        {
            this.labelProgress.Content = String.Format("{0}% Completed", value + 1);
            this.progressBar1.Value = value + 1;
        })     
    );
}
```

Al final lo que sucede, es que para realizar una sencilla operación tenemos un código dificil de entender, en el que tenemos la gestión de hilos mezclada con la lógica de la aplicación. Aquí es cuando la programación orientada a aspectos y _PostSharp_ intervienen para ayudarnos a tener un código más legible, aplicando dos aspectos a nuestros métodos.

```csharp
[WorkerThread]
private void buttonStart_Click(object sender, RoutedEventArgs e)
{
    // Do something a hundred times
    for (int i = 0; i < 100; i++)
    {
        Thread.Sleep(20);
        this.UpdateProgressBar(i);
    }
}

[GUIThread]
private void UpdateProgressBar(int value)
{
    this.labelProgress.Content = String.Format("{0}% Completed", value + 1);
    this.progressBar1.Value = value + 1;
}
```

En el primer caso indicamos mediante el atributo _WorkerThread_ que el método se ejecutará en un _thread_ y en el segundo atributo indicamos que el método se ejecutará en el _thread_ de la interfaz de usuario. Una codificación con una diferencia más que notable, ¿no? Veamos entonces la implementación de las clases de estos dos atributos:

```csharp
[Serializable]
public class WorkerThreadAttribute : MethodInterceptionAspect
{
    public override void OnInvoke(MethodInterceptionArgs args)
    {
        ThreadPool.QueueUserWorkItem(x => args.Proceed());
    }
}

[Serializable]
public class GUIThreadAttribute : MethodInterceptionAspect
{
    public override void OnInvoke(MethodInterceptionArgs eventArgs)
    {
        DispatcherObject dispatcherObject = (DispatcherObject)eventArgs.Instance;

        if (dispatcherObject.CheckAccess())
        {
            eventArgs.Proceed();
        }
        else
        {
            dispatcherObject.Dispatcher.Invoke(
                DispatcherPriority.Normal, 
                new Action(eventArgs.Proceed));
        }
    }
}
```

Los dos atributos heredan de la clase *MethodInterceptionAspect* e interceptaran las llamadas a los métodos donde estén aplicados. En ambos atributos se sobrecarga el método *OnInvoke* que es que se lanza en lugar del método interceptado. A partir de aquí, la implementación de los dos atributos es bastante sencilla.

En el atributo *WorkerThreadAttribute* encolamos el método interceptado que obtenemos con *args.Proceed()*, y en el atributo *GuiThreadAttribute* comprobamos mediante el método *CheckAccess* si el *thread* está en el subproceso de la interfaz de usuario y, en el caso de que no esté, invocamos el método interceptado a través de la clase *Dispatcher*

Hasta aquí hemos visto como con muy poco código podemos hacer de nuestro código algo mucho más manejable y fácil de entender. En próximos posts intentaré mostrar otros atributos para añadir nuevos comportamientos a nuestros métodos.

**Descarga código fuente:** 
[Threading.PostSharp.WPF.zip](/files/Threading.PostSharp.WPF.zip)
