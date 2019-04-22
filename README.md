# Proyecto Nro.1 - XML Parse.
La comisión de trabajo de grado de la escuela de ingenieria y ciencias aplicadas desea que usted cree una aplicación para validar la información almacenada en su base de datos acerca de los trabajos de grado presentados mediante un archivo XML. El formato de los datos de este archivo es el siguiente:

[Imgur](https://i.imgur.com/I1ToNri.png)

## Debe tener en cuenta las siguientes caracteristicas del formato:
- El titulo permite todo tipo de caracteres excepto < >. Puede tener mas de una linea.
- La primera letra tiene que ser siempre mayuscula.
- Las modalidades siempre seran investigacion, pasantias o cursos especiales de grado.
La nota numerica puede ir del 0 al 10 sin decimales.
- La nota no numerica será una de las palabra (Publicacion, aprobado o reprobado). En un trabajo de grado puede aparecer un tipo de nota o ambas, en orden no numerico y numerico.
- Las etiquetas XML son de dos tipos, apertura y cierre. Cada etiqueta tiene una palabra entre < > y las de cierre contienen / .
- Las etiquetas claves son las de el formato. Las cuales serán exclusivamente en minuscula.
- Las palabras solo contienen letras y el carracter _ .
- Las fechas deben tener 2 numeros para el dia, mes y año, y deben estar separadas por el caracter / .
- Construya la gramatica EBNF para el respectivo proyecto y una aplicacion para el leguaje python(2.7) que valide el archivo XML.

### Observaciones.  
- Su aplicación debe solicitar el nombre del archivo XML, para cualquier archivo.
- Las salidas posibles son: ***`Archivo Ok`***, ***`Error. Registro #n, linea m`*** o ***`Archivo no encontrado'`***.

Debe entregar su aplicacion con codigo fuente y un archivo de prueba
