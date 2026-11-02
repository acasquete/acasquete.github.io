---
title: "Demo de lectura adaptativa"
description: "Artículo de prueba para la lectura adaptativa: párrafos, listas, código, imágenes, enlaces y citas."
date: 2026-11-02
tags: [ai]
---

Cuando escribo una nota técnica suelo pensar en un lector que ya conoce el contexto, pero casi nunca es el único que llega hasta ella. Algunas personas buscan una idea general en cinco minutos y otras quieren entender cada decisión de diseño con todos sus matices.

## Un mismo texto, varios ritmos

Una cola de mensajes permite que dos sistemas se comuniquen sin estar disponibles al mismo tiempo: el productor deja el mensaje y el consumidor lo recoge cuando puede, de modo que un fallo temporal de uno de los dos no tumba al otro. Esta idea se explica con detalle en la [documentación de Azure Service Bus](https://learn.microsoft.com/azure/service-bus-messaging/) y aparece una y otra vez en arquitecturas modernas.

![Panorámica de Barcelona](/img/rio1.jpg)

En una prueba con 250 mensajes por segundo, el consumidor tardó 3,5 segundos de media en vaciar la cola tras una caída de diez minutos, y nadie perdió un solo pedido durante todo ese tiempo, que era justo lo que queríamos demostrar.

Para comprobarlo basta con ejecutar el siguiente fragmento, que publica un mensaje y espera a que alguien lo procese:

```csharp
await sender.SendMessageAsync(new ServiceBusMessage("hola"));
```

Lo que más me ha costado aprender no es la herramienta, sino a vivir con ciertas consecuencias:

- Los mensajes pueden llegar duplicados, así que el consumidor debe ser idempotente y tolerar repeticiones sin efectos secundarios.
- El orden de llegada no está garantizado salvo que se configuren sesiones, y eso tiene un coste de rendimiento que conviene medir antes de decidir.
- Una cola sin monitorización acaba llenándose en silencio hasta que alguien nota que los pedidos tardan días en procesarse.

Como decía un compañero de equipo, "lo difícil de los sistemas asíncronos no es hacerlos funcionar, sino entender por qué a veces no funcionan". Desde entonces miro con más cariño las métricas de la cola que cualquier otro panel.

En resumen, usa `ServiceBusClient` cuando necesites desacoplar dos sistemas y acepta que la complejidad no desaparece, solo cambia de sitio. Si quieres profundizar, la nota sobre [colas y reintentos](https://acasquetenotes.com/colas-y-reintentos) amplía este razonamiento.
