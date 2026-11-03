---
# Private preview: a page, not a post, so it stays out of the home page, /blog, tags, the feed and search.
layout: post
permalink: /p/cda77c06/el-nuevo-ide
date: 2026-11-02
sitemap: false
noindex: true
comments: false
header_image: el-nuevo-ide-cover.jpg
cover_ratio: 16 / 9
description: Ya no abrimos el IDE. No es una preferencia, es una prueba de madurez. Y lo que necesitamos ahora no es un editor mejor, sino una forma de controlar decenas de sesiones a la vez.
title: El nuevo IDE
tags: [artificial_intelligence, programming]
reviewed: false
home: false
ai: true
---
En abril de 2025 se publicó [*AI 2027*](https://ai-2027.com/), un escenario que contaba, mes a mes, cómo podría llegar una inteligencia artificial superhumana. Casi todo el texto habla de geopolítica y de riesgos, pero hay una línea, fechada a finales de 2026, que leí entonces como ciencia ficción: a los programadores que mejor les iría serían los que supieran «gestionar y controlar la calidad de equipos de IA».<!-- excerpt-end -->

Estamos a finales de 2026. No tenemos las doscientas mil copias de agentes que imaginaba el escenario, pero en nuestro equipo de plataforma una persona puede tener abiertas decenas de sesiones a la vez. Y hay algo que *AI 2027* daba por hecho sin explicarlo nunca: con qué herramienta se supervisa todo eso. Esa herramienta todavía no existe.

## Ya no abrimos el IDE

En el [post anterior](/ya-no-revisamos-codigo) conté que habíamos dejado de revisar cada cambio a mano. La consecuencia lógica llegó sola: si no lees el código antes del *merge*, el editor deja de ser el sitio donde pasa el trabajo. Hoy no usamos IDE. Trabajamos con agentes en la terminal.

En el equipo de plataforma trabajamos con Claude Code, en su versión de terminal, y con OpenCode. Y delegamos todo el trabajo que podemos en flujos agénticos que se ejecutan en GitHub.

No lo cuento como una preferencia, ni como una pose. Lo planteo como una **prueba de madurez**. Dejar el IDE solo es posible cuando el resto del sistema es lo bastante bueno como para no necesitar mirar el código: una especificación ejecutable, puertas que bloquean, permisos claros y trazabilidad de cada cambio. Si para confiar en lo que ha hecho un agente todavía tienes que abrir el editor y leerlo, el problema no es la herramienta: es que tu sistema aún no está listo.

## La paradoja

Los datos dicen lo contrario de lo que vivimos, o eso parece. En la [encuesta de Stack Overflow de 2026](https://visualstudiomagazine.com/articles/2026/10/06/stack-overflow-2026-survey-vs-code-leads-visual-studio-takes-third.aspx), VS Code sigue siendo el IDE más usado. Pero en la misma encuesta, Claude Code es el agente más usado, con un 65,5 %, y el uso de agentes ha pasado del 31 % en 2025 al 59 % en abril de este año.

Todo el mundo tiene el IDE instalado. Cada vez menos gente trabaja dentro de él. Y los fabricantes lo saben:

- Microsoft ha sacado [VS Code Agents](https://www.infoworld.com/article/4156038/visual-studio-code-1-115-introduces-vs-code-agents-app.html), una aplicación aparte del editor para lanzar y seguir sesiones de agentes en paralelo. La novedad de Visual Studio 2026 se resumió con un titular que lo dice todo: [asigna una tarea, cierra el IDE, recibe una PR](https://visualstudiomagazine.com/articles/2026/04/29/vs-2026-joins-vs-code-with-integrated-cloud-agent-assign-a-task-close-the-ide-get-a-pr.aspx).
- Cursor 3 estrenó una [ventana de agentes](https://www.datacamp.com/blog/cursor-3) construida desde cero alrededor de los agentes, no del editor de archivos.
- JetBrains lanzó [Air](https://tech-insider.org/jetbrains-air-eap-ides-multi-agent-2026/), un orquestador de varios agentes que ni siquiera trae agentes propios: ejecuta los que tengas instalados.

Los tres hacen lo mismo: construir, al lado del editor, una ventana para los agentes. Es la forma más honesta de reconocer que el trabajo ya no pasa por el editor. Pero también es una solución a medias: siguen pensando en conversaciones.

## Sesiones, no conversaciones

Esta es la distinción que creo que importa.

Una **conversación** es un chat: preguntas, el modelo responde, sigues preguntando. Está pensada para una persona y un agente, y para que la persona esté delante.

Una **sesión** es un trabajo en marcha. Tiene un objetivo (una *issue*, una especificación), una rama o un *worktree*, unos permisos, un coste acumulado, un estado (trabajando, bloqueada, esperando una decisión, en revisión) y un resultado que se puede verificar: las puertas que ha pasado y las que no.

Con una conversación, la pregunta es *qué me ha dicho*. Con decenas de sesiones, las preguntas son otras: cuáles me necesitan ahora, cuáles se han atascado, cuáles están gastando sin avanzar y cuáles puedo dar por buenas sin mirarlas.

Hoy lo resolvemos con lo más simple que hay: varias pestañas en una terminal, una por sesión. Funciona mientras son pocas. Cuando son decenas, la terminal deja de ser una herramienta y se convierte en un pasillo de puertas cerradas.

Y ahí es donde se nota lo que falta. Saber qué sesión espera una decisión mía sin ir pestaña por pestaña. Ver cuánto cuesta cada una y cuántas veces llega al tope de la ventana de contexto. Retomar una sesión que dejé ayer. Saber si una ya ha entrado en el flujo de despliegue, si una puerta ha fallado en alguna parte de ese flujo y el agente está reimplementando, y cuánto tarda en hacerlo.

Y todo eso es dentro de un solo proyecto. En el equipo de plataforma no llevamos uno, sino varios a la vez, cada uno con sus sesiones, sus despliegues y sus dependencias. Las pestañas de una terminal son de una persona; el trabajo es del equipo. Lo que hace falta no es una ventana por persona, sino un panel compartido en el que todo el equipo vea lo mismo: qué sesiones hay en marcha en cada proyecto, quién atiende cada una y qué está esperando a quién.

## Cómo debería ser el nuevo IDE

Si el IDE clásico era un editor con herramientas alrededor, el nuevo es una consola de operaciones. Si tuviera que ponerle nombre, bastaría con cambiar una letra: no un IDE, sino un **ICE**, un *Integrated Control Environment*. La D de desarrollo deja paso a la C de control: ya no es el sitio donde se escribe el código, sino desde donde se supervisa a quienes lo escriben.

Sin pretender tener el diseño cerrado, esto es lo que creo que necesita un ICE:

1. **Una bandeja de decisiones, no de mensajes.** Lo primero que ves no es código ni chats, sino lo que te espera: una sesión que pide permiso para tocar algo sensible, una especificación ambigua, un *gate* que ha fallado dos veces.
2. **El estado de cada sesión de un vistazo.** Trabajando, bloqueada, esperando, lista. En qué punto del flujo de despliegue está, si alguna puerta ha fallado y cuántas veces y cuánto tiempo lleva reimplementando. Como un tablero de despliegues, no como una lista de pestañas.
3. **Varios proyectos, un panel compartido.** Las sesiones se agrupan por proyecto, pero se ven juntas, y el panel es del equipo, no de una persona: todos ven lo mismo, se sabe quién atiende cada sesión y cualquiera con contexto puede tomar una decisión pendiente.
4. **Evidencias antes que *diffs*.** De cada sesión quiero ver primero qué puertas ha pasado (tests, mutación, seguridad, especificación) y solo después, si hace falta, el cambio. El *diff* deja de ser la puerta de entrada.
5. **Coste y presupuesto por sesión.** Cuánto lleva gastado, cuánto se espera que gaste y cuándo pararla. Una sesión que da vueltas es dinero que se va. Y cuántas veces ha llegado al tope de la ventana de contexto: una sesión que se compacta una y otra vez pierde memoria y gasta de más, y suele ser la señal de que hay algo que optimizar, como una tarea demasiado grande, un contexto inflado con archivos que no hacían falta o una especificación que habría que partir.
6. **Permisos y líneas rojas visibles.** Qué puede hacer cada sesión, qué no, y cuándo se va a detener para pedir confirmación. Y de quién depende: si para desplegar necesita algo de otro equipo, tiene que saberse antes de empezar y no cuando ya está bloqueada, junto con una estimación de cuánto le falta para terminar.
7. **Trazabilidad de punta a punta.** De la *issue* a la especificación, de la especificación a la sesión, de la sesión a la PR y de la PR a producción. Si algo falla en producción, tiene que poder seguirse hacia atrás.
8. **Pausar, retomar y repartir.** Las sesiones duran horas o días. Tienen que poder pararse, retomarse con su contexto y pasarse a otra persona.
9. **Un límite de trabajo en curso.** Tener cien sesiones abiertas no es productividad si nadie puede atenderlas. La herramienta debería ayudar a no lanzar más de las que se pueden supervisar.

Fíjate en lo que no aparece en la lista: escribir código. El editor no desaparece, pero pasa a ser una vista más, la que abres en el caso raro en que de verdad necesitas leer algo.

## Lo que no es

No es un chat con pestañas. Tampoco es el editor de siempre con un panel lateral para el agente. Y no es una herramienta personal: si las sesiones son trabajo del equipo y abarcan varios proyectos, el nuevo IDE es, sobre todo, un panel compartido.

Steve Yegge lo describe como el momento en que [tu IDE desaparece y no vuelves a abrirlo nunca](https://newsletter.pragmaticengineer.com/p/from-ides-to-ai-agents-with-steve), y ahora habla de que el IDE volverá, pero como centro de control de agentes. Estoy de acuerdo con la segunda parte. Lo que vuelve no es el editor: es la necesidad de un sitio donde trabajar.

## Una prueba de madurez

Antes de dejar el IDE, o de presumir de haberlo dejado, conviene hacerse unas pocas preguntas:

- ¿Puedes saber si un cambio es correcto sin leerlo?
- ¿Las puertas bloquean de verdad, o solo avisan?
- ¿Sabes qué puede tocar cada agente y qué no?
- ¿Puedes seguir un incidente de producción hasta la sesión que lo provocó?
- ¿Sabes cuánto te cuesta cada cambio?

Si la respuesta a alguna es no, el IDE todavía te hace falta. No porque escribas código en él, sino porque es tu última red de seguridad.

## El IDE que falta

*AI 2027* imaginaba ingenieros que ya no programan y se pasan el día intentando seguir el ritmo de lo que producen los agentes. La primera parte ya la estamos viviendo. La segunda es la que nadie ha resuelto: seguir el ritmo no puede consistir en abrir pestañas una a una.

Los modelos seguirán cambiando cada pocos meses, y las herramientas también. Lo que no va a cambiar es que alguien tiene que decidir qué se construye, comprobar que lo que ha salido es lo que se pidió y responder por ello. El nuevo IDE, el ICE, no es el sitio donde escribimos código. Es el sitio desde el que respondemos por él.
