---
title: Detectando deadlocks con PostSharp
tags: [aop]
---
Esta breve entrada la voy a dedicar a comentar una característica poco conocida de **PostSharp**, pero que nos puede ser bastante útil para ahorrarnos algo de tiempo detectando _deadlocks_, ya que posiblemente estos sean los problemas más complicados de depurar, sobre todo si se producen en producción.

La **Threading Pattern Library** de PostSharp contiene un aspecto para detectar deadlocks. Lo que se consigue al aplicar este aspecto es que al detectarse un _deadlock_, en lugar de quedarse la aplicación congelada, se lanza una excepción con la información de los threads y los objetos que están involucrados en ese deadlock.

Supongamos que tenemos una aplicación en la que dos o más threads tienen que tener acceso al mismo recurso, pero solo uno a la vez puede tener acceso al recurso de forma segura. Si la implementación de exclusión mutua se hace de forma incorrecta, podemos crear un _deadlock_ y obtendremos dos threads que esperan la liberación de un recurso y ninguno puede continuar con su ejecución.

Pongamos, como ejemplo, la implementación más típica para provocar el deadlock más simple.

    class Program
    {
        static Object lockA = new Object();
        static Object lockB = new Object();
    
        static void Main()
        {
            Task.Factory.StartNew(() => DoWorkOne());
            DoWorkTwo();
        }
    
        static void DoWorkOne()
        {
            lock (lockA)
            {
                Console.WriteLine("One Lock A");
                lock (lockB)
                {
                    Console.WriteLine("One Lock B");
                }
            }
        }
    
        static void DoWorkTwo()
        {
    
            lock (lockB)
            {
                Thread.Sleep(100);
    
                Console.WriteLine("Two Lock B");
                lock (lockA)
                {
                    Console.WriteLine("Two Lock A");
                }
            }
        }
    }
    </pre>
    
    Si ejecutamos este programa obtendremos el siguiente resultado en la consola:
    
    <pre>
    One Lock A
    Two Lock B
    </pre>
    
    Y el programa permanecerá detenido indefinidamente. Veamos la secuencia de lo que ha sucedido:
    
    1. Thread 1 bloquea el objeto A.
    1. Thread 2 bloquea el objeto B.
    3. Thread 1 intenta bloquear el objeto B, pero está bloqueado por el Thread 2.
    4. Thread 2 intenta bloquear el objeto A, pero está bloqueado por el Thread 1.
    
    ¡Conseguido! ¡Este es el aspecto que tiene un DeadLock! 
    
    Para habilitar la detección de deadlocks con PostSharp tenemos que añadir el paquete **PostSharp Threading Pattern Library** de Nuget.
    
    <a href="http://www.casquete.es/wp-content/uploads/2014/01/AddThreadingPatternLibrary.png">![AddThreadingPatternLibrary](http://www.casquete.es/wp-content/uploads/2014/01/AddThreadingPatternLibrary.png)</a>
    
    Y añadir el atributo **DeadlockDetectionPolicy** en cada uno de los ensamblados de la solución. Lo podemos hacer añadiendo la siguiente línea en el fichero **AssemblyInfo.cs** de cada proyecto.
    
    <pre class="brush:csharp">
    [assembly: PostSharp.Patterns.Threading.DeadlockDetectionPolicy]
    </pre>
    
    Si ejecutamos de nuevo el programa, obtendremos una excepción **DeadlockException** indicándonos los hilos que están involucrados. El mensaje de la excepción será algo parecido a esto:
    
    <pre>
    Additional information: Deadlock detected. The following synchronization elements form a cycle: #0=; #1=; #2=; #3=
    

[![DeadlockException](/img/DeadlockException.png)](/img/DeadlockException.png)

Con la ventana de Threads de Visual Studio podemos identificar rápidamente qué métodos son los que están parados en cada hilo de ejecución, en este caso los threads 6 y 10.

¿Y cómo funciona todo esto?
---------------------------

Existen dos técnicas para la detección de deadlocks: detección basada en timeout o en grafos. Si estáis interesados en conocer más de estas dos técnicas, os recomiendo que leáis un artículo de hace ya unos años de la MSDN Magazine: [Advanced Techniques To Avoid And Detect Deadlocks In .NET Apps](http://msdn.microsoft.com/en-us/magazine/cc163618.aspx).

El atributo **DeadlockDetectionPolicy** funciona creando un grafo de dependencias de los threads y los objetos bloqueados. Cuando un objeto de sincronización espera más de 200ms se realiza una detección de deadlock y el algoritmo analiza el grafo de dependencias buscando ciclos, lanzando una **DeadlockException** en todos los threads involucrados en el deadlock en el caso de encontrar uno.

El proceso de detección de _deadlocks_ basado en grafos es bastante pesado y solo hay que echar un vistazo al código que genera PostSharp para saber que solo deberíamos activar este tipo de detección cuando tengamos que depurar algún error.

Referencias
-----------

[Advanced Techniques To Avoid And Detect Deadlocks In .NET Apps](http://msdn.microsoft.com/en-us/magazine/cc163618.aspx) 
[Deadlock Detection using PostSharp Threading Toolkit](http://www.postsharp.net/blog/post/Deadlock-Detection-using-PostSharp-Threading-Toolkit) 
[Await, and UI, and deadlocks! Oh my!](http://blogs.msdn.com/b/pfxteam/archive/2011/01/13/10115163.aspx)

