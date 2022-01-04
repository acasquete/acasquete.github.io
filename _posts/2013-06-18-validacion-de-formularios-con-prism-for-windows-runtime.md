---
title: Validación de formularios con Prism for Windows Runtime
tags: [windows_store, winrt]
reviewed: true
---
Continuamos la serie de posts en el que estamos viendo las funcionalidades más interesantes que nos proporciona **Prism for Windows Runtime**. En esta ocasión vamos a ver que clases nos proporciona Prism para validar un modelo y cómo guardar el estado de validación para que pueda ser restaurado en caso de que la aplicación sea finalizada.

En la librería **Microsoft.Practices.Prism.StoreApps** tenemos dos clases que nos proporcionan todo el soporte de validación: **ValidatableBindableBase** y **BindableValidator**. ValidatableBindableBase es la clase principal que contiene la propiedad Errors, una instancia de la clase BindableValidator que contiene todos los errores de validación. Además, en la solución de referencia AdventureWorks, tenemos varias clases que nos ayudarán a resaltar visualmente los errores de validación.

La primera decisión que debemos tomar cuando queremos validar el valor de un campo, es si lo queremos hacer en el View Model o en el Model. Lo aconsejable es realizar la validación en el Model, ya que de hacerlo en el VM, muy posiblemente significará que estamos duplicando las propiedades del modelo. Para comenzar con el ejemplo más sencillo vamos a crear una clase de modelo que herede de **ValidatableBindableBase** y especificamos las reglas de validación añadiendo atributos **DataAnnotation** a las propiedades. La lista de los atributos que podemos utilizar los podéis encontrar en la documentación de [System.ComponentModel.DataAnnotations de la MSDN](http://msdn.microsoft.com/en-us/library/system.componentmodel.dataannotations(v=vs.100).aspx). Y para evitar tener que exponer todas las propiedades en el VM, se expone en el VM una instancia de la clase UserInfo.

```csharp
public class UserInfo : ValidatableBindableBase {
    private string firstName;

    [Required] 
    public string FirstName 
    { 
        get { return firstName; } 
    set { SetProperty(ref firstName, value); } } 
    }

public class UserInfoViewModel : ViewModel { 
    public MainPageViewModel() : this(new UserInfo()) 
    {

    }

    public MainPageViewModel(UserInfo userInfo) 
    { 
        this.userInfo = userInfo; 
    }

    private UserInfo userInfo;

    public UserInfo UserInfo { 
        get 
        { 
            return userInfo; 
        } 
        set 
        { 
            SetProperty(ref userInfo, value); 
        } 
    } 
}
```

En este ejemplo, solo tenemos una propiedad en el modlo que hemos marcado como obligatoria mediante el atributo **Required**. Este atributo indica que la validación fallará si el campo está nulo, contiene una cadena válida o solo espacios en blanco.

El siguiente paso es mostrar visualmente el error de validación, para esto necesitamos que en el XAML contenga tres controles: la etiqueta del campo, el textbox y un textblock para mostrar el error de validación.

```xml
<TextBlock x:Name="FirstNameTitle"
           Style="{StaticResource BasicTextStyle}"
           Text="First Name" />

<TextBox x:Name="FirstNameValue"
         Text="{Binding UserInfo.FirstName, Mode=TwoWay}"
         behaviors:HighlightFormFieldOnErrors.PropertyErrors="{Binding UserInfo.Errors\[FirstName\]}" />

<TextBlock x:Name="ErrorFirstName"
           Style="{StaticResource ErrorMessageStyle}"
           Text="{Binding UserInfo.Errors\[FirstName\], Converter={StaticResource FirstErrorConverter}}"
            />
```

Lo nuevo en este código es que estamos utilizando la _Attached Property_ **HighlightFormFieldOnErrors.PropertyErrors** y el converter **FirstErrorConverter**. La implementación de estas clases las encontraremos en la implementación de referencia **AdventureWorks**, ya que no forman parte de las DLL de Prism, así que vamos a poder modificarlas según nuestras necesidades.

La _attached property_ **PropertyErrors** está enlazada con la propiedad Errors del modelo y se utiliza para comprobar si hay errores de validación en el campo y cambiar el estilo. Concretamente se establece el estilo **HighlightFormFieldStyle** y, si no hay errores, el estilo **FormFieldStyle**. Estos dos estilos no son estándar y los tenemos que definir también en un diccionario de recursos de nuestra solución. La otra clase que se utiliza es **FirstErrorConverter**, un converter para ocultar o mostrar el TextBlock de validación dependiendo de si hay o no hay errores de validación.

Esta es la implementación sencilla, la más básica. Pero la realidad es que en las aplicaciones reales, al final las validaciones simples son las menos frecuentes.

## Validando propiedades dependientes

Lo normal es que tengamos validaciones en un campo que dependen del valor de otro campo. El ejemplo típico es el de fecha inicio y fecha fin, donde la final no puede ser inferior a la inicial. En el siguiente ejemplo voy a utilizar otro caso bastante habitual, voy a añadir al modelo las propiedades **Country** e **IBAN**, que nos servirán para guardar la nacionalidad y el número de cuenta internacional. La característica del IBAN es que comienza con dos caracteres que corresponden al código de país, así que vamos a añadir la validación para que verifique que el código comienza con el código correcto de país. No voy a implementar toda la validación de IBAN, porque para este post carece de interés.

```csharp
public string CountryCode
{
    get { return countryCode; }
    set { SetProperty(ref countryCode, value); }
}

[Required]
[CustomValidation(typeof(UserInfo), "ValidateIBAN")]
public string IBAN
{
    get { return iban; }
    set { SetProperty(ref iban, value); }
}
```

En este código hemos definido las dos nuevas propiedades, y hemos aplicado el atributo **CustomValidation** a la propiedad IBAN. Mediante este atributo podemos indicar mediante en el segundo parámetro el nombre de un método que se utilizará la propiedad donde está aplicado. **Este método de validación debe ser público y estático**.

```csharp
public static ValidationResult ValidateIBAN(object value, ValidationContext validationContext)
{
    if (value == null) { throw new ArgumentNullException("value"); }

    if (validationContext == null) { throw new ArgumentNullException("validationContext"); }

    var userinfo = (UserInfo)validationContext.ObjectInstance;

    if (!userinfo.iban.ToUpper().StartsWith(userinfo.countryCode))
    {
        return new ValidationResult("IBAN not valid");
    }

    return ValidationResult.Success;
}
```

El parámetro **ValidationContext** nos permite acceder a la instancia del modelo para obtener el valor de otra propiedad, en este caso de la propiedad _CountryCode_. Si la validación es correcta, devolvemos un **ValidationResult.Success** y si es incorrecta, una nueva instancia de **ValidationResult** pasando el mensaje de validación.

## Suspendiendo y reanudando el estado de las validaciones
    
Otro tema tan importante como el poder validar los campos de un formulario es que esas validaciones sobrevivan a una suspensión y finalización de la aplicación. Veamos como hacerlo.

Para guardar el estado, tenemos que sobrescribir el método **OnNavigatedFrom** del ViewModel y añadir el siguiente código:

```csharp
public override void OnNavigatedFrom(Dictionary<string, object> viewModelState, bool suspending)
{
    base.OnNavigatedFrom(viewModelState, suspending);

    if (viewModelState != null)
    {
        AddEntityStateValue("errorsCollection", userInfo.GetAllErrors(), viewModelState);
    }
}
```

Este método nos garantiza que cuando la aplicación se suspenda, los errores de validación se serializarán a disco. Por un lado, el método **GetAllErrors** devuelve todos los errores que contiene la clase **BindableValidator** y, por otro, el método **AddEntityStateValue** añade esa colección de errores de validación en un diccionario en el sesión state.

Y para restaurar el estado, sobrecribimos el método **OnNavigatedTo** de la siguiente forma:

```csharp
public override void OnNavigatedTo(object navigationParameter, NavigationMode navigationMode, Dictionary<string, object> viewModelState)
{
    if (viewModelState == null) return;

    base.OnNavigatedTo(navigationParameter, navigationMode, viewModelState);

    if (navigationMode == NavigationMode.Refresh)
    {
        var errorsCollection = RetrieveEntityStateValue<IDictionary<string, ReadOnlyCollection<string>>>("errorsCollection", viewModelState);

        if (errorsCollection != null)
        {
            userInfo.SetAllErrors(errorsCollection);
        }
    }
}
```

En este caso, primero estamos obteniendo la colección de errores mediante **RetrieveEntityStateValue** y lo establecemos en el **BindableValidator** mediante el método **SetAllErrors**.

## Conclusión


En esta entrada hemos vistos dos aspectos importantes que tenemos que tener en cuenta para añadir validaciones en formulario. Por un lado, hemos visto que haciendo uso de la clase **ValidatableBindableBase**, los atributos de **DataAnotation** y el _behavior_ **HighlightFormFieldOnErrors** podemos añadir fácilmente validaciones en campos y que podemos seguir utilizando el atributo **CustomValidator** para crear validaciones personalizas. Hemos visto también cómo guardar el estado de las validaciones mediante los métodos de la clase **ValidatableBindableBase** para que se pueda restaurar si la aplicación es finalizada.


## Referencias


[Validating user input in AdventureWorks Shopper](http://msdn.microsoft.com/en-us/library/windows/apps/xx130659.aspx)

