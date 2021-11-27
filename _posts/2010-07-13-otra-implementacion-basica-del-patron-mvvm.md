---
title: Otra implementación básica del patrón MVVM
tags: []
---
Desde hace unos días estoy preparando el examen de certificación en desarrollo de aplicaciones Windows, y ha sido buscando información sobre patrones de capa de presentación, cuando me he percatado de la gran cantidad de implementaciones y _frameworks_ de **MVVM** que existen para **\*\*WPF**\*\* y **Silverlight**. Muchas veces, sin embargo, tener tantas opciones desconcierta a los nuevos desarrolladores, primero por no conocer las diferencias entre cada una de estas opciones, pero sobre todo porque generalmente los ejemplos de implementación no son sencillos o, incluso, contienen errores.

Con esta entrada voy a iniciar una serie dedicada a explicar las distintas implementaciones del **patrón MVVM** existentes, los principales problemas que nos podemos encontrar y cómo los _frameworks_ de **MVVM** nos pueden ayudar a resolverlos. Para comenzar, vamos a sentar las bases y en esta entrada veremos la implementación básica del patrón de presentación en una sencilla aplicación de demostración.

El proyecto WPF del que partimos va a consistir en una vista (ventana) con cinco controles: cuatro controles _Button_ y un control _ComboBox_. Los botones realizarán cuatro acciones: modificar y restablecer el título de la ventana y añadir y eliminar elementos al _ComboBox_. Al seleccionar un elemento del _ComboBox_ se mostrará la descripción, valor y fecha de creación del elemento.

El **patrón MVVM** se caracteriza por no utilizar el _code-behind_ de la vista para realizar una acción de negocio, que siempre debe ser una responsabilidad del **ViewModel**. En nuestro ejemplo, la vista no tiene ni siquiera el fichero de _code-behind_, aunque podemos encontrar algunas implementaciones que utilizan este código para establecer el _DataContext_. Otra característica es que la vista siempre se comunica con el **ViewModel** mediante _binding_, utilizando la propiedad _Command_ de los controles.

Comenzamos creando nuestra clase **ViewModel** con la propiedad _Title_, a la que le asignaremos un valor en el constructor de la clase. Como es evidente, esto no es una acción de negocio, este código podría ir perfectamente en la vista, pero nos sirve a modo de ejemplo.

class ViewModel { public string Title { get; set; }

    public ViewModel()
    {
        Title = "My title";
    } }</pre> Ahora creamos la vista a la que añadiremos una referencia al modelo y además indicaremos que el *DataContext* de la ventana es la clase **ViewModel** que acabamos de crear.
    

<Window x:Class="BasicMVVM.Views.View"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:viewmodel="clr-namespace:BasicMVVM.ViewModels"
        Title="{Binding Title}">

    <Window.DataContext>
        <viewmodel:ViewModel />
    </Window.DataContext>
</Window>

Si ejecutamos la aplicación, veremos que el título de la ventana se muestra correctamente. No está mal para comenzar, ¿no? ¡Continuemos añadiendo más funcionalidad!

Hagamos que al pulsar un botón, el título de la ventana cambie. Para llevar a cabo esta funcionalidad vamos a definir un comando mediante la interfaz **ICommand**. En el proyecto podemos encontrar la clase _RelayCommand_ que implementa la interfaz _ICommand_. Esta clase nos permite definir, mediante delegados, un método que se llamará cuando se invoque el comando y un método para determinar si el comando se puede ejecutar. Además la clase tiene el evento _CanExecuteChanged_, que es parte de la interfaz _ICommand_, que se lanza cuando se producen cambios que modifiquen si el comando se debe ejecutar o no y delega en el evento _CommandManager.RequerySuggested_.

public class RelayCommand : ICommand
{
    public Predicate<object> CanExecuteDelegate;
    public Action<object> ExecuteDelegate;

    public bool CanExecute(object parameter)
    {
        return CanExecuteDelegate(parameter);
    }

    public event EventHandler CanExecuteChanged
    {
        add { CommandManager.RequerySuggested += value; }
        remove { CommandManager.RequerySuggested -= value; }
    }

    public void Execute(object parameter)
    {
        ExecuteDelegate(parameter);
    }
}

Lo siguiente es definir el comando en el **ViewModel** y crear los métodos _CanUpdateTitle_, que comprueba que el título tenga menos de 50 carácteres, y el método _SetTitle_ que modifica la propiedad _Title_.

public ICommand SetTextCommand
{
    get
    {
        this.\_SetTitleCommand = new RelayCommand()
        {
            CanExecuteDelegate = c => CanUpdateTitle(),
            ExecuteDelegate    = c => SetTitle()
        };
        return this.\_SetTitleCommand;
    }
}

private bool CanUpdateTitle()
{
    return Title.Length < 50;
}

private void SetTitle()
{
    Title += " grows! ";
}

Para que todo funcione correctamente, y la vista conozca cuando se produce algún cambio en alguna propiedad, el **ViewModel** debe implementar la interfaz _INotifyPropertyChanged_ para notificar los cambios mediante el evento _PropertyChanged_.

class ViewModel : INotifyPropertyChanged 
{
    public event PropertyChangedEventHandler PropertyChanged;

    protected void NotifyPropertyChanged(String propertyName)
    {
        if (PropertyChanged != null)
        {
            PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
        }
    } 
}

Cómo esta funcionalidad es común a todos los _ViewModels_, una buena práctica es crear una clase base y hacer que todos nuestros _ViewModels_ hereden de ella. En nuestro ejemplo, por simplificar al máximo, todo está en una única clase.

Ahora, en la propiedad _Title_ debemos llamar al método _PropertyChanged_ pasando el nombre de la propiedad que se ha modificado.

public string Title
{
    get {    return \_title;}

    set
    {
        \_title = value;
        NotifyPropertyChanged("Title");
    }
}

Y crear el botón en la vista:

<Button Command="{Binding SetTitleCommand}" Content="Change Title" Name="cmdSetTitle" />

Para terminar, vamos a ver como enlazar desde la vista un control _ComboBox_.

<ComboBox DisplayMemberPath="Name" ItemsSource="{Binding Items}" Name="cmbItems" />

En la propiedad _ItemsSource_ indicamos la colección _Items_ de nuestro **ViewModel** y con la propiedad _DisplayMemberPath_ le indicamos la propiedad que debe mostrar. La colección _Items_ es una _ObservableCollection_. Añadir ahora un botón que añada un nuevo elemento a esta colección, no debería ser tarea difícil.

public ICommand AddItemCommand
{
    get
    {
        this.\_AddItemCommand = new RelayCommand()
        {
            CanExecuteDelegate = p => true,
            ExecuteDelegate    = p => AddItem()
        };
        return this.\_AddItemCommand;
    }
}

private void AddItem()
{
    Model newItem = new Model();
    newItem.Code = Items.Count == 0 ? 1 : Items\[Items.Count - 1\].Code + 1;
    newItem.Name = "Item #" + newItem.Code;

    Items.Add(newItem);
    NotifyPropertyChanged("Items");
}

Sólo queda que al seleccionar un elemento del _ComboBox_ nos muestre en un _TextBlock_ la información del elemento seleccionado. Esto lo hacemos enlazando la propiedad _SelectedItem_ del _ComboBox_ con su homónima del **ViewModel**.

<ComboBox Name="cmbItems"
    SelectedValuePath="Value" DisplayMemberPath="Name"
    ItemsSource="{Binding Items}" SelectedItem="{Binding SelectedItem}" />

<TextBlock Name="textBlock1" Text="{Binding SelectedItem}" />

Hasta aquí esta primera introducción al patrón \*\*Model View ViewModel\*\* en WPF. Como he dicho al principio, seguiré dedicando los próximos posts a la mejora de esta implementación del patrón y al funcionamiento de los muchos frameworks de \*\*MVVM\*\* que tenemos disponibles.

