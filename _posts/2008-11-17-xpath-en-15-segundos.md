---
title: XPath en 15 segundos
tags: []
---
Sin comentarios…

XPathNavigator xNav; XPathNodeIterator xIter; xNav = new XPathDocument(@”MyLibrary.xml”).CreateNavigator(); xIter = xNav.Select(“library/book/author\[contains(.,’Süskind’)\]”); while (xIter.MoveNext()){ Console.WriteLine(“{0}”, xIter.Current.Value); }

