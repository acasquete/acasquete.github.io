
public class OrdenaArray
{
	/// <summary>
	/// Compara pares de elementos adyacentes y si estan desordenados los intercambia
	/// entre si, hasta que est�n todos ordenados.
	/// </summary>
	/// <param name="Array">Array de enteros a ordenar.</param>
	
	public static void Burbuja (int[] Array)
	{
		int i, j, x;

		for(i=0;i<Array.Length-1;i++) 
			for(j=0;j<Array.Length-i-1;j++)
				if(Array[j+1]<Array[j])			
				{
					x=Array[j+1];			
					Array[j+1]=Array[j];
					Array[j]=x; 
				}
	}
	
	/// <summary>
	/// Busca el elemento m�s peque�o del array y lo intercambia con el que 
	/// ocupa la primera posici�n. Luego busca el segundo m�s peque�o y lo intercambia
	/// con el segundo, y as� sucesivamente hasta ordenar todo el array.
	/// </summary>
	/// <param name="Array">Array de enteros a ordenar.</param>

	public static void Seleccion (int[] Array)
	{
		int i, j, x, min;

		for(i=0;i<Array.Length-1;i++)
		{
			for(j=i+1,min=i;j<Array.Length;j++)
				if(Array[j]<Array[min])	min=j;				

			x=Array[i];				
			Array[i]=Array[min];		
			Array[min]=x;			
		}
	}

	/// <summary>
	/// Toma cada elemento del array y lo compara con los que se encuentran en
	/// posiciones anteriores. Si el elemento con el que se est� comparando es mayor
	/// que el elemento a ordenar se intercambia y se recorre hacia la posici�n anterior.
	/// </summary>
	/// <param name="Array">Array de enteros a ordenar.</param>

	public static void Insercion (int[] Array) 
	{
		int i, j, x;

		for (i=1; i < Array.Length; i++) 
		{
			x = Array[i];
			j    = i-1;
			while ( j>=0 && Array[j]>x ) 
			{
				Array[j+1] = Array[j];
				j--;
			}
			Array[j+1]=x;
		}
	}

	/// <summary>
	/// Compara a cada elemento con el que est� a K lugares a su izquierda. Este salto es
	/// constante, y su valor inicial es N/2 (N=Array.Length). Se dan pasadas hasta que
	/// no se intercambie ning�n elemento. Entonces K se reduce a la mitad, y se vuelven
	/// a dar pasadas hasta que no se intercambie ning�n elemento, y as� sucesivamente
	/// hasta que K=1.
	/// </summary>
	/// <param name="Array">Array de enteros a ordenar.</param>

	public static void Shell (int[] Array) 
	{
		int i, j, B, h = 1;
			
		while ( h * 3 + 1 < Array.Length)
		{
			h = 3 * h + 1;
		}				
		while (h > 0)
		{
			for (i = h - 1; i < Array.Length; i++)
			{		
				B = Array[i];
				
				for (j = i; (j >= h) && (Array[j - h] > B); j -= h)
				{
					Array[j] = Array[j - h];
				}			
				Array[j] = B;
			}
			h = h / 3;
		}
	}

	/// <summary>
	/// Subdivide el array en arrays m�s peque�os, y ordena �stos. Para hacer esta
	/// divisi�n, se toma un valor del array como pivote, y se mueven todos los 
	/// elementos menores que este pivote a su izquierda, y los mayores a su derecha. 
	/// A continuaci�n se aplica el mismo m�todo a cada una de las dos partes en las
	/// que queda dividido el array.	
	/// </summary>
	/// <param name="Array">Array de enteros a ordenar.</param>
																																																																																								
	public static void QuickSort (int[] Array)
	{
		QuickSort(Array, 0, Array.Length-1);
	}

	public static void QuickSort (int[] Array, int lo0, int hi0)
	{
		int lo = lo0;
		int hi = hi0;
		int T, pivot;
    
		if (lo >= hi) return;

		if (lo == hi - 1)
		{				
			if (Array[lo] > Array[hi])
			{
				T = Array[lo];
				Array[lo] = Array[hi];
				Array[hi] = T;
			}
			return;
		}				
		
		pivot = Array[(lo + hi) / 2];
		Array[(lo + hi) / 2] = Array[hi];
		Array[hi] = pivot;

		while (lo < hi)
		{			
			while (Array[lo] <= pivot && lo < hi)	  
				lo++;
			
			while (pivot <= Array[hi] && lo < hi) 
				hi--;
			
			if (lo < hi)
			{
				T = Array[lo];
				Array[lo] = Array[hi];
				Array[hi] = T;
			}
		}
		Array[hi0] = Array[hi];
		Array[hi] = pivot;	
	
		QuickSort (Array, lo0, lo - 1);
		QuickSort (Array, hi + 1, hi0);
	}

}
