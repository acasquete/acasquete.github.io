---
title: Layouts personalizados para el ListView de WinJS 2.0
tags: [winjs, windows_store]
---
Una de las grandes mejoras del control **ListView** en **WinJS 2.0** es que se ha rediseñado para que podamos extender fácilmente el _layout_. Si queremos modificar, ni siquiera un poco, el diseño de los elementos dentro de un ListView con WinJS 1.0, tenemos que pelearnos con JavaScript para mostrar los elementos del tamaño y en la posición deseada, tanto que en algunos casos se convierte en una tarea imposible.

Ahora con WinJS 2.0 las interfaces **ILayout** y **LayoutSite** de WinJS 1.0 ya no están soportadas y la personalización del diseño se puede llevar a cabo de una forma mucho más simple, utilizando los métodos y propiedades que proporciona la interfaz [WinJS.UI.ILayout2](http://msdn.microsoft.com/library/windows/apps/dn255168.aspx). Podemos crear un tipo propio y establecerlo utilizando la propiedad **layout** de forma declarativa o mediante programación de la misma forma que lo hacemos con los _layouts_ incorporados, **GridView** o **ListView**.

    &lt;div class="listView" data-win-control="WinJS.UI.ListView" data-win-options="{
      layout: { type: WinJS.UI.GridLayout }}"&gt;
    &lt;/div&gt;
    </pre>
    
    La clase de *layout* tiene que implementar cómo mínimo los siguientes métodos de la interfaz **ILayout2**:
    
    **initialize** – Se llama pasando un objeto *site* y un indicador para saber si el ListView está agrupado o no. El objeto *site* es el que nos da la información del ListView mediante los métodos de la interfaz [ILayoutSite2](http://msdn.microsoft.com/library/windows/apps/dn255175.aspx). 
    **uninitialize** – Se llama para liberar los recursos obtenidos en el **initialize**.
    **layout** – Es el que realiza el renderizado del layout.
    
    Podemos implementar otros métodos (itemsFromRage, getAdjacent, etc.), pero para nuestro el ejemplo inicial nos basta con implementar solo estos tres.
    
    En esta entrada vamos a implementar un *layout* personalizado que ubique los elementos siguiendo el patrón de una [espiral de Ulam](http://es.wikipedia.org/wiki/Espiral_de_Ulam). Algo parecido a esto:
    
    <a href="/img/layout.png">![layout](/img/layout.png)</a>
    
    El primer elemento se ubica en el centro y los siguientes se van colocando siguiendo una espiral, el 2 a su derecha, el 3 arriba, el 4 encima del 1 y así sucesivamente.
    
    Para comenzar necesitamos una lista de elementos con los que trabajar. Esto lo hacemos definiendo el *namespace* **Data** que expone una lista objetos muy simple, con las propiedades **id** y **background**.
    
    <pre class="brush:javascript">
    (function () {
        "use strict";
    
        var items = [];
        var max = 20;
        var list = new WinJS.Binding.List(items);
    
        for (var i = 0; i < max; i++) {
            list.push(getNextItem());
        }
    
        function getNextItem() {
            var id = list.length + 1;
            return { id: id, background: getGradientColor(id) };
        }
    
        function getGradientColor (i)
        {
            var frequency = .3;
        
            var r = Math.floor(Math.sin(frequency * i + 0) * 127 + 128);
            var g = Math.floor(Math.sin(frequency * i + 2) * 127 + 128);
            var b = Math.floor(Math.sin(frequency * i + 4) * 127 + 128);
    
            return 'rgb(' + r + ',' + g + ',' + b + ')';
        }
    
        WinJS.Namespace.define("Data", {
            list: list,
            getNextItem: getNextItem
        });
    })();
    </pre>
    
    El valor del color de fondo se calcula para crear un efecto de degradado entre todos los elementos. Ahora para mostrar los elementos, declaramos en el HTML un control **ListView** y su correspondiente plantilla utilizando el objeto **Data.list.dataSource** como origen de datos.
    
    <pre class="brush:html">
    &lt;div class="itemTemplate" data-win-control="WinJS.Binding.Template"&gt;
        &lt;div style="width: 144px; height: 72px;" data-win-bind="style.background: background"&gt;
            &lt;span data-win-bind="textContent: id"&gt;&lt;/span&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    
    &lt;div class="listView" data-win-control="WinJS.UI.ListView" data-win-options="{
      itemDataSource: Data.list.dataSource,
      itemTemplate: select('.itemTemplate'),
      layout: { type: WinJS.UI.GridLayout }}"&gt;
    &lt;/div&gt;
    </pre>
    
    Si ejecutamos la aplicación, veremos un listado tal y como se muestra en la siguiente imagen, en la que el **ListView** utiliza el layout **GridView**, que es el predeterminado.
    
    <a href="/img/custom-layout-step1.png">![custom-layout-step1](/img/custom-layout-step1.png)</a>
    
    Para crear nuestro diseño personalizado, partimos de una clase que creamos utilizando **WinJS.Class.define** y en la que definimos los métodos **initialize**, **uninitialize** y **layout**.
    
    <pre class="brush:javascript">
    WinJS.Namespace.define("CustomLayouts", {
        UlamSpiralLayout: WinJS.Class.define(function (options) {
            this._site = null;
            options = options || {};
        },
        {
            initialize: function (site) {
                this._site = site;
                           
                return WinJS.UI.Orientation.horizontal;
            },
    
            uninitialize: function () {
                this._site = null;
            },
    
            layout: function (tree, changedRange, modifiedElements, modifiedGroups) {
                
                return WinJS.Promise.as();
            }        
        })
    });
    </pre>
    
    En el método **initialize** guardamos el estado del objeto **site** que utilizaremos más adelante. El método **layout** recibe en el argumento **tree** todos los elementos del control. Los otros argumentos nos indican que elementos se han modificado cuando añadimos o eliminamos elementos, en nuestro caso no los vamos a utilizar, pero puede ser conveniente utilizarlo para reducir el tiempo de renderizado. El valor que devuelve el método **layout** es una **Promise** que se completará cuando el cálculo de las posiciones haya finalizado.
    
    Como en nuestro ejemplo no vamos a utilizar ninguna agrupación, podemos trabajar solo con el primer grupo que es que contiene todos los elementos a mostrar.
    
    <pre class="brush:javascript">
    var itemsContainer = tree[0].itemsContainer;
    var items = itemsContainer.items;
    </pre>
    
    Con esto tenemos la lista de elementos y ahora solo tenemos que iterar por cada uno de ellos y establecer su posición final. Por ejemplo, podemos hacer que aparezcan en orden secuencial con una separación de 5 píxeles.
    
    <pre class="brush:javascript">
    for (var itemIndex = 0; itemIndex < items.length; itemIndex++) {
       var item = items[itemIndex];
       item.style.left = (itemIndex * itemWidth) + (5 * itemIndex) + "px";
    }
    </pre>
    
    Al estar estableciendo la propiedad **left** tenemos que definir el posicionamiento absoluto para el contenedor del **ListView**. Si no hiciésemos esto, los elementos no se mostrarían en la posición correcta.
    
    <pre class="brush:css">
    .listView .win-container {
        position: absolute;
    }
    </pre>
    
    <pre class="brush:html">
    &lt;div class="listView" data-win-control="WinJS.UI.ListView" data-win-options="{
      itemDataSource: Data.list.dataSource,
      itemTemplate: select('.itemTemplate'),
      layout: { type: CustomLayouts.UlamSpiralLayout }}"&gt;
    &lt;/div&gt;
    </pre>
    
    Si ejecutamos ahora la aplicación, veremos el siguiente resultado.
    
    <a href="/img/custom-layout-step2.png">![custom-layout-step2](/img/custom-layout-step2.png)</a>
    
    Llegados a este punto, el límite para crear un diseño personalizado es nuestra imaginación. Vamos a crear un método (**indexToPoint**) que será el encargado de calcular y devolver las coordenadas x e y, según el índice de cada elemento. 
    
    <pre class="brush:javascript">
    var centerPointY = (site.viewportSize.height - 72) / 2;
    var centerPointX = (site.viewportSize.width - 144) / 2;
    
    for (var itemIndex = 0; itemIndex < items.length; itemIndex++) {
      var item = items[itemIndex];
      var point = this._indexToPoint(itemIndex);
      item.style.left = centerPointX + point.x + "px";
      item.style.top = centerPointY + point.y + "px";
    }
    </pre>
    
    Como se puede ver, estamos ubicando los elementos partiendo del centro del **ListView**, para lo que utilizamos el objeto **site.viewportSize** . Y para devolver las coordenadas según una espiral de Ulam, utilizaremos el siguiente código.
    
    <pre class="brush:javascript">
    _indexToPoint: function (n) {
        var c = [[-1, 0, 0, -1, 1, 0], [-1, 1, 1, 1, 0, 0], [1, 0, 1, 1, -1, -1], [1, -1, 0, -1, 0, -1]];
    
        var square = Math.floor(Math.sqrt(n / 4));
    
        var y = n - 4 * square * square;
        var x = 2 * square + 1;
    
        var index = y % x;
        var side = Math.floor(y / x);
    
        var x1 = c[side][0] * square + c[side][1] * index + c[side][2];
        var y1 = c[side][3] * square + c[side][4] * index + c[side][5];
    
        return { x: x1 * 144 + 8 * x1 + "px", y: y1 * 72 + 8 * y1 + "px" };
    }
    </pre>
    
    Con esto daríamos el diseño personalizado finalizado, pero si utilizamos un poco de CSS y aplicamos transiciones y animaciones podemos personalizar un poco más la forma en la que aparecen los elementos por primera vez. 
    
    <a href="/img/custom-layout-step3.png">![custom-layout-step3](/img/custom-layout-step3.png)</a>
    
    
    
    ## Animando los elementos
    
    
    En lugar de que los elementos aparezcan directamente en su posición final, podemos ubicarlos inicialmente en el centro del **ListView** y aplicar una transformación de traslación CSS para que podamos ver como se desplaza hasta su posición. Además, y para que la animación no empiece al mismo tiempo en todos los elementos, podemos añadirle un retraso mediante **transitionDelay**.
    
    <pre class="brush:javascript">
    for (var itemIndex = 0; itemIndex < items.length; itemIndex++) {
    
        var point = this._indexToPoint(itemIndex);
        var item = items[itemIndex];
    
        item.style.left = centerPointX + "px";
        item.style.top = centerPointY + "px";
    
        item.style.transitionDelay = (itemIndex * 50) + "ms";
        item.style.transform = "translate(" + point.x + 'px, ' + point.y + 'px)';
    }
    </pre>
    
    En el CSS del contenedor del ListView aplicamos una rotación inicial y le indicamos que la translación se realice gradualmente en medio segundo y de forma linear.
    
    <pre class="brush:css">
    .listView .win-container {
        position: absolute;
        transform: rotate(180deg);
        transition: transform 500ms linear;
    }
    

En este vídeo podéis ver el resultado final. En el código de ejemplo podéis ver también otro ejemplo de diseño circular, que está extraído de la segunda edición del libro [Programming Windows Store Apps with HTML, CSS, and JavaScript](http://blogs.msdn.com/b/microsoft_press/archive/2013/10/29/free-ebook-programming-windows-store-apps-with-html-css-and-javascript-second-edition-second-preview.aspx)

Descarga código fuente
----------------------

[ListViewCustomLayout.zip](https://skydrive.live.com/redir?resid=483C407ED85318FE!22024&authkey=!AHlRj-YXuGZ7Jls&ithint=file%2c.zip)

Referencias
-----------

[WinJS.UI.ILayout2 interface](http://msdn.microsoft.com/library/windows/apps/dn255168.aspx) 
[ListView Changes between WinJS 1.0 and WinJS 2.0](http://kraigbrockschmidt.com/blog/?p=1031) 
[Free ebook: Programming Windows Store Apps with HTML, CSS, and JavaScript, Second Edition (second preview)](http://blogs.msdn.com/b/microsoft_press/archive/2013/10/29/free-ebook-programming-windows-store-apps-with-html-css-and-javascript-second-edition-second-preview.aspx)

