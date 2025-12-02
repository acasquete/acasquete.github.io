---
title: La era cuántica, más allá del silicio
tags: [personal, quantum_computing]
reviewed: true
home: true
ai: true
header_image: quantum-hardware-closeup.jpg
---
La **computación cuántica** promete transformar la informática al aprovechar fenómenos de la mecánica cuántica como la *superposición* y el *entrelazamiento* para procesar información de formas imposibles para los ordenadores clásicos. <!-- excerpt-end --> En lugar de bits, utiliza **cúbits**, capaces de mantenerse en múltiples estados a la vez, lo que multiplica exponencialmente la capacidad de cómputo[^1]. Esto abre la puerta a resolver problemas hoy inabordables, desde la simulación de moléculas complejas hasta la optimización de sistemas logísticos o financieros[^2].

Para quienes se acercan por primera vez a la **tecnología cuántica**, es habitual que el párrafo anterior resulte abrumador. Conceptos como **superposición**, **entrelazamiento** o **estados simultáneos** requieren cierta base de física cuántica y pueden parecer intimidantes al principio.

El objetivo de esta serie de artículos no es profundizar en la teoría, sino ofrecer una visión clara y práctica del estado actual de la tecnología cuántica. Quienes deseen explorar los fundamentos pueden encontrar excelentes recursos introductorios, como *Quantum Computing for Everyone*, de Chris Bernhardt (MIT Press, 2020)[^3]. Además, cada artículo incluirá referencias adicionales para ampliar información.

Hoy la tecnología cuántica sigue siendo **emergente**: las aplicaciones reales son limitadas y los retos de ingeniería son enormes. Los cúbits son extremadamente sensibles al entorno y sufren **decoherencia** y errores que dificultan cálculos estables. Aun así, los avances de los últimos años han sido rápidos, con empresas e instituciones compitiendo por superar desafíos como la corrección de errores y la escalabilidad[^4] [^5].

Desde que Google anunció en 2019 la llamada *supremacía cuántica* con su procesador **Sycamore**, capaz de completar en 200 segundos una tarea que a un superordenador le llevaría miles de años[^1], la carrera hacia una **ventaja cuántica práctica** se ha intensificado. IBM ha escalado sus procesadores superconductores desde 5 cúbits en 2016 hasta más de 1000 en 2023 con su chip **Condor**[^6]. Microsoft, en cambio, apuesta por cúbits **topológicos de Majorana**, que en teoría permiten una corrección de errores más eficiente[^7].

En 2025, Google Quantum AI sigue centrada en la construcción de cúbits lógicos más estables mediante códigos de superficie. Tras los avances de 2023 y 2024, en los que logró reducir los errores por debajo del umbral necesario para la corrección lógica, la compañía ha demostrado memorias cuánticas donde el cúbit lógico supera en fidelidad a los mejores cúbits físicos, un paso importante hacia sistemas tolerantes a fallos.[^5]

IBM avanza en una dirección complementaria con **IBM Quantum System Two**, una arquitectura modular diseñada para la nueva era del "quantum-centric supercomputing". Su enfoque combina criogenia escalable, electrónica de control modular y varios procesadores Heron integrados en una misma plataforma, con la intención de facilitar la interconexión de múltiples chips y el aumento progresivo de la capacidad de cómputo.[^4]

Microsoft, por su parte, apuesta por una vía distinta con el procesador **Majorana 1**, basado en su propuesta de cúbits topológicos más robustos frente al ruido. Aunque la empresa afirma haber dado un paso relevante hacia esa meta, parte de la comunidad científica se mantiene cauta y considera que aún no hay pruebas concluyentes de que estos cúbits topológicos operen de forma plenamente funcional. Esto mantiene abierto el debate sobre la madurez real de este enfoque frente a las plataformas superconductoras o de iones atrapados.[^7]

Al mismo tiempo, startups como **IonQ**, **Quantinuum**, **Atom Computing** o **QuEra** avanzan con plataformas basadas en iones atrapados o átomos neutros, mientras que **Xanadu** y **PsiQuantum** exploran arquitecturas fotónicas. Cada alternativa ofrece ventajas y limitaciones propias en términos de errores, estabilidad y escalabilidad[^8] [^9].

En el ámbito del software, han surgido lenguajes y frameworks como **Qiskit** (IBM), **Q#** (Microsoft), **Cirq** (Google) y **PennyLane** (Xanadu), que permiten diseñar y ejecutar algoritmos cuánticos tanto en simuladores como en hardware real disponible en la nube[^10] [^11].

Finalmente, la revolución cuántica también transformará la **ciberseguridad**. Los algoritmos de Shor y Grover amenazan los sistemas criptográficos basados en RSA y ECC una vez existan ordenadores cuánticos tolerantes a fallos[^12]. Para adelantarse a ese escenario, el **NIST** publicó en 2024 los primeros estándares de **criptografía post-cuántica**, iniciando una transición global hacia algoritmos resistentes a ataques cuánticos[^13].

La computación cuántica avanza en varios frentes a la vez: hardware, software, ciberseguridad, nuevas arquitecturas y corrección de errores. Comprender este panorama requiere analizar cada línea de desarrollo por separado, pero también considerar cómo se integran todas en un camino común hacia sistemas cuánticos realmente útiles.

En los próximos artículos abordaremos:

- Los hitos recientes desde la *supremacía cuántica* hasta la *ventaja cuántica práctica*.  
- Los principales actores y líneas de investigación.  
- Las distintas arquitecturas de procesadores cuánticos y sus retos.  
- Los lenguajes y frameworks más utilizados en programación cuántica.  
- El impacto en seguridad y el avance de la criptografía post-cuántica.  
- Aplicaciones emergentes en simulación química, inteligencia artificial y optimización.

La intención es ofrecer una visión clara, actualizada y accesible del panorama cuántico: qué es viable hoy, qué avances se aproximan y cómo pueden prepararse las organizaciones para esta transformación.

# Referencias

[^1]: Arute et al., "Quantum supremacy using a programmable superconducting processor," *Nature*, 574(7779), 505–510 (2019). [https://doi.org/10.1038/s41586-019-1666-5](https://doi.org/10.1038/s41586-019-1666-5)  
[^2]: Preskill, J., "Quantum Computing in the NISQ era and beyond," *Quantum*, 2, 79 (2018). [https://doi.org/10.22331/q-2018-08-06-79](https://doi.org/10.22331/q-2018-08-06-79)  
[^3]: Bernhardt, C. (2020). *Quantum Computing for Everyone*. MIT Press.  
[^4]: IBM Quantum Roadmap, "The era of quantum utility is here," IBM Research Blog (2023). [https://research.ibm.com/blog/quantum-roadmap-2033](https://research.ibm.com/blog/quantum-roadmap-2033)  
[^5]: Google Quantum AI, "Suppressing quantum errors by scaling a surface code logical qubit," *Nature* (2023). [https://doi.org/10.1038/s41586-022-05434-1](https://doi.org/10.1038/s41586-022-05434-1)  
[^6]: IBM Research, "IBM Condor: 1,121-qubit processor unveiled," IBM Newsroom (2023). [https://postquantum.com/industry-news/ibm-condor](https://postquantum.com/industry-news/ibm-condor))  
[^7]: Microsoft Azure Quantum Blog, "Introducing Majorana 1: topological qubits for scalable quantum computing" (2025). [https://cloudblogs.microsoft.com/quantum/](https://cloudblogs.microsoft.com/quantum)  
[^8]: Quantinuum, "System Model H2: trapped-ion quantum computer with all-to-all connectivity," Press Release (2023). [https://www.quantinuum.com/hardware/h2](https://www.quantinuum.com/hardware/h2)  
[^9]: Xanadu, "Borealis: programmable photonic processor achieves quantum advantage," *Nature* (2022). [https://doi.org/10.1038/s41586-022-04725-x](https://doi.org/10.1038/s41586-022-04725-x)  
[^10]: IBM, "Qiskit documentation" (2025). [https://qiskit.org/documentation](https://qiskit.org/documentation)  
[^11]: Microsoft Learn, "Q# and the Quantum Development Kit" (2025). [https://learn.microsoft.com/azure/quantum](https://learn.microsoft.com/azure/quantum)  
[^12]: Shor, P., "Algorithms for quantum computation: discrete logarithms and factoring," *Proc. 35th IEEE Symposium on Foundations of Computer Science* (1994). [https://doi.org/10.1109/SFCS.1994.365700](https://doi.org/10.1109/SFCS.1994.365700)  
[^13]: NIST, "Finalized post-quantum cryptography standards (FIPS 203–205)," August 2024. [https://csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)  
