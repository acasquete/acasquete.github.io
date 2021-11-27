---
title: Cambiar el cursor mediante aspectos con PostSharp
tags: [aop]
---
Un problema recurrente y común en aplicaciones que ejecutan procesos largos o pesados es el bloqueo de la interfaz de usuario, sinónimo de lentitud y en general de una experiencia de usuario pobre. No hay nada peor para el usuario de una aplicación que pulsar un botón o hacer doble clic sobre un elemento y no tener la certeza de que la acción se ha llevado a cabo. Esto sucede cuando la interfaz no muestra nada, ningún indicador de progreso ni signo de cambio, provocando que el usuario tenga o intente repetir la misma acción. Esta situación seguro que os es bastante familiar a muchos de vosotros y es también una situación que debemos evitar a toda costa.

Una forma de mejorar la percepción del usuario es añadir un elemento que indique que se está realizando una operación, por ejemplo, un barra de progreso, un mensaje informativo, etc. De entre todas las opciones que tenemos a nuestro alcance, la más sencilla es modificar el cursor del ratón para que muestre el estado ocupado. Algo muy simple, ¿verdad? En esta entrada no voy a tratar de la forma en que el proceso debe ser lanzado fuera del _thread_ de UI, sino de las posibilidades que tenemos para cambiar el cursor al ejecutar un proceso largo, terminando con la opción que considero óptima, utilizando un aspecto con **PostSharp**.

Imaginemos que tenemos un método que realiza una serie de operaciones: llamadas a servicios web, consultas a bases de datos, procesos de cálculo masivo, etc. En definitiva, lo que tendremos al final es un método que hará, entre otras cosas, lo siguiente: tardar.

public void VeryHardProcess () { // Un falso proceso largo System.Threading.Thread.Sleep(3000); } </pre>

¿De qué forma podemos cambiar el cursor del ratón dada está situación? La primera idea que nos viene a todos es cambiar el cursor al principio de del proceso y devolverlo a su estado original justo después de la ejecución del proceso, antes del fin del método. Este planteamiento, como resulta evidente, tiene una serie de inconvenientes, el primero es que si el proceso lanza una excepción, nunca se restablecerá el cursor. Aunque esto se podría solucionar mediante una serie de alternativas (que no quiero ni mencionar), como imaginaréis, son implementaciones nada atractivas.

Lo que vamos a hacer es una clase para cambiar el cursor para utilizando la propiedad **OverrideCursor** de la clase **Mouse** y pasando parámetro al constructor el cursor que queremos establecer. Pero lo interesante de nuestra clase es que la vamos a hacer que implemente **IDisposable** y en el método **Dispose** vamos a restaurar el valor anterior del cursor. La clase quedaría de la siguiente forma.

public class BusyCursor : IDisposable
{
  private readonly Cursor \_previous;

  public BusyCursor(Cursor newcursor)
  {
    \_previous = Mouse.OverrideCursor;
    Mouse.OverrideCursor = newcursor;
  }

  public void Dispose()
  {
    Mouse.OverrideCursor = \_previous;
  }
}

Ahora la forma de utilizar la clase resulta evidente, tenemos que hacer uso de la instrucción [using](http://msdn.microsoft.com/es-es/library/yh598w02(v=vs.80).aspx) proporcionando una nueva instancia de nuestra clase **BusyCursor**.

public void VeryHardProcess ()
{
  using (new BusyCursor(Cursors.Wait))
  {
    System.Threading.Thread.Sleep(3000);
  }
}

Para simplificar la llamada y no tener que declarar explícitamente una nueva instancia, podríamos encapsular esta implementación haciendo una clase con una propiedad estática que devuelva una instancia de **BusyCursor** con el cursor predeterminado. Más o menos de la siguiente forma:

public class UICursor
{
  static public BusyCursor Busy
  {
    get { return new BusyCursor(Cursors.Wait); }
  }
}

Así que ahora para cambiar el cursor solo debemos hacer lo siguiente:

public void VeryHardProcess ()
{
  using (UICursor.Busy)
  {
    System.Threading.Thread.Sleep(3000);
  }
}

Pero hay algo que todavía no acaba de quedar bien. ¿Qué es lo que tenemos ahora? Tenemos un método de negocio ensuciado por una lógica para la gestión del cursor. Aquí es donde la programación orientada a aspectos, los aspectos en general, y **PostSharp** en particular nos echan la mano que necesitamos. En otra entrada anterior ([Threading mediante aspectos con PostSharp](/threading-mediante-aspectos-con-postsharp/)) ya hablé de **PostSharp**, si necesitáis más información podéis leerla o ir directamente a la [página de los creadores](http://www.sharpcrafters.com/). Básicamente, y resumiendo mucho, los aspectos nos proporcionan una forma de aplicar un comportamiento predeterminado a nuestras clases aplicando atributos.

Para nuestro caso, necesitamos un atributo que intercepte la llamada al método y que en la invocación encapsule toda la implementación del método dentro de la instrucción **using**.

\[Serializable\]
public class BusyCursorAttribute : MethodInterceptionAspect
{
  public override void OnInvoke(MethodInterceptionArgs args)
  {
    using (UICursor.Busy)
    {
      args.Proceed();
    }
  }
}

Ahora solo tenemos que aplicar nuestro nuevo atributo al método y eliminar el uso del **using**.

\[BusyCursor\]
public void VeryHardProcess ()
{
  // Un falso proceso largo
  System.Threading.Thread.Sleep(3000);
}


¡Y ya está!, una vez más hemos visto como los aspectos con **PostSharp** nos han ayudado a limpiar nuestro código, dejando visible en el método únicamente lo que nos interesa, la funcionalidad de negocio, y aislando el código de gestión del cursor, algo transversal en toda la aplicación, en una clase separada. Además podremos añadir este aspecto en otros métodos simplemente añadiendo una línea de código.
