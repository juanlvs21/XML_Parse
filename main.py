import xml.etree.ElementTree as ET
import time
import os

# validTags es un arreglo de las etiquetas permitidas y en el orden exacto
validTags = ["<tg>","<autor>","</autor>","<fecha_pre>","</fecha_pre>","<titulo_tg>","</titulo_tg>","<modalidad>","</modalidad>","<tutor>","</tutor>","<nota>","</nota>","</tg>"]

countLine = 0
countRegister = 0
countTag = 0
openRegister = False
closeRegister = True
error = False
nameFile = ""
register = ""
listRegister = []

# Funcion para verficar cada una de las etiquetas de nuestro archivo XML
def checkTags(xmlFile):
    global countLine
    global countRegister
    global countTag
    global openRegister 
    global closeRegister
    global error 
    global nameFile 
    global register 
    global listRegister 

    openTag = False
    
    # Se recorre el archivo linea por linea
    for line in xmlFile.readlines():
        countLine = countLine + 1

        # Verifica en cada linea que no exista ningun error
        if error == False: 
            # Si una etiqueta ya se encuentra abierta resulta un error ya que el caracter "<" no puede encontrarse dentro del texto
            if openTag == True:
                errorMsg(countRegister,countLine-1)

            # Compara si es la etiqueta raiz <tg>
            if line.strip('\n') == validTags[0]:
                countLine = 1
                register = register + line

                # closeRegister sirve para llevar el control del cierre de la etiqueta raiz <tg>
                if closeRegister == True:
                    countRegister = countRegister + 1
                    openRegister = True
                    closeRegister = False
                else:
                    # Habra error cuando exista un <tg> sin un </tg> de cierre previo
                    errorMsg(countRegister,countLine)
            else:
                # En caso que no sea la etiqueta raiz <tg>
                # Lleva el control de si el registro esta abierto
                if openRegister == True:
                    tag = ""

                    # charCloseTag sirve para reflejar cuando la etiqueta tenga / de cierre
                    charCloseTag = False

                    # Se recorre cada linea caracter por caracter
                    for letter in line:
                        # Vuelve a verificar que no exista ningun error
                        if error == False:
                            register = register + letter

                            # Si letter es igual a '<' significa que esta abierndo una etiqueta
                            if letter == '<' and openTag == False:
                                # openTag permite ir agregando los caracteres siguiente luego de abrir la etiqueta
                                openTag = True
                                charCloseTag = False
                                tag = letter
                            else:
                                # Si la etiqueta esta abierta se concatenan los caracteres
                                if openTag == True:
                                    tag = tag + letter

                                    # Si letter es igual a '/' charCloseTag se vuelve True para indicar que es una etiqueta de cierre
                                    if letter == "/":
                                        charCloseTag = True

                                    if letter == ">":
                                        # Si letter es igual a '>' quiere decir que ya se cierra la etiqueta (openTag es igual a False)
                                        openTag = False
                                        # Cada vez que se cierra una etiqueta se aumenta countTag para ir a la par con las etiquetas en validTags
                                        countTag = countTag + 1
                                        # Se verifica si la etiqueta actual concuerda con la correspondiente en validTags
                                        if tag == validTags[countTag]:
                                            # Si es la ultima etiqueta (cierre de la raiz </tg>) se marca el registro como cerrado
                                            if tag == validTags[13]:
                                                closeRegister = True
                                                openRegister = False
                                                countTag = 0
                                                # listRegister es un arreglo que contiene los registros separados para su posterior validacion del texto dentro de las etiquetas
                                                listRegister.append(register)
                                                register = ""
                                            tag = ""
                                        else:
                                            #En caso de que la etiqueta no sea la correspondiente se marca un error
                                            if charCloseTag == False:
                                                countLine = countLine - 1
                                            countTag = countTag + 1
                                            errorMsg(countRegister,countLine)
                else:
                    # Si la etiqueta actual no es la de inicio ni el registro esta abierto se marca un error
                    countRegister = countRegister + 1
                    countLine = 1
                    errorMsg(countRegister,countLine)

# Funcion para verficar el texto dentro de cada etiqueta XML
def checkText():
    global countLine
    global error
    global countRegister
    countRegister = 0
    
    # Se recorre el arreglo de registros que se lleno el la validacion de etiquetas
    for reg in listRegister:
        countRegister = countRegister + 1
        countLine = 1

        # Se crea un DOM para cada registro con xml.etree para obtener el texto que contiene cada etiqueta
        registerDOM = ET.fromstring(reg)

        # Se recorre el DOM creado por xml.etree
        for registerTag in registerDOM:
            countLine = countLine + 1
            # arrayTitle contiene las lineas totales del titulo
            arrayTitle = []

            # Ya que la etiqueta "titulo_tg" puede tener mas de una linea se debe llevar el control de ello
            if registerTag.tag == "titulo_tg":
                # Se llena arrayTitle separandose el texto de la etiqueta mediante el salto de linea "\n"
                arrayTitle = registerTag.text.split("\n")
                # Si tiene mas de una linea verifica si contiene brackeds linea por linea para asi llevar el control de las lineas del error
                if len(arrayTitle) > 1:
                    countLine = countLine - 1
                    for title in arrayTitle:
                        countLine = countLine + 1
                        verifyBrackeds(title,countRegister,countLine)
                else:
                    # Si no tiene mas de una linea se verifica si contiene brackeds ese unico texto
                    verifyBrackeds(registerTag.text,countRegister,countLine)               
            else:     
                # en caso de no se la etiqueta "titulo_tg" se verifican los brackeds normalmente ya que solo esta etiqueta puede poseer mas de una linea
                verifyBrackeds(registerTag.text,countRegister,countLine)
   
            # El texto de las etiquetas deben comenzar por mayuscula, en caso contrario ocurre un error
            if registerTag.text[0].islower():
                # Este if estabiliza el contador de las lineas si algun registro posee una etiqueta "<titulo_tg>" con mas de una linea
                if registerTag.tag == "titulo_tg" and len(arrayTitle) > 1:
                    countLine = countLine - 1
                errorMsg(countRegister,countLine)

            # Las etiquetas no pueden comenzar por un numero, excepto la etiqueta "<fecha_pre>"       
            if registerTag.tag != "fecha_pre" and registerTag.tag != "nota":
                if registerTag.text[0].isdigit():
                    errorMsg(countRegister,countLine)
            
            # La etiqueta "<modalidad>" unicamente puede ser "Investigacion","Pasantias","Cursos especiales de grado". En caso contrario sera error
            if registerTag.tag == "modalidad":
                if registerTag.text != "Investigacion" and registerTag.text != "Pasantias" and registerTag.text != "Cursos especiales de grado":
                    errorMsg(countRegister,countLine)

            # La etiqueta "<nota>" debe es estar conformada con una nota "no numerica" y una "numerica", puede contener solo una de ellas
            if registerTag.tag == "nota":
                qualification = registerTag.text.split(" ") 
                # Se separa el texto de la etiqueta "<nota>" por medio de un espacio para verificar si posee solo una o ambas notas
                if len(qualification) == 1:
                    # En caso de solo ser la nota numerica esta debe estar entre 0 y 10, en caso contrario sera error
                    if qualification[0].isdigit() or qualification[0][0] == "-":
                        if int(qualification[0]) < 0 or int(qualification[0]) > 10:
                            errorMsg(countRegister,countLine)
                    else:
                        # En caso de ser solo la nota no numerica su valor puede ser unicamente "Aprobado","Reprobado" o "Publicacion", en caso contrario error
                        if qualification[0] != "Publicacion" and qualification[0] != "Aprobado" and qualification[0] != "Reprobado":
                            errorMsg(countRegister,countLine)
                elif len(qualification) == 2:
                    # En caso de poseer ambas notas igualmente se validan de forma individual
                    if qualification[0] != "Publicacion" and qualification[0] != "Aprobado" and qualification[0] != "Reprobado":
                        errorMsg(countRegister,countLine)
                    if qualification[1].isdigit() or qualification[1][0] == "-":
                        if int(qualification[1]) < 0 or int(qualification[1]) > 10:
                            errorMsg(countRegister,countLine)

            # La etiqueta "<fecha_pre>" debe poseer un estandar de dd/mm/yy
            if registerTag.tag == "fecha_pre":
                for format in ['%d/%m/%y']:
                    try:
                        result = time.strptime(registerTag.text, format)
                    except:
                        errorMsg(countRegister,countLine)
                # La validacion anterior permitia dia y mes con 1 solo digito, es extrictamente obligatorio contener dos
                fecha = registerTag.text.split("/")
                # Se separan mediante "/" y luego se verifica si dia y mes tienen 2 digitos cada uno, en caso contrario error
                if len(fecha[0]) != 2 or len(fecha[1]) != 2:
                    errorMsg(countRegister,countLine)

# Funcion para mostrar errores con su numero de registro y numero de linea respectivo
def errorMsg(regMsg, lineMsg):
    global error
    if error == False:
        print "\n           Error en el registro #", regMsg, ", Linea", lineMsg,"\n"
        error = True

# Funcion para verificar si los textos de las etiquetas contienen brackeds, si contienen alguno sera error
def verifyBrackeds(textTag, countRegister, countLine):
    for registerLetter in textTag:
        if registerLetter == "<" or registerLetter == ">":
            errorMsg(countRegister,countLine) 

# Inicio del script
if __name__ == "__main__":
    os.system("clear")

    try:
        # Se solicita al usuario el nombre del archivo
        # Se puede insertar un archivo con o sin extension 
        nameFileInput = raw_input("Introduce el archivo que desea validar:    \n       ")
        # Se separan por medio de un punto
        nameFileArray = nameFileInput.split(".")
        # Si la ultima posicion del arreglo es "xml" quiere decir que fue ingresado con extension
        if nameFileArray[-1] == "xml":
            nameFile = nameFileInput
        else:
            # En caso contrario se le procede a agregarse
            nameFile = nameFileInput+".xml"
        # Se abre el archivo ingresado
        xml = open(nameFile)
        # Se verifican las etiquetas
        checkTags(xml)
        # Si ocurre un error al verificar las etiquetas se detiene la ejecucion
        if error == False:
            # En caso de no ocurrir error se procede a verificar el texto
            checkText()
        # Si no ocurrio ningun error se muestra en pantalla "Archivo Ok"
        if error == False:
            print "\n       Archivo Ok.\n"

    except IOError:
        # En caso de no haber encontrado el archivo ocurre un error "Archivo no encontrado"
        print "\n       Archivo no encontrado.\n"
        error = True


############################## EBNF ##############################
# -Terminales:
# notacion: tg,autor,fecha_pre,titulo_tg,modalidad,tutor,nota,<,>,/,Investigacion, Pasantias,
#           Cursos,especiales,de,grado,Aprobado,Reprobado,Publicacion,0,1,2,3,4,5,6,7,8,9
# -No terminales:
# metanocion: <digito>,<letra>,<palabra_etiqueta>,<etiqueta>,<espacio_vacio>,<texto>,
#             <formato_fecha>,<fecha>,<palabra_modalidad>,<modalidad>,<palabra_nota>,
#             <nota>,<linea>,<registro>,<archivo>
# <digito>::= 0|1|2|3|4|5|6|7|8|9
# <letra>::= a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|
#            A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
# <palabra_etiqueta>::= tg|autor|fecha_pre|titulo_tg|modalidad|tutor|nota
# <etiqueta>::= ('<'|'<'/)<palabra_etiqueta>
# <espacio_vacio>::= ' '
# <texto>::= {<letra>|<espacio_vacio>}
# <formato_fecha>::= {<digito>}^2 [/]
# <fecha>::= {<formato_fecha>}^3
# <palabra_modalidad>::= Investigacion|Pasantias|Cursos|especiales|de|grado
# <modalidad>::= <palabra_modalidad> | {<palabra_modalidad>}^4
# <palabra_nota>::= Aprobado|Reprobado|Publicacion
# <nota>::= <palabra_nota>|
#           ((0<digito>)|{<digito>}^2)|
#           <palabra_nota> ((0<digito>)|{<digito>}^2)
# <linea>::= <etiqueta>|<etiqueta>(<texto>|<fecha>|<modalidad>|<nota>)<etiqueta>
# <registro>::= {<linea>}^8
# <archivo>::= {<registro>}
##################################################################