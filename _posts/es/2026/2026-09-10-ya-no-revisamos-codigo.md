---
title: Ya no revisamos código
tags: [artificial_intelligence, programming]
reviewed: true
home: true
ai: true
header_image: ya-no-revisamos-codigo-cover.jpg
---
Este mes compartí una nota interna con toda la gente de Plain Concepts. El titular, *"ya no revisamos código"*, lo elegí a propósito para que llamara la atención. Pero el titular es lo de menos. Lo importante son las conversaciones que este tipo de declaraciones abre y que, por fin, nos pusiéramos de acuerdo sobre algo que todos veíamos venir desde hacía un año, aunque nadie tuviera muy claro cómo iba a llegar.<!-- excerpt-end -->

Ya está aquí. Y no se parece del todo a lo que imaginábamos.

## Qué ha pasado

Hasta hace poco, revisar una PR significaba lo de siempre: alguien se leía los cambios, dejaba comentarios, la aprobaba y solo entonces el código llegaba a producción. Hoy, en ocho aplicaciones internas que compartimos en la compañía, ese paso está desapareciendo. Y no porque hayamos bajado el listón, sino porque lo hemos subido en otro sitio.

En esas aplicaciones, buena parte de los pasos del ciclo (leer la issue, escribir el código, ejecutar los tests, abrir la PR) ya no los hace una persona, sino un agente de IA con sus propias herramientas y permisos, dentro de los límites que le marcamos. Los pasos son los de siempre; lo que ha cambiado es quién los da. Y eso nos obliga a replantearnos dónde ponemos la atención humana.

La decisión que tomamos fue esta: **la revisión humana deja de ser una puerta antes del merge y pasa a ser una capa posterior.** Una PR solo se integra si todas sus puertas (tests, spec, auditoría, contratos) están en verde. La persona revisa el resultado, no cada línea que lo ha producido.

El motivo no es ir más rápido. El motivo es que, cuando una persona lee diffs generados por agentes al ritmo al que los agentes los generan, esa lectura deja de ser una señal de calidad. **Se convierte en teatro.**

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

Alguien tiene que dibujar los *bounded contexts*, decidir los invariantes, escribir la *especificación* contra la que construye el agente y diseñar la batería de tests que tiene que cazar la regresión antes de que nadie mire el diff. Eso es bastante más difícil que escribir el código a mano. Es, de hecho, **la ingeniería que antes nos saltábamos**, porque siempre había un revisor detrás haciendo de red de seguridad.

Ahora la red de seguridad es el sistema. Y eso significa que el sistema tiene que estar bien construido, o nadie cazará el error. Justo ahora, cuando tenemos más capacidad de ingeniería que nunca, es cuando más disciplina de ingeniería necesitamos.

## Cómo es la jaula por dentro

Todo esto suena abstracto hasta que abres una jaula. Así que, en la aplicación donde tomamos la decisión, la jaula es más o menos así.

**Cada cambio empieza con una spec escrita.** Antes de generar una sola línea, el cambio tiene que estar descrito: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla. Una spec vaga no produce mal código; produce buen código para el problema equivocado.

**Miles de tests en cada cambio.** Unos cuatro mil entre la API y la web, y los que tocan la base de datos se ejecutan contra una base de datos real. Esto es lo que sustituye al ojo del revisor, y necesita ese tamaño porque tiene que cazar lo que una persona cazaba leyendo.

**Rompemos nuestro propio código a propósito para ver si los tests se dan cuenta.** Se llama mutation testing. No basta con que una línea esté cubierta por un test: introducimos pequeños errores deliberados y comprobamos que al menos un test falla . Un test que se ejecuta pero nunca falla es decoración. Así sabemos que la red funciona de verdad, que es lo único que importa cuando nadie lee el código.

**Seguridad en cada build, sin tener que pedirla.** TruffleHog para secretos filtrados, Trivy para vulnerabilidades conocidas en dependencias e infraestructura y Semgrep para patrones inseguros en el código. Los tres bloquean. Nada de esto depende de que alguien se dé cuenta, ni debería.

**Cada build sabe lo que lleva dentro.** Cada build genera con Syft una lista de materiales del software, un SBOM: un inventario completo y legible por máquina de cada paquete y componente que contiene la aplicación, con su licencia. Un paquete con una licencia que no podemos distribuir se caza antes de llegar a un entregable. Además, es lo primero que pide un equipo de seguridad o un auditor, precisamente por eso, antes se hacía a mano, una vez, la semana antes de la auditoría.

**Lo que se despliega se vuelve a probar con el sistema en marcha.** Después del merge, el código va a un entorno de staging y ZAP lo sondea automáticamente como lo haría un atacante, antes de que una persona confirme el paso a producción. La jaula no termina en el merge.

**La ingeniería que siempre se aplazaba ahora se hace.** Todos los equipos conocen la lista: restaurar un backup para demostrar que funciona, rotar los secretos, revisar quién sigue teniendo acceso, comprobar que lo que se está ejecutando coincide con lo documentado, mantener el runbook al día. Siempre importante, siempre lo primero que pide el auditor, siempre para el trimestre que viene. Un backup que nadie ha restaurado es una hipótesis, y una lista de accesos que nadie revisa es un riesgo. Las evidencias de auditoría, que antes eran una carrera de última hora, pasan a ser un subproducto del build.

## Las 7 puertas que pasa una PR antes de que la vea una persona

La misma jaula, en forma de lista para copiar y adaptar. Cada punto bloquea el merge.

1. **Spec.** El cambio se describe antes de generar código: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla.
2. **Tests.** Unos 4.000 entre API y web. Los que tocan la base de datos se ejecutan contra una real.
3. **Mutation score.** Stryker inyecta pequeños bugs y comprueba que algún test falla. Cada módulo tiene que mantener una puntuación mínima.
4. **Secretos.** TruffleHog busca credenciales filtradas. Bloqueante.
5. **Vulnerabilidades.** Trivy analiza las dependencias y el código de infraestructura. Bloquea ante vulnerabilidades críticas y altas.
6. **Patrones inseguros.** Semgrep como análisis estático. Bloqueante.
7. **SBOM y licencias.** Syft inventaría cada componente y una política valida cada licencia contra lo que podemos distribuir.

Después del merge, queda una más antes de producción: ZAP sondea el despliegue en staging como lo haría un atacante, y solo entonces una persona confirma el paso.

Nada de esto llegó de golpe y nada sale gratis. Casi todas las protecciones de esa lista existen porque algo se coló, o porque vimos cómo podía colarse. Ese es el trato, dicho con honestidad: **no dejas de leer código y luego construyes la jaula. Construyes la jaula primero, la sigues manteniendo y, el día que deja de cazar cosas, vuelves a leer código.** Saltarse la primera mitad y quedarse con la segunda no es lo que describo. Eso es, sin más, no revisar código.

## Lo que sigue siendo humano

Nada de esto significa soltar el volante. Sigue habiendo una puerta de entrada innegociable: la issue. Ningún cambio nace de una idea suelta o de un prompt improvisado, sino de un problema descrito, analizado y con criterios de aceptación explícitos. Ahí es donde ponemos el criterio humano: en qué construir y por qué, no en la sintaxis de cómo se construye.

Y hay líneas rojas que no se negocian, venga el cambio de un agente o de una persona: nadie toca las claves de firma, nadie hace force-push sobre el trabajo de otro y nadie despliega a producción sin que una persona lo confirme.

La responsabilidad tampoco se mueve. **Nadie explica un incidente en producción diciendo que lo escribió el agente.** Decidir no leer cada línea es decidir dónde merece la pena poner la atención, no ceder la autoría. Quien integró el cambio sigue respondiendo por él.

## Y los modelos siguen mejorando

Sería fácil terminar con "y por eso necesitas una jaula" y quedarse ahí. También sería un error. Construimos la jaula pensando en los modelos que teníamos en ese momento, y los modelos mejoran más rápido que las herramientas que los contienen. Parte de lo que pusimos para que un agente no se saliera del carril ya sobra, y sobrará más. Fingir lo contrario sería el mismo teatro del que me quejaba al principio.

Así que no perdamos la cabeza ni en un sentido ni en otro. La ingeniería no desaparece: alguien tiene que escribir la spec, decidir los invariantes y construir las comprobaciones que te dicen si lo que ha salido es lo que se pidió. Esa parte gana importancia a medida que mejoran los modelos, porque es lo único que queda entre un modelo muy capaz y producción.

Lo que se abarata es el *harness*, todo lo que construimos para mantener al modelo en el camino: el andamiaje, la ceremonia, los pasos añadidos porque un modelo anterior se perdía sin ellos. Cada uno de ellos es un barrote que conviene quitar el día que deje de cazar algo, y cuanto antes llegue ese día, mejor: **cada barrote que quitas es esfuerzo que vuelve a la ingeniería que importa.**

> Una puerta se gana su sitio cazando algo. Si lleva meses sin cazar nada, es un coste, no una protección.

La forma de gestionarlo es la misma con la que construimos la jaula: midiendo. Las puertas de resultado seguirán ganándose su sitio durante mucho tiempo. Muchas de las de camino no, y no pasa nada. Es lo que ocurre cuando los modelos son lo bastante buenos como para que el cuello de botella vuelva a desplazarse a la ingeniería que los rodea.

La revisión se ha movido; la responsabilidad, no. Puedes dejar de leer cada diff, pero no puedes dejar de responder por lo que sale a producción. Por eso construir la jaula es ingeniería de verdad, y decidir qué barrotes quitar a medida que mejoran los modelos es la parte que menos estoy dispuesto a delegar.

