---
title: Primeros pasos con Silverlight, algoritmo MiniMax y 3 en raya
tags: [algorithms]
reviewed: true
---
Organizando los directorios donde guardo todos mis proyectos, he encontrado dos juegos que hice hace ya catorce años: el 3 en raya y _Dernier_. Lamentablemente [no puedo ver el código fuente](http://support.microsoft.com/default.aspx/kb/58956/es) de ninguno de los dos porque están compilados con _QuickBASIC_. Recuerdo que programé estos dos juegos a base de un sinfín de _ifs_ anidados, ya que por aquel entonces no tenía ni idea de lo que era el algoritmo [MiniMax](http://es.wikipedia.org/wiki/Minimax). El resultado me convenció durante un tiempo ya que, a pesar de todo, eran juegos imbatibles, pero enseguida entendí que utilizando este sistema de programación nunca podría hacer un juego más complejo, como las damas o el ajedrez.

Ahora me he propuesto realizar, a modo de primera práctica con _Silverlight_, una versión renovada de estos dos juegos. Aprovechando estos días de inicio de año en los que estoy de vacaciones y tomándome un respiro en los estudios del [MCTS](/tag/mcts), he comenzado la implementación del «apasionante» 3 en raya, en esta ocasión haciendo uso del algoritmo _MiniMax_ con dos optimizaciones ([poda alpha-beta](http://en.wikipedia.org/wiki/Alpha-beta_pruning) y límite de profundidad).

Esta primera versión que he subido no incluye ningún comentario en el código, si dispongo de más tiempo comentaré las partes del código más interesantes, e implementaré las otras variantes de _MiniMax_ para poder comparar las mejoras de rendimiento que se obtienen. El código fuente de la solución se puede descargar en el enlace que pongo al final de esta entrada.

El proyecto tiene dos clases principales (_Board_ y _IAGame_). La clase _Board_ contiene los métodos para saber si una partida ha finalizado (_GameEnded_) y tiene ganador (_GetWinner_) o está empatada (_IsTie_), y para saber los posibles movimientos a partir de una situación de tablero dada (_GetAllowedMovements_). La clase _IAGame \*contiene la implementación del algortimo _MiniMax_ con las distintas optimizaciones.

Para los interesados exclusivamente en el código del algoritmo _MiniMax_, aquí dejo mi implementación del método recursivo en C#.

```csharp
public Movement MiniMaxBasic(Board board, int player) 
{ 
    if (board.GetWinner() != 0 || board.IsTie()) 
    { 
        Movement mov = new Movement(); mov.Value = board.GetWinner();

        return mov;
    }
    else
    {
        int[] successors = board.GetAllowedMovements(true);
        Movement best = null;
    
        foreach (int successor in successors)
        {
            Board successorBoard = (Board)board.Clone();
            successorBoard.SetMove(successor, player);
            Movement tmp = MiniMaxBasic(successorBoard, -player);
    
            if (best == null || (player == -1 && tmp.Value < best.Value) || (player == 1 && tmp.Value > best.Value))
            {
                tmp.Position = successor;
                best = tmp;
            }
        }
        return best;
    } 
}
```

Este método —como se puede ver— no tiene ninguna optimización en la generación del árbol de búsqueda, en el código completo están las otras dos implementaciones del algoritmo con poda alpha-beta y profundidad de búsqueda.

**Actualización (11/Nov/09):** Para aquellos que no tengáis Blend, he añadido un nuevo enlace para descargar el código fuente de un ejemplo de **aplicación de consola**. Este código permite jugar una partida contra el ordenador utilizando 3 variantes del algoritmo _MiniMax_.

Descargas
---
[ConsoleTicTacToe.zip](/files/ConsoleTicTacToe.zip)  
[SilverlightTicTacToe.zip](/files/SilverlightTicTacToe.zip)

