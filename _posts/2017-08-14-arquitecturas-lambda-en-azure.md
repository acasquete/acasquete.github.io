---
title: Arquitecturas Lambda en Azure
tags: [architecture, azure, big_data]
reviewed: true
header_fullview: lambda-architecture.jpg
---
En este artículo veremos los principales desafíos a los que nos enfrentamos cuando tenemos que desarrollar soluciones de procesamiento de datos masivos en sistemas de **Big Data**.<!-- excerpt-end -->

Mostraré el enfoque y tecnologías utilizadas para dar respuesta a esos desafíos y cómo implementamos estas soluciones basadas en servicios de Azure: [HDInsight](https://azure.microsoft.com/es-es/services/hdinsight/), [Stream Analytics](https://azure.microsoft.com/es-es/services/stream-analytics/), [EventHub](https://azure.microsoft.com/es-es/services/event-hubs/), [Data Lake](https://azure.microsoft.com/es-es/solutions/data-lake/), etc. Antes de entrar en materia, aprovecho esta primera entrada para introducir el concepto de **Arquitectura Lambda**, en la que veremos las técnicas de **Big Data** en contraposición a los sistemas tradicionales.

Una **Arquitectura Lambda** es una arquitectura de procesamiento de datos diseñada para manejar cantidades masivas de datos utilizando procesamiento en **batch** y en tiempo real. Muchas veces nos referimos a estos dos modos de procesar los datos como **cold path** y **hot path** respectivamente. Uno de los objetivos de este tipo de arquitecturas es que podamos consultar y preguntar a los datos de una forma consistente, independientemente del camino que utilicemos, ya sea consultando los datos en reposo o en movimiento.

El término **Arquitectura Lambda** fue acuñado por Nathan Marz, el creador de Storm, en el libro [Big Data](https://www.manning.com/books/big-data) de Manning. A grandes rasgos, la idea detrás de esta arquitectura es la de poder ofrecer un sistema más intuitivo y sencillo que el ofrecido por las arquitecturas tradicionales, caracterizadas por utilizar bases de datos de lectura y escritura que mantienen el estado de forma incremental, presentando ciertas complejidades tanto a nivel operacional como al querer aumentar la disponibilidad mediante [consistencia eventual](https://en.wikipedia.org/wiki/Eventual_consistency) o réplicas. Además, las arquitecturas incrementales presentan como último inconveniente la falta de tolerancia a fallos humanos, ya que modificando el estado de la base de datos y entendiendo que los errores son inevitables, estamos casi garantizando que los datos en algún momento se corromperán.

> «Las arquitecturas Lambda pueden producir soluciones con mejor rendimiento evitando las complejidades de las arquitecturas incrementales.»

En la práctica veremos que no existe una solución única para implementar una **Arquitectura Lambda**, esto significa que tendremos que hacer uso de un conjunto de distintas tecnologías y técnicas para construir un sistema completo de **Big Data**. En las siguientes entradas veremos en detalle cada una de estas tecnologías, basadas en servicios de Azure, y distintos enfoques para afrontar el diseño de una **Arquitectura Lambda**.

La idea de las **Arquitecturas Lambda** es crear un sistema de **Big Data** diferenciando tres capas, cada una basada en la funcionalidad proporcionada por las capas inferiores.

**Batch Layer** - Es la responsable de guardar una copia inmutable de los datos en constante crecimiento y de precalcular una serie de vistas sobre esos datos.

**Serving Layer** - Normalmente consiste en una base de datos distribuida que carga las vistas generadas por la _batch layer_ y permite realizar lecturas aleatorias. Cuando existen nuevas vistas _batch_ disponibles la _serving layer_ intercambia automáticamente para que los datos más recientes estén disponibles. Una base de datos _serving layer_ debe soportar actualizaciones en lote y lecturas aleatorias, pero no necesita soportar escrituras aleatorias.

**Speed Layer** - La _serving layer_ se actualiza tan pronto la _batch layer_ termina de precalcular una vista. Esto significa que los datos que no están disponibles en la _batch view_ son los datos que llegaron mientras se estaba procesando la vista. El propósito de la _speed layer_ es asegurar que los nuevos datos están representados tan pronto la aplicación los necesita, consiguiendo de esta forma un sistema de datos en tiempo real.

![Layers of a Lambda Architectures](/img/lambda_architecture_layers_orange.jpg)

La _speed layer_ y la _batch layer_ son similares en cuanto a funcionalidad ya que son las encargadas de generar las vistas, ya sea en tiempo real o mediante procesos batch a medida que se reciben nuevos datos. Sin embargo, existen dos diferencias en cuanto a la forma de procesar los datos. La _speed layer_ solo utiliza los datos más recientes y realiza cálculos incrementales para obtener las menores latencias posibles. Esto significa que la _speed layer_ debe generar las vistas en tiempo real basándose en los datos nuevos y otras vistas en tiempo real existentes.

Resumen
-------

Cuando hablamos de sistemas de procesamiento masivo de datos no debemos preocuparnos exclusivamente de que la solución sea altamente eficiente, hay otras propiedades que tenemos que poner en valor: robustez, tolerancia a fallos, escalabilidad, extensibilidad… Las **Arquitecturas Lambda** definen cómo deben construirse estos sistemas basándose en tres capas, que establecen la forma en la que los datos deben procesarse y a la vez satisfacen todas las propiedades necesarias en un sistema de **Big Data**.

Referencias
-----------

[Analytics on Large Scale, Unstructured, Dynamic Data using Lambda Architecture](https://www.youtube.com/watch?v=awvdJTDCA-k)  
[Vehicle telemetry analytics solution playbook](https://docs.microsoft.com/en-us/azure/machine-learning/cortana-analytics-playbook-vehicle-telemetry)  
[Lambda Architecture](http://lambda-architecture.net/)  
[Lambda Architecture for Connected Car Fleet Management](https://channel9.msdn.com/Events/Build/2017/P4017)  
[Nathan Marz on Storm, Immutability in the Lambda Architecture, Clojure](https://www.infoq.com/interviews/marz-lambda-architecture)