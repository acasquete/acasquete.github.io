---
description: "Suavizar expresiones artificiales conservando la voz del autor"
mode: "edit"
---

Objetivo

Céntrate únicamente en mejorar expresiones que suenen muy artificiales, forzadas o poco naturales en entradas del blog, manteniendo la voz y el estilo del autor.

Instrucciones (uso en el editor o Chat)

- Alcance: modifica solo frases o expresiones que resulten claramente artificiales o poco naturales. Evita reescribir párrafos completos salvo que sea imprescindible para corregir una frase concreta.
- Mantén la voz, tono y estructura del autor. No introduzcas ideas nuevas ni cambies el argumento.
- No modifiques citas, títulos, referencias bibliográficas ni front matter (metadatos al principio del archivo).
- Corrige errores tipográficos, ortográficos y de acentuación cuando los detectes (por ejemplo, "codigo" → "código").
- Conserva el formato Markdown (listas, blockquotes, encabezados, etc.).
- Evita cambios de estilo global (p. ej. no convertir un texto informal en uno formal).
- Unifica el tratamiento del lector, utilizado usted en lugar de tú. Utilizar “Si es la primera vez que te enfrentas…” → “Si es la primera vez que usted se enfrenta…”
- Al terminar, incluye un breve comentario (1–2 líneas) al final del archivo indicando las correcciones realizadas, por ejemplo: "Corregidas 3 expresiones: líneas 12–16".

Cómo usarlo en VS Code

- Si quieres editar la selección actual, ejecuta este prompt con la variable ${selection}.
- Para editar un archivo completo, abre el archivo y ejecuta el prompt; el modo `edit` aplicará cambios directamente al archivo.

Variables útiles en VS Code

- ${workspaceFolder}, ${workspaceFolderBasename}
- ${selection}, ${selectedText}
- ${file}, ${fileBasename}, ${fileDirname}, ${fileBasenameNoExtension}
- ${input:variableName} (para solicitar valores desde la interfaz)

Ejemplos

- Antes: "la IA puede ayudar a crear codigo repetitivo"
- Después: "la IA puede ayudar a crear código repetitivo"

- Antes: "los estudiantes confían en la IA para redactar ensayos"
- Después: "algunos estudiantes recurren a la IA para redactar ensayos"

Notas y límites

- No generes contenido nuevo que amplíe el argumento del autor.
- Si detectas una frase ambigua que requiere contexto adicional, deja un comentario en el archivo en lugar de adivinar (ej.: "REVISAR: posible ambigüedad sobre X").

Salida esperada

- El archivo modificado en el workspace con cambios mínimos y conservando la voz del autor.
- Una línea al final del archivo con el resumen de correcciones.

Referencia rápida

- Variables útiles: ${selection}, ${file}, ${fileBasename}
- Modo recomendado: edit

Gracias.
