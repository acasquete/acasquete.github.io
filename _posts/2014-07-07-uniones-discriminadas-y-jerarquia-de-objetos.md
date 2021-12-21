---
title: Uniones discriminadas y jerarquía de objetos
tags: [fsharp, functional_programming]
reviewed: true
---
Durante las próximas entradas vamos realizar un repaso de los conceptos más importantes de la programación funcional con F#. Hoy comenzamos con las **uniones discriminadas**.

Las uniones discriminadas son uno de los tipos de datos funcionales más importantes, en los que los valores están limitados a un conjunto cerrado de valores y, en la práctica, se utilizan para representar una **jerarquía de objetos**, una **estructura en árbol** o para **reemplazar las abreviaturas de tipos**.

![Propósito de uso de las uniones discriminadas](/img/uniones-discriminadas-usos.png)

Para definir una unión discriminada, al igual que con otros tipos, tenemos que utilizar la palabra clave **type** seguida del nombre del tipo y cada caso de unión separado con una barra vertical (|). Por ejemplo, los distintos tipos de empleados de una empresa pueden ser representados con la siguiente unión discriminada.

```csharp
type Employee =
| Consultant
| Manager
| Director
```

Cada caso de unión recibe el nombre de discriminador y también es posible definirlos en línea omitiendo la barra antes del primer caso de unión.

```csharp
    type Employee = Consultant | Manager | Director
``` 

Además de las reglas usuales para la nomenclatura de los identificadores, los casos de unión tienen una regla adicional. **Si un nombre de un caso de unión no comienza con una letra mayúscula, el compilador devolverá un error**. El motivo de esta restricción es poder ayudar al compilador a diferenciar los casos de unión de otros identificadores en _pattern matching_.

Aunque en un primer momento la sintaxis de las uniones discriminadas nos puede recordar a la de las enumeraciones, las semejanzas no van más lejos. Recordemos que una enumeración se define de la siguiente forma.

```csharp
type Employee =
| Consultant = 1
| Manager = 2
| Director = 3
```  

La principal diferencia entre estos dos tipos, a parte de que las uniones discriminadas son un tipo de referencia y las enumeraciones de valor, es que estas últimas no ofrecen una garantía de seguridad. Es decir, es posible crear una instancia de un tipo de enumeración con un valor que no está asociado con una de las constantes con nombre. Siguiendo el ejemplo anterior, podríamos crear una instancia de **Employee** con un valor no definido.

```csharp
let noEmployee = enum&lt;Employee&gt;(4)
```  

Por el contrario, los valores válidos para las uniones discriminadas son solo sus casos de unión. Si intentamos asignar cualquier otro valor, obtendremos un error de compilación.

Otra diferencia entre las dos construcciones es que las enumeraciones solo pueden contener un solo elemento mientras que las uniones discriminadas pueden mantener una tupla de datos. En el siguiente ejemplo se define una unión discriminada en la que cada caso de unión tiene asociado una instancia de Person que está indicado por la palabra clave **of**.

```csharp
type Person = { FirstName : string; LastName : string }

type Employee = 
    | Consultant of Person
    | Manager    of Person
    | Director   of Person
```
    

Y podemos crear instancias de cada caso del tipo Employee de la siguiente forma.

```csharp
let employeeC = Consultant ({ FirstName = "Roger"  ; LastName = "Evans" })
let employeeM = Manager    ({ FirstName = "Arthur" ; LastName = "Scott" })
let employeeD = Director   ({ FirstName = "Henry"  ; LastName = "Wood"  })
```  

En estos ejemplos estamos asociando con un solo dato, pero, como hemos dicho anteriormente, es posible asociar cada caso de unión con múltiples valores. Por ejemplo, podemos asociar el caso **Director** con un dato adicional de tipo entero para indicar el número de asistentes. En el siguiente ejemplo, vemos como haciendo uso de la sintaxis de tupla es posible asociar múltiples valores con un caso.

```csharp
type Employee = 
    | Consultant of Person
    | Manager    of Person
    | Director   of Person * int

let employeeD = Director   ({ FirstName = "Henry"  ; LastName = "Wood"  }, 2)
````

A pesar de utilizar la sintaxis de tupla, los casos se compilan a una propiedad que sigue el patrón Item1, Item2. Si queremos utilizar una tupla como tipo de dato, tenemos que colocar los tipos entre paréntesis. Si escribimos (Person \* int) en lugar de Person \* int, el compilador sí que lo tratará como una tupla real.

El mayor problema con esta sintaxis para asociar múltiples valores es que no se puede saber que representa cada valor, sin embargo, es posible definir un nombre para cada campo.

```csharp
type Employee = 
    | Consultant of Person
    | Manager    of Person
    | Director   of Person * Assistants: int
```    

De esta forma las etiquetas aparecen en Intellisense y además podemos utilizar los argumentos con nombre de la siguiente forma:

```csharp
    let employeeD = Director ({ FirstName = "Henry"  ; LastName = "Wood"  }, Assistants = 2)
```

Clases y herencia de la jerarquía de objetos
--------------------------------------------

Las uniones discriminadas se utilizan habitualmente para sustituir las clases y la herencia al representar una jerarquía de objetos. Si inspeccionamos el compilado del tipo Employee que hemos definido en la sección anterior, veremos una clase abstracta **Employee** con las propiedades **IsConsultant**, **IsManager**, **IsDirector** y tres \*Factory methods \*(**NewConsultant**, **NewManager** y **NewDirector**) para la construcción de las instancias de todos los subtipos. De la misma forma, para cada caso de unión se genera una clase anidada que hereda de la clase de unión. En estas clases se definen las propiedades y los campos para cada uno de los valores asociados con un constructor interno. Si hemos definido las clases de unión con un nombre las propiedades utilizarán ese nombre, y en caso contrario utilizaran el nombre Item, o Item1, Item2, etc… en el caso de que tengamos varios valores asociados con algún caso.

Aunque, como vemos, es posible replicar la funcionalidad de las uniones discriminadas mediante orientación a objetos, no existe un tipo de estructura equivalente en otros lenguajes .NET. Además, las más de 250 líneas de código generado nos pueden dar una idea de que no es algo sencillo.

Estructura en árbol
-------------------

Como se ha comentado al principio, otro de los usos de las uniones discriminadas es la creación de estructuras en árbol. Siguiendo el mismo ejemplo de la jerarquía de empleados podríamos generar la siguiente estructura en la que se representa el organigrama de una empresa.

```csharp
type Employee = 
    | Consultant of Person
    | Manager    of Person * Reports: Employee list
    | Director   of Person * Reports: Employee list * Assistants: int
```

Como vemos, los datos asociados con un caso de unión se pueden auto-referenciar, es decir, pueden ser otro caso de la misma unión. En ejemplo anterior, los casos **Manager** y **Director** tienen asociado un valor de tipo **Person** y una lista de valores de tipo **Employee**.

Podemos definir una estructura completa de la siguiente forma:

```csharp
let boss = 
    Director   ({ FirstName = "Andrew"  ; LastName = "Fuller"  }, Assistants = 2,
    Reports = [ 
    Manager   ({ FirstName = "Nancy"  ; LastName = "Davolio"  }, Reports = [ ] )
    Manager   ({ FirstName = "Janet"  ; LastName = "Leverling"  }, 
        Reports = [ 
        Consultant   ({ FirstName = "Tim"  ; LastName = "Smith"  } )
        ] )
    Manager   ({ FirstName = "Margaret"  ; LastName = "Peacock"  }, Reports = [ ] )
    Manager   ({ FirstName = "Steven"  ; LastName = "Buchanan"  }, 
        Reports = [ 
        Consultant   ({ FirstName = "Caroline"  ; LastName = "Patterson"  } )
        Consultant   ({ FirstName = "Robert"  ; LastName = "King"  } )
        Consultant   ({ FirstName = "Anne"  ; LastName = "Dodsworth"  } ) ] )
    Manager   ({ FirstName = "Laura"  ; LastName = "Callahan"  }, Reports = [ ] )
    Manager   ({ FirstName = "Albert"  ; LastName = "Hellstern"  }, Reports = [ ] )
    Manager   ({ FirstName = "Justin"  ; LastName = "Justin"  }, 
        Reports = [ 
        Consultant   ({ FirstName = "Xavier"  ; LastName = "Martin"  } ) ] ) 
    ])
```

Ahora, para mostrar la estructura por la consola podemos definir una función recursiva con una expresión para manejar cada caso de unión de esta forma:

```csharp
let rec print level employee  =
    match employee with
    | Director (person, reports, assistants) -> 
        printf "%s %d - %s %s (%d assistant) \n" (String.replicate level "\t") level person.FirstName person.LastName assistants
        reports |> Seq.iter (fun x -> x |> print (level + 1) )
    | Manager (person, reports) -> 
        printf "%s %d - %s %s \n" (String.replicate level "\t") level person.FirstName person.LastName
        reports |> Seq.iter (fun x -> x |> print (level + 1))
    | Consultant (person) -> 
        printf "%s %d - %s %s \n" (String.replicate level "\t") level person.FirstName person.LastName
```

Si ejecutamos la función **print** pasando el objeto **boss**, el resultado que obtendremos en la consola será el siguiente.

```csharp
> boss |> print 1;;
        1 - Andrew Fuller (2 assistant) 
            2 - Nancy Davolio 
            2 - Janet Leverling 
                3 - Tim Smith 
            2 - Margaret Peacock 
            2 - Steven Buchanan 
                3 - Caroline Patterson 
                3 - Robert King 
                3 - Anne Dodsworth 
            2 - Laura Callahan 
            2 - Albert Hellstern 
            2 - Justin Justin 
                3 - Xavier Martin 
val it : unit = ()
```

Miembros adicionales
--------------------

Al igual que los _record types_, las uniones discriminadas también permiten definir miembros adicionales. Por ejemplo, podemos redefinir la función **print** como un método en la unión discriminada **Employee** de la siguiente forma:

```csharp
type Employee = 
    | Consultant of Person
    | Manager    of Person * Reports: Employee list 
    | Director   of Person * Reports: Employee list * Assistants : int
    member employee.Print level =
        match employee with
        | Director (person, reports, assistants) -> 
            printf "%s %d - %s %s (%d assistant) \n" (String.replicate level "\t") level person.FirstName person.LastName assistants
            reports |> Seq.iter (fun x -> x.Print (level + 1) )
        | Manager (person, reports) -> 
            printf "%s %d - %s %s \n" (String.replicate level "\t") level person.FirstName person.LastName
            reports |> Seq.iter (fun x -> x.Print (level + 1))
        | Consultant (person) -> 
            printf "%s %d - %s %s \n" (String.replicate level "\t") level person.FirstName person.LastName
```

Y podemos llamar a este método de la misma forma que llamamos a un método en cualquier otro tipo.

```csharp
boss.print(1)
```

Resumen
-------

La unión discriminada es uno de los tipos de datos funcionales que nos ayudan a escribir un código más claro, menos propenso a errores y con el que podemos representar fácilmente una jerarquía de objetos o una estructura en árbol.

Si quieres saber más sobre la programación funcional, puedes ver el [webcast que presenté hace unos meses](http://vimeo.com/88283954) junto a [@_jmgomez_](http://twitter.com/_jmgomez_) de introducción a F#.
