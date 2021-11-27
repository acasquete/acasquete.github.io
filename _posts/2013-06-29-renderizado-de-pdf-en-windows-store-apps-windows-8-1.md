---
title: Renderizado de PDF en Windows Store apps (Windows 8.1)
tags: [windows_store, winrt, winjs]
---
Ya tenemos aquí **Windows 8.1 Preview** y con él muchos cambios y [novedades en la API de Windows Runtime y WinJS](http://msdn.microsoft.com/library/windows/apps/bg182410). Una de las primeras novedades que he querido probar ha sido la lectura y renderizado de documentos PDF, ya que, hasta ahora, no teníamos otra forma de mostrar el contenido de un PDF en una aplicación de la Windows Store que no pasase por utilizar un motor de terceros o crearnos uno propio en C++, algo nada trivial.

Ahora con Windows 8.1 tenemos una API que nos da soporte para poder leer un fichero PDF y renderizar cada página como una imagen. En esta entrada vamos a ver cómo utilizar esta API, y cómo visualizar el contenido de un PDF con la ayuda de un FlipView.

Las clases principales que vamos a utilizar para trabajar con ficheros PDF son **PdfDocument** y **PdfPage,** definidas dentro del nuevo [namespace Windows.Data.Pdf](http://msdn.microsoft.com/en-us/library/windows/apps/windows.data.pdf.aspx). Para cargar un fichero PDF y obtener un objeto **PdfDocument**, podemos llamar a los métodos _loadFromFileAsync_ o _loadFromStreamAsync,_ dependiendo de si queremos cargar el fichero desde un _StorageFile_ o a partir de una secuencia _RandomAccessStream_. Recordemos que los objetos StorageFile se obtienen llamando a los métodos estáticos _getFileFromPathAsync_ y _getFileFromApplicationUriAsync_, o mostrando el selector de archivos (FilePicker) para que el usuario pueda elegir uno o varios archivos. En cualquiera de estos dos casos se devuelve un StorageFile que representa el archivo especificado.

En este ejemplo se muestra cómo lanzar el selector de archivos mediante FileOpenPicker.PickSingleFileAsync para que el usuario seleccione un fichero PDF. Después de obtener el StorageFile se llama a loadFromFIleAsync para cargar el documento y conseguir un objeto **PdfDocument**.

var openPicker = new Windows.Storage.Pickers.FileOpenPicker(); openPicker.viewMode = Windows.Storage.Pickers.PickerViewMode.list; openPicker.suggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.documentsLibrary; openPicker.fileTypeFilter.replaceAll(\[“.pdf”\]);

openPicker.pickSingleFileAsync().then(function (file) { if (file) {

        Windows.Data.Pdf.PdfDocument.loadFromFileAsync(file).then(function (pdfDocument) {
            renderPage(pdfDocument).then(function (result) {
                // TODO Render Document
            });
        });
    } });</pre> Tanto el método *loadFromFileAsync* como *loadFromStreamAsync *tienen una sobrecarga para indicar la contraseña en el caso de que queramos abrir un PDF protegido. Sin embargo, no tenemos un método que nos indique antes de cargarlo si el PDF está o no protegido, solo tenemos la propiedad *IsPasswordProtected *que nos indica esto, pero se establece una vez hemos cargado el PDF. Así que tendremos que solicitar la contraseña cuando la lectura del PDF falle.
    

function openFile(file, password) {
    if (file) {

        Windows.Data.Pdf.PdfDocument.loadFromFileAsync(file, password).then(function (pdfDocument) {
            // TODO Render Document
        }, function (error) {
            // TODO Ask for password
            openFile(file, "password");
        });
    }
}

Una vez tenemos cargado el documento, la forma de proceder para mostrar el contenido es iterar por todas las páginas y convertir cada una de ellas a imagen. Podemos obtener una referencia a cada página llamando al método _GetPage \*del objeto PdfDocument. Este método nos devuelve una referencia a un objeto **PdfPage** del que podemos tener acceso a su contenido en una secuencia con el método \*renderToStreamAsync_. Además, este método admite un segundo parámetro en el que podemos especificar opciones para personalizar el renderizado de las páginas. Podemos modificar el color de fondo, las dimensiones o renderizar solo una parte de la página. Para establecer estas opciones tenemos que instanciar la clase [PdfPageRenderOptions](http://msdn.microsoft.com/en-us/library/windows/apps/windows.data.pdf.pdfpagerenderoptions.aspx), establecer los valores y pasarlo como parámetro. En nuestro ejemplo no vamos a utilizar este parámetro porque queremos el renderizado predeterminado.

En el siguiente ejemplo vamos a ver cómo convertir a imagen la primera página del PDF. Para esto vamos a crear la función renderPDF, al que le pasaremos el objeto PdfDocument que hemos obtenido en el ejemplo anterior. Este método obtiene referencia a la primera página del PDF y después la secuencia mediante _renderToStreamAsync_. Una vez tenemos esta secuencia, tenemos que crear una de acceso aleatorio, mediante la clase **RandomAccessStreamReference**, con la que podremos obtener el **blob**.

function renderPage(pdfDocument) {

    var promise = WinJS.Promise.wrap(new Windows.Storage.Streams.InMemoryRandomAccessStream());

    return promise.then(function (pageStream) {
        var pdfPage = pdfDocument.getPage(0);

        return pdfPage.renderToStreamAsync(pageStream).then(function Flush() {
            return pageStream.flushAsync();
        }).then(function () {

            var renderStream = Windows.Storage.Streams.RandomAccessStreamReference.createFromStream(pageStream);
            return renderStream.openReadAsync().then(function (stream) {

                pageStream.close();
                pdfPage.close();

                var picURL = URL.createObjectURL(stream);

                return { pageIndex: 0, imageSrc: picURL };

            });
        });
    });
}

Ahora podemos asignar fácilmente la propiedad imageSrc como origen de cualquier elemento imagen.

Windows.Data.Pdf.PdfDocument.loadFromFileAsync(file).then(function (pdfDocument) {
    if (pdfDocument !== null) {
        renderPage(pdfDocument).then(function (result) {
            pdfImage.src = result.imageSrc;
        });
    }
}

Ahora, partiendo de este código en el que solo mostramos la primera página, vamos a extenderlo para mostrar todas las páginas con la ayuda de un control Flipview. La única complejidad que nos vamos a encontrar es la gestión de todas las llamadas asíncronas. Primero vamos a modificar ligeramente la función _renderPage_ para que podamos pasar como parámetro el índice de la página que queremos convertir.

function renderPage(pdfDocument, pageIndex) {

    var promise = WinJS.Promise.wrap(new Windows.Storage.Streams.InMemoryRandomAccessStream());

    return promise.then(function (pageStream) {
        var pdfPage = pdfDocument.getPage(pageIndex);

        return pdfPage.renderToStreamAsync(pageStream).then(function Flush() {
            return pageStream.flushAsync();
        }).then(function () {

            var renderStream = Windows.Storage.Streams.RandomAccessStreamReference.createFromStream(pageStream);
            return renderStream.openReadAsync().then(function (stream) {

                pageStream.close();
                pdfPage.close();

                var picURL = URL.createObjectURL(stream);

                return { pageIndex: pageIndex, imageSrc: picURL };

            });
        });
    });
}

Después creamos un método que nos carge todas las páginas en un array. Para obtener el número total de páginas del documento PDF utilizamos la propiedad **PageCount** del objeto **PdfDocument** y creamos una promise que se completará cuando se hayan convertido todas las páginas.

function loadPages(pdfDocument) {
      var promisePages = \[\];

      for (var count = 0; count < pdfDocument.pageCount; count++) {
          var promise = renderPage(pdfDocument, count).then(function (pageData) {
              return pageData;
          });
          promiseArray.push(promise);
      }

      return WinJS.Promise.join(promiseArray);
  }

Ahora solo queda hacer una lista enlazable que podamos asignar como origen de datos a un control **FlipView** y un método que rellene esta lista. Este método llama a la función _loadPages_ que hemos definido antes y cuando la promise se complete, se añade el resultado a la lista enlazable.

var pageList = new WinJS.Binding.List();

function getPageList(pdfDocument) {

    loadPages(pdfDocument).then(function (pageDataArray) {
        for (var i = 0, len = pageDataArray.length; i < len; i++) {
            var index = pageDataArray\[i\].pageIndex;
            pageList.push({ pageIndex: i, imageSrc: pageDataArray\[i\].imageSrc });
        }
    });

    return pageList;
}

Para terminar, necesitamos declarar el control **FlipView** con su correspondiente plantilla en el HTML. En la plantilla estoy utilizando un control ViewBox para que se adapte al tamaño de pantalla.

<div id="imagePageTemplate" data-win-control="WinJS.Binding.Template"> 
    <div id="pdfitemmainviewdiv" data-win-control="WinJS.UI.ViewBox">
        <img data-win-bind="src: imageSrc"  /> 
    </div>
</div> 

<div id="pdfFlipView"
     data-win-control="WinJS.UI.FlipView" 
     data-win-options="{itemTemplate: select('#imagePageTemplate')}">
</div>

Y asignar el dataSource de la lista a la propiedad itemDataSource del control.

function renderDocument(pdfDocument) {
    var pdfFlipView = document.getElementById("pdfFlipView");

    pdfFlipView.winControl.itemDataSource = null;

    var pages = getPageList(pdfDocument);

    pdfFlipView.winControl.itemDataSource = pages.dataSource;
}

¡Ya tenemos nuestro primer lector de PDF creado con la nueva API de WinRT y en JavaScript! La mala noticia es que este ejemplo tiene varios puntos de mejora. El más importante es relativo al rendimiento, ahora estamos cargando y procesando todas las páginas del fichero con lo que si cargamos ficheros pesados, el tiempo de renderizado aumentará. Lo ideal sería que el renderizado fuese incremental, utilizando un objeto \*\*VirtualizedDataSource\*\* en lugar de una Binding.List. En \[este ejemplo el Windows Dev Center\](http://code.msdn.microsoft.com/windowsapps/PDF-viewer-showcase-sample-39ced1e8) tenéis la forma de implementarlo.

He dejado el código completo del ejemplo de esta entrada en SkyDrive: \[http://sdrv.ms/12wJ3dX\](http://sdrv.ms/12wJ3dX). Recordad que esta solución solo funciona con Windows 8.1 y Visual Studio 2013 Preview.


## Referencias


[PDF viewer showcase sample (Windows 8.1)](http://code.msdn.microsoft.com/windowsapps/PDF-viewer-showcase-sample-39ced1e8)
[Windows.Data.Pdf namespace](http://msdn.microsoft.com/en-us/library/windows/apps/windows.data.pdf.aspx)

