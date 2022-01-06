---
title: Comenzando con Entity Framework en MVVM
tags: [programming]
reviewed: true
---
En las dos entradas anteriores sobre el [patrón MVVM](/tag/mvvm) vimos [cómo realizar una implementación básica del patrón MVVM en WPF](/otra-implementacion-basica-del-patron-mvvm) y [cómo hacer pruebas unitarias con ayuda del patrón Service Locator](/tests-unitarios-con-messagebox-en-mvvm). Esta vez me centraré en el uso de **Entity Framework** como modelo de nuestra aplicación, y para mostrarlo voy a partir del mismo proyecto de ejemplo que he utilizado en las anteriores ocasiones.

Con Entity Framework podemos generar un modelo conceptual desde tres enfoques distintos: a partir una base de datos existente (llamado enfoque _database-first_), partiendo desde cero, comenzando con un modelo vacío (enfoque _model-first_), o utilizando entidades POCO (Plain Old CLR Objects) que es el llamado enfoque _code-first_. Tengo que recordar también que no sólo en el diseño _code-first_ podemos hacer uso de entidades POCO, pero esto ya es un tema para otro post. En este primer ejemplo con EF voy a utilizar el enfoque **database-first**, en el que generamos el modelo a partir de una base de datos, que en esta ocasión será la base de datos **AdventureWorksLT**, una versión simplificada de **AdventureWorks** y que también está disponible para descargar en [Codeplex](http://msftdbprodsamples.codeplex.com/).

Ahora que ya sabemos de dónde va a partir nuestro modelo, definamos nuestro objetivo. Es algo bien sencillo, vamos a añadir en nuestra aplicación de ejemplo la posibilidad de consultar y modificar la tabla _Customer_ y sus tablas relacionadas _CustomerAddress_ y _Address_. Vamos a ver cómo conseguirlo sin complicaciones…

Comenzamos añadiendo un nuevo proyecto de biblioteca de clases a la solución con el nombre **BasicMVVM.Models**, en el que vamos a agregar un elemento **ADO.NET Entity Data Model**. Al seleccionarlo, nos aparece el asistente preguntándonos si queremos crear un modelo vacío o desde una base de datos. Seleccionamos ‘Generar desde Base de datos’ y creamos una nueva conexión con nuestro servidor en el que tenemos que tener la base de datos **AdventureWorksLT2008**. Una vez creada la conexión, seleccionamos la tablas **Customer**, **CustomerAddress** y **Address**. Al finalizar el proceso tendremos el modelo generado tal y como aparece en la imagen. Este modelo no lo tendremos que modificar más para nuestro ejemplo.

Volvamos ahora al proyecto de capa de presentación, al proyecto **BasicMVVM**. Creamos una nueva vista (Data.xaml) en la que vamos a añadir los controles necesarios para mostrar el contenido de la tabla _Customer_ y _CustomerAddress_, poder realizar una sencilla búsqueda y modificar varios campos de la entidad _Customer_. El código XAML de la vista queda de la siguiente forma.

```xml
<Window x:Class=”BasicMVVM.Views.Data” xmlns=”http://schemas.microsoft.com/winfx/2006/xaml/presentation” xmlns:x=”http://schemas.microsoft.com/winfx/2006/xaml” xmlns:vm=”clr-namespace:BasicMVVM.ViewModels” Title=”Sample EF” Height=”500” Width=”750” ResizeMode=”CanResize”>

<Window.DataContext> 
  <vm:Data /> 
</Window.DataContext>

<TabControl Margin=”10”> 
  <TabItem Header=”Data”> 
    <Grid>
      <Grid.ColumnDefinitions> 
        <ColumnDefinition Width=”70_” /> <ColumnDefinition Width=”30_” /> 
      </Grid.ColumnDefinitions> 
      <Grid.RowDefinitions> 
        <RowDefinition Height=”Auto” /> 
        <RowDefinition Height=”50_” /> <RowDefinition Height=”50_” /> <RowDefinition Height=”20” /> 
      </Grid.RowDefinitions> 
      
      <Expander Header=”Search Filter” Grid.ColumnSpan=”2” IsExpanded=”True”>
        <StackPanel Orientation=”Horizontal” Margin=”10”>
          <Label Content=”Name” /> 
        <TextBox Height=”23” Width=”300” Text=”{Binding SearchName, UpdateSourceTrigger=PropertyChanged}”/> <Button Content=”Search” Width=”75” Command=”{Binding SearchCommand}” /> <CheckBox Content=”Instant Search” Height=”16” IsChecked=”{Binding InstantSearch}” /> </StackPanel>
      </Expander> 
      <ListView Grid.Row=”1” ItemsSource=”{Binding CustomersCollection}” IsSynchronizedWithCurrentItem=”True”>
        <ListView.View>
          <GridView>
            <GridViewColumn Header=”First Name” DisplayMemberBinding=”{Binding FirstName}”/>
            <GridViewColumn Header=”Last Name” DisplayMemberBinding=”{Binding LastName}”/>
            <GridViewColumn Header=”Company Name” DisplayMemberBinding=”{Binding CompanyName}”/>
            <GridViewColumn Header=”Entity State” DisplayMemberBinding=”{Binding EntityState}”/>
          </GridView> 
        </ListView.View>
      </ListView>

      <ListView Margin="0,10,0,0"
        Grid.Row="2"
        ItemsSource="{Binding CurrentCustomer.CustomerAddress}"
        IsSynchronizedWithCurrentItem="True">
          <ListView.View>
            <GridView>
              <GridViewColumn Header="AddressLine1" DisplayMemberBinding="{Binding FirstName}"/>
              <GridViewColumn Header="Entity State" DisplayMemberBinding="{Binding EntityState}"/>
            </GridView>
          </ListView.View>
      </ListView>
    
      <StatusBar Grid.Row="3" Grid.ColumnSpan="2">
          <TextBlock Text="{Binding Panel1StatusBar}"/>
          <Separator/>
          <TextBlock Text="{Binding Panel2StatusBar}"/>
      </StatusBar>
    
      <StackPanel Grid.Column="1" Grid.Row="1" Margin="10" Grid.RowSpan="2"
                  DataContext="{Binding CurrentCustomer}">
          <Label Content="First Name"/>
          <TextBox Text="{Binding FirstName}" />
          <Label Content="Last Name"/>
          <TextBox Text="{Binding LastName}"/>
          <Label Content="Company Name"/>
          <TextBox Text="{Binding CompanyName}" />
          <Button Content="Update Entity" />
      </StackPanel>
    </Grid>
  </TabItem>   
</TabControl> 
</Window>
```

Una vez ya tenemos la vista creada, vamos a crear el **ViewModel** correspondiente. Añadimos una referencia al proyecto **BasicMVVM.Models** y creamos una nueva clase (Data) que herede de **ViewModelBase**, nuestra clase base para los **ViewModels**. Para comenzar creamos una propiedad ObservableCollection y en el constructor del ViewModel creamos una instancia del contexto de base de datos e inicializamos la instancia de la ObservableCollection con la lista de clientes.
    
```cs
public class Data : ViewModelBase
{
  private readonly AdventureWorksLT2008Entities DbContext;
  private ObservableCollection<Customer> _CustomersCollection;

  public ObservableCollection<Customer> CustomersCollection
  {
    get
    {
      return _CustomersCollection;
    }
    set
    {
      _CustomersCollection = value;
      NotifyPropertyChanged("CustomersCollection");
    }
  }

  public Data()
  {
    DbContext = new AdventureWorksLT2008Entities();
    CustomersCollection = new ObservableCollection<Customer>(from c in DbContext.Customers
    select c);
  }
}
```

Si ejecutamos la aplicación, el **ListView** mostrará el contenido de la tabla _Customer_ ya que tiene un _binding_ con la propiedad **CustomersCollection**. Llegado este momento, nos paramos un instante para resolver un problema que ya hemos provocado. Si intentamos modificar la vista veremos que nos salta una excepción **ArgumentException** con el mensaje «The specified named connection is either not found in the configuration, not intended to be used with the EntityClient provider, or not valid» o en castellano «La conexión con nombre especificada no se encuentra en la configuración, no es apropiada para ser utilizada con el proveedor de EntityClient, o no es válida». Esto sucede porque estamos estableciendo la conexión en el contructor del ViewModel y el diseñador, al cargar el XAML, intenta crear una instancia e intenta leer la información de conexión del fichero de configuración, pero en tiempo de diseño la aplicación es el propio Visual Studio y su fichero de configuración obviamente no contiene esta información.

Podemos solucionar este problema de varias formas. La más sencilla es añadir el código necesario para comprobar si estamos en tiempo de diseño. Esto lo conseguimos modificando el constructor de la siguiente manera.

```cs
public Data()
{
  if (DesignerProperties.GetIsInDesignMode(new DependencyObject()))
  {
    return;
  }

  DbContext = new AdventureWorksLT2008Entities();
  CustomersCollection = new ObservableCollection<Customer>(from c in DbContext.Customers select c);
}
```

Con esta modificación el contructor no realizará ninguna acción en tiempo de diseño, pero podemos hacer que haga algo más interesante como, por ejemplo, mostrar unos datos de muestra para comprobar que el _Binding_ se está realizando correctamente, además podemos hacer uso de las directivas del compilador y la compilación condicional para evitar que este código se compile en modo _Release_.

```cs
public Data()
{
#if DEBUG
  if (DesignerProperties.GetIsInDesignMode(new DependencyObject()))
  {
    CustomersCollection = new ObservableCollection<Customer> {
      new Customer { FirstName="John", LastName="Doe", CompanyName="Nomen nescio" },
      new Customer { FirstName="Jane", LastName="Doe", CompanyName="Nomen nescio" }
    };
    return;
  }
#endif               
  DbContext = new AdventureWorksLT2008Entities();
  CustomersCollection = new ObservableCollection<Customer>(from c in DbContext.Customers 
  select c);
}
```

Continuamos añadiendo la funcionalidad de búsqueda a nuestra pequeña demostración. En el ViewModel añadimos la propiedad SearchName, un ICommand (SearchCommand) para el botón y un método que actualizará la lista de clientes según el contenido del campo.

```cs
public string SearchName { get; set; }

public ICommand SearchCommand
{
  get
  {
    this._searchCommand = new RelayCommand()
    {
      CanExecuteDelegate = p => true,
      ExecuteDelegate = p => Search()
    };
    return this._searchCommand;
  }
}

private void Search()
{
  CustomersList = new ObservableCollection<Customer>(from c in DBContext.Customers
    where c.FirstName.Contains(NameSearch) || c.LastName.Contains(NameSearch)
    select c);
}
```

Si ejecutamos la aplicación veremos que al pulsar el botón _Search_ el resultado del _ListView_ se actualiza. Sin embargo, esto no es lo óptimo, ya que estamos realizando una consulta al servidor SQL en cada petición, cuando en realidad ya tenemos todos los resultados y solo deberíamos filtrarlos. Esto lo solucionamos utilizando un objeto **ICollectionView** y el metodo **GetDefaultView** de la clase **CollectionViewSource**, que nos devuelve un objeto **ICollectionView**. Modificamos el constructor y el método _Search_ de la siguiente forma:

```cs
public Data()
{
#if DEBUG
        ...
#endif               
  DbContext = new AdventureWorksLT2008Entities();
  CustomersCollection = new ObservableCollection<Customer>(from c in DbContext.Customers 
  select c);

  _CustomersView = CollectionViewSource.GetDefaultView(CustomersCollection);

}

private void Search()
{
  _CustomersView.Filter = c => ((Customer)c).FirstName.Contains(SearchName) ||
  ((Customer)c).LastName.Contains(SearchName);
}
```

El siguiente paso que vamos a dar es añadir una búsqueda instantánea, es decir que el resultado de la búsqueda se actualice cada vez que escribamos un carácter en el **TextBox**. Si nos fijamos en el XAML de la vista, en el **TextBox** utilizamos la propiedad **UpdateSourceTrigger** para indicar que actualice el origen del _Binding_ cada vez que se produzca algún cambio en el **TextBox** en lugar de al perder el foco, que es su comportamiento predeterminado.

```xml
<Label Content="Name" />
<TextBox Height="23" Width="300" Text="{Binding SearchName, UpdateSourceTrigger=PropertyChanged}"/>
<Button Content="Search" Width="75" Command="{Binding SearchCommand}" />
<CheckBox Content="Instant Search" Height="16" IsChecked="{Binding InstantSearch}" />
```

Ahora solo tenemos que crear la propiedad _InstantSearch_ para enlazar con la propiedad **IsChecked** del **CheckBox** y modificar la propiedad **SearchName** para que llame al método _Search_ en el descriptor de acceso **set**.

```cs
public bool InstantSearch { get; set; }

private string _searchName = "";

public string SearchName
{
  get
  {
    return _searchName;
  }
  set
  {
    _searchName = value;
    if (InstantSearch) this.Search();
  }
}
```

Nos centramos ahora en la actualización de la entidad _Customer_. Vamos a enlazar los **TextBox** de la derecha para que muestren el valor del elemento seleccionado en el **ListView**. Para conseguir esto, vamos a hacer uso del evento **CurrentChanged** del objeto **ICollectionView**. Este evento se lanza cada vez que cambia la propiedad **CurrentItem** del ListView.

Creamos la propiedad _CurrentCustomer_ que devuelva el _CurrentItem_ del **ICollectionView**.

```cs
public Customer CurrentCustomer
{
  get
  {
    if (_CustomersView == null)
    {
      return new Customer();
    }
    else
    {
      return _CustomersView.CurrentItem as Customer;
    }
  }
}
```

y añadimos en el constructor el tratamiento para cuando se lance el evento **CurrentChanged** se notifique un cambio de la propiedad _CurrentCustomer_.

```cs
_CustomersView.CurrentChanged += (sender, e) => { NotifyPropertyChanged("CurrentCustomer"); };
```

Ahora al seleccionar un elemento del **ListView** aparecerá el valor de los campos FirstName, LastName y CompanyName a la derecha y si modificamos alguno de ellos, el cambio se verá reflejado en la lista. Hay que tener en cuenta que para que esto funcione la propiedad **IsSynchronizedWithCurrentItem** del **ListView** debe estar a **True**.

El siguiente paso es actualizar la base de datos. Añadimos a nuestro ViewModel los tres comandos para añadir una nueva entidad, borrar la entidad actualmente seleccionada y guardar todos los cambios.

```xml
<Button Content="Add Customer" Command="{Binding AddCustomer}" />
<Button Content="Delete Customer" Command="{Binding DeleteCustomer}" />
<Button Content="Save Changes" Command="{Binding SaveChanges}" />
```

```cs
private ICommand _AddCustomer;
private ICommand _DeleteCustomer;
private ICommand _SaveChanges;

public ICommand AddCustomer
{
  get
  {
    this._AddCustomer = new RelayCommand()
    {
      CanExecuteDelegate = p => true,
      ExecuteDelegate = p =>
      {
        Customer nc = new Customer
        {
            FirstName = "NewCustomer",
            LastName = "NewCustomer",
            PasswordHash = "",
            PasswordSalt = "",
            rowguid = Guid.NewGuid(),
            ModifiedDate = DateTime.Now
        };

        this.CustomersCollection.Add(nc);
        DbContext.Customers.AddObject(nc);
        _CustomersView.Refresh();
      }
    };
    return this._AddCustomer;
  }
}

public ICommand DeleteCustomer
{
  get
  {
    this._DeleteCustomer = new RelayCommand()
    {
      CanExecuteDelegate = o => CurrentCustomer != null,
      ExecuteDelegate = o =>
      {
        if (CurrentCustomer.EntityKey != null)
        {
            DbContext.Customers.DeleteObject(CurrentCustomer);
            _CustomersView.Refresh();
        }
      }
    };
    return this._DeleteCustomer;
  }
}    

public ICommand SaveChanges
{
  get
  {
    this._SaveChanges = new RelayCommand()
    {
        CanExecuteDelegate = p => true,
        ExecuteDelegate = p =>
        {
          DbContext.SaveChanges();
          _CustomersView.Refresh();
        }
    };
    return this._SaveChanges;
  }
}
```

Después de cada operación llamo al método Refresh del objeto **ICollectionView** para actualizar la lista. Si nos fijamos, el _ListView_ tiene una columna para mostrar el valor de la propiedad _EntityState_ de la entidad. Veremos que este valor puede tomar alguno de los siguientes valores al realizar las distintas operaciones CRUD.

**Detached:** Indica que el objeto existe, pero no se está realizando seguimiento de cambios. **Unchanged:** El objeto no ha sido modificado desde que se cargó en el contexto, o desde el último SaveChanges. **Added:** El objeto se ha añadido al contexto. **Deleted:** El objeto se ha eliminado del contexto. **Modified:** El objeto se ha modificado.

Para terminar, sólo queda comentar que para enlazar el otro ListView con la entidad _Address_, solo tenemos que definir el enlace de la propiedad **ItemsSource** a **CurrentCustomer.CustomerAddresses**.

```xml
<ListView Margin="0,10,0,0" Grid.Row="2" ItemsSource="{Binding CurrentCustomer.CustomerAddresses}">
  <ListView.View>
    <GridView>
      <GridViewColumn DisplayMemberBinding="{Binding AddressType}" Header="Address Type" />
      <GridViewColumn DisplayMemberBinding="{Binding Address.AddressLine1}" Header="Address" />
      <GridViewColumn DisplayMemberBinding="{Binding Address.City}" Header="City" />
      <GridViewColumn DisplayMemberBinding="{Binding EntityState}" Header="Entity State" />
    </GridView>
  </ListView.View>
</ListView>
```

Y hasta aquí esta primera toma de contacto con el modelo de Entity Framework. Hemos hecho un acercamiento muy básico al uso de EF en una aplicación MVVM utilizando el enfoque más sencillo, *Database-First*. En próximas entradas veremos los otros dos enfoques (*Model-First* y *Code-only*) y cómo realizar un desarrollo en diferentes capas físicas.

**Descarga código fuente:**  
[BasicMVVM-EntityFramework.zip](/files/BasicMVVM-EntityFramework.zip)
