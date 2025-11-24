---
title: La era cuántica, más allá del silicio
tags: [personal, quantum]
reviewed: true
home: true
ai: true
header_fullview: quantum-hardware-closeup.jpg
---
La **computación cuántica** promete revolucionar la informática al aprovechar fenómenos de la mecánica cuántica como la *superposición* y el *entrelazamiento* para procesar información de formas imposibles para los ordenadores clásicos. <!-- excerpt-end --> En lugar de bits binarios, emplea **cúbits**, que pueden estar en múltiples estados simultáneamente, multiplicando exponencialmente la capacidad de cómputo[^1]. Esto abre la puerta a resolver problemas intratables hoy en día, desde la simulación de moléculas complejas hasta la optimización de sistemas logísticos o financieros[^2].

Si es la primera vez que se enfrenta a un texto sobre **tecnología cuántica**, el párrafo anterior puede resultar aturdidor. Términos como **superposición**, **entrelazamiento** o **estados simultáneos** requieren cierto **conocimiento previo de física cuántica**, lo que puede resultar intimidante al principio

El propósito de este artículo no es profundizar en la teoría física que hay detrás, sino ofrecer una visión comprensible y práctica del estado actual de la tecnología cuántica. Para quienes deseen explorar con más detalle los fundamentos teóricos, existen excelentes recursos introductorios de física cuántica y computación cuántica a los que el lector puede remitirse, como *Quantum Computing for Everyone* de Chris Bernhardt (MIT Press, 2020) [^75]. Además, cada artículo incluirá una referencia bibliográfica para ampliar la información.

La tecnología se encuentra aún en una fase **emergente**: sus aplicaciones prácticas son limitadas y enfrenta grandes desafíos de ingeniería. Los cúbits son extremadamente sensibles al entorno y sufren **decoherencia** y errores que dificultan mantener cálculos estables. Aun así, los avances en los últimos años han sido rápidos, con empresas e instituciones compitiendo por superar obstáculos como la corrección de errores y la escalabilidad de los sistemas cuánticos [^3] [^4].

Desde 2019, cuando Google anunció haber alcanzado la llamada *supremacía cuántica* con su procesador **Sycamore** —capaz de realizar en 200 segundos una tarea que habría llevado miles de años a un superordenador clásico— [^1], la carrera por lograr una **ventaja cuántica práctica** se ha intensificado. IBM, por su parte, ha escalado sus procesadores superconductores desde 5 cúbits en 2016 hasta más de 1 000 cúbits en 2023 con el chip **Condor** [^6]. Microsoft ha apostado por una vía diferente, basada en cúbits **topológicos de Majorana**, que podrían ofrecer una corrección de errores más eficiente [^7].

En 2025, Google se centra en la construcción de cúbits lógicos estables mediante códigos de superficie y ha mostrado avances al reducir las tasas de error al escalar cúbits físicos dentro de un mismo cúbit lógico. IBM continúa desarrollando arquitecturas modulares con su sistema Quantum System Two, orientadas a interconectar múltiples chips cuánticos en una misma plataforma para facilitar el escalado. Microsoft, tras anunciar el procesador Majorana 1 y presentar una hoja de ruta hacia sistemas de gran escala, ha generado controversia: parte de la comunidad científica cuestiona que los experimentos publicados demuestren de forma concluyente la presencia y control de cúbits topológicos operativos. Algunos investigadores y figuras de la industria han señalado que los resultados podrían representar etapas intermedias y no todavía una implementación funcional completa, lo que ha abierto un debate sobre el grado real de madurez de este enfoque en comparación con las plataformas superconductoras o de iones atrapados.

Paralelamente, startups como **IonQ**, **Quantinuum**, **Atom Computing** o **QuEra** han desarrollado plataformas basadas en iones atrapados o átomos neutros, mientras **Xanadu** y **PsiQuantum** exploran arquitecturas fotónicas. Estas alternativas persiguen reducir los errores y facilitar la escalabilidad, cada una con ventajas y limitaciones propias [^8] [^9].

A nivel de software, han surgido lenguajes y frameworks de programación cuántica como **Qiskit** (IBM), **Q#** (Microsoft), **Cirq** (Google) y **PennyLane** (Xanadu), que permiten a desarrolladores e investigadores diseñar y ejecutar algoritmos cuánticos en entornos simulados o en hardware real accesible desde la nube [^10] [^11].

La revolución cuántica no solo afectará al cómputo: también redefine la **ciberseguridad**. Los algoritmos de Shor y Grover podrían poner en riesgo los sistemas criptográficos actuales basados en RSA y ECC una vez existan computadoras cuánticas tolerantes a fallos [^12]. Para adelantarse a ese riesgo, el **NIST** publicó en 2024 los primeros estándares de **criptografía post-cuántica**, inaugurando una transición global hacia algoritmos resistentes a ataques cuánticos [^13].

En los próximos artículos exploraremos el **estado del arte de la tecnología cuántica en 2025**, abordando:

- Los hitos recientes desde la *supremacía cuántica* hasta la *ventaja cuántica práctica*.  
- Los principales actores y líneas de investigación.  
- Las diferentes arquitecturas de procesadores cuánticos y sus desafíos.  
- Los lenguajes y frameworks más utilizados para la programación cuántica.  
- El impacto en seguridad y criptografía post-cuántica.  
- Aplicaciones emergentes en simulación química, IA y optimización.

El objetivo es ofrecer una visión clara, actualizada y accesible del panorama cuántico para quienes necesiten entender qué es viable hoy, qué avances se avecinan y cómo pueden preparar a sus organizaciones para esta transformación.

# Referencias

[^1]: Arute et al., “[Quantum supremacy using a programmable superconducting processor](https://www.nature.com/articles/s41586-019-1666-5)” *Nature*, 574(7779), 505–510 (2019). 
[^2]: Preskill, J., “[Quantum Computing in the NISQ era and beyond](https://quantum-journal.org/papers/q-2018-08-06-79/),” *Quantum*, 2, 79 (2018).  
[^3]: IBM Quantum Roadmap, “[The era of quantum utility is here](https://www.ibm.com/quantum/blog/quantum-roadmap-2033),” IBM Research Blog (2023).  
[^4]: Google Quantum AI, “[Suppressing quantum errors by scaling a surface code logical qubit](https://www.nature.com/articles/s41586-022-05434-1),” *Nature* (2023).    
[^6]: IBM Research, “IBM Condor: 1,121-qubit processor unveiled,” IBM Newsroom (2023).  
[^7]: Microsoft Azure Quantum Blog, “Introducing Majorana 1: topological qubits for scalable quantum computing” (2025).  
[^8]: Quantinuum, “System Model H2: trapped-ion quantum computer with all-to-all connectivity,” Press Release (2023).  
[^9]: Xanadu, “Borealis: programmable photonic processor achieves quantum advantage,” *Nature* (2022).  
[^10]: IBM, “Qiskit documentation,” https://qiskit.org (2025).  
[^11]: Microsoft Learn, “Q# and the Quantum Development Kit,” https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview (2025).  
[^12]: Shor, P., “Algorithms for quantum computation: discrete logarithms and factoring,” *Proc. 35th IEEE Symposium on Foundations of Computer Science* (1994).  
[^13]: NIST, “Finalized post-quantum cryptography standards (FIPS 203–205),” August 2024. https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
[^14]: Preskill, J., “Quantum Computing in the NISQ era and beyond,” *Quantum*, 2, 79 (2018).  
[^75]: Bernhardt, C. (2020). Quantum Computing for Everyone. MIT Press.
