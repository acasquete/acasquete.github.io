---
title: La era cuántica, más allá del silicio
tags: [personal, quantum]
reviewed: true
home: true
ai: true
header_fullview: majorana.jpg
---
La **computación cuántica** promete revolucionar la informática al aprovechar fenómenos de la mecánica cuántica como la *superposición* y el *entrelazamiento* para procesar información de formas imposibles para los ordenadores clásicos. <!-- excerpt-end -->En lugar de bits binarios, emplea **cúbits**, que pueden estar en múltiples estados simultáneamente, multiplicando exponencialmente la capacidad de cómputo[^1]. Esto abre la puerta a resolver problemas intratables hoy en día, desde la simulación de moléculas complejas hasta la optimización de sistemas logísticos o financieros[^2].

Si es la primera vez que te enfrentas a un texto sobre **tecnología cuántica**, el párrafo anterior puede resultar aturdidor. Términos como **superposición**, **entrelazamiento** o **estados simultáneos** requieren cierto **conocimiento previo de física cuántica**, algo que puede intimidar al principio.

El objetivo de este artículo no es profundizar en la teoría física que hay detrás, sino ofrecer una visión comprensible y práctica del estado actual de la tecnología cuántica. Para quienes deseen explorar con más detalle los fundamentos teóricos, existen excelentes recursos introductorios de física cuántica y computación cuántica a los que el lector puede remitirse, como *Quantum Computing for Everyone* de Chris Bernhardt (MIT Press, 2020) [^75].

Sin embargo, la tecnología aún se encuentra en una fase **emergente**: sus aplicaciones prácticas son limitadas y enfrenta grandes desafíos de ingeniería. Los cúbits son extremadamente sensibles al entorno, sufriendo **decoherencia** y errores que dificultan mantener cálculos estables. Aun así, los avances en los últimos años han sido acelerados, con empresas e instituciones compitiendo por superar obstáculos como la corrección de errores y la escalabilidad de los sistemas cuánticos [^3] [^4].

Desde 2019, cuando Google anunció haber alcanzado la llamada *supremacía cuántica* con su procesador **Sycamore** —capaz de realizar en 200 segundos una tarea que habría llevado miles de años a un superordenador clásico— [^5], la carrera por lograr una **ventaja cuántica práctica** se ha intensificado. IBM, por su parte, ha escalado sus procesadores superconductores desde 5 cúbits en 2016 hasta más de 1 000 cúbits en 2023 con el chip **Condor** [^6]. Microsoft ha apostado por una vía diferente, basada en cúbits **topológicos de Majorana**, que podrían ofrecer una corrección de errores más eficiente [^7].

Paralelamente, startups como **IonQ**, **Quantinuum**, **Atom Computing** o **QuEra** han desarrollado plataformas basadas en iones atrapados o átomos neutros, mientras **Xanadu** y **PsiQuantum** exploran arquitecturas fotónicas. Estas alternativas persiguen reducir los errores y facilitar la escalabilidad, cada una con ventajas y limitaciones propias [^8] [^9].

A nivel de software, han surgido lenguajes y frameworks de programación cuántica como **Qiskit** (IBM), **Q#** (Microsoft), **Cirq** (Google) y **PennyLane** (Xanadu), que permiten a desarrolladores e investigadores diseñar y ejecutar algoritmos cuánticos en entornos simulados o en hardware real accesible desde la nube [^10] [^11].

La revolución cuántica no solo afectará al cómputo: también redefine la **ciberseguridad**. Los algoritmos de Shor y Grover podrían quebrar los sistemas criptográficos actuales basados en RSA y ECC una vez existan computadoras cuánticas tolerantes a fallos [^12]. Para adelantarse a ese riesgo, el **NIST** publicó en 2024 los primeros estándares de **criptografía post-cuántica**, inaugurando una transición global hacia algoritmos resistentes a ataques cuánticos [^13].

Este artículo explora el **estado del arte de la tecnología cuántica en 2025**, abordando:

- Los hitos recientes desde la *supremacía cuántica* hasta la *ventaja cuántica práctica*.  
- Los principales actores y líneas de investigación.  
- Las diferentes arquitecturas de procesadores cuánticos y sus desafíos.  
- Los lenguajes y frameworks más utilizados para la programación cuántica.  
- El impacto en seguridad y criptografía post-cuántica.  
- Aplicaciones emergentes en simulación química, IA y optimización.

El objetivo es ofrecer una visión clara, actualizada y accesible del panorama cuántico para quienes necesiten entender qué es viable hoy, qué avances se avecinan y cómo pueden preparar a sus organizaciones para esta transformación.

# De la “supremacía cuántica” a la ventaja cuántica

El término **“supremacía cuántica”**, propuesto por John Preskill en 2012, describe el punto en el que un ordenador cuántico es capaz de **realizar una tarea que ningún ordenador clásico podría completar en un tiempo razonable** [^14]. Se trata de un concepto teórico que marcó durante años la meta simbólica del campo: demostrar experimentalmente que los principios cuánticos pueden ofrecer una ventaja real en capacidad de cálculo.

En **2019**, Google anunció haber alcanzado ese hito con su procesador **Sycamore** de 53 cúbits superconductores. Según el equipo de Google, el sistema resolvió en **200 segundos** un problema de muestreo aleatorio (*random circuit sampling*) que, en un superordenador clásico, habría requerido **10 000 años** [^15]. El resultado, publicado en *Nature*, fue la primera evidencia experimental de una capacidad cuántica superior en un problema concreto. IBM cuestionó esa afirmación, argumentando que con un algoritmo clásico optimizado y suficiente almacenamiento, la misma tarea podría resolverse en **2,5 días**, pero incluso así el logro de Google marcó un antes y un después en la historia del cómputo cuántico [^16].

A partir de ese momento, el foco de la investigación cambió: ya no se trataba solo de “ganar” frente a los sistemas clásicos en un experimento sintético, sino de **obtener una ventaja cuántica práctica** en problemas de utilidad científica o industrial. Esta nueva fase, conocida como la era **NISQ** (*Noisy Intermediate-Scale Quantum*), busca aprovechar dispositivos con entre 50 y 1 000 cúbits —aún ruidosos y sin corrección de errores completa— para realizar cálculos imposibles o extremadamente costosos para un ordenador clásico [^17].

En los años siguientes se sucedieron nuevas demostraciones de ventaja cuántica. En **2020**, un grupo de la Universidad de Ciencia y Tecnología de China (USTC) presentó **Jiuzhang**, una computadora cuántica **fotónica** que realizó un experimento de *boson sampling* con 76 fotones detectados, completando en 200 segundos un cálculo que a un superordenador le habría llevado 2 500 millones de años [^18]. En **2022**, la startup canadiense **Xanadu** logró una hazaña similar con su procesador **Borealis**, capaz de generar estados entrelazados de luz en 216 modos y ejecutar en 36 microsegundos un muestreo que requeriría 9 000 años en una computadora clásica [^19].

Por su parte, el equipo de **Google Quantum AI** volvió a marcar un hito en **2023** al demostrar experimentalmente que **aumentar el número de cúbits físicos puede reducir la tasa de error lógica**, validando por primera vez la hipótesis de que la corrección de errores cuánticos escala favorablemente [^20]. Este avance constituye un paso esencial hacia la construcción de **cúbits lógicos estables**, condición indispensable para una computación cuántica útil a gran escala.

Hoy, la comunidad científica tiende a preferir el término **“ventaja cuántica”** frente a “supremacía”, no solo por razones semánticas, sino porque refleja mejor la realidad actual: los ordenadores cuánticos no son todavía superiores en aplicaciones generales, pero ya comienzan a ofrecer ventajas **cuantificables** en ámbitos específicos y controlados. La meta no es simplemente superar a los clásicos, sino **coexistir y complementarlos**, integrando capacidades cuánticas dentro de arquitecturas híbridas que aprovechen lo mejor de ambos mundos.

En síntesis, la “supremacía cuántica” fue un **punto de inflexión simbólico**; la “ventaja cuántica” representa ahora el **camino hacia la utilidad práctica**. El reto ya no es demostrar que los cúbits funcionan, sino hacer que trabajen juntos con suficiente fidelidad, escalabilidad y corrección de errores para resolver problemas reales en ciencia, industria y seguridad.

# Principales actores de la computación cuántica

Diversas empresas líderes y centros de investigación compiten por desarrollar la primera computadora cuántica útil y escalable. **IBM**, pionera en este campo, encabeza la vanguardia con un enfoque en cúbits superconductores. En 2016 presentó un chip de 5 cúbits y desde entonces ha seguido duplicando capacidades; a finales de **2023** reveló su procesador **IBM Condor** de *1 121 cúbits*, superando la barrera de los mil años antes de lo previsto [^21]. IBM dispone de la mayor infraestructura cuántica en la nube (*IBM Quantum*), múltiples equipos operativos (como *Eagle* de 127 cúbits en 2021 y *Osprey* de 433 cúbits en 2022) y una hoja de ruta que apunta a construir sistemas tolerantes a fallos en la próxima década [^22]. Su plan aspira a lograr hacia **2033** un modelo denominado *IBM Blue Jay* con corrección de errores incorporada, solventando los actuales obstáculos de decoherencia y ruido [^22].

**Google**, a través de su división *Quantum AI*, es el otro gigante destacado. Fue el primero en proclamar la *supremacía cuántica* en 2019 con *Sycamore* y desde entonces ha continuado investigando chips superconductores más potentes. En **2023** presentó su procesador **Google Willow** de 72 cúbits, diseñado para experimentos de corrección de errores cuánticos. Los investigadores de Google demostraron que al escalar su código de superficie de 9 a 49 cúbits físicos (de una rejilla 3×3 a 7×7), lograban reducir a la mitad la tasa de error lógica en cada incremento, validando por primera vez que *más cúbits pueden significar menos errores* gracias a la redundancia del código [^23]. Este avance hacia cúbits lógicos libres de errores es crucial para construir computadoras cuánticas útiles a gran escala. Google, con laboratorios en Santa Bárbara, apunta a sistemas con **millones de cúbits físicos** a largo plazo, combinando hardware cuántico con controladores clásicos avanzados e inteligencia artificial para optimizar operaciones.

**Microsoft** ha tomado una ruta diferenciada enfocada en **cúbits topológicos**. Busca aprovechar cuasipartículas llamadas *fermiones de Majorana* para crear cúbits inherentemente más estables y resistentes a la decoherencia, reduciendo así la necesidad de corrección activa de errores [^24] [^25]. Durante más de una década, Microsoft ha invertido en investigar estos exóticos materiales (nanocables de indio y aluminio a temperaturas ultrafrías) y en **2022** publicó evidencias *peer-reviewed* de haber logrado producir y controlar estados Majorana en laboratorio [^25]. En **2023**, la compañía anunció su chip experimental **Majorana 1**, con los primeros cúbits topológicos operativos, integrando 8 cúbits en un módulo y con un diseño escalable a un millón de cúbits [^26] [^27]. Aunque aún no ofrece un dispositivo cuántico general, Microsoft proporciona el servicio **Azure Quantum**, que da acceso en la nube a hardware cuántico de socios (*IonQ*, *Quantinuum*, etc.) y herramientas de desarrollo propias (lenguaje **Q#**). Su apuesta a largo plazo es que los cúbits topológicos permitirán computadoras cuánticas con **corrección de errores intrínseca** en el hardware, facilitando la escalabilidad industrial de la computación cuántica [^28] [^29].

Además de estos tres titanes, existe un ecosistema de **empresas especializadas e iniciativas gubernamentales** empujando los límites de la tecnología cuántica:

- **D-Wave Systems**: Compañía canadiense pionera en ofrecer computadoras cuánticas comerciales desde 2011. Sus sistemas usan *recocido cuántico* (*quantum annealing*) en lugar de puertas lógicas, orientados a resolver problemas de optimización. Los modelos más recientes de D-Wave operan con más de **5 000 cúbits** (aunque de tipo análogo, no cúbits universales) [^30], y han mostrado ventajas en tareas de logística y *machine learning*.

- **IonQ**: Startup estadounidense líder en cúbits de *iones atrapados*. Fue la primera empresa puramente cuántica en cotizar en bolsa (NASDAQ) en **2021** y colabora con gigantes en la nube: sus equipos están disponibles a través de **AWS Braket** y **Microsoft Azure** [^31]. La tecnología de IonQ usa átomos de iterbio atrapados con láseres, logrando tiempos de coherencia largos y puertas de altísima fidelidad. Sus sistemas actuales (~29 cúbits efectivos) ofrecen fidelidades comparables a las de 100 cúbits superconductores. IonQ ha anunciado una hoja de ruta agresiva, proyectando sistemas con varios cientos de cúbits atrapados en los próximos años, con aplicaciones en química cuántica y IA.

- **Quantinuum**: Nacida de la fusión en **2021** de Honeywell Quantum Solutions (EE. UU.) y Cambridge Quantum Computing (Reino Unido), es una de las mayores empresas cuánticas integradas, con unos **450 empleados** [^32]. Ofrece computadores de iones atrapados de alta calidad (modelo *H1* con 20 cúbits y *H2* con hasta 32 cúbits de iterbio) [^33], combinados con un sólido *stack* de software (compilador t\|ket⟩, generador de números cuánticos, etc.). Quantinuum ha demostrado récords en rendimiento de puertas lógicas y lidera experimentos de cúbits lógicos en hardware de iones: en **2023**, junto a Microsoft, logró entrelazar 12 cúbits lógicos con baja tasa de error usando su sistema H2 [^34] [^35]. También desarrolla algoritmos cuánticos para química y optimización, y colabora con JPMorgan Chase en aplicaciones financieras.

- **Atom Computing**: Startup estadounidense centrada en cúbits de *átomos neutros*. En **2021** presentó *Phoenix*, su primer prototipo con 100 cúbits de estroncio atrapados mediante matrices de láseres (*optical tweezers*) [^36]. Tras lograr ese hito inicial, recaudó **60 millones USD** en **2022** para continuar el desarrollo [^37]. Los átomos neutros prometen escalabilidad (cientos de cúbits dispuestos en rejillas ópticas) y operaciones paralelas, aunque aún se trabaja en mejorar la fidelidad de las puertas. En **2023**, Atom Computing anunció una alianza estratégica con el gobierno de EE. UU. para acelerar la expansión de esta tecnología [^38], y se integró como socio de **Azure Quantum** para ofrecer su hardware a desarrolladores en la nube [^39].

- **QuEra Computing**: Startup surgida del MIT y Harvard, especializada también en átomos neutros. En **2022** reveló su dispositivo *Aquila* de 256 átomos de rubidio dispuestos en 2D, y anunció una hoja de ruta que proyecta lograr **corrección de errores cuánticos para 2026**, adelantándose incluso a los planes de IBM [^40]. QuEra explora un enfoque híbrido entre computación cuántica digital y analógica, y ha publicado avances en simulación de materiales usando sus arreglos atómicos. Aunque aún en fase temprana, su potencial para escalar a miles de átomos la sitúa como competidor prometedor.

- **Otras iniciativas**: La carrera cuántica es global. Empresas como **Rigetti Computing** (EE. UU., chips superconductores de 80 cúbits), **Pasqal** (Francia, átomos neutros, 100 cúbits anunciados), así como **Amazon** (*AWS Braket*, plataforma que integra hardware de varios proveedores) y **Intel** (cúbits de *spin* en silicio), contribuyen al rápido progreso del sector. En el ámbito gubernamental, **China** destaca por su fuerte inversión estatal: en **2021** inauguró el *Centro Nacional de Computación Cuántica* en Hefei y presentó en **2023** el ordenador **Tianyan-504** de 504 cúbits superconductores [^41] [^42]. En Europa, la **Unión Europea** impulsa el programa *Quantum Flagship*, con proyectos de hardware (como IQM en Finlandia) y la creación de una red paneuropea de computación cuántica. Esta multiplicidad de actores refleja el enorme interés global por liderar la próxima revolución tecnológica.

# Procesadores cuánticos: diferentes enfoques tecnológicos

*Interior de IBM Quantum System Two, un sistema modular de computación cuántica que integra múltiples procesadores superconductores con electrónica criogénica de control (Imagen: IBM).*

No todas las computadoras cuánticas se construyen de la misma manera. Existen **varios enfoques físicos** para implementar cúbits, cada uno con sus ventajas y desafíos. En términos generales, hay **cinco arquitecturas principales** que se exploran en la actualidad: **circuitos superconductores**, **iones atrapados**, **átomos neutros**, **espín en semiconductores** y **fotónica** (cúbits de luz) [^43]. A continuación, se describen brevemente estas tecnologías:

### Cúbits superconductores

Son **circuitos eléctricos** fabricados con materiales superconductores (como aluminio o niobio) que operan a temperaturas cercanas al **cero absoluto** (≈15 mK). Mediante arreglos de **uniones Josephson** y condensadores, se crean niveles de energía que actúan como los estados \|0⟩ y \|1⟩ del cúbit [^44].  

Gigantes como **IBM**, **Google**, **Rigetti** y **Amazon** (en colaboración) emplean esta tecnología. Sus ventajas incluyen **velocidades de operación muy altas** (puertas en nanosegundos) y la posibilidad de fabricar chips con técnicas similares a la microelectrónica. IBM ha escalado sus procesadores superconductores de 5 a **1 121 cúbits** en siete años [^21].  

Sin embargo, presentan desafíos importantes: requieren **criogenia compleja**, y cada cúbit es efímero, con tiempos de coherencia de apenas **microsegundos**. Además, las interferencias entre cúbits cercanos dificultan el escalado. Para mitigarlo, empresas como IBM y Google han introducido diseños de **conectividad mejorada** (como la disposición *heavy-hexagon* de IBM) y han alcanzado **fidelidades de puerta superiores al 99,9 %** en chips pequeños. El siguiente reto es escalar a miles de cúbits sin comprometer esa fidelidad, mediante **interconexiones 3D, empaquetado avanzado** y sistemas de enfriamiento más potentes.

### Iones atrapados

Esta técnica utiliza **átomos ionizados** (por ejemplo, iterbio o berilio) confinados en trampas electromagnéticas dentro de un vacío ultraalto. Los **estados electrónicos internos** del ion, o sus **modos de vibración compartidos**, sirven como estados del cúbit. Todos los iones son idénticos, evitando variaciones de fabricación, y pueden mantener **coherencia durante segundos o incluso minutos**, mucho más que otros tipos de cúbits [^34].  

Las **puertas lógicas** se implementan con láseres que inducen interacciones entre los iones. **IonQ** y **Quantinuum** lideran este campo: han logrado operaciones de dos cúbits con fidelidad > 99,9 % y utilizan cadenas lineales de ~20 iones para computación universal.  

El principal obstáculo es la **escalabilidad física**: controlar y mover muchos iones simultáneamente es complejo, y las puertas se ralentizan al aumentar la longitud de la cadena. Se exploran arquitecturas modulares y el uso de **iones híbridos** (diferentes especies para almacenamiento y operaciones). Aun con pocas decenas de cúbits, las máquinas de iones atrapados encabezan hoy los rankings de **quantum volume** y son referencia en **algoritmos de química cuántica**.

### Átomos neutros

En este enfoque se utilizan **átomos no cargados** (rubidio, cesio, estroncio) confinados mediante **pinzas ópticas**: haces láser que crean redes tridimensionales donde se atrapan cientos de átomos [^43]. Los cúbits pueden codificarse en los niveles de energía o en **estados de Rydberg**, altamente excitados y con fuertes interacciones.  

Startups como **Pasqal** y **QuEra** han desarrollado rejillas de **100 – 300 átomos** neutros, controlando dinámicamente sus interacciones. La gran promesa es la **escalabilidad**, pues es relativamente fácil aumentar el número de átomos atrapados y reorganizarlos con precisión óptica.  

El ruido por decoherencia sigue siendo un desafío (tiempos de coherencia de 100 µs a 1 ms) y las fidelidades de puerta rondan el 98 %. Aun así, los sistemas de átomos neutros se han mostrado muy útiles en **simulación cuántica**, reproduciendo fenómenos de magnetismo y dinámica de espines. Los próximos avances apuntan a la computación universal mediante **puertas portátiles de dos cúbits** y esquemas de corrección de errores adaptados a Rydberg.

### Espín en semiconductores (silicio)

Otra vía explora el uso del **espín del electrón** en **puntos cuánticos** de silicio. Estos cúbits se basan en electrones individuales atrapados en estructuras semiconductoras, donde la orientación del espín (↑ o ↓) representa los estados lógicos.  

Empresas como **Intel**, **QuTech** (Delft) y **UNSW** (Australia) lideran esta línea. Sus ventajas son la **miniaturización extrema** y la **compatibilidad con procesos CMOS**, lo que permitiría fabricar millones de cúbits usando la infraestructura de la industria de chips. Además, los cúbits de espín presentan **largos tiempos de coherencia** (hasta segundos) en silicio isotópico purificado.  

Sus limitaciones incluyen la complejidad del **control electrónico** a escala nanométrica y fidelidades aún inferiores (90–99 %). Intel presentó en **2022** su chip **Tunnel Falls** de 12 cúbits de espín, disponible para investigación, e investiga la integración de **controladores criogénicos CMOS** para operar miles de cúbits dentro de un mismo criostato [^43] [^45].

### Fotónica cuántica

En la fotónica cuántica los cúbits son **fotones**, partículas de luz que codifican información en propiedades como **polarización, fase o modo temporal**. La computación fotónica funciona a **temperatura ambiente** y es inherentemente resistente a la decoherencia. Por ello, se considera ideal para **comunicaciones cuánticas** (como la distribución de clave cuántica, QKD) y potencialmente para cómputo.  

El gran desafío es que los fotones **no interactúan fácilmente entre sí**, complicando la implementación de puertas lógicas de dos cúbits. Se exploran dos aproximaciones:  
1. **Fotónica lineal**, basada en interferómetros y detectores, donde las interacciones son probabilísticas y requieren recursos auxiliares.  
2. **Materiales no lineales**, que podrían inducir interacciones directas entre fotones.  

El enfoque lineal fue usado por el equipo chino en la computadora **Jiuzhang**, y también por **Xanadu** en su procesador **Borealis**, que alcanzó **ventaja cuántica en muestreo de bosones** [^46]. Por su parte, **PsiQuantum** colabora con **GlobalFoundries** para fabricar chips fotónicos integrados y aspira a alcanzar **un millón de cúbits fotónicos** con corrección de errores en la próxima década.  

Aunque aún no existe una computadora fotónica universal, esta tecnología avanza rápidamente en **simulación, comunicaciones seguras y redes cuánticas**. Se investiga la producción de **fuentes de fotones individuales**, **detectores superconductores ultrarrápidos** y **esquemas de codificación topológica**, que podrían habilitar una computación óptica escalable y tolerante a fallos.

En resumen, **no existe aún una tecnología dominante**. Probablemente distintas plataformas coexistan optimizadas para distintos fines:  
- cúbits superconductores para **computación de alta velocidad**,  
- iones atrapados o átomos neutros para **precisión y fidelidad**,  
- y fotónica para **comunicación cuántica**.  

También emergen **enfoques híbridos**, como la **computación cuántica distribuida**, que conecta chips cuánticos mediante enlaces fotónicos. La diversidad actual recuerda a los inicios de la computación clásica, cuando se exploraban válvulas de vacío y transistores antes de converger en una tecnología dominante. Los próximos años serán decisivos para determinar qué arquitectura logrará **escalar con tolerancia a fallos** y convertirse en la base de la computación cuántica comercial.

# Programación cuántica: lenguajes y herramientas de software

Disponer de hardware cuántico es solo parte del reto; también se requieren **lenguajes y herramientas** que permitan aprovechar estas máquinas. Al ser un paradigma distinto, la programación cuántica demanda pensar en **puertas lógicas**, **registros de cúbits**, **medidas probabilísticas** y **algoritmos reversibles**. Para facilitarlo, en los últimos años se han desarrollado varios *frameworks* y lenguajes especializados, muchos con el apoyo de los grandes actores del sector [^47]:

- **Qiskit**. *Framework* abierto impulsado por IBM. Es una biblioteca en **Python** para **crear y ejecutar circuitos cuánticos** en simuladores locales o en procesadores de IBM en la nube [^48]. Incluye abstracciones de alto nivel (química, ML, optimización) y **transpilación** para optimizar circuitos antes de ejecutarlos. Por su facilidad de uso y el acceso en la nube, Qiskit es uno de los entornos más populares.

- **Q#**. Lenguaje de Microsoft (parte del **Quantum Development Kit**). A diferencia de Qiskit o Cirq (basados en Python), Q# es **dedicado** a lo cuántico, con sintaxis cercana a C# y diseño **independiente del hardware**. Permite ejecutar en simuladores locales o enviar trabajos a **Azure Quantum**, con tipos nativos para cúbits y buena **composición modular** para flujos híbridos cuántico-clásicos.

- **Cirq**. Biblioteca de **Google Quantum AI** enfocada en describir circuitos a **bajo nivel** y en detalles de hardware (especialmente superconductores). Se usa ampliamente en investigación NISQ, simulación y **optimización de puertas**; varias demostraciones emblemáticas (supremacía, códigos de superficie) se programaron con Cirq.

- **Amazon Braket**. Plataforma de **AWS** para ejecutar circuitos en múltiples *backends* (IonQ, Rigetti, OQC, QuEra, etc.). No es un lenguaje, sino un **SDK y servicio gestionado** que orquesta simuladores y hardware, e integra resultados con el ecosistema AWS (S3, EC2, Step Functions), útil para **pipelines híbridos**.

- **Otras herramientas**. El ecosistema crece con aportaciones de academia y *startups*. **PennyLane** (Xanadu) se centra en **algoritmos variacionales** y **ML cuántico** con diferenciación automática e integración con PyTorch, JAX y TensorFlow [^49]. **ProjectQ** (ETH Zurich) introdujo un compilador modular; **PyQuil** (Rigetti) se enfocó en su hardware superconductor; **t\|ket⟩** (Quantinuum) es un **compilador** muy utilizado para optimizar y transpilar entre dispositivos; **pytket** y **OpenQL** amplían la interoperabilidad. Además, se proponen lenguajes de **pseudocódigo estandarizado** como **OpenQASM** para describir secuencias de puertas de bajo nivel.

Un indicador de madurez del *stack* es que ya existen “**Hola, mundo**” cuánticos **multilenguaje**: crear un **estado de Bell** (par de cúbits entrelazados) puede demostrarse fácilmente en **Qiskit** y **Cirq**, y existen guías equivalentes en **Q#**, **Braket**, **PennyLane**, **ProjectQ** y **pytket** [^50] [^47]. Esto evidencia la **diversidad** de herramientas disponibles.

Otra tendencia clave es la **accesibilidad vía nube**. Hoy cualquiera puede registrarse en **IBM Quantum Experience**, **Azure Quantum** o **AWS Braket** y ejecutar experimentos reales o simulados sin poseer hardware propio [^51]. Esto ha **democratizado** la educación y la investigación, y potencia una comunidad abierta de tutoriales, librerías y ejemplos. Para ejecutivos técnicos, la implicación es clara: el *stack* tenderá a **integrarse** cada vez más con la computación clásica, habilitando **flujos híbridos** donde CPUs/GPUs y cúbits se coordinen de forma transparente. En resumen, el software está **allanando la curva de aprendizaje** y preparando el terreno para cuando el hardware alcance la escala necesaria para aplicaciones prácticas.

# Plataformas de integración cuántica

A medida que la investigación cuántica avanza, las grandes tecnológicas están desarrollando plataformas que integran simulación, inteligencia artificial y recursos cuánticos en la nube para resolver problemas científicos y de ingeniería. Entre las más destacadas se encuentran **Azure Quantum Elements** (Microsoft) y **Google Quantum AI**.

## Microsoft Azure Quantum Elements

Microsoft adopta un enfoque híbrido que combina **computación de alto rendimiento (HPC)**, **inteligencia artificial generativa** y **recursos cuánticos experimentales** dentro de un mismo entorno en la nube. Su objetivo es acelerar el descubrimiento de **nuevos materiales, fármacos y procesos químicos** mediante simulación y optimización cuántica asistida por IA [^82].

Entre sus capacidades destacan **Generative Chemistry**, que emplea modelos generativos para proponer nuevas estructuras moleculares, y **Accelerated DFT**, que usa IA para acelerar los cálculos de teoría funcional de la densidad [^76]. Estas herramientas no dependen aún de hardware cuántico real, pero sirven como **puente hacia la integración futura de recursos cuánticos** en pipelines industriales.

Quantum Elements refleja la visión de Microsoft de que el valor de la computación cuántica emergerá de forma **gradual y complementaria**, combinando recursos clásicos, IA y simuladores cuánticos antes de alcanzar computadoras cuánticas tolerantes a fallos [^77].

## Google Quantum AI

Google Quantum AI, con sede en Santa Bárbara, persigue la construcción de una **computadora cuántica tolerante a errores** mediante cúbits superconductores [^78]. Entre sus hitos recientes destaca el procesador **Willow**, diseñado para escalar la corrección de errores cuánticos y mejorar la fidelidad de las operaciones [^79].

Además del hardware, Google mantiene un robusto ecosistema de **software abierto**, incluyendo **Cirq**, **TensorFlow Quantum** y otras librerías que permiten diseñar y ejecutar algoritmos cuánticos en entornos simulados o reales. La compañía investiga aplicaciones en **simulación química, optimización y aprendizaje automático**, y colabora con la industria para identificar casos donde la computación cuántica pueda ofrecer ventajas prácticas en los próximos años [^80].

Su estrategia combina investigación en física cuántica con desarrollo de software y algoritmos aplicados, apuntando a generar **utilidad cuántica antes de alcanzar la corrección total de errores** [^81].

# Ciberseguridad cuántica y criptografía post-cuántica

El advenimiento de las computadoras cuánticas también tiene implicaciones profundas en el campo de la seguridad informática. Muchos de los sistemas criptográficos actuales –por ejemplo, RSA y ECC que protegen nuestras transacciones bancarias, comunicaciones y certificados digitales– se basan en la dificultad de problemas matemáticos (factoreo de enteros, logaritmos discretos) que serían trivialmente resolubles por un algoritmo cuántico como Shor si dispusiéramos de una computadora cuántica lo suficientemente potente [^19]. En concreto, Shor demostró teóricamente que un computador cuántico podría factorizar números de miles de bits en tiempo polinomial, rompiendo RSA, y calcular logaritmos discretos, rompiendo ECC, comprometiendo así la base de la seguridad actual [^52]. Aunque para lograr esto harían falta quizá millones de cúbits corriendo algoritmos de corrección de errores –lo que aún no existe–, la rápida progresión de la tecnología cuántica en las últimas décadas ha encendido las alarmas: es cuestión de tiempo (quizá una o dos décadas) que los cifrados clásicos hoy seguros puedan quebrarse con cómputo cuántico [^20].

Por ello, se ha lanzado una carrera para desplegar criptografía post-cuántica (PQC), es decir, nuevos algoritmos de cifrado y firma digital diseñados para ser seguros incluso frente a ataques con computadores cuánticos [^53]. Estos algoritmos se basan en problemas matemáticos que (hasta donde sabemos) son difíciles tanto para ordenadores clásicos como cuánticos – por ejemplo, problemas de retículos en alta dimensión, códigos correctores, o funciones hash. Desde 2016, el Instituto Nacional de Estándares y Tecnología (NIST) de EE. UU. lidera un proceso de estandarización de criptografía post-cuántica que atrajo decenas de propuestas de todo el mundo. Tras varias rondas de análisis, en 2022 se seleccionaron los candidatos ganadores, y en agosto de 2024 se publicaron los primeros estándares oficiales: el esquema de cifrado Kyber y las firmas digitales Dilithium y SPHINCS+, formalizados como estándares FIPS 203, 204 y 205 respectivamente [^54]. Estos nuevos algoritmos quantum-safe han sido validados por la comunidad científica y ahora la tarea es implementarlos en protocolos y productos de seguridad.

La transición hacia la criptografía post-cuántica se considera urgente. Expertos advierten de la amenaza del modelo "store now, decrypt later" – actores maliciosos podrían estar interceptando y almacenando hoy comunicaciones cifradas (por ejemplo, datos gubernamentales o financieros sensibles) con la expectativa de desencriptarlos en el futuro cuando dispongan de una computadora cuántica poderosa [^55] [^56]. Para mitigar ese riesgo, es crucial empezar cuanto antes a desplegar algoritmos post-cuánticos en infraestructuras críticas. Organismos gubernamentales han establecido plazos: por ejemplo, el gobierno de EE. UU. planea deprecar RSA de 2048 bits y curvas ECC estándar hacia 2030, y exigir exclusivamente algoritmos PQC para 2035 [^57]. Grandes proveedores de navegadores y sistemas operativos (como Google, Cloudflare, Microsoft) ya están probando suites híbridas que combinan algoritmos clásicos y post-cuánticos en conexiones TLS, para evaluar su rendimiento y compatibilidad. En 2023, algunas autoridades certificadoras comenzaron a emitir certificados digitales post-cuánticos (que usan firmas Dilithium en lugar de RSA, por ejemplo) de manera experimental.

Por otro lado, la criptografía cuántica (que aprovecha directamente la física cuántica para comunicaciones seguras) también avanza. El caso más conocido es la distribución cuántica de claves (QKD), donde dos partes pueden generar una clave secreta compartida enviando fotones entrelazados o en estados cuánticos aleatorios; gracias al teorema de no-clonación, cualquier intento de espionaje en el canal cuántico será detectable. Ya existen redes QKD operativas: China desplegó en 2016 la primera línea Beijing-Shanghai con repetidores cuánticos, además de utilizar el satélite Micius para intercambio de claves a larga distancia. Europa cuenta con la Quantum Communication Infrastructure (EuroQCI) en desarrollo para conectar capitales con enlaces cuánticos, y países como Estados Unidos, Japón y Corea tienen proyectos pilotos. Si bien el QKD garantiza seguridad teórica incondicional, tiene limitaciones prácticas (alcance restringido sin repetidores confiables, costos altos, solo distribuye claves y no datos en sí). No obstante, se vislumbra en el horizonte una posible “Internet cuántica”, donde redes de fibra óptica y satélites transmitan información cuántica (cúbits) a través de fotones, habilitando comunicaciones absolutamente seguras y también computación cuántica distribuida [^58]. Tecnologías como repetidores cuánticos (nodos intermedios que extienden el entrelazamiento) están en prototipo, y protocolos de teletransporte cuántico multi-salto se han demostrado en laboratorio.

En resumen, desde la perspectiva de ciberseguridad, nos encontramos en una carrera dual: por un lado, preparar nuestros sistemas criptográficos clásicos para resistir el poder de la computación cuántica futura (adoptando algoritmos post-cuánticos lo antes posible), y por otro, aprovechar los principios cuánticos para crear nuevos métodos de comunicación y seguridad (QKD, identidades cuánticas, generación cuántica de números aleatorios) que refuercen la privacidad. Las empresas y gobiernos deben comenzar a inventariar dónde usan criptografía vulnerable (RSA/ECC, Diffie-Hellman, etc.) y planificar migraciones hacia alternativas post-cuánticas. La publicación de estándares oficiales por NIST en 2024 [^54] marca el inicio de esta transición a gran escala. En paralelo, conviene monitorear los avances de los laboratorios cuánticos: cada progreso en cúbits y algoritmos nos acerca un poco más al día en que ciertos cifrados se volverán obsoletos – un evento apodado por algunos como el "criptoapocalipsis". La buena noticia es que ya contamos con las herramientas criptográficas para afrontarlo; la tarea pendiente es implementarlas a tiempo en la infraestructura global.

# Aplicaciones potenciales y perspectivas futuras

Aunque la computación cuántica todavía no supera a la clásica en aplicaciones prácticas, sus potenciales casos de uso abarcan muchos sectores industriales y científicos. A medida que la tecnología madure en la próxima década, podría transformar áreas como:

- **Descubrimiento de fármacos y materiales:** Las computadoras cuánticas pueden simular sistemas cuánticos de forma nativa, algo extremadamente costoso para los clásicos. Esto permitiría modelar moléculas complejas, reacciones químicas y materiales con una precisión inalcanzable hoy. Empresas farmacéuticas esperan acelerar el diseño de nuevos medicamentos (por ejemplo, simulando la interacción de un fármaco con una proteína objetivo) en días en lugar de años [^59]. En materiales, se podrían descubrir superconductores a temperatura ambiente, polímeros más resistentes o catalizadores para energías limpias mediante simulación cuántica de sus propiedades atómicas [^60] [^61].

- **Optimización logística y financiera:** Muchos problemas de optimización combinatoria (rutas de entrega, asignación de recursos, carteras de inversión) crecen exponencialmente con el tamaño, volviéndose intratables. Los algoritmos cuánticos (como QAOA o *annealing* cuántico) podrían encontrar soluciones cuasi óptimas mucho más rápido que los métodos actuales. Esto impactaría la gestión de cadenas de suministro, el ruteo de tráfico, la planificación de redes eléctricas y la optimización de portafolios financieros para maximizar retornos y minimizar riesgos [^62] [^63]. Varias firmas de Wall Street ya experimentan con algoritmos cuánticos para ajustar precios de derivados o optimizar arbitrajes, aunque aún en simuladores.

- **Inteligencia Artificial y aprendizaje automático:** Existe una gran expectativa por la sinergia entre IA y computación cuántica. En principio, algoritmos cuánticos podrían acelerar tareas de *machine learning*, como el análisis de grandes bases de datos o el entrenamiento de modelos. Ya se han propuesto algoritmos cuánticos para redes neuronales (*quantum neural networks*), *clustering*, *quantum SVM*, etc., que teóricamente podrían detectar patrones en datos masivos más eficazmente [^64] [^65]. En 2023, Google y IBM mostraron prototipos de aceleración cuántica de modelos de IA a pequeña escala. Otra vía es usar técnicas de IA para optimizar sistemas cuánticos —por ejemplo, *auto-ML* para descubrir mejores circuitos variacionales, o *reinforcement learning* para calibrar cúbits y corregir errores adaptativamente [^66]. Es probable que las primeras aplicaciones útiles de la computación cuántica sean híbridas con la IA, resolviendo subproblemas específicos dentro de *pipelines* más amplios de datos.

- **Ciberseguridad y criptografía:** Como se discutió, la computación cuántica exige una renovación de los esquemas de seguridad. Al mismo tiempo, brinda oportunidades como la **generación cuántica de números aleatorios** (ya comercializada, garantizando entropía impredecible) y protocolos criptográficos cuánticos innovadores. Por ejemplo, se investiga la **identificación cuántica** (verificación de identidad física a través de propiedades cuánticas de un dispositivo) y las **firmas digitales cuánticas**. Un computador cuántico suficientemente grande podría quebrar cifrados actuales, pero también ayudar a diseñar cifrados nuevos más fuertes y optimizar protocolos de seguridad.

- **Simulación y ciencia básica:** Los científicos utilizan supercomputadoras clásicas para simular todo tipo de fenómenos (clima, astrofísica, dinámica de fluidos, economía). Muchas de esas simulaciones podrían beneficiarse de acelerar subcálculos particulares mediante algoritmos cuánticos. Por ejemplo, en climatología, un computador cuántico podría mejorar la simulación de reacciones químicas atmosféricas o procesos de nucleación a nivel molecular [^67], refinando modelos de cambio climático. En energética, optimizar diseños de fusión nuclear o nuevas baterías. En finanzas, generar mejores modelos de riesgo mediante simulación estocástica cuántica. En inteligencia artificial, explorar modelos de **computación cuántica neuromórfica** inspirados en el cerebro. Asimismo, la computación cuántica abre preguntas fundamentales en física: su misma construcción ayuda a probar los límites de la física cuántica (por ejemplo, pruebas de entropía de agujeros negros en laboratorios cuánticos, o simulaciones de cosmología cuántica). En palabras de un investigador, *“una computadora cuántica nos enseña el lenguaje de la naturaleza”*, permitiendo que incluso la IA formule descubrimientos científicos directamente a partir de principios cuánticos [^68] [^69].

Por supuesto, alcanzar estas aplicaciones de impacto general requiere **superar los desafíos actuales**. ¿Qué falta para lograrlo? Principalmente, **más cúbits y mejores cúbits**. La corrección de errores cuánticos debe pasar de experimentos con <100 cúbits a implementarse a escala de miles o millones, lo cual es una tarea de ingeniería colosal. Cada cúbit lógico en una computadora cuántica tolerante a fallos probablemente exigirá del orden de **1 000 cúbits físicos** o más dedicados a corrección de errores. Hoy apenas rozamos ~100 cúbits físicos en los chips líderes, y ninguno es *error-corrected*. El *overhead* es enorme pero no imposible: IBM, Google y otros trazan *roadmaps* hacia sistemas de ~1 millón de cúbits físicos en la próxima década, y confían en que las mejoras en materiales, conectividad y firmware reducirán la tasa de error lo suficiente para que ese millón de cúbits pueda encapsular quizá unos cientos de cúbits lógicos útiles [^22] [^70]. Junto a ello, habrá que desarrollar nuevos **algoritmos cuánticos optimizados para hardware ruidoso (NISQ)**, de modo que las computadoras cuánticas puedan aportar valor útil aun antes de ser perfectamente estables.

También persisten retos de **escalabilidad práctica**: la electrónica de control y lectura (actualmente decenas de cables coaxiales por cada cúbit en un frigorífico) debe simplificarse, posiblemente integrando **controladores criogénicos** en el criostato, como investiga Intel, o usando **fotónica de microondas** para multiplexar señales. El **consumo energético** de un centro de datos cuántico con miles de cúbits y refrigeración sub-Kelvin es no trivial; se estudian refrigeradores de dilución más eficientes y materiales superconductores topológicos que reduzcan la carga de enfriamiento. La **reproducibilidad industrial** de cúbits con parámetros uniformes y baja variación es otra área activa —aquí las técnicas de **nanofabricación** y **metrología cuántica** juegan un papel clave.

Finalmente, está el **factor humano y la multidisciplinariedad**. Desarrollar una computadora cuántica útil no solo involucra físicos; se necesitan **ingenieros electrónicos**, **expertos en criogenia**, **científicos de materiales**, **informáticos en algoritmos** y **teóricos de la información**. Grandes corporaciones y gobiernos invierten en la formación de profesionales cuánticos. Universidades de todo el mundo han creado centros de investigación especializados (Chicago Quantum Exchange, MIT CQE, ETH Quantum Center, etc.) para cultivar la próxima generación de expertos [^71]. La colaboración público-privada también se refleja en consorcios como el **IBM Quantum Network** (más de 180 miembros institucionales) o el programa **Quantum Inspire** europeo.

# Conclusión

El estado del arte de la tecnología cuántica en 2025 muestra un panorama dinámico: por un lado, **hitos impresionantes** que validan los principios (supremacía cuántica, prototipos de cientos de cúbits, primeras redes cuánticas), y por otro, **un largo camino hacia la utilidad práctica**. Para un ejecutivo técnico, es vital apreciar tanto el potencial disruptivo como la realidad actual. La computación cuántica **no reemplazará a la clásica** en el corto plazo; más bien la **complementará** en nichos especializados.  

La recomendación es **seguir de cerca los desarrollos**, experimentar con **problemas piloto** que puedan beneficiarse (optimizaciones pequeñas, simulaciones moleculares acotadas) e **iniciar la adaptación en seguridad** ante la futura amenaza cuántica.  

Las organizaciones que **construyan conocimiento interno** en algoritmos cuánticos y post-cuánticos estarán mejor posicionadas para **aprovechar —y mitigar—** el impacto de esta tecnología cuando madure plenamente [^72]. La revolución cuántica, al igual que la inteligencia artificial, no ocurrirá de la noche a la mañana, pero **sus cimientos ya se están colocando**.  

En la próxima década podríamos ver cómo las promesas cuánticas se convierten en herramientas prácticas que impulsen nuevas olas de innovación en la industria y la ciencia. Las piezas se están alineando para que la computación cuántica, acompañada de la IA y la computación clásica, inaugure una era de **supercomputación heterogénea** al servicio de resolver problemas antes inabordables [^73] [^74].  

La pregunta ya no es *“¿llegará la computación cuántica?”*, sino *“¿estaremos preparados para cuando llegue a su plenitud?”*.

# Referencias

[^1]: Arute et al., “Quantum supremacy using a programmable superconducting processor,” *Nature*, 574(7779), 505–510 (2019).  
[^2]: Preskill, J., “Quantum Computing in the NISQ era and beyond,” *Quantum*, 2, 79 (2018).  
[^3]: IBM Quantum Roadmap, “The era of quantum utility is here,” IBM Research Blog (2023).  
[^4]: Google Quantum AI, “Suppressing quantum errors by scaling a surface code logical qubit,” *Nature* (2023).  
[^5]: Arute et al., “Quantum supremacy...,” *Nature* (2019).  
[^6]: IBM Research, “IBM Condor: 1,121-qubit processor unveiled,” IBM Newsroom (2023).  
[^7]: Microsoft Azure Quantum Blog, “Introducing Majorana 1: topological qubits for scalable quantum computing” (2025).  
[^8]: Quantinuum, “System Model H2: trapped-ion quantum computer with all-to-all connectivity,” Press Release (2023).  
[^9]: Xanadu, “Borealis: programmable photonic processor achieves quantum advantage,” *Nature* (2022).  
[^10]: IBM, “Qiskit documentation,” https://qiskit.org (2025).  
[^11]: Microsoft Learn, “Q# and the Quantum Development Kit,” https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview (2025).  
[^12]: Shor, P., “Algorithms for quantum computation: discrete logarithms and factoring,” *Proc. 35th IEEE Symposium on Foundations of Computer Science* (1994).  
[^13]: NIST, “Finalized post-quantum cryptography standards (FIPS 203–205),” August 2024. https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
[^14]: Preskill, J., “Quantum Computing in the NISQ era and beyond,” *Quantum*, 2, 79 (2018).  
[^15]: Arute et al., “Quantum supremacy using a programmable superconducting processor,” *Nature*, 574(7779), 505–510 (2019).  
[^16]: Pednault et al., “On ‘Quantum Supremacy’,” IBM Research Blog (2019).  
[^17]: Preskill, J., “The NISQ era and the future of quantum computing,” Caltech Lecture (2018).  
[^18]: Zhong et al., “Quantum computational advantage using photons,” *Science*, 370(6523), 1460–1463 (2020).  
[^19]: Madsen et al., “Quantum computational advantage with a programmable photonic processor,” *Nature*, 606(7912), 75–81 (2022).  
[^20]: Google Quantum AI, “Suppressing quantum errors by scaling a surface code logical qubit,” *Nature*, 614(7949), 676–681 (2023).
[^21]: IBM Research Blog, “IBM Condor: 1,121-qubit processor unveiled,” IBM (2023).  
[^22]: IBM Quantum Roadmap 2033, “The Era of Quantum Utility Is Here” (2023).  
[^23]: Google Quantum AI, “Suppressing quantum errors by scaling a surface code logical qubit,” *Nature*, 614(7949), 676–681 (2023).  
[^24]: Microsoft Azure Quantum Blog, “Introducing Majorana 1: topological qubits for scalable quantum computing” (2025).  
[^25]: Microsoft Research, “Evidence of Majorana zero modes in hybrid nanowires,” *Physical Review B* (2022).  
[^26]: Microsoft Newsroom, “Majorana 1 chip demonstrates topological quantum architecture” (2023).  
[^27]: Reuters Technology, “Microsoft claims breakthrough in quantum computing with Majorana-based chip” (2023).  
[^28]: Microsoft Quantum Development Kit, documentación oficial Q# (2025).  
[^29]: Azure Quantum Overview, https://learn.microsoft.com/en-us/azure/quantum/overview-azure-quantum (2025).  
[^30]: D-Wave Systems, “Advantage2 Quantum Computer: 5,000+ qubits for optimization,” (2024).  
[^31]: IonQ Press Release, “IonQ systems available via AWS Braket and Azure Quantum” (2023).  
[^32]: Quantinuum, “Company Overview and Quantum Solutions,” (2024).  
[^33]: Quantinuum Product Sheet, “System Model H2,” (2024).  
[^34]: Microsoft & Quantinuum Joint Press Release, “Entangling logical qubits with record low error” (2023).  
[^35]: Quantinuum Blog, “Demonstrating logical qubit entanglement on H2” (2023).  
[^36]: Atom Computing, “Phoenix: 100-qubit neutral atom prototype” (2021).  
[^37]: TechCrunch, “Atom Computing raises $60M to scale neutral-atom platform” (2022).  
[^38]: U.S. Department of Energy, “Quantum Partnership with Atom Computing Announced” (2023).  
[^39]: Microsoft Azure Quantum Partners, “Atom Computing joins Azure Quantum hardware ecosystem” (2023).  
[^40]: QuEra Computing, “Aquila: 256-atom neutral quantum processor demonstration” (2022).  
[^41]: South China Morning Post, “China unveils Tianyan-504, its most powerful superconducting quantum computer” (2023).  
[^42]: Nature Asia, “China’s Tianyan-504 Quantum Processor Sets New Benchmark” (2023).
[^43]: European Quantum Flagship, “Quantum Hardware Landscape 2024,” Technical Roadmap (2024).  
[^44]: Devoret, M. & Schoelkopf, R., “Superconducting Circuits for Quantum Information,” *Science*, 339(6124), 1169–1174 (2013).  
[^45]: Intel Labs, “Tunnel Falls: 12-qubit silicon spin quantum chip,” Intel Newsroom (2022).  
[^46]: Madsen et al., “Quantum computational advantage with a programmable photonic processor,” *Nature*, 606(7912), 75–81 (2022).
[^47]: IBM Quantum — Panorama de SDKs y recursos para desarrollo cuántico. https://quantum.ibm.com/  
[^48]: **Qiskit** — Documentación y guías. https://qiskit.org/  
[^49]: **PennyLane** — Quantum ML y algoritmos variacionales. https://pennylane.ai/  
[^50]: Ejemplos “estado de Bell” en múltiples SDKs: • Qiskit Tutorial “Bell State” — https://qiskit.org/documentation/intro_tutorials/03_qubits_and_gates.html • Cirq “Bell state” — https://quantumai.google/cirq/start/basics • Q# Samples (entrelazamiento) — https://learn.microsoft.com/azure/quantum/user-guide/ • PennyLane “Entangling qubits” — https://pennylane.ai/qml/demos/  
[^51]: Acceso en la nube: • **IBM Quantum Experience** — https://quantum.ibm.com/ • **Azure Quantum** — https://learn.microsoft.com/azure/quantum/ • **AWS Braket** — https://docs.aws.amazon.com/braket/
[^52]: Shor, P. W., “Algorithms for quantum computation: discrete logarithms and factoring,” *Proceedings of the 35th IEEE Symposium on Foundations of Computer Science* (1994).  
[^53]: Bernstein, D., Buchmann, J., & Dahmen, E. (Eds.), *Post-Quantum Cryptography*, Springer (2009).  
[^54]: NIST, “FIPS 203, 204, 205: First finalized post-quantum encryption and signature standards,” Press Release, August 2024.  
[^55]: NSA, “Quantum Computing and Cryptography: Risks and Recommendations,” Technical Report (2022).  
[^56]: ETSI Quantum-Safe Working Group, “Migration Strategies for Post-Quantum Cryptography,” Whitepaper (2023).  
[^57]: U.S. Office of the National Cyber Director, “National Security Memorandum on Promoting U.S. Leadership in Quantum-Resistant Cryptography” (2022).  
[^58]: European Commission, “EuroQCI – European Quantum Communication Infrastructure,” Digital Strategy (2024).
[^59]: Cao, Y. et al., “Quantum Chemistry in the Age of Quantum Computing,” *Chemical Reviews*, 119(19), 10856–10915 (2019).  
[^60]: Reiher, M. et al., “Elucidating reaction mechanisms on quantum computers,” *PNAS*, 114(29), 7555–7560 (2017).  
[^61]: Aspuru-Guzik, A. et al., “Simulated quantum computation of molecular energies,” *Science*, 309(5741), 1704–1707 (2005).  
[^62]: Farhi, E. et al., “A Quantum Approximate Optimization Algorithm,” *arXiv:1411.4028* (2014).  
[^63]: Orús, R., Mugel, S., & Lizaso, E., “Quantum computing for finance: Overview and prospects,” *Rev. Phys.*, 4, 100028 (2019).  
[^64]: Biamonte, J. et al., “Quantum machine learning,” *Nature*, 549(7671), 195–202 (2017).  
[^65]: Schuld, M. & Petruccione, F., *Machine Learning with Quantum Computers*, Springer (2021).  
[^66]: Bukov, M. et al., “Reinforcement learning in different phases of quantum control,” *Phys. Rev. X*, 8, 031086 (2018).  
[^67]: Kassal, I. et al., “Simulating chemistry using quantum computers,” *Annu. Rev. Phys. Chem.*, 62, 185–207 (2011).  
[^68]: Preskill, J., “Quantum Computing and the Entanglement Frontier,” *arXiv:1203.5813* (2012).  
[^69]: Lloyd, S., “Quantum Computation and Quantum Information,” *Cambridge University Press* (2014).  
[^70]: IBM Quantum Roadmap 2025–2033, IBM Research Blog (2024).  
[^71]: Chicago Quantum Exchange, “Training the Next Quantum Workforce,” *CQE Report* (2023).  
[^72]: McKinsey & Co., “The Quantum Technology Monitor,” (2025).  
[^73]: Harrow, A. & Montanaro, A., “Quantum computational advantage,” *Nature*, 549(7671), 203–209 (2017).  
[^74]: Arute et al., “Quantum supremacy revisited,” *Nature Physics*, 19, 1410–1417 (2023).
[^75]: Bernhardt, C. (2020). Quantum Computing for Everyone. MIT Press.
[^76]: Microsoft. *New capabilities in Azure Quantum Elements: Generative Chemistry and Accelerated DFT*. Azure Quantum Blog, 2024.
[^77]: Microsoft. *Compressing 250 years of scientific discovery into the next 25*. Microsoft News Center, 2023.
[^78]: Google Quantum AI. *The road to a useful, error-corrected quantum computer*. Quantum AI Research Blog, 2024.
[^79]: Google Blog. *Meet Willow, our state-of-the-art quantum chip*. Google Research, 2024.
[^80]: Google Quantum AI. *Applications of quantum computing in materials, chemistry, and machine learning*. quantumai.google, 2024.
[^81]: The Quantum Insider. *Google predicts commercial quantum applications within five years*, 2025.
[^82]: Microsoft. *Introducing Azure Quantum Elements: Accelerating scientific discovery with AI, HPC, and quantum computing*. Microsoft Research Blog, 2023.