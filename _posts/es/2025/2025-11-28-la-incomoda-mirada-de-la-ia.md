---
title: La incómoda mirada de la IA
tags: [personal, artificial_intelligence]
reviewed: true
home: true
ai: true
header_image: ai-driven-leader.jpg
---
Trabajar con modelos de IA genera una sensación engañosa.  Parecen colaborativos, atentos y sorprendentemente dispuestos a alinearse contigo. Esa impresión no es casual. Muchos de los modelos conversacionales generalistas con los que trabajamos hoy están entrenados mediante técnicas de alineamiento para reducir conflicto, suavizar el tono y priorizar respuestas seguras. En la práctica, eso se traduce a menudo en respuestas neutras, matizadas o llenas de aclaraciones que acompañan más que cuestionan. Si no lo detectas, esa amabilidad puede convertirse en una forma silenciosa de autoafirmación.

*The AI-Driven Leader*, de Geoff Woods, arranca precisamente desde este punto, aunque no como libro técnico, sino como una guía sobre cómo pensar cuando la IA participa en tus decisiones. Su marco —IA como entrevistador, comunicador o desafiante— tiene dos aciertos claros. Por un lado, obliga a explicitar qué rol quieres que adopte el modelo y normaliza la idea de que la IA puede participar en decisiones de liderazgo. Sin embargo, evita entrar en cuestiones que son centrales para entender el comportamiento real de los modelos, como sesgos inducidos por entrenamiento, aversión a la confrontación, variabilidad de respuestas, límites de contexto o riesgos derivados de interpretaciones incompletas. Ese vacío obliga a complementar sus ideas con un uso más metódico y un criterio más exigente.

La IA acelera tareas como resumir o depurar contenido y ese uso sí puede modificar tu percepción de un problema. Un buen resumen puede hacer visibles conexiones que no habías visto o sacar a la superficie un riesgo que estaba enterrado en el detalle. Aun así, en mi práctica el salto más relevante aparece cuando pasamos de la automatización a la confrontación, cuando pedimos a la IA que cuestione nuestros supuestos de manera explícita. Y esto es importante. La IA no adopta un rol crítico por defecto ni basta una única instruccion bien escrita para garantizarlo. Requiere instrucciones claras, iteración y cierta tolerancia al ruido.

> El salto más relevante aparece cuando pasamos de la automatización a la confrontación.

Si no se hace ese trabajo explícito, la combinación de alineamiento de seguridad, prudencia en el tono y generación probabilística produce algo reconocible, una confirmación amable, críticas superficiales y una falsa sensación de solidez que puede llevarte a creer que tus planteamientos están mejor fundamentados de lo que realmente están.

# La incomodidad bien definida

Hablar de “incomodidad” puede sonar abstracto, así que conviene precisarlo. En este contexto, incomodidad significa descubrir que habías dado por válidos supuestos no verificados o dependencias que dabas por obvias. Esa ruptura no surge sola. Aparece, a veces, cuando fuerzas al modelo a adoptar un rol adversarial, no asistencial.

Lo que marca la diferencia no es la tarea, sino la instrucción que le das al modelo. Una petición como esta —inspirada en el libro, pero afinada para uso real— cambia el tipo de interacción:

**“Entrevístame como un consultor externo. Formula preguntas destinadas a identificar supuestos no validados, dependencias difusas, riesgos que no he considerado y cualquier inconsistencia que pueda comprometer la decisión. No suavices el análisis.”**

Un *prompt* así no convierte mágicamente a la IA en un oráculo adversarial. A veces genera preguntas triviales, otras se va por tangentes o formula objeciones que se caen con dos datos. Pero cuando funciona, el efecto es muy concreto.

> Un modelo puede sonar incisivo y, aun así, estar generando hipótesis irrelevantes.

El libro menciona la idea de usar la IA como desafiante, pero no entra en el mecanismo. La calidad del desafío no depende de “la IA” en abstracto, sino de tres factores combinados:

- cómo enmarcas la interacción (rol, objetivo, límites),
- qué contexto proporcionas,
- y cómo filtras luego lo que recibes.

Un modelo puede sonar incisivo y, aun así, estar generando hipótesis irrelevantes. O puede formular objeciones convincentes basadas en un malentendido del contexto. La incomodidad productiva no consiste en recibir críticas, sino en distinguir qué críticas tienen fundamento, cuáles son operativas y cuáles deben descartarse.

> La incomodidad productiva consiste en discriminar qué críticas merecen trabajo y cuáles son solo ruido generativo.

# La IA como comunicador, con límites claros

El libro también propone usar la IA para depurar mensajes complejos. Un modelo sin experiencia directa en tu dominio puede, aun así, ayudarte a clarificar una explicación, reorganizar argumentos o ajustar el tono para audiencias distintas.

Ese valor tiene, sin embargo, una limitación estructural, el modelo puede resumir con gran claridad algo que no entiende en profundidad. Esa claridad artificial, si no se revisa, puede generar una falsa sensación de precisión.

> Esa claridad artificial puede generar una falsa sensación de precisión.

Cuando la IA reformula contenido para equipos que no están en el detalle técnico, su utilidad está en obligarte a priorizar: qué es esencial, qué sobra y qué requiere una explicación mejor. A veces esa síntesis te devuelve conexiones que tú mismo no habías articulado con nitidez. Pero ese beneficio convive con un riesgo evidente. La simplificación puede borrar matices importantes, suavizar riesgos críticos o presentar como “resuelto” un problema que sigue siendo ambiguo.

La IA no distingue, por sí sola, lo crítico de lo accesorio. Solo puede aproximarse a partir de patrones lingüísticos y del énfasis que tú le marques. La responsabilidad de decidir qué matices no se pueden sacrificar sigue siendo tuya.

> La responsabilidad de decidir qué matices no se pueden sacrificar sigue siendo tuya.

# Lo que el libro no aborda (y por qué importa)

El enfoque del libro es estimulante, pero incompleto. No profundiza en las razones por las que un modelo rara vez contradice de entrada. Entre ellas están:

- un entrenamiento que penaliza el conflicto abierto y recompensa respuestas razonables y seguras;
- mitigaciones de seguridad que desincentivan posiciones extremas o confrontaciones directas;
- un mecanismo de generación probabilística que tiende a la formulación de respuestas plausibles, no necesariamente correctas;
- y limitaciones estructurales para captar de forma robusta un contexto organizativo, político o cultural.

Aquí conviene matizar dos cosas. Primero, que estas dinámicas no se traducen siempre en “confirmación activa”: muchas veces lo que generan es neutralidad, cautela o una crítica tan abstracta que apenas incomoda. Segundo, que distintos modelos, proveedores y modos de uso muestran comportamientos diferentes; generalizar a “la IA” es, como mínimo, arriesgado.

Tampoco entra el libro en algo que, en la práctica, determina cualquier análisis: las dinámicas internas de una organización. Un modelo no tiene acceso directo a ritmos, agendas, tensiones políticas ni inercias culturales. Solo puede inferirlas a partir del contexto que tú le das. Si ese contexto es parcial, interesado o incompleto (y casi siempre lo es), cualquier recomendación basada únicamente en lo que produce el modelo queda coja.

La pregunta clave es cómo integrar ese contexto de forma útil, sin caer en la ilusión de que, por describirlo, la IA “entiende” tu organización.

En mi experiencia, eso pasa por tres gestos concretos:

1. **Definir el marco real del problema antes de pedir análisis.**  
   Qué está en juego, qué restricciones existen, quiénes son los actores relevantes, qué límites organizativos importan. Sin ese marco, la IA rellena huecos con suposiciones que pueden distorsionar el razonamiento.

2. **Explicitar fricciones que no son visibles desde fuera.**  
   Dependencias políticas, resistencias históricas, sensibilidades personales, prioridades no declaradas. Si esa información no se proporciona, el modelo tiende a proponer soluciones teóricamente impecables pero políticamente inviables.

3. **Delimitar el papel que la IA debe desempeñar.**  
   Auditor externo, abogado del diablo, sintetizador para comunicación, generador de escenarios… El modelo solo adopta una postura crítica, exploratoria o descriptiva si se le indica. Sin esa delimitación, su tendencia a evitar fricción produce lecturas acomodadas que proyectan una versión más pulida que real del problema.

Integrar contexto no convierte a la IA en experta de tu organización. Solo le da el mínimo necesario para que sus preguntas y objeciones sean menos ingenuas. Y aun así, ese contexto será una narrativa parcial, construida desde tu punto de vista. El resto —contrastar esas objeciones con otros actores, con datos y con la historia real de la organización— sigue dependiendo de las personas.

# Costes, riesgos y límites del modo adversarial

Idealizar el “modo adversarial” también tiene sus riesgos. Algunos de ellos apenas aparecen en el libro y conviene explicitarlos:

- **Coste cognitivo y de tiempo** - Mantener a la IA como auditor externo de forma sistemática puede ser inviable en decisiones cotidianas. No todo merece una sesión de objeciones exhaustivas: podrías paralizar procesos que necesitan rapidez.

- **Ruido disfrazado de lucidez** - Un modelo instruido para ser adversarial puede generar escenarios catastróficos improbables, sobre-detectar riesgos menores o cuestionar supuestos razonables solo por cumplir su rol. Esa “hipervigilancia” puede distraer de los problemas relevantes.

- **Sesgos reforzados, no corregidos** - Si quien tiene la última palabra utiliza la IA solo para legitimar decisiones ya tomadas, la insistencia en “tu criterio es lo que manda” puede reforzar sesgos de autoridad. La fricción que aporta el modelo se usa como barniz, no como contraste real.

Reconocer estos límites no invalida el uso adversarial. Simplemente lo sitúa donde pertenece, una herramienta más en un ecosistema de mecanismos de contraste que incluye revisión por pares, comités de riesgo, auditorías externas y, sobre todo, conversaciones humanas difíciles.

# Un uso más honesto y menos ingenuo

La IA puede ser un socio valioso, pero no solo por lo que automatiza ni solo por lo que incomoda. Su aportación real aparece cuando se combinan tres condiciones:

1. **Pedir explícitamente un rol crítico** - Los modelos conversacionales tienden a la cooperación segura. Si no defines el rol, tenderán a confirmar tu razonamiento o a criticarlo de forma inofensiva. Instrucciones directas (“actúa como auditor externo”, “detecta contradicciones”, “señala riesgos no identificados”) abren la puerta a un análisis distinto.

2. **Validar lo que dice con mecanismos algo más rigurosos que “me encaja/no me encaja”** - La IA formula críticas con seguridad incluso cuando interpreta mal un contexto o exagera problemas menores. El valor no está en la crítica literal, sino en lo que te obliga a revisar. Esa validación puede incluir contrastar con datos, pedir una segunda opinión (humana o de otro modelo) o someter las objeciones a una revisión por pares dentro del equipo.

3. **Aceptar que no toda la incomodidad es insight y que el modelo tiene límites estructurales** - Parte de la incomodidad será simplemente ruido: hipótesis poco probables, malentendidos, repeticiones. Además, hay ámbitos donde el modelo, por capacidad o por *guardrails*, no va a ir mucho más allá de lugares comunes, por más contexto y *prompts* que le des. Tu trabajo no es acatar ni descartar por reflejo, sino clasificar: qué merece trabajo adicional, qué se descarta y qué se aparca a la espera de más información.

Antes de cualquier decisión relevante, una instrucción simple puede elevar la calidad del análisis sin convertir a la IA en juez final:

**“Desafía mi planteamiento como si fueras un auditor externo con interés en demostrar que estoy equivocado. Luego clasifica tus objeciones según su solidez y probabilidad.”**

Si la respuesta solo trae elogios o críticas superficiales, puede que el problema esté en el *prompt*, en el planteamiento, en el nivel de contexto o, simplemente, en las limitaciones del modelo para ese tipo de análisis. No conviene eximir a la IA de sus límites, ni cargar siempre la responsabilidad en el usuario.

Pensar con IA no es pensar más rápido. Tampoco es pensar mejor por defecto. Es introducir un interlocutor adicional que amplifica tanto tus aciertos como tus sesgos. Puede sonar convincente al decir algo correcto… o al decir algo equivocado. Tu tarea es distinguir lo uno de lo otro.

La incomodidad no es un efecto secundario. Es el mecanismo que convierte a la IA en un interlocutor crítico, siempre que renuncies a su versión amable y mantengas intacto lo único que no puede automatizar: tu criterio.
