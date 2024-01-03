---
title: Integrando FxCop 10 en Visual Studio
tags: [programming]
reviewed: true
---
Si eres de los que utilizas la edición _Professional_ de **Visual Studio 2010** y además programas en VB.NET, tienes muy pocas opciones si quieres añadir análisis estático de código a tus proyectos, yo diría que la única opción gratuita disponible es **FxCop**.

[FxCop 10](http://www.microsoft.com/downloads/details.aspx?FamilyID=917023F6-D5B7-41BB-BBC0-411A7D66CF3C&displaylang=en&displaylang=en) es la última versión que ha publicado Microsoft y está incluida en el [Windows SDK 7.1 para Windows 7](http://www.microsoft.com/downloads/details.aspx?displaylang=en&FamilyID=6b6c21d2-2006-4afa-9702-529fa782d63b). Esta versión funciona con el CLR v4 e incluye, respecto a versiones anteriores, el nuevo grupo de [reglas de transparencia en seguridad](http://msdn.microsoft.com/es-es/library/ee191569.aspx).

**FxCop** dispone de dos aplicaciones: una con interfaz gráfica (_FxCop.exe_) y otra sin ella (_FxCopCmd.exe_). Hoy vamos a centrarnos exclusivamente en cómo integrar **FxCop** con _Visual Studio_ utilizando la segunda opción, la aplicación por línea de comandos.

Después de instalar el _SDK de Windows_, podremos encontrar el instalador de **FxCop 10** en esta ruta:

**%ProgramFiles%Microsoft SDKsWindowsv7.1BinFXCopFxCopSetup.exe**

Una vez lo tengamos instalado, podremos integrarlo con _Visual Studio_ de dos formas distintas: como una herramienta externa o personalizando el [proceso de compilación](http://msdn.microsoft.com/es-es/library/e2s2128d(v=VS.80).aspx) del proyecto mediante el evento _Post-Build_. Vamos a ver a continuación las diferencias entre los dos métodos.

Herramienta externa
---

Para añadir **FxCop** como una herramienta externa en VS debemos acceder a la opción **Herramientas externas** del menú **Herramientas**, añadir un nuevo elemento con la siguiente información: **Title**: Microsoft FxCop 10.0 **Command**: %programfiles%Microsoft Fxcop 10.0FxCopCmd.exe **Arguments**: /c /f:$(TargetPath) /d:$(BinDir) /r:”%programfiles%Microsoft FxCop 10.0Rules” **Initial Directory**: %programfiles%Microsoft FxCop 10.0 y marcar la casilla **Usar la ventana de resultados** (_Use Output Window_). Al aceptar, tendremos en el menú **Herramientas** la nueva opción **Microsoft FxCop 10.0** que podremos utilizar para analizar nuestro ensamblado después de compilar el proyecto. El resultado del análisis de **FxCop** se mostrará en el panel **Resultados** de forma parecida a como aparece en la siguiente imagen.

Para automatizar este proceso he creado un _script_ que registra **FxCop** como herramienta externa. El _script_ modifica la clave **\[HKEY\_CURRENT\_USERSoftwareMicrosoftVisualStudio10.0External Tools\]** del registro del sistema. Hay que tener en cuenta que sólo funciona para VS2010 y para el usuario actual, pero se puede adaptar fácilmente para versiones anteriores (cambiando la versión a 9.0) y para todos los usuarios (cambiando la clave a **HKEY\_LOCAL\_MACHINE**).

Para completar la integración, podemos [personalizar el menú contextual](http://msdn.microsoft.com/es-es/library/ms241445(VS.80).aspx) del proyecto añadiendo un comando que ejecute una herramienta externa, en este caso, FxCop. De esta forma, podremos lanzar el análisis de código directamente desde el explorador de la solución.

# Evento de compilación

Otra forma de integrar **FxCop** es especificando un evento de generación. Simplemente tenemos que añadir la siguiente línea de comando en el evento _Post-Build_ de nuestro proyecto:

```bash
“%programfiles%Microsoft FxCop 10.0FxCopCmd.exe” /c /f:”$(TargetPath)” /r:”%programfiles%Microsoft FxCop 10.0Rules”
```

Al finalizar la compilación con éxito aparecerá en el panel **Lista de errores** todos los avisos del análisis de código generados por **FxCop**.

En muchas ocasiones **FxCop** mostrará el mensaje _Location not stored in Pdb_ como nombre de fichero, haciendo imposible enlazar el aviso con en el código fuente. Este mensaje normalmente indica que el fichero PDB no está presente en el directorio del ensamblado, pero también hay que tener en cuenta que los compiladores de C# y VB.NET sólo generan información para métodos y propiedades, así que **FxCop** no podrá localizar el código fuente para atributos, tipos o espacios de nombres.

Personalmente prefiero la integración mediante el evento _Post-Build_ ya que me parece mucho más confusa la ventana de resultados que la de errores, pero el inconveniente es que el análisis de código se ejecuta en cada compilación, aumentando el tiempo total de generación. Una solución a este problema es realizar el análisis de código sólo en configuración _Release_ (o en una nueva configuración), y añadir la condición al evento de la siguiente forma:

```bash
if $(ConfigurationName) == Release "%programfiles%Microsoft FxCop 10.0FxCopCmd.exe" /c /f:"$(TargetPath)" /r:"%programfiles%Microsoft FxCop 10.0Rules"
```

Hasta aquí esta breve guía para utilizar análisis de código con **FxCop** en nuestros proyectos, característica que debería estar implantada en todos los equipos de desarrollo.

**Descarga Script:**
[FxCop_VS2010ExternalTool.vbs.zip](/files/FxCop_VS2010ExternalTool.vbs.zip)

