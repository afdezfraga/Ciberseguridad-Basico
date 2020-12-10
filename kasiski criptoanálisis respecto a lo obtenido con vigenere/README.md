##Instrucciones de uso del programa:


Debes indicar un fichero de texto a descifrar, y opcionalmente el argumento -i si quieres que el programa se ejecute en modo interactivo:
python kasiski.py texto_cifrado.txt [-i]


En modo estándar el programa muestra la clave que le parece más probable directamente. 


En modo interactivo el programa nos permite tomar decisiones sobre la obtención de la clave en base a información que nos va mostrando. Aquí veremos las instrucciones del modo interactivo:

Cuando se nos diga “Input the key length that will be used:” introduciremos la longitud de clave teniendo en cuenta las más probables que el programa nos indicará por pantalla.
Al mensaje “Introduce action 'c' to continue, 'e' to exit” introduciremos c si queremos continuar el descifrado o e si por algún motivo queremos detenerlo.
Cuando aparezca “Introduce sub-text to analyze between 1 to n”, dónde n será la longitud de clave que hemos elegido, introducimos un número que será el subtexto que vamos a analizar de siguiente.
Cuando nos pida “Character on plaintext:” y “Character on cyphertext:” introduciremos en base a la proporción de cada caracter en el texto cifrado que aparecen en pantalla qué caracter en el texto plano debería corresponderse con el cifrado. En base a lo que introduzcamos el programa nos indicará en qué caracteres se convierten los más comunes.
Ahora el programa nos pregunta “Does this solution fit?(y/n):” a lo cual respondemos y en caso de que la solución tenga sentido, o n si queremos repetir el proceso. Si respondemos y se rellena un espacio de la clave y continuamos.
