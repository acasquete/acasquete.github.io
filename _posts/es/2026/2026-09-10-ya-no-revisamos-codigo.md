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
Este mes compartí una nota interna con todo el equipo de Plain Concepts. El titular, *"ya no revisamos código"*, lo elegí a propósito para que llamara la atención, pero es lo de menos: lo importante son las conversaciones que abre este tipo de declaraciones y que, por fin, dijéramos en voz alta algo que muchos veíamos venir desde hacía un año, aunque nadie tuviera muy claro cómo iba a llegar.<!-- excerpt-end -->

Puede que lo único que hizo el titular fuera poner palabras a algo que muchos pensábamos, esperando a que alguien lo dijera: una nueva forma de hacer software ha llegado y no se parece del todo a lo que imaginábamos.

## Qué ha pasado

Hasta hace poco, revisar una PR significaba lo de siempre: alguien leía los cambios, dejaba comentarios, la aprobaba y solo entonces el código llegaba a producción. Hoy, en catorce aplicaciones internas de la compañía, ese paso está desapareciendo. Y no porque hayamos bajado el listón, sino porque lo hemos subido en otro sitio.

En esas aplicaciones, buena parte de los pasos del ciclo (leer la *issue*, escribir el código, ejecutar los tests, abrir la PR) ya no los hace una persona, sino un agente de IA con sus propias herramientas y permisos, dentro de los límites que le marcamos. Los pasos son los de siempre; lo que ha cambiado es quién los da, y eso nos obliga a replantearnos dónde ponemos la atención humana.

La decisión que tomamos fue esta: **la revisión humana deja de ser una puerta antes del merge y pasa a ser una capa posterior.** Una PR solo se integra si todas sus puertas (tests, spec, auditoría, contratos) están en verde: comprueban que hace lo que se pidió, que no rompe lo que ya funcionaba y que respeta los requisitos de seguridad. La persona revisa el resultado, no cada línea que lo ha producido.

El motivo no es ir más rápido, sino que, con este volumen de cambios, leer cada uno deja de ser una señal fiable de calidad. **Se convierte en teatro.**

## No somos los únicos

Robert C. Martin, Uncle Bob, el autor de *Clean Code*, el que se pasó veinte años enseñándonos a leer código con lupa, le respondió hace poco a un desarrollador que decía que no podía dejar que un agente tocara código que no entendía. Su respuesta se hizo viral:

> "Empecé a programar a finales de los 60. Mi estrategia actual es no leer nada del código que escriben mis agentes. Es la única forma de aprovechar su productividad. Lo que hago en su lugar es rodear a los agentes de restricciones extremas. Tests unitarios, tests en Gherkin, procedimientos de QA, métricas de calidad, mutation testing, cobertura de tests y un montón más. Al final, tengo muchísima confianza en el código que producen porque han tenido que superar todas mis restricciones y tests."
>
> — [Robert C. Martin](https://x.com/unclebobmartin/status/2080257779395154409), 23 de julio de 2026

Ya lo había [dicho en abril](https://x.com/unclebobmartin/status/2044114698451476492), en una respuesta que tuvo mucha menos repercusión: no revisa el código de los agentes; mide cobertura, estructura de dependencias, complejidad ciclomática y mutation score, porque "los humanos somos lentos con el código". La de julio, en cambio, dio mucho que hablar.

Viniendo de él, incomoda. Pero apunta justo a lo que ya estábamos construyendo: en vez de leer el código, diseñar la jaula de tests que ese código tiene que superar y dejar que el agente escriba dentro de ella. Si el conjunto de restricciones está bien construido, la calidad deja de depender de que alguien mire cada línea.

## Dos cosas distintas a las que llamamos jaula

Hay dos cosas a las que llamamos "jaula" y no son lo mismo, una distinción que me costó ver. La primera es el conjunto de comprobaciones que un cambio tiene que pasar antes de salir: los tests, el mutation score, los escaneos de seguridad, la spec contra la que se construyó. Eso **comprueba el resultado** y le da igual lo bueno que sea el modelo, porque tendría que existir aunque el código lo hubiera escrito una persona.

La segunda es el proceso por el que obligamos a pasar al agente para llegar hasta ahí: qué paso va primero, qué artefacto tiene que producir antes de dejarle pasar al siguiente, cuánto del trabajo es andamiaje para que un modelo flojo no se salga del carril. Eso **comprueba el camino**. Es lo que en inglés se llama el *harness* del agente: el arnés de herramientas, permisos, pasos y plantillas que envuelve al modelo y le marca por dónde puede moverse. Y con cada nueva versión de los modelos, una parte deja de tener sentido.

> La jaula que comprueba el resultado no envejece con los modelos. La que comprueba el camino, sí.

La nuestra es sobre todo del primer tipo, aunque no del todo: exigir que cada cambio toque una especificación es una restricción de camino, y la mantenemos porque la *spec* es aquello contra lo que se comprueba el resultado. Separar con honestidad nuestras puertas es un trabajo que todavía no hemos terminado.

## Más ingeniería, no menos

Es tentador leer todo esto como "menos ingeniería, más automatización", pero es justo al revés.

Alguien tiene que dibujar los *bounded contexts*, decidir los invariantes (lo que nunca puede dejar de cumplirse), escribir la *especificación* contra la que construye el agente y diseñar la batería de tests que tiene que cazar la regresión antes de que nadie mire el código. Eso es bastante más difícil que escribir el código a mano y es, de hecho, **la ingeniería que antes nos saltábamos**, porque siempre había un revisor detrás haciendo de red de seguridad.

Ahora la red de seguridad es el sistema, así que tiene que estar bien construido o nadie cazará el error. Justo ahora, cuando tenemos más capacidad de ingeniería que nunca, es cuando más disciplina de ingeniería necesitamos.

## Las 11 puertas, una a una

Todo esto suena abstracto hasta que abres una jaula. Nuestras cifras importan poco y no hace falta copiar nuestras herramientas: lo útil es saber qué se puede controlar en cada cambio sin que nadie lea el código. Nosotros lo hemos concretado en once puertas: nueve se ejecutan en cada build y dos contra el sistema ya desplegado en un entorno de pruebas.

Las medimos en Pulse, un panel interno que lee de GitHub qué prácticas protegen cada repositorio, con qué herramienta y si pasaron en su última ejecución.

![Tabla de Pulse con las puertas que se ejecutan en cada build: especificación, tests y cobertura, mutación, secretos, vulnerabilidades, patrones inseguros, SBOM y licencias, complejidad e higiene de código.](/img/ya-no-revisamos/pulse-puertas.png)

*Las puertas de una de nuestras aplicaciones en Pulse. Cada una indica su modo: bloquear, exigir un umbral o aplicar una política.*

### En cada build

**1. Especificación ejecutable.** Antes de generar una sola línea, el cambio tiene que estar descrito: qué hace, qué no puede romper y cómo sabremos que funciona. Ese comportamiento se escribe en escenarios que se ejecutan de verdad, por ejemplo en Gherkin. Controla que el cambio hace lo que se pidió, no solo que compila. Si la spec falta o está mal formada, el build falla, porque una spec vaga no produce mal código; produce buen código para el problema equivocado.

**2. Tests y cobertura.** Los tests de la API y de la web se ejecutan en cada cambio y sustituyen al ojo del revisor, así que deben cazar lo que una persona cazaba leyendo. La cobertura no demuestra que el código funcione; dice qué código no se ha ejecutado nunca. Por eso el mínimo se fija por módulo y no como media global, que puede esconder una parte crítica sin probar.

**3. Mutación.** Herramientas como Stryker introducen pequeños errores a propósito, como cambiar un `>` por un `>=`, y comprueban que al menos un test falla. Si ninguno falla, los tests no estaban comprobando nada. Un test que se ejecuta pero nunca falla es decoración. Esta puerta es clave cuando el mismo agente escribe el código y sus tests: cada módulo tiene una puntuación mínima y un cambio que la baja no entra.

**4. Secretos.** TruffleHog busca contraseñas, claves y tokens en el código. Un agente puede copiar una credencial de un ejemplo o de un fichero de configuración sin darse cuenta, igual que una persona con prisa. Si aparece una, el build falla.

**5. Vulnerabilidades en dependencias e infraestructura.** Trivy revisa los paquetes que usa la aplicación y el código de infraestructura en busca de vulnerabilidades conocidas y configuraciones inseguras. Importa aún más con agentes, porque añadir una dependencia les cuesta muy poco. Los hallazgos críticos y altos bloquean el cambio.

**6. Patrones inseguros.** Semgrep analiza el código sin ejecutarlo y detecta formas de programar que suelen acabar en un problema de seguridad, como las que abren la puerta a una inyección. Es análisis estático (SAST): caza el problema en el momento en que se escribe, no cuando ya está en producción.

**7. SBOM y licencias.** Cada build genera una lista de materiales del software: un inventario completo y legible por máquina de cada paquete que contiene la aplicación, con su licencia. Una política comprueba que podemos distribuirlos todos. Además, es lo primero que pide un auditor, y antes se hacía a mano, una sola vez, la semana anterior a la auditoría.

**8. Complejidad.** Mide la complejidad ciclomática y el índice CRAP, que combina la complejidad de un método con lo poco que está probado, porque ahí es donde suelen esconderse los errores. Esta puerta no exige limpiar todo lo antiguo, sino impedir que aparezcan nuevos puntos críticos. Si hay una excepción, se justifica por escrito.

**9. Higiene de código.** La llamamos así, pero es la puerta contra lo que en inglés se conoce como *AI slop*: código duplicado, excepciones silenciadas y código muerto. Un agente tiende a escribir algo nuevo en lugar de reutilizar lo que ya existe, y el resultado funciona, pero se degrada con el tiempo. Herramientas como jscpd lo miden en cada build y un umbral impide que empeore.

### Con el sistema en marcha

**10. Análisis dinámico.** Después del merge, el código se despliega en un entorno de pruebas y ZAP lo sondea automáticamente como lo haría un atacante. Es análisis dinámico (DAST): encuentra lo que no se ve en el código, sino en la aplicación funcionando. La jaula no termina en el merge.

**11. Rendimiento.** Cuando el proyecto lo requiere, las pruebas de carga, por ejemplo con k6, comprueban que los tiempos de respuesta se mantienen dentro de un presupuesto. Un cambio puede pasar todas las puertas anteriores y hacer que la aplicación sea lenta. Solo después de estas dos comprobaciones una persona confirma el paso a producción.

![Tabla de Pulse con las dos puertas que se ejecutan tras desplegar en el entorno de pruebas: DAST con OWASP ZAP y rendimiento con k6.](/img/ya-no-revisamos/pulse-puertas-despliegue.png)

*Las dos puertas que se ejecutan contra el entorno de pruebas ya desplegado.*

### Lo que medimos: excelencia de ingeniería

Las puertas dicen si un cambio entra; la excelencia de ingeniería dice cómo evoluciona el sistema con el tiempo. El propio pipeline de cada aplicación publica estos indicadores en cada commit:

![Indicadores de excelencia de ingeniería en Pulse: cobertura, mutación, métodos con CRAP superior a 30, vulnerabilidades críticas y altas, componentes en el SBOM y deuda de complejidad.](/img/ya-no-revisamos/pulse-excelencia.png)

* **Cobertura:** qué parte del código se ejecuta en los tests.
* **Mutación:** cuántos errores introducidos a propósito detectan esos tests.
* **CRAP > 30:** cuántos métodos combinan mucha complejidad con pocas pruebas.
* **Críticas y altas:** vulnerabilidades graves abiertas, que deberían estar a cero.
* **Componentes:** el tamaño de lo que contiene la aplicación, según su SBOM.
* **Deuda de complejidad:** la complejidad acumulada y si crece. Lo importante no es tanto la cifra como que no aparezca deuda nueva sin justificar.

El detalle por módulo enseña lo que una media esconde: cada módulo tiene su propio mínimo, la línea discontinua, y se ve a simple vista cuál se está acercando a él:

![Cuatro gráficas de Pulse con la puntuación de mutación por módulo durante un mes, cada una con su mínimo marcado con una línea discontinua.](/img/ya-no-revisamos/pulse-mutacion.png)

*La puntuación de mutación de cada módulo frente a su mínimo a lo largo de un mes.*

### Lo que todavía no es una puerta: el pentesting

La prueba de intrusión aún no forma parte de nuestro flujo, pero la IA la ha hecho mucho más fácil. Antes era un proyecto en sí mismo; ahora se puede preparar y ejecutar una prueba acotada casi como cualquier otra tarea.

Lo importante no es cuándo se hace, sino qué se revisa y qué se puede tocar en cada entorno.

**En preproducción, una prueba activa de caja gris.** Con datos de prueba, un acceso por cada rol y sin ataques de denegación de servicio, se revisa:

* **Reconocimiento:** qué rutas expone la aplicación y si cada ruta protegida declara el permiso que exige.
* **Autenticación:** que se rechacen los tokens caducados, falsificados o ausentes.
* **Permisos:** que un usuario no pueda ver los datos de otro ni usar las funciones de un rol superior.
* **Validación de entradas:** que nadie se salte las validaciones, que no se puedan modificar campos no previstos y que no haya inyecciones ni código malicioso almacenado.
* **Auditoría:** que ningún cambio de estado escape del registro y que el registro no se pueda alterar.
* **Configuración:** las cabeceras de seguridad, los mensajes de error que dan demasiada información y la exposición de secretos.

**En producción, solo pruebas no destructivas.** Sin ninguna petición que cambie datos, se revisa:

* **Autenticación:** que se rechacen las credenciales ausentes, mal formadas o falsificadas.
* **Superficie expuesta:** que la documentación de la API no sea accesible sin autenticarse.
* **Peticiones desde otros orígenes:** que la aplicación no las acepte sin más.
* **Cifrado y cabeceras:** que se rechacen las versiones antiguas de TLS y que las cabeceras de seguridad estén bien configuradas.
* **Auditoría:** una verificación de solo lectura de que el registro sigue íntegro.

Lo que no se puede probar ahí sin riesgo, como los permisos entre usuarios, se prueba en preproducción. Cada hallazgo confirmado se convierte en una tarea con su severidad, los pasos para reproducirlo y el criterio para darlo por resuelto.

No sustituye a una auditoría externa, pero es algo que podemos ejecutar mucho más a menudo. Es especialmente importante hacerlo antes de una versión relevante, al tocar la autenticación, los permisos o los datos sensibles, y cada vez que se expone algo nuevo a internet.

### La ingeniería que siempre se aplazaba

Por fin hacemos la ingeniería que muchos sabíamos necesaria, pero que la falta de tiempo dejaba siempre para después. Muchos equipos conocen esta lista: restaurar un backup para demostrar que funciona, ejecutar pruebas de rendimiento y de intrusión, revisar quién sigue teniendo acceso, comprobar que lo que se está ejecutando coincide con lo documentado, mantener el runbook al día. Siempre importante, siempre lo primero que pide el auditor, siempre para el trimestre que viene. Un backup que nadie ha restaurado es una hipótesis, y una lista de accesos que nadie revisa es un riesgo. Las evidencias de auditoría, que antes eran una carrera de última hora, ahora salen solas con cada build.

Nada de esto llegó de golpe ni sale gratis. La jaula hay que diseñarla, mantenerla y ajustarla a medida que cambian los riesgos. Ese es el trato: **primero construyes los mecanismos que demuestran que el software funciona y solo entonces dejas de depender de que alguien lea cada cambio.** Dejar de revisar sin haberlos construido no es lo que describo: eso es, sin más, bajar el listón.

## Lo que sigue siendo humano

Nada de esto significa soltar el volante. Sigue habiendo una puerta de entrada innegociable: ningún cambio nace de una idea suelta o de un prompt improvisado, sino de un problema descrito, analizado y con criterios de aceptación explícitos. Ahí es donde ponemos el criterio humano: en qué construir y por qué, no en la sintaxis de cómo se construye.

Y hay líneas rojas que el agente no cruza solo: antes de tocar producción, se detiene y pide confirmación a una persona. Los cambios que afectan a dominios sensibles, como la seguridad, o a una decisión de arquitectura documentada (ADR) también necesitan su aprobación.

La responsabilidad tampoco se mueve. **Nadie explica un incidente en producción diciendo que lo escribió el agente.** Decidir no leer cada línea es decidir dónde merece la pena poner la atención, no ceder la autoría. Quien integró el cambio sigue respondiendo por él.

## Y los modelos siguen mejorando

Sería fácil terminar con "y por eso necesitas una jaula" y quedarse ahí, pero sería un error. Construimos la jaula pensando en los modelos que teníamos en ese momento, y los modelos mejoran más rápido que las herramientas que los contienen. Parte de lo que pusimos para que un agente no se saliera del carril ya sobra, y sobrará más. Fingir lo contrario sería el mismo teatro del que me quejaba al principio.

Así que no perdamos la cabeza ni en un sentido ni en otro. La ingeniería no desaparece: alguien tiene que escribir la spec, decidir los invariantes y construir las comprobaciones que te dicen si lo que ha salido es lo que se pidió. Esa parte gana importancia a medida que mejoran los modelos, porque es lo único que queda entre un modelo muy capaz y producción.

Lo que se abarata es el *harness*, todo lo que construimos para mantener al modelo en el camino: el andamiaje, la ceremonia, los pasos añadidos porque un modelo anterior se perdía sin ellos. Cada uno de ellos es un barrote que conviene quitar el día que deje de cazar algo, y cuanto antes llegue ese día, mejor: **cada barrote que quitas es esfuerzo que vuelve a la ingeniería que importa.**

> Una puerta se gana su sitio cazando algo. Si lleva meses sin cazar nada, es un coste, no una protección.

La forma de gestionarlo es la misma con la que construimos la jaula: midiendo. Las puertas de resultado seguirán ganándose su sitio durante mucho tiempo; muchas de las de camino no, y no pasa nada: es lo que ocurre cuando los modelos son lo bastante buenos como para que el cuello de botella vuelva a desplazarse a la ingeniería que los rodea.

La transformación no consiste en sustituir el criterio humano por una sucesión de herramientas. Consiste en reservar ese criterio para las decisiones en las que realmente aporta valor: entender el problema, definir qué solución necesitamos y establecer los límites que no deben cruzarse.

El futuro del desarrollo no pasa por revisar más código, sino por tener mejores mecanismos para saber qué estamos construyendo, cómo funciona y qué garantías tenemos de que podemos confiar en ello.
