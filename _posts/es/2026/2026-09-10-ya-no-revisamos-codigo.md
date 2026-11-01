---
featured: 1
hero_position: center 40%
hero_position_mobile: 22% center
description: Una nueva forma de hacer software ha llegado, y no se parece del todo a lo que imaginábamos.
title: Ya no revisamos código
tags: [artificial_intelligence, programming]
reviewed: true
home: true
ai: true
header_image: ya-no-revisamos-codigo-cover.jpg
---
Este mes compartí una nota interna con todo el equipo de Plain Concepts. El titular, *"ya no revisamos código"*, lo elegí a propósito para que llamara la atención. Pero el titular es lo de menos. Lo importante son las conversaciones que abre este tipo de declaraciones y que, por fin, dijéramos en voz alta algo que muchos veíamos venir desde hacía un año, aunque nadie tuviera muy claro cómo iba a llegar.<!-- excerpt-end -->

Puede que lo único que hizo el titular fuera poner palabras a algo que muchos pensábamos, esperando a que alguien lo dijera: una nueva forma de hacer software ha llegado y no se parece del todo a lo que imaginábamos.

## Qué ha pasado

Hasta hace poco, revisar una PR significaba lo de siempre: alguien leía los cambios, dejaba comentarios, la aprobaba y solo entonces el código llegaba a producción. Hoy, en catorce aplicaciones internas de la compañía, ese paso está desapareciendo. Y no porque hayamos bajado el listón, sino porque lo hemos subido en otro sitio.

En esas aplicaciones, buena parte de los pasos del ciclo (leer la *issue*, escribir el código, ejecutar los tests, abrir la PR) ya no los hace una persona, sino un agente de IA con sus propias herramientas y permisos, dentro de los límites que le marcamos. Los pasos son los de siempre; lo que ha cambiado es quién los da. Y eso nos obliga a replantearnos dónde ponemos la atención humana.

La decisión que tomamos fue esta: **la revisión humana deja de ser una puerta antes del merge y pasa a ser una capa posterior.** Una PR solo se integra si todas sus puertas (tests, spec, auditoría, contratos) están en verde: comprueban que hace lo que se pidió, que no rompe lo que ya funcionaba y que respeta los requisitos de seguridad. La persona revisa el resultado, no cada línea que lo ha producido.

El motivo no es ir más rápido. El motivo es que, con este volumen de cambios, leer cada uno deja de ser una señal fiable de calidad. **Se convierte en teatro.**

## No somos los únicos

Robert C. Martin, Uncle Bob, el autor de *Clean Code*, el que se pasó veinte años enseñándonos a leer código con lupa, le respondió hace poco a un desarrollador que decía que no podía dejar que un agente tocara código que no entendía. Su respuesta se hizo viral:

> "Empecé a programar a finales de los 60. Mi estrategia actual es no leer nada del código que escriben mis agentes. Es la única forma de aprovechar su productividad. Lo que hago en su lugar es rodear a los agentes de restricciones extremas. Tests unitarios, tests en Gherkin, procedimientos de QA, métricas de calidad, mutation testing, cobertura de tests y un montón más. Al final, tengo muchísima confianza en el código que producen porque han tenido que superar todas mis restricciones y tests."
>
> — [Robert C. Martin](https://x.com/unclebobmartin/status/2080257779395154409), 23 de julio de 2026

Ya lo había [dicho en abril](https://x.com/unclebobmartin/status/2044114698451476492), en una respuesta que tuvo mucha menos repercusión: no revisa el código de los agentes; mide cobertura, estructura de dependencias, complejidad ciclomática y mutation score, porque "los humanos somos lentos con el código". La de julio, en cambio, dio mucho que hablar.

Viniendo de él, incomoda. Pero apunta justo a lo que ya estábamos construyendo: en vez de leer el código, diseñar la jaula de tests que ese código tiene que superar y dejar que el agente escriba dentro de ella. Si el conjunto de restricciones está bien construido, la calidad deja de depender de que alguien mire cada línea.

## Dos cosas distintas a las que llamamos jaula

Esta es una distinción que me costó ver.

Hay dos cosas a las que llamamos "jaula" y no son lo mismo. La primera es el conjunto de comprobaciones que un cambio tiene que pasar antes de salir: los tests, el mutation score, los escaneos de seguridad, la spec contra la que se construyó. Eso **comprueba el resultado**. Le da igual lo bueno que sea el modelo, porque tendría que existir aunque el código lo hubiera escrito una persona.

La segunda es el proceso por el que obligamos a pasar al agente para llegar hasta ahí: qué paso va primero, qué artefacto tiene que producir antes de dejarle pasar al siguiente, cuánto del trabajo es andamiaje para que un modelo flojo no se salga del carril. Eso **comprueba el camino**. Es lo que en inglés se llama el *harness* del agente: el arnés de herramientas, permisos, pasos y plantillas que envuelve al modelo y le marca por dónde puede moverse. Y con cada nueva versión de los modelos, una parte deja de tener sentido.

> La jaula que comprueba el resultado no envejece con los modelos. La que comprueba el camino, sí.

La nuestra es sobre todo del primer tipo, aunque no del todo: exigir que cada cambio toque una especificación es una restricción de camino, y la mantenemos porque la *spec* es aquello contra lo que se comprueba el resultado. Separar con honestidad nuestras puertas es un trabajo que todavía no hemos terminado.

## Más ingeniería, no menos

Es tentador leer todo esto como "menos ingeniería, más automatización". Es justo al revés.

Alguien tiene que dibujar los *bounded contexts*, decidir los invariantes (lo que nunca puede dejar de cumplirse), escribir la *especificación* contra la que construye el agente y diseñar la batería de tests que tiene que cazar la regresión antes de que nadie mire el código. Eso es bastante más difícil que escribir el código a mano. Es, de hecho, **la ingeniería que antes nos saltábamos**, porque siempre había un revisor detrás haciendo de red de seguridad.

Ahora la red de seguridad es el sistema. Y eso significa que el sistema tiene que estar bien construido, o nadie cazará el error. Justo ahora, cuando tenemos más capacidad de ingeniería que nunca, es cuando más disciplina de ingeniería necesitamos.

## Cómo es la jaula por dentro

Todo esto suena abstracto hasta que abres una jaula. Así que, en la aplicación donde tomamos la decisión, la jaula es más o menos así.

**Cada cambio empieza con una spec escrita.** Antes de generar una sola línea, el cambio tiene que estar descrito: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla. Una spec vaga no produce mal código; produce buen código para el problema equivocado.

**Tests en cada cambio.** Esto es lo que sustituye al ojo del revisor, y tienen que ser muchos porque deben cazar lo que una persona cazaba leyendo.

**Rompemos nuestro propio código a propósito para ver si los tests se dan cuenta.** Se llama mutation testing. No basta con que una línea esté cubierta por un test: introducimos pequeños errores deliberados y comprobamos que al menos un test falla. Un test que se ejecuta pero nunca falla es decoración. Así sabemos que la red funciona de verdad, que es lo único que importa cuando nadie lee el código.

**Seguridad en cada build, sin tener que pedirla.** TruffleHog para secretos filtrados, Trivy para vulnerabilidades conocidas en dependencias e infraestructura y Semgrep para patrones inseguros en el código. Los tres bloquean. Nada de esto depende de que alguien se dé cuenta, ni debería.

**Cada build sabe lo que lleva dentro.** Cada build genera con Syft una lista de materiales del software, un SBOM: un inventario completo y legible por máquina de cada paquete y componente que contiene la aplicación, con su licencia. Un paquete con una licencia que no podemos distribuir se caza antes de llegar a un entregable. Además, es lo primero que pide un equipo de seguridad o un auditor. Antes se hacía a mano, una vez, la semana anterior a la auditoría.

**Lo que se despliega se vuelve a probar con el sistema en marcha.** Después del merge, el código va a un entorno de staging y ZAP lo sondea automáticamente como lo haría un atacante, antes de que una persona confirme el paso a producción. La jaula no termina en el merge.

**Por fin hacemos la ingeniería que muchos sabíamos necesaria, pero que la falta de tiempo dejaba siempre para después.** Muchos equipos conocen esta lista: restaurar un backup para demostrar que funciona, ejecutar pruebas de rendimiento y de intrusión, revisar quién sigue teniendo acceso, comprobar que lo que se está ejecutando coincide con lo documentado, mantener el runbook al día. Siempre importante, siempre lo primero que pide el auditor, siempre para el trimestre que viene. Un backup que nadie ha restaurado es una hipótesis, y una lista de accesos que nadie revisa es un riesgo. Las evidencias de auditoría, que antes eran una carrera de última hora, ahora salen solas con cada build.

## Las 7 puertas que pasa una PR antes de que la vea una persona

La misma jaula, en forma de lista para copiar y adaptar. Cada punto bloquea el merge.

1. **Spec.** El cambio se describe antes de generar código: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla.
2. **Tests.** Unitarios, de integración y de aceptación en cada cambio.
3. **Mutation score.** Stryker inyecta pequeños bugs y comprueba que algún test falla. Cada módulo tiene que mantener una puntuación mínima.
4. **Secretos.** TruffleHog busca credenciales filtradas. Bloqueante.
5. **Vulnerabilidades.** Trivy analiza las dependencias y el código de infraestructura. Bloquea ante vulnerabilidades críticas y altas.
6. **Patrones inseguros.** Semgrep como análisis estático. Bloqueante.
7. **SBOM y licencias.** Syft inventaría cada componente y una política valida cada licencia contra lo que podemos distribuir.

Después del merge, queda una más antes de producción: ZAP sondea el despliegue en staging como lo haría un atacante, y solo entonces una persona confirma el paso.

Nada de esto llegó de golpe y nada sale gratis. Casi todas las protecciones de esa lista existen porque algo se coló, o porque vimos cómo podía colarse. Ese es el trato, dicho con honestidad: **no dejas de leer código y luego construyes la jaula. Construyes la jaula primero, la sigues manteniendo y, el día que deja de cazar cosas, vuelves a leer código.** Saltarse la primera mitad y quedarse con la segunda no es lo que describo. Eso es, sin más, no revisar código.

## Un mes en números

Una jaula también hay que poder medirla. Medimos nuestras 14 aplicaciones y 4 herramientas de plataforma con Pulse, un panel interno que lee de GitHub qué prácticas protegen cada repositorio y cómo se comportan.

**El conjunto.** A 1 de noviembre, las aplicaciones pasan de media el 86 % de sus puertas y ninguna está en producción casi sin puertas, por debajo del nivel L1. Pero el estándar completo, el nivel L3, solo lo cumplen 6 de las 14, y 5 de las 9 que están en producción. Esto todavía no está terminado.

![Resumen de Pulse: 86 % de puertas superadas de media, 6 de 14 aplicaciones en nivel L3, ninguna en producción por debajo de L1 y 5 de 9 proyectos en producción con el estándar completo.](/img/ya-no-revisamos/pulse-general.png)

*La vista general de Pulse. El uso de IA solo tiene datos de una aplicación, la del resto de capturas.*

Las siguientes capturas son de octubre de 2026 y corresponden a la aplicación donde tomamos la decisión.

**Las puertas.** Cumple las 11 prácticas que le aplican y cada una tiene un modo: bloquear, exigir un umbral o aplicar una política. En el mes, 250 de sus 256 commits se hicieron con IA.

![Tabla de Pulse con las prácticas de ingeniería de la aplicación: spec, tests, mutación, secretos, vulnerabilidades, patrones inseguros, SBOM, complejidad e higiene de código, todas en verde. Nivel L3, puntuación 100, 11 de 11 puertas y 250 de 256 commits con IA.](/img/ya-no-revisamos/pulse-puertas.png)

*El scorecard: qué prácticas protegen la rama principal, con qué herramienta y si pasaron en la última ejecución.*

**La entrega.** Hicimos 66 despliegues a producción, unos 15 por semana, con una mediana de 2,9 horas entre uno y otro. La mitad de los cambios llegó a producción en menos de 1,4 horas y el 90 % en menos de 5,9.

El dato incómodo también está ahí: 13 de esos 66 despliegues, casi uno de cada cinco, fueron trabajo no planificado para corregir errores. La jaula no lo caza todo, y por eso sigue creciendo.

![Panel de entrega de Pulse: 14,9 despliegues por semana, 66 en el mes, 2,9 horas de mediana entre despliegues, tiempo de entrega de 1,4 horas en el percentil 50 y 5,9 horas en el 90, y una tasa de retrabajo del 19,7 %.](/img/ya-no-revisamos/pulse-entrega.png)

*Frecuencia de despliegue, tiempo de entrega de los cambios y tasa de retrabajo, las señales que mejor dicen si ir rápido sale caro.*

**La calidad.** La cobertura es del 75,7 %, la puntuación de mutación del 85,5 %, no hay vulnerabilidades críticas ni altas y el SBOM inventaría 571 componentes. Tampoco aquí está todo limpio: quedan 340 métodos con una puntuación CRAP superior a 30, es decir, complejos y poco probados, y 382 puntos de deuda de complejidad. La regla es que no aparezca deuda nueva sin justificar.

![Indicadores de excelencia de ingeniería en Pulse: 75,7 % de cobertura, 85,5 % de mutación, 340 métodos con CRAP superior a 30, 0 vulnerabilidades críticas o altas, 571 componentes en el SBOM y 382 de deuda de complejidad.](/img/ya-no-revisamos/pulse-calidad.png)

*Los indicadores que publica el propio pipeline de la aplicación en cada commit.*

**La mutación por módulo.** Cada módulo tiene su propio mínimo, la línea discontinua, y un cambio que lo baja no entra. A finales de mes, *domain* quedó justo sobre su mínimo del 83 %. Nadie tiene que acordarse de vigilarlo: el siguiente cambio que lo baje se queda fuera.

![Cuatro gráficas de Pulse con la puntuación de mutación por módulo durante octubre: application, domain, sharedkernel y web, cada una por encima de su mínimo del 82, 83, 87 y 92 %.](/img/ya-no-revisamos/pulse-mutacion.png)

*La puntuación de mutación de cada módulo frente a su mínimo durante octubre.*

## Lo que sigue siendo humano

Nada de esto significa soltar el volante. Sigue habiendo una puerta de entrada innegociable. Ningún cambio nace de una idea suelta o de un prompt improvisado, sino de un problema descrito, analizado y con criterios de aceptación explícitos. Ahí es donde ponemos el criterio humano: en qué construir y por qué, no en la sintaxis de cómo se construye.

Y hay líneas rojas que el agente no cruza solo: antes de reescribir el historial compartido o de tocar producción, se detiene y pide confirmación a una persona. Los cambios que afectan a dominios sensibles, como la seguridad, o a una decisión de arquitectura documentada (ADR) también necesitan su aprobación.

La responsabilidad tampoco se mueve. **Nadie explica un incidente en producción diciendo que lo escribió el agente.** Decidir no leer cada línea es decidir dónde merece la pena poner la atención, no ceder la autoría. Quien integró el cambio sigue respondiendo por él.

## Y los modelos siguen mejorando

Sería fácil terminar con "y por eso necesitas una jaula" y quedarse ahí. También sería un error. Construimos la jaula pensando en los modelos que teníamos en ese momento, y los modelos mejoran más rápido que las herramientas que los contienen. Parte de lo que pusimos para que un agente no se saliera del carril ya sobra, y sobrará más. Fingir lo contrario sería el mismo teatro del que me quejaba al principio.

Así que no perdamos la cabeza ni en un sentido ni en otro. La ingeniería no desaparece: alguien tiene que escribir la spec, decidir los invariantes y construir las comprobaciones que te dicen si lo que ha salido es lo que se pidió. Esa parte gana importancia a medida que mejoran los modelos, porque es lo único que queda entre un modelo muy capaz y producción.

Lo que se abarata es el *harness*, todo lo que construimos para mantener al modelo en el camino: el andamiaje, la ceremonia, los pasos añadidos porque un modelo anterior se perdía sin ellos. Cada uno de ellos es un barrote que conviene quitar el día que deje de cazar algo, y cuanto antes llegue ese día, mejor: **cada barrote que quitas es esfuerzo que vuelve a la ingeniería que importa.**

> Una puerta se gana su sitio cazando algo. Si lleva meses sin cazar nada, es un coste, no una protección.

La forma de gestionarlo es la misma con la que construimos la jaula: midiendo. Las puertas de resultado seguirán ganándose su sitio durante mucho tiempo. Muchas de las de camino no, y no pasa nada. Es lo que ocurre cuando los modelos son lo bastante buenos como para que el cuello de botella vuelva a desplazarse a la ingeniería que los rodea.

La revisión se ha movido; la responsabilidad, no. Puedes dejar de leer cada diff, pero no puedes dejar de responder por lo que sale a producción. Por eso construir la jaula es ingeniería de verdad, y decidir qué barrotes quitar a medida que mejoran los modelos es la parte que menos estoy dispuesto a delegar.

*Actualizado en noviembre de 2026: las cifras y las líneas rojas reflejan cómo trabajamos hoy.*
