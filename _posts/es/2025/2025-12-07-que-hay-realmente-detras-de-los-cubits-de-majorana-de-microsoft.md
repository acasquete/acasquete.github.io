---
featured: 2
description: Sobre el papel suena a revolución. En la práctica, la historia es bastante más matizada.
title: ¿Qué hay realmente detrás de los cúbits de Majorana de Microsoft?
tags: [personal, quantum_computing]
reviewed: true
home: true
ai: true
header_image: majorana-cover.jpg
cover_ratio: 3 / 2
hero_position_mobile: 57% center
---
En los últimos meses, Microsoft ha vuelto a acaparar titulares con una promesa muy concreta: está construyendo un «ordenador cuántico topológico» basado en cúbits de Majorana y, según la compañía, ya tiene funcionando un primer chip, Majorana 1, con la vista puesta en llegar a millones de cúbits en pocos años.

Sobre el papel suena a revolución. En la práctica, si se examina la literatura científica en detalle, la historia es bastante más matizada. Todavía no hay ninguna demostración sólida de cúbits topológicos de Majorana funcionando, ni de Microsoft ni de nadie. Además, la trayectoria del grupo de Azure Quantum está marcada por retractaciones, polémicas y una expectación que choca con la prudencia habitual en la física de la materia condensada. ([arXiv][^1])

Este artículo intenta aclarar qué son esos supuestos cúbits de Majorana, qué ha hecho exactamente Microsoft y qué sigue sin estar demostrado.

# De Majorana en física de partículas a «Majoranas» en materiales

Empecemos por el principio: **los «modos de Majorana» en materiales no son nuevas partículas fundamentales** ni tienen relación directa con los neutrinos de Majorana o la supersimetría. Son **cuasipartículas** que surgen en ciertos superconductores topológicos como estados de energía muy cercana a cero, localizados en los extremos de una estructura.

La idea teórica toma forma en 2001 con el *modelo de Kitaev*: una cadena unidimensional de fermiones en un superconductor «exótico» en la que, al enfriar el sistema y ajustar sus parámetros, aparecen dos modos especiales en los extremos. Ambos están correlacionados de forma no local y pueden describirse matemáticamente como un par de modos de Majorana.

Más tarde se descubre un truco clave: no hace falta un superconductor exótico de tipo p. Basta con colocar un **nanohilo semiconductor** (por ejemplo, de arseniuro de indio, InAs) sobre una **capa superconductora convencional** (aluminio, de tipo s). En ciertas condiciones de campo magnético, acoplamiento y geometría, el sistema se comporta en la práctica como el superconductor topológico que pedía el modelo de Kitaev. ([arXiv][^1])

En ese contexto aparecen dos tipos de estados importantes:

* **Modos de Majorana (modos cero)**: energía prácticamente nula, con carácter topológico y no local.
* **Estados de Andreev**: estados de baja energía pero triviales, locales, sin protección topológica.

El problema práctico es que, experimentalmente, distinguirlos es muy difícil. La frontera entre «casi cero» y «cero» en energía no es algo que puedas trazar con un rotulador en el laboratorio.

# Por qué los cúbits topológicos serían el santo grial

La computación cuántica «convencional» (de circuitos superconductores, de iones atrapados, etc.) trabaja con cúbits locales y frágiles. Su gran coste es la **corrección de errores**: hacen falta muchos cúbits físicos para obtener un cúbit lógico razonablemente estable.

Los cúbits topológicos de Majorana prometen justo lo contrario:

* El cúbit se codifica de forma **no local**, por ejemplo en los extremos de un nanohilo o en una estructura en forma de H llamada **tetrón** (cuatro modos de Majorana para un cúbit efectivo).
* Las pequeñas perturbaciones locales no destruyen el estado global, igual que un nudo no se deshace porque tires un poco de la cuerda por un punto intermedio.

Esa protección topológica, si fuera real, podría dar **tiempos de coherencia muy largos** y reducir drásticamente el sobrecoste de la corrección de errores. De ahí el entusiasmo: un cúbit topológico auténtico con un tiempo de coherencia de, digamos, un segundo supondría un salto de varios órdenes de magnitud respecto a los microsegundos típicos de los cúbits superconductores estándar.

Pero esa promesa depende de demostrar dos cosas:

1. Que los **modos de Majorana existen realmente** en tu dispositivo.
2. Que puedes **trenzarlos («braiding») y leer su paridad** de forma controlada, mostrando la estadística no abeliana que les da su carácter topológico.

Ninguna de las dos se ha demostrado de forma incontestable.

# Microsoft, el fiasco de 2018 y el borrón y cuenta nueva

Microsoft apuesta con fuerza por la vía topológica desde aproximadamente 2010. Crea un gran grupo de investigación (Microsoft Station Q / Azure Quantum), incorpora a figuras de primer nivel y se centra en nanohilos de InAs/Al con estados de Majorana.

En 2018, el equipo publica en *Nature* un artículo que se presenta como una prueba sólida de modos de Majorana en estos dispositivos. Poco después, otros grupos intentan reproducir los resultados y descubren que pueden obtenerse curvas muy similares con estados de Andreev triviales.

Al revisar los datos brutos, se comprueba que hubo un **sesgo de selección**: se habían publicado solo los dispositivos y barridos de campo más favorables, y quedaron fuera muchos que no encajaban con la hipótesis de Majorana. Como resultado, el artículo acaba **retirándose en 2021** ([Nature][^6]), y varios responsables del trabajo experimental dejan Microsoft.

La reputación del programa topológico de Azure Quantum queda dañada, y a partir de ahí empieza una «segunda generación» con una nueva dirección, encabezada por Chetan Nayak, y un mensaje de «hemos aprendido de los errores».

# El nuevo artículo en *Nature* (2025): qué hace y qué no hace

En febrero de 2025, Azure Quantum publica en *Nature* el artículo titulado:

> «Interferometric single-shot parity measurement in InAs–Al hybrid devices» ([PubMed][^2])

Lo esencial:

* El dispositivo es un **nanohilo de InAs/Al** con puntos cuánticos definidos por puertas, una configuración pensada como paso intermedio hacia un **tetrón lineal**.
* Lo que los autores demuestran realmente es una **técnica de medida**: consiguen medir en un **solo disparo la paridad fermiónica** de una región del dispositivo, con una buena relación señal/ruido y tiempos de permanencia de los estados del orden de milisegundos. ([arXiv][^1])
* En la versión final del artículo, tras la revisión por pares, **no se afirma en ningún momento que haya Majoranas ni cúbits topológicos funcionando**. De hecho, unas notas editoriales aclaran explícitamente que no se observan modos de Majorana ni computación topológica como tal. ([PMC][^3])

La parte delicada está en la interpretación:

* Los autores presentan sus datos como «compatibles» con la lectura de paridad de un par de modos de tipo Majorana separados por micras.
* Sin embargo, **no descartan de forma concluyente** que lo observado pueda explicarse con estados de Andreev de baja energía.
* Poco después aparece en arXiv un **comentario crítico** de Henry F. Legg (2025) que cuestiona la fiabilidad del protocolo de «brecha topológica» usado para afirmar que la región se encuentra en una fase superconductora con brecha. Tras analizar los datos de conductancia sin filtrar, Legg sostiene que en las regiones medidas no hay tal brecha y que, por tanto, la interpretación topológica no está justificada. ([arXiv][^4])

En resumen, el artículo es técnicamente interesante como avance en la **lectura de paridad** de estos dispositivos híbridos, pero está muy lejos de ser la demostración limpia de un cúbit de Majorana que sugieren muchos titulares.

# ¿Y el «ordenador topológico» que anuncia Microsoft?

Al mismo tiempo, el CEO de Microsoft y varios portavoces de Azure Quantum han hablado en los medios de:

* un primer chip llamado **Majorana 1**, con **8 cúbits topológicos**;
* una hoja de ruta para llegar a **millones de cúbits** en pocos años;
* y la idea de que ya estarían por delante de otros enfoques en la carrera cuántica.

El problema es que, a día de hoy, **ningún artículo científico describe ese supuesto procesador con detalle**, ni hay una demostración de:

* un **tetrón completo** que funcione como cúbit, con tiempos de coherencia medidos;
* ni, mucho menos, del **trenzado** de modos de Majorana en una geometría en H o en una red más compleja, que sería la prueba inequívoca de la estadística no abeliana.

Lo que sí hay es:

* Un artículo de metrología que implementa la lectura de paridad en un dispositivo parecido a «medio tetrón» y que los propios autores presentan solo como un paso intermedio. ([Microsoft][^5])
* Declaraciones en blogs y entrevistas según las cuales, desde que se envió el artículo en 2024, la empresa ha progresado y ya cuenta con decenas de modos de Majorana y varios cúbits funcionando, sin que se hayan publicado todavía manuscritos revisados por pares.

Es el clásico choque entre el **marketing corporativo** y el **rigor científico**: mientras no haya artículos que describan el dispositivo completo, con datos y protocolos reproducibles, para la física académica el contador de cúbits topológicos demostrados sigue **a cero**.

# La prueba de fuego que sigue pendiente: el trenzado

En teoría, la forma inequívoca de demostrar que tienes **modos de Majorana topológicos**, y no simples impostores de Andreev, es observar su **comportamiento** al trenzarlos:

1. Construyes una geometría de **dos nanohilos conectados por un segmento central superconductor**, con forma de H (un tetrón).
2. En los cuatro extremos hay cuatro modos que, si son de Majorana, codifican un cúbit de forma no local.
3. Mediante campos eléctricos y magnéticos, mueves adiabáticamente esos modos por la H e intercambias sus posiciones de forma controlada.
4. Intercambiar dos de ellos no conmuta con otras operaciones y deja una huella reconocible en las medidas de paridad: esa es la estadística no abeliana.

Esa secuencia de trenzado sería la **prueba topológica definitiva**. Hasta ahora, nadie ha mostrado un experimento así con datos convincentes, tampoco Microsoft. El propio Nayak reconoce que es un objetivo de futuro, no algo logrado.

# Cómo leer las próximas noticias sobre Majorana y cúbits topológicos

Al margen del caso de Microsoft, la computación cuántica topológica sigue siendo una línea de investigación fascinante y probablemente veremos avances reales en los próximos años. Pero, para no perderse entre tanto ruido, conviene aplicar una regla muy sencilla:

**Confía, pero verifica**, también en la cuántica:

1. **¿Hay un artículo revisado por pares?** Si solo hay una nota de prensa o una entrada de blog de la empresa, tómalo como marketing, no como una prueba.
2. **¿Qué afirman exactamente?** «Compatible con…» no es lo mismo que «demostramos sin ambigüedad…». Lee la letra pequeña.
3. **¿Se descartan explícitamente las explicaciones triviales (Andreev, desorden, etc.)?** Si no hay un análisis sistemático de las alternativas, el resultado es prometedor, pero no concluyente.
4. **¿Hay replicación independiente o, al menos, críticas técnicas serias?** Los comentarios en arXiv y las respuestas de otros grupos forman parte del proceso normal. Cuando varias réplicas independientes apuntan en la misma dirección, empieza a formarse un consenso.
5. **¿Se ha demostrado el trenzado o solo una lectura local de la paridad?** Hasta que no haya un experimento de trenzado convincente, hablar de «cúbits topológicos funcionales» es, como mínimo, prematuro.

# En resumen

La apuesta de Microsoft por Majorana es valiente y, si saliera bien, podría cambiar el panorama de la computación cuántica. Pero, a día de hoy, lo esencial no ha cambiado: **nadie ha observado de forma incontestable un modo cero de Majorana en estos dispositivos, ni un cúbit topológico funcionando como tal**. Lo que hay son buenos experimentos de metrología y muchas expectativas.

Queda por ver si los próximos artículos estarán a la altura de las promesas o si este capítulo acabará siendo otro ejemplo de cómo la expectación puede ir varios pasos por delante de la ciencia.

# Referencias

[^1]: https://arxiv.org/abs/2401.09549 "Interferometric Single-Shot Parity Measurement in an InAs-Al Hybrid Device"
[^2]: https://pubmed.ncbi.nlm.nih.gov/39972225/ "Interferometric single-shot parity measurement in InAs-Al ..."
[^3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11839464/ "Interferometric single-shot parity measurement in InAs–Al ..."
[^4]: https://arxiv.org/abs/2503.08944 "Comment on \"Interferometric single-shot parity measurement in InAs-Al hybrid devices\", Microsoft Quantum, Nature 638, 651-655 (2025)"
[^5]: https://www.microsoft.com/en-us/research/publication/interferometric-single-shot-parity-measurement-in-an-inas-al-hybrid-device/ "Interferometric Single-Shot Parity Measurement in an InAs- ..."
[^6]: https://www.nature.com/articles/s41586-021-03373-x "Retraction Note: Quantized Majorana conductance"
