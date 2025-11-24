---
title: El mito del ataque cuántico
tags: [personal, quantum]
reviewed: true
home: true
ai: true
header_fullview: elliptic-curve-bitcoin-chalkboard-side-view.jpg
---
A principios de año apareció en *Voz Pópuli* un artículo titulado [*“En solo 320 segundos hackean a Bitcoin con el primer ataque cuántico de la historia”*](https://www.vozpopuli.com/economia/solo-320-segundos-hackean-bitcoin-con-el-primer-ataque-cuantico-historia-sd.html). El artículo generó un notable eco mediático y el propio medio finalmente modificó el titular por uno más prudente (aunque igualmente impreciso): *“Un experto alerta de un posible intento de hackeo a Bitcoin con computación cuántica”*.

El problema no es solo el alarmismo. Es que la premisa fundamental del artículo es falsa: **no existe ningún ataque cuántico contra Bitcoin con un ordenador de 18 qubits, ni en 320 segundos ni de ningún tipo**.

Esta anécdota, sin embargo, sirve para repasar cómo funcionan distintos algoritmos de clave pública, explicar con claridad la criptografía que utiliza Bitcoin y entender qué requeriría realmente la computación cuántica para convertirse en una amenaza.

Antes de continuar, conviene recordar algo esencial: la computación cuántica no es magia ni un atajo inmediato para romper cifrados. Su estado actual está limitado por ruido, escalabilidad, fidelidad y la necesidad de corrección de errores masiva. Comprender estas limitaciones técnicas es clave para evaluar cualquier supuesto “ataque cuántico”.

# RSA y el problema de la factorización

RSA, uno de los estándares clásicos de cifrado de clave pública, se basa en una idea muy sencilla: multiplicar dos números primos grandes es fácil, pero averiguar qué dos primos se usaron —es decir, factorizar el número resultante— es extremadamente difícil. Esa asimetría es la base de su seguridad y explica por qué un atacante debe invertir enormes recursos computacionales para romper una clave RSA convencional.

La construcción de RSA sigue siempre el mismo proceso: se escogen dos primos grandes (p y q), se multiplica n = p × q y se deriva un exponente público e junto con un exponente privado d que es el inverso modular de e respecto a (p-1)(q-1). El par (e, n) forma la clave pública, mientras que (d, n) constituye la clave privada. Sobre este mecanismo se construyen tanto el cifrado como la firma: el mensaje se eleva a una potencia módulo n, con la clave pública para cifrar y con la clave privada para firmar; el proceso inverso se hace con la clave complementaria.

Las claves RSA modernas tienen normalmente **2048 bits**, una longitud que garantiza que la factorización clásica resulte impracticable. Pero en 1994 Peter Shor demostró que un ordenador cuántico suficientemente grande podría factorizar estos números de forma eficiente mediante su algoritmo cuántico, lo que rompería RSA de forma directa.

El problema —y es la razón por la que RSA sigue siendo seguro hoy— es que ese “ordenador cuántico suficientemente grande” está muy lejos de la tecnología actual: sería necesario disponer de **miles de qubits lógicos**, lo que se traduce en **millones de qubits físicos** una vez añadida la corrección de errores cuánticos. No existe hoy ningún sistema que se acerque mínimamente a esa escala.

En entornos reales como TLS (y anteriormente SSL), RSA ha desempeñado históricamente dos funciones: por un lado, autenticar al servidor mediante las firmas empleadas en los certificados, algo que sigue siendo habitual; por otro, actuar como mecanismo de intercambio de claves, una función que hoy se ha abandonado porque no ofrece *Forward Secrecy* (garantizar que, aunque la clave privada del servidor se vea comprometida en el futuro, las sesiones cifradas del pasado sigan siendo imposibles de descifrar). En las versiones modernas del protocolo (TLS 1.3), el intercambio de claves se realiza mediante ECDHE —basado en curvas elípticas—, mientras que RSA queda relegado a la autenticación o sustituido directamente por firmas ECDSA o, de forma aún limitada, por algoritmos postcuánticos en fase de adopción.

Por todo ello, RSA sigue siendo relevante, pero su futuro depende de la evolución tanto de la computación cuántica como de la transición hacia esquemas criptográficos postcuánticos más resistentes.

# Criptografía de curvas elípticas y por qué Bitcoin no usa RSA

A diferencia de RSA, Bitcoin no se apoya en la factorización de números grandes, sino en la criptografía de curvas elípticas, concretamente en el esquema **ECDSA** sobre la curva *secp256k1*. Este enfoque permite ofrecer un nivel de seguridad muy alto con claves mucho más pequeñas.

La curva utilizada por Bitcoin se define por la ecuación:

\[
y^2 = x^3 + 7 \mod p
\]

donde \(p\) es un número primo de 256 bits. En este sistema:

- La **clave privada** es simplemente un número entero de 256 bits.
- La **clave pública** es un punto en la curva, obtenido mediante la operación de multiplicación escalar \(P = k \cdot G\), donde \(G\) es un punto base bien conocido.
- A partir de la clave pública se genera la **dirección Bitcoin** mediante funciones hash.

La seguridad se basa en el **problema del logaritmo discreto en curvas elípticas (ECDLP)**: dado un punto \(P = k \cdot G\), es computacionalmente inviable recuperar el valor de \(k\). Esta operación es fácil en una dirección (multiplicar), pero extraordinariamente difícil en la otra (invertir), del mismo modo que ocurre con la factorización en RSA.

Aunque una clave de Bitcoin tiene solo **256 bits**, su nivel de seguridad es equivalente al de una clave RSA de más de **3000 bits**, debido a la mayor complejidad matemática del ECDLP. Por eso Bitcoin no necesita claves largas ni grandes tamaños de módulo: la curva elíptica proporciona una resistencia criptográfica muy superior por bit.

En este contexto, el famoso algoritmo de Shor también podría, en teoría, resolver el logaritmo discreto, igual que factoriza números para romper RSA. Sin embargo, aplicarlo a curvas elípticas requiere aún más recursos: para atacar claves de 256 bits serían necesarios **centenares de qubits lógicos** y, por extensión, **millones de qubits físicos** cuando se incorpora la corrección de errores cuánticos. Nada de esto es posible con los dispositivos cuánticos actuales, que siguen limitados por ruido elevado, profundidades de circuito muy bajas y tamaños muy reducidos.

Por esta razón, la criptografía de curvas elípticas sigue siendo completamente segura frente a la tecnología cuántica disponible hoy en día y constituye la base robusta sobre la que se construyen las firmas digitales de Bitcoin.

# Una verdadera amenaza cuántica

Para que un ataque cuántico contra Bitcoin o RSA fuera realmente viable, no bastaría con un procesador de unas pocas decenas o incluso cientos de qubits físicos. Sería necesario un tipo de máquina cuántica radicalmente más avanzada que las actuales. En concreto, un ataque práctico requeriría:

- **Qubits lógicos y corrección de errores completa**. La criptografía moderna no cae con qubits físicos: hace falta ejecutar el algoritmo de Shor de forma tolerante a fallos. Esto implica miles de qubits lógicos, cada uno respaldado por miles de qubits físicos mediante códigos de corrección de errores.
- **Profundidad de circuito muy elevada**. Shor, aplicado a claves reales de 2048 o 3072 bits (RSA) o a claves de 256 bits en curvas elípticas (Bitcoin), exige millones de puertas cuánticas consecutivas. Los dispositivos actuales apenas soportan unas decenas.
- **Tasas de error ultrabajas**. Incluso un pequeño error acumulado destruye el estado cuántico y hace fracasar la ejecución. Se necesitarían tasas de error por puerta y por qubit varios órdenes de magnitud mejores que las actuales.
- **Quantum RAM (QRAM)**. Para manejar eficientemente estructuras de datos a la escala necesaria en ataques criptográficos. La QRAM no es estrictamente necesaria para ejecutar Shor, pero sería imprescindible para escalar muchos ataques criptográficos cuánticos más avanzados y hoy sigue siendo solo un concepto teórico.
- **Estabilidad durante tiempos largos**. Ejecutar Shor sobre claves reales demandaría minutos u horas de operación coherente, mientras que los sistemas actuales mantienen la coherencia durante milisegundos o microsegundos.

Solo la combinación de estos elementos permitiría, en la práctica, romper RSA o ECDSA. Y ninguno de ellos está disponible hoy. La distancia tecnológica entre los ordenadores cuánticos actuales y una máquina capaz de atacar criptografía real sigue siendo enorme.

# Conclusión

El supuesto “ataque cuántico a Bitcoin en 320 segundos” no solo era falso, sino técnicamente imposible con el hardware cuántico disponible hoy. Tanto RSA como las curvas elípticas que utiliza Bitcoin se basan en problemas matemáticos cuya inversión sigue estando muy lejos del alcance de los ordenadores cuánticos actuales. El algoritmo de Shor demuestra que, en teoría, el futuro cuántico podrá romper ambos sistemas, pero ese escenario exige miles de qubits lógicos y millones de qubits físicos, una escala que ninguna plataforma cuántica moderna puede ofrecer.

Mientras tanto, Bitcoin continúa protegido por ECDSA sobre *secp256k1*, una estructura criptográfica altamente resistente y con niveles de seguridad equivalentes a claves RSA mucho más largas. La amenaza cuántica llegará si la tecnología consigue escalar de forma significativa, algo que hoy está muy lejos de estar resuelto. Será un proceso gradual que la comunidad criptográfica, las infraestructuras de Internet y las cadenas de bloques tendrán que afrontar mediante algoritmos postcuánticos estandarizados.

# Referencias

Shor, P. W. (1994). *Algorithms for quantum computation: Discrete logarithms and factoring*. IEEE FOCS. [https://doi.org/10.1109/SFCS.1994.365700](https://doi.org/10.1109/SFCS.1994.365700)

Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System*. [https://bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf)

Hankerson, D., Menezes, A., Vanstone, S. (2004). *Guide to Elliptic Curve Cryptography*. Springer. [https://link.springer.com/book/10.1007/b97644](https://link.springer.com/book/10.1007/b97644)

NIST (2022). *Post-Quantum Cryptography Standardization Project*.  [https://csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)

Bernstein, D. J., Lange, T. (2017). *Post-quantum cryptography*. *Nature* 549, 188–194. [https://doi.org/10.1038/nature23461](https://doi.org/10.1038/nature23461)

Google Quantum AI (2019). *Quantum supremacy using a programmable superconducting processor*. *Nature* 574, 505–510. [https://www.nature.com/articles/s41586-019-1666-5](https://www.nature.com/articles/s41586-019-1666-5)

Google Quantum AI (2024). Información técnica del procesador Willow (105 qubits). [https://quantumai.google](https://quantumai.google)

IETF (2018). *RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3*. [https://datatracker.ietf.org/doc/rfc8446/](https://datatracker.ietf.org/doc/rfc8446/)

Bernstein, D. J., Buchmann, J., Dahmen, E. (2009). *Post-Quantum Cryptography*. Springer. [https://link.springer.com/book/10.1007/978-3-540-88702-7](https://link.springer.com/book/10.1007/978-3-540-88702-7)

Menezes, A., Van Oorschot, P., Vanstone, S. (1996). *Handbook of Applied Cryptography*. CRC Press. [https://cacr.uwaterloo.ca/hac/](https://cacr.uwaterloo.ca/hac/)
