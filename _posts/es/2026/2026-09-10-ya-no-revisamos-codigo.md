---
title: Ya no revisamos código
tags: [artificial_intelligence, programming]
reviewed: true
home: true
ai: true
header_image: ya-no-revisamos-codigo-cover.jpg
---
Este mes compartí una nota interna con toda la gente de Plain Concepts. El titular, *"ya no revisamos código"*, lo elegimos a propósito para que golpeara fuerte. Pero el titular no es lo importante. Lo importante son las conversaciones que abrió, y el alineamiento alrededor de algo que todos sabíamos que venía desde hace un año, aunque nadie tuviera muy claro cómo.<!-- excerpt-end -->

Ya está aquí. Y no se parece exactamente a lo que imaginábamos.

## Qué ha pasado

Hasta hace poco, revisar una PR significaba lo de siempre: alguien leía el diff, dejaba comentarios, la aprobaba, y solo entonces el código llegaba a producción. Hoy, en ocho aplicaciones internas que compartimos en la compañía, ese paso está desapareciendo. No porque hayamos bajado el listón. Porque lo hemos subido en otro sitio.

En esas aplicaciones, buena parte de los pasos del ciclo (leer la issue, escribir el código, ejecutar los tests, abrir la PR) ya no los ejecuta una persona. Los ejecuta un agente de IA con sus propias herramientas y permisos, dentro de los límites que le marcamos. Los pasos son los mismos de siempre. Lo que ha cambiado es quién los ejecuta. Y eso obliga a repensar dónde va la atención humana.

La decisión que tomamos fue esta: **la revisión humana deja de ser una puerta antes del merge y pasa a ser una capa después.** Una PR solo se integra si todas sus puertas (tests, spec, auditoría, contratos) están en verde. La persona revisa el resultado, no cada línea que lo produjo.

El motivo no es la velocidad. El motivo es que una persona leyendo diffs generados por agentes, al ritmo al que los generan, deja de ser una señal de calidad. **Se convierte en teatro.**

## No somos los únicos

Robert C. Martin, Uncle Bob, el autor de *Clean Code*, el que se pasó veinte años enseñándonos a leer código con lupa, respondió esto a un desarrollador que decía que no podía dejar que un agente tocara código que no entendía, y se hizo viral:

> "Empecé a programar a finales de los 60. Mi estrategia actual es no leer nada del código que escriben mis agentes. Es la única forma de aprovechar su productividad. Lo que hago en su lugar es rodear a los agentes de restricciones extremas. Tests unitarios, tests en gherkin, procedimientos de QA, métricas de calidad, mutation testing, cobertura de tests y un montón más. Al final, tengo muchísima confianza en el código que producen porque han tenido que superar la prueba de todas mis restricciones y tests."
>
> — [Robert C. Martin](https://x.com/unclebobmartin/status/2080257779395154409), 23 de julio de 2026

Ya lo había [dicho en abril](https://x.com/unclebobmartin/status/2044114698451476492), en una respuesta que tuvo mucha menos repercusión: no revisa el código de los agentes, mide cobertura, estructura de dependencias, complejidad ciclomática y mutation score, porque "los humanos somos lentos con el código". La versión de julio es la que caló.

Viniendo de él, incomoda. Pero apunta exactamente a lo que ya estábamos construyendo: en vez de leer el código, diseñar la jaula de tests que ese código tiene que superar, y dejar que el agente escriba dentro de ella. Si la superficie de restricciones está bien construida, la calidad deja de depender de que alguien mire cada línea.

## Dos cosas distintas a las que llamamos jaula

Esta es una distinción que me costó ver.

Hay dos cosas a las que llamamos "jaula" y no son lo mismo. La primera es el conjunto de comprobaciones que un cambio tiene que pasar antes de salir: los tests, el mutation score, los escaneos de seguridad, la spec contra la que se construyó. Eso **comprueba el resultado**. No le importa lo bueno que sea el modelo, porque tendría que existir aunque el código lo hubiera escrito una persona.

La segunda es el proceso por el que obligamos al agente a pasar para llegar ahí: qué paso va primero, qué artefacto tiene que producir antes de dejarle producir el siguiente, cuánto del trabajo es andamiaje para que un modelo flojo no se salga de los raíles. Eso **comprueba el camino**. Y cada nueva versión de modelo deja parte de ello sin sentido.

> La jaula que comprueba el resultado no envejece con los modelos. La que comprueba el camino, sí.

La nuestra es sobre todo del primer tipo. No del todo: exigir que cada cambio toque una spec es una restricción de camino, que mantenemos porque la spec es contra lo que se comprueba el resultado. Clasificar honestamente nuestras puertas en esos dos montones es trabajo que aún no hemos terminado.

## Más ingeniería, no menos

Es tentador leer todo esto como "menos ingeniería, más automatización". Es exactamente al revés.

Alguien tiene que dibujar los bounded contexts, decidir los invariantes, escribir la spec contra la que construye el agente, diseñar la batería de tests que tiene que cazar la regresión antes de que ninguna persona mire el diff. Eso es ingeniería más difícil que teclear la línea a mano. Es, de hecho, **la ingeniería que antes nos saltábamos**, porque siempre había un revisor detrás haciendo de red de seguridad.

Ahora la red de seguridad es el sistema. Y eso significa que el sistema tiene que estar bien construido, o nada caza el error. Justo ahora, cuando tenemos más capacidad de ingeniería que nunca, es cuando más disciplina de ingeniería necesitamos, no menos.

## Cómo es la jaula por dentro

Todo esto se queda en abstracto hasta que abres una. Así que, en la aplicación donde tomamos la decisión, la jaula es más o menos esta.

**Cada cambio empieza con una spec escrita.** Antes de generar una sola línea, el cambio tiene que estar descrito: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla. Una spec vaga no produce mal código. Produce buen código para el problema equivocado.

**Miles de tests en cada cambio.** Unos cuatro mil entre la API y la web, y los que tocan la base de datos se ejecutan contra una base de datos real. Esto es lo que sustituye al ojo del revisor, y tiene que ser grande porque tiene que cazar lo que una persona cazaba leyendo.

**Rompemos nuestro propio código a propósito para ver si los tests se dan cuenta.** Se llama mutation testing. No basta con que una línea esté cubierta por un test: introducimos pequeños errores deliberados y comprobamos que al menos un test falla por su culpa. Un test que se ejecuta pero nunca falla es decoración. Así sabemos que la red es real, que es la pregunta que de verdad importa cuando nadie lee el diff.

**Seguridad en cada build, sin pedirla.** TruffleHog para secretos filtrados, Trivy para vulnerabilidades conocidas en dependencias e infraestructura, Semgrep para patrones inseguros en el código. Los tres bloquean. Nada de esto necesita que una persona se dé cuenta, y nada debería depender de una.

**Cada build sabe lo que lleva dentro.** Cada build genera una lista de materiales del software, un SBOM, con Syft: una lista completa y legible por máquina de cada paquete y componente que contiene la aplicación, y con qué licencia. Una comprobación aparte valida cada licencia de esa lista contra lo que podemos distribuir. Cuando se anuncia una vulnerabilidad nueva, responder "¿nos afecta?" lleva segundos en lugar de abrir cada build. Un paquete con una licencia que no podemos distribuir se caza antes de llegar a un entregable. Y es lo primero que pide un equipo de seguridad o un auditor ISO, que es justo por lo que antes se hacía a mano, una vez, la semana antes de la auditoría.

**Lo que se despliega se vuelve a probar como sistema en marcha.** Después del merge, el código va a un entorno de staging y ZAP lo sondea automáticamente como lo haría un atacante, antes de que una persona confirme el paso a producción. La jaula no termina en el merge.

**La ingeniería que siempre se aplazaba ahora se hace.** Todos los equipos conocen la lista: restaurar un backup para demostrar que funciona, rotar los secretos, revisar quién sigue teniendo acceso, comprobar que lo que corre coincide con lo descrito, mantener el runbook al día. Siempre importante, siempre lo primero que pide el auditor, siempre para el trimestre que viene. La restauración del backup ahora corre con un temporizador, y el resto de la lista es a donde va la capacidad liberada. Un backup que nadie ha restaurado es una hipótesis, y una lista de accesos que nadie revisa es un riesgo. La evidencia de auditoría que antes era una carrera de última hora pasa a ser un subproducto del build.

## Las 7 puertas que pasa una PR antes de que la vea una persona

La misma jaula, como lista para copiar y adaptar. Cada línea bloquea el merge.

1. **Spec.** El cambio se describe antes de generar código: qué hace, qué no puede romper, cómo sabremos que funciona. Si falta o está mal formada, el build falla.
2. **Tests.** Unos 4.000 entre API y web. Los que tocan la base de datos se ejecutan contra una real.
3. **Mutation score.** Stryker inyecta pequeños bugs y comprueba que un test falla. Cada módulo mantiene una puntuación mínima.
4. **Secretos.** TruffleHog busca credenciales filtradas. Bloqueante.
5. **Vulnerabilidades.** Trivy analiza dependencias y código de infraestructura. Bloquea en críticas y altas.
6. **Patrones inseguros.** Semgrep como análisis estático. Bloqueante.
7. **SBOM y licencias.** Syft lista cada componente; una política valida cada licencia contra lo que podemos distribuir.

Después del merge, una más antes de producción: ZAP sondea el despliegue en staging como lo haría un atacante, y solo entonces una persona confirma el paso.

Nada de esto llegó de golpe y nada es gratis. Casi todas las protecciones de esa lista existen porque algo se coló, o porque vimos cómo podía colarse. Esa es la forma honesta del trato: **no dejas de leer diffs y luego construyes la jaula. Construyes la jaula primero, la sigues pagando, y el día que deja de cazar cosas vuelves a leer diffs.** Saltarse la primera mitad y quedarse con la segunda no es lo que describo. Eso es simplemente no revisar código.

## Lo que sigue siendo humano

Nada de esto significa soltar el volante. Sigue habiendo una puerta de entrada innegociable: la issue. Ningún cambio nace de una idea suelta o de un prompt improvisado. Nace de un problema descrito, analizado y con criterios de aceptación explícitos. Ahí es donde ponemos el criterio humano: en qué construir y por qué, no en la sintaxis de cómo se construye.

Y hay líneas rojas que no se negocian, venga el cambio de un agente o de una persona: nadie toca las claves de firma, nadie hace force-push sobre el trabajo de otro, nadie despliega a producción sin que una persona lo confirme.

Tampoco se mueve la responsabilidad. **Nadie explica un incidente en producción diciendo que lo escribió el agente.** Decidir no leer cada línea es una decisión sobre dónde merece la pena poner la atención, no una cesión de autoría. Quien integró el cambio sigue respondiendo por él.

## Y los modelos siguen mejorando

Sería fácil terminar con "y por eso necesitas una jaula" y dejarlo ahí. También sería un error. Construimos la jaula contra los modelos que teníamos cuando la construimos, y los modelos mejoran más rápido que las herramientas que los contienen. Parte de lo que pusimos para mantener a un agente en los raíles ya sobra, y sobrará más. Fingir lo contrario sería el mismo teatro del que me quejaba al principio.

Así que no perdamos la cabeza en ninguna de las dos direcciones. La ingeniería no desaparece: alguien tiene que escribir la spec, decidir los invariantes y construir las comprobaciones que te dicen si lo que ha salido es lo que se pidió. Esa parte gana importancia a medida que mejoran los modelos, no la pierde, porque es lo único que queda entre un modelo muy capaz y producción.

Lo que se abarata es todo lo construido para mantener al modelo en el camino: el andamiaje, la ceremonia, los pasos añadidos porque un modelo anterior se perdía sin ellos. Cada uno de esos es un barrote que quitar el día que deja de cazar nada, y cuanto antes llegue ese día, mejor: **cada barrote que quitas es esfuerzo que vuelve a la ingeniería que importa.**

> Una puerta se gana su sitio cazando algo. Cuando lleva meses sin cazar nada, es un coste, no una protección.

La forma de gestionarlo es la misma con la que construimos la jaula: midiendo. Las puertas de resultado seguirán ganándose su sitio durante mucho tiempo. Muchas de las de camino no, y está bien. Así se ve cuando los modelos son lo bastante buenos como para que el cuello de botella se mueva, otra vez, a la ingeniería que los rodea.

La revisión se ha movido. La responsabilidad, no. Puedes dejar de leer cada diff. No puedes dejar de responder por lo que sale a producción. Y por eso construir la jaula es la ingeniería, y saber qué barrotes quitar a medida que mejoran los modelos es la parte que menos estoy dispuesto a delegar.

*Este artículo parte de una nota interna escrita junto a Quique Fernández.*
