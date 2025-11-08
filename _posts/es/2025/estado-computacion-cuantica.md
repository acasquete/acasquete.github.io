---
title: Tecnología cuántica en 2025
tags: [personal, quantum]
reviewed: false
home: true
ai: true
---
La computación cuántica busca explotar superposición y entrelazamiento para resolver problemas que los sistemas clásicos no abordan de forma práctica. El progreso es real pero desigual: se han logrado demostraciones de “ventaja” cuántica en tareas específicas, mientras que la utilidad empresarial general requiere todavía cúbits con menos errores, escalabilidad y corrección de errores efectiva.

## De “supremacía” a ventaja cuántica

En 2019, Google mostró que su procesador **Sycamore** (53 cúbits superconductores) podía muestrear circuitos aleatorios en ~200 s, frente a una estimación clásica de ~10 000 años. Fue la primera demostración ampliamente aceptada de lo que entonces se llamó “supremacía cuántica” en una tarea sintética de muestreo [1]. El término ha ido cediendo terreno a **ventaja cuántica** por razones técnicas y semánticas [2][3].

Tras Google, el grupo de USTC en China logró ventaja en **boson sampling** con el sistema fotónico **Jiuzhang** (76 fotones) [4], seguido por mejoras posteriores. En 2022, **Xanadu** demostró ventaja con el procesador fotónico **Borealis** de 216 modos, programable y accesible en la nube [5][6].

El foco actual se desplaza de “ganar en un benchmark” a **aportar utilidad** y a demostrar que la corrección de errores mejora al escalar. En 2023, Google mostró que aumentar el tamaño del código de superficie reduce la tasa de error lógica, un hito clave hacia cúbits lógicos utilizables [7][8].

## Actores principales y panorama competitivo

- **IBM**. Presentó **Condor** (1 121 cúbits superconductores) en 2023 y una hoja de ruta hacia sistemas tolerantes a fallos, con avances en corrección de errores tipo LDPC y métricas de calidad a escala [9][10][11][12][13][14].

- **Google Quantum AI**. Tras Sycamore, ha publicado resultados en corrección de errores con códigos de superficie y lanzó nuevas generaciones de chips. El trabajo de 2023 probó mejora lógica con mayor distancia de código [7][8]. También anunció chips como Willow en 2024 dentro de su trayectoria hacia “cómputo útil más allá de lo clásico” [15].

- **Microsoft**. Apuesta por **cúbits topológicos** basados en modos de **Majorana**. En 2025 presentó el chip **Majorana 1** y afirmó un salto hacia cúbits más estables por diseño [16][17][18][19]. La comunidad mantiene un debate abierto sobre la solidez de las evidencias y el grado de verificación independiente [20][21].

- **D-Wave**. Especialista en **recocido cuántico** para optimización, con sistemas **Advantage** de más de 5 000 cúbits, uso comercial y resultados recientes en problemas útiles y simulación cuántica análoga [22][23][24][25][26].

- **Trapped-ion y átomos neutros**.  
  - **Quantinuum** (iones atrapados) con **H2** y conectividad all-to-all, mid-circuit measurement y progresos en corrección de errores y cúbits lógicos [27][28][29].  
  - **IonQ** (iones atrapados), acceso por nube y una hoja de ruta agresiva. En 2025 reportó 99.99% de fidelidad en puertas de dos cúbits y adquisiciones estratégicas para acelerar su plataforma [30][31][32].  
  - **QuEra** (átomos neutros) con **Aquila** de 256 cúbits analógicos accesible vía Amazon Braket [33][34].  
  - **Atom Computing** (átomos neutros) anunció sistemas de más de 1 000 cúbits y publica hojas de ruta técnicas para escalar con matrices ópticas [35][36].  
  - **Rigetti** (superconductores) evolucionó su línea **Ankaa** de 84 cúbits y trabaja en integración multi-chip y disponibilidad en la nube propia y de terceros [37][38][39].

- **Nube cuántica**. **AWS Braket**, **Azure Quantum** e **IBM Quantum** ofrecen acceso a múltiples hardwares y SDKs (Cirq, Qiskit, Q#, PennyLane), facilitando experimentación y pipelines híbridos [40][41][42][43].

## Hardware cuántico: enfoques

- **Superconductores**. Dominan Google, IBM, Rigetti. Ventajas en velocidad de puerta y fabricación avanzada. Retos en escalado y conectividad con fidelidades de 2-qubit en el rango 10⁻³ a 10⁻² según contexto y generación [9][11][12][14].

- **Iones atrapados**. Fidelidades muy altas y conectividad densa a pequeña escala. Retos en velocidad y escalado físico. Quantinuum e IonQ lideran demostraciones de calidad y protocolos avanzados [27][28][30].

- **Átomos neutros**. Escalabilidad prometedora con “optical tweezers” y estados de Rydberg. QuEra, Pasqal y Atom Computing empujan el estado del arte, con dispositivos de cientos a más de mil cúbits físicos en modos analógicos o mixtos [33][34][35][36].

- **Fotónica**. Robustez a temperatura ambiente y redes cuánticas como caso natural. Ventaja demostrada en muestreo bosónico con Jiuzhang y Borealis. El reto es la interacción efectiva entre fotones para cómputo universal [4][5][6].

- **Topológicos**. Objetivo a largo plazo de Microsoft para cúbits intrínsecamente protegidos. Resultados de 2025 han generado atención y también escepticismo hasta mayor validación independiente [16][17][20][21].

## Programación cuántica y herramientas

- **Qiskit** (IBM). SDK abierto en Python con acceso a hardware IBM, transpilación optimizada y librerías para química, ML y optimización [44][45][46][47].

- **Cirq** (Google). Biblioteca Python orientada a NISQ y a detalles de hardware. Integra ejecución en simuladores y backends de Google e incluso soportes de terceros [48][49][50][51].

- **Q#** (Microsoft). Lenguaje dedicado con el Quantum Development Kit y ejecución vía Azure Quantum. Orientado a composición modular y flujos híbridos [52][53][54].

- **PennyLane** (Xanadu). Framework para algoritmos variacionales y ML cuántico con integración nativa con PyTorch, JAX y TensorFlow, y múltiples backends [55][56][57].

- **AWS Braket SDK**. Orquesta flujos con varios hardwares y simuladores, integración con CUDA-Q y servicios de AWS para pipelines híbridos [40][58].

## Seguridad cuántica y estándares post-cuánticos

Los algoritmos de **Shor** y **Grover** amenazan la criptografía asimétrica actual cuando existan computadores cuánticos tolerantes a fallos de gran tamaño. Para mitigar el riesgo de “capturar ahora y descifrar después”, el **NIST** publicó en agosto de 2024 los **primeros estándares FIPS** de criptografía post-cuántica: **FIPS 203 (ML-KEM/Kyber)**, **FIPS 204 (ML-DSA/Dilithium)** y **FIPS 205 (SPHINCS+)**. La migración a estos algoritmos ya ha comenzado en navegadores, TLS y PKI piloto [59] [60].

En paralelo, las **comunicaciones cuánticas** avanzan con **QKD** terrestre y espacial. El satélite chino **Micius** demostró distribución de entrelazamiento y QKD a >1 000 km, consolidando la viabilidad de redes cuánticas espacio-tierra. Europa impulsa **EuroQCI** para una infraestructura cuántica de comunicaciones a escala continental [61] [62] [63] [64] [65] [66] [67] [68].

## Aplicaciones y hoja de ruta

Las primeras aplicaciones con impacto se perfilan en **simulación química y de materiales**, **optimización**, **finanzas** y **IA híbrida**. En el corto plazo, son probables **ventajas específicas** en tareas bien encajadas al hardware. La **corrección de errores** y la **integración híbrida** serán los diferenciales. Para ejecutivos técnicos, conviene:

1) Identificar problemas candidatos que encajen en VQA, QAOA u otros esquemas híbridos.  
2) Probar prototipos en la nube cuántica con datasets y métricas de negocio.  
3) Iniciar planes de **migración PQC** para 2025-2030 conforme a los calendarios regulatorios y de proveedores.  
4) Seguir de cerca los avances en calidad lógica y cúbits lógicos.

---

## Referencias

[1] Arute et al., “Quantum supremacy using a programmable superconducting processor,” *Nature* (2019). https://www.nature.com/articles/s41586-019-1666-5  
[2] Preskill, “Why I Called It ‘Quantum Supremacy’,” Quanta/essay PDF (2019). https://www.preskill.caltech.edu/pubs/preskill-2019-supremacy.pdf  
[3] Meinsma, “Goodbye to ‘quantum supremacy’?” QuTech Blog (2021). https://blog.qutech.nl/2021/11/25/goodbye-to-quantum-supremacy/  
[4] Zhong et al., “Quantum computational advantage using photons,” *Science* (2020). https://www.science.org/doi/10.1126/science.abe8770  
[5] Madsen et al., “Quantum computational advantage with a programmable photonic processor,” *Nature* (2022). https://www.nature.com/articles/s41586-022-04725-x  
[6] Xanadu, “Beating classical computers with Borealis” (2022). https://www.xanadu.ai/blog/beating-classical-computers-with-Borealis  
[7] Google Quantum AI, “Suppressing quantum errors by scaling a surface code logical qubit,” *Nature* (2023). https://www.nature.com/articles/s41586-022-05434-1  
[8] Google Research Blog, resumen del trabajo de corrección de errores (2023). https://research.google/blog/suppressing-quantum-errors-by-scaling-a-surface-code-logical-qubit/  
[9] IBM, “The era of quantum utility is here” y anuncio de **Condor** 1 121 cúbits (2023). https://www.ibm.com/quantum/blog/quantum-roadmap-2033  
[10] Nature News, “IBM releases first-ever 1000-qubit quantum chip” (2023). https://www.nature.com/articles/d41586-023-03854-1  
[11] Quantum Computing Report, “IBM reveals more details about its quantum error correction roadmap” (2025). https://quantumcomputingreport.com/ibm-reveals-more-details-about-its-quantum-error-correction-roadmap/  
[12] McKay et al., arXiv:2311.05933, benchmark de fidelidad a escala (2023). https://arxiv.org/pdf/2311.05933  
[13] Bravyi et al., “High-threshold and low-overhead fault-tolerant quantum memory with LDPC codes,” *Nature* (2024). https://www.nature.com/articles/s41586-024-07107-7  
[14] Phys. Rev. Research 6, 043249, evaluación de errores en heavy-hex (2024). https://link.aps.org/doi/10.1103/PhysRevResearch.6.043249  
[15] The Verge, “Google reveals quantum computing chip ‘Willow’…” (2024). https://www.theverge.com/2024/12/9/24317382/google-willow-quantum-computing-chip-breakthrough  
[16] Microsoft Azure Blog, “Microsoft unveils Majorana 1…” (2025). https://azure.microsoft.com/en-us/blog/quantum/2025/02/19/microsoft-unveils-majorana-1-the-worlds-first-quantum-processor-powered-by-topological-qubits/  
[17] Microsoft Source, detalle técnico de Majorana 1 (2025). https://news.microsoft.com/source/features/innovation/microsofts-majorana-1-chip-carves-new-path-for-quantum-computing/  
[18] Reuters, cobertura del anuncio de Majorana 1 (2025). https://www.reuters.com/technology/microsoft-creates-chip-it-says-shows-quantum-computers-are-years-not-decades-2025-02-19/  
[19] FT, “Microsoft claims quantum breakthrough…” (2025). https://www.ft.com/content/a60f44f5-81ca-4e66-8193-64c956b09820  
[20] APS Physics, “Experts Weigh in on Microsoft’s Topological Qubit Claim” (2025). https://link.aps.org/doi/10.1103/Physics.18.57  
[21] Business Insider, dudas internas de Amazon sobre Majorana 1 (2025). https://www.businessinsider.com/amazon-exec-casts-doubt-microsoft-quantum-claims-2025-3  
[22] D-Wave, ficha de **Advantage** y **Advantage2** (>5 000 cúbits) (2024-2025). https://www.dwavequantum.com/solutions-and-products/systems/  
[23] NextPlatform, actualización tecnológica de Advantage/Advantage2 (2024). https://www.nextplatform.com/2024/06/18/d-wave-is-still-making-the-case-for-annealing-quantum-computing/  
[24] *Science* (King et al., 2025), “Beyond-classical computation in quantum simulation” en annealing. https://www.science.org/doi/10.1126/science.ado6285  
[25] D-Wave IR, nota “Beyond Classical…” y disponibilidad comercial (2025). https://ir.dwavesys.com/news/news-details/2025/Beyond-Classical-D-Wave-First-to-Demonstrate-Quantum-Supremacy-on-Useful-Real-World-Problem/default.aspx  
[26] The Quantum Insider, ventas on-prem y bookings 2024 (2025). https://thequantuminsider.com/2025/01/10/d-wave-announces-2024-bookings-and-first-on-premise-advantage-system-sale/  
[27] Quantinuum H2, producto y capacidades (all-to-all, MCM, lógica condicional) (2023-2024). https://www.quantinuum.com/products-solutions/quantinuum-systems/system-model-h2  
[28] HPCwire, lanzamiento H2 (2023). https://www.hpcwire.com/2023/05/09/quantinuum-launches-h2-reports-breakthrough-in-work-on-topological-qubits/  
[29] Quantinuum blog, H2-1 actualizado a 56 cúbits (2024). https://www.quantinuum.com/blog/quantinuums-h-series-hits-56-physical-qubits-that-are-all-to-all-connected-and-departs-the-era-of-classical-simulation  
[30] IonQ news, récord 99.99% puerta 2-cúbits (2025). https://ionq.com/news/ionq-achieves-landmark-result-setting-new-world-record-in-quantum-computing  
[31] Investors.com, adquisición de Oxford Ionics y hoja de ruta IonQ (2025). https://www.investors.com/news/technology/quantum-computing-stocks-ionq-oxford-ionics-acqusition/  
[32] Barron’s, adquisiciones de IonQ en 2025 (2025). https://www.barrons.com/articles/ionq-quantum-acquisitions-4e32a5ef  
[33] QuEra **Aquila** 256 cúbits neutral-atom, Braket (2022). https://www.quera.com/aquila  
[34] Wurtz et al., arXiv:2306.11727, descripción técnica de Aquila (2023). https://arxiv.org/abs/2306.11727  
[35] HPCwire, “Atom Computing wins the race to 1000 qubits” (2023). https://www.hpcwire.com/2023/10/24/atom-computing-wins-the-race-to-1000-qubits/  
[36] Atom Computing, whitepaper 2025 y plataforma AC1000 (>1 200 cúbits) (2025). https://atom-computing.com/wp-content/uploads/2025/01/Atom-Computing-Whitepaper-2025.pdf  
[37] Rigetti investors, Ankaa-2 público (2023). https://investors.rigetti.com/news-releases/news-release-details/rigetti-computing-reports-fourth-quarter-and-full-year-2023  
[38] Rigetti, lanzamiento **Ankaa-3** (2024). https://investors.rigetti.com/news-releases/news-release-details/rigetti-computing-launches-84-qubit-ankaatm-3-system-achieves  
[39] Quantum Computing Report, Ankaa-3 en QCS (2025). https://quantumcomputingreport.com/rigetti-computing-launches-84-qubit-ankaa-3-its-quantum-cloud-services-platform-qcs/  
[40] AWS docs, “What is Amazon Braket?” y dispositivos soportados (2025). https://docs.aws.amazon.com/braket/latest/developerguide/what-is-braket.html  
[41] AWS Braket devices, proveedores IonQ, IQM, QuEra, Rigetti (2025). https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html  
[42] Azure Quantum docs, visión general y lenguajes soportados (Q#, Python) (2025). https://learn.microsoft.com/en-us/azure/quantum/  
[43] IBM Quantum docs y guías de Qiskit (2025). https://quantum.cloud.ibm.com/docs/guides  
[44] IBM, “Introduction to Qiskit” (2025). https://quantum.cloud.ibm.com/docs/guides  
[45] Qiskit site, características de transpilación y operadores (2025). https://www.ibm.com/quantum/qiskit  
[46] Qiskit API docs (2025). https://quantum.cloud.ibm.com/docs/api/qiskit  
[47] Qiskit Functions, guía (2025). https://quantum.cloud.ibm.com/docs/guides/functions  
[48] Cirq homepage (Google Quantum AI) (2025). https://quantumai.google/cirq  
[49] Cirq basics tutorial (2025). https://quantumai.google/cirq/start/basics  
[50] Cirq reference (2025). https://quantumai.google/reference/python/cirq  
[51] Cirq ecosystem overview (2025). https://quantumai.google/cirq/build/ecosystem  
[52] Q# overview (Microsoft) (2025). https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview  
[53] Azure Quantum overview (2025). https://learn.microsoft.com/en-us/azure/quantum/overview-azure-quantum  
[54] Microsoft Quantum site, descripción de Q# (2025). https://quantum.microsoft.com/en-us/insights/education/concepts/qsharp  
[55] PennyLane QML portal (Xanadu) (2025). https://pennylane.ai/qml/quantum-machine-learning  
[56] PennyLane codebook VQAs (2025). https://pennylane.ai/codebook/variational-quantum-algorithms  
[57] AWS blog, “Working with PennyLane for variational quantum computing” (2021). https://aws.amazon.com/blogs/quantum-computing/pennylane-quantum-machine-learning/  
[58] AWS blog, Braket y NVIDIA CUDA-Q para híbrido (2024). https://aws.amazon.com/blogs/quantum-computing/advancing-hybrid-quantum-computing-research-with-amazon-braket-and-nvidia-cuda-q/  
[59] NIST, anuncio oficial FIPS 203, 204, 205 (2024). https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards  
[60] NIST CSRC, nota de aprobación FIPS PQC (2024). https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved  
[61] Yin et al., “Satellite-based entanglement distribution over 1200 km,” *Science* (2017). https://www.science.org/doi/10.1126/science.aan3211  
[62] Rev. Mod. Phys., “Micius quantum experiments in space” (2022). https://link.aps.org/doi/10.1103/RevModPhys.94.035001  
[63] IEEE Spectrum, resumen divulgativo enlaces satelitales >1000 km (2020). https://spectrum.ieee.org/entangled-satellite  
[64] Comisión Europea, **EuroQCI** visión general (2025). https://digital-strategy.ec.europa.eu/en/policies/european-quantum-communication-infrastructure-euroqci  
[65] Quantum Flagship, **EuroQCI** contexto (2025). https://qt.eu/ecosystem/quantum-communication-infrastructure  
[66] HADEA, programa CEF Digital para EuroQCI (2025). https://hadea.ec.europa.eu/programmes/connecting-europe-facility/about/quantum-communication-infrastructure-euroqci_en  
[67] ESA y Comisión Europea, red de comunicaciones cuánticas seguras (2025). https://www.esa.int/Applications/Connectivity_and_Secure_Communications/ESA_and_European_Commission_to_build_quantum-secure-space-communications-network  
[68] EuroQCI Irlanda, visión y objetivos (2025). https://irelandqci.ie/euroqci-overview/
