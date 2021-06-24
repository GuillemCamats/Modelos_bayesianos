from io import open_code
from posixpath import split
import sys
import os
import random

# Aquesta funció es la que s'utilitza per escriure en els fitxers arff. Simplement obre els fitxers
# i escriu el que correspont a cada fitxer. 

def writeOnArff(path,nums,instances,file_list):
    with open(path, "w") as file: 
        file.write("@RELATION file\n") # la funcio write escriu al fitxer que tinguem obert en aquell moment
        file.write("\n")

        for i in range(len(instances)-1):
            file.write("@ATTRIBUTE "+str(instances[i])+" {"+str(nums).replace(' ','')+"}\n")# replace, substitueix una cosa per una altra

        file.write("@ATTRIBUTE Type {1,2,3,4,5,6,7}\n")
        file.write("\n")
        
        file.write("@DATA\n")
        for line in file_list:
            line = str(line)[1 : -1]
            file.write("%s\n" % line)
            
    file.close()


# Aquesta funcio divideix les dades en dades de aprenentatge un 75% aproximadament, i la resta en dades
# de testing. Aqui apliquem la funció seed amb els 5 digits finals dem meu DNI. Tot seguit cridem la 
# funció que escriura ens els fitxers arff.

def split7525(list,learnig_path,testing_path,argval,instances):
    learning_list = []
    testing_list = []
    random.seed(42287)
    for sublist in list:
        if random.randint(1,100) < 75: # tria un numero random entre 1 i 100
            learning_list.append(sublist)
        else:
            testing_list.append(sublist)

    nums = [ j+1 for j in range(int(argval))]
    nums = str(nums)[1 : -1]
    writeOnArff(learnig_path,nums,instances,learning_list)
    writeOnArff(testing_path,nums,instances,testing_list)
    

# Com es comenta en la funció openAndRead la llista amb la que treballem esta dividida amb sub llistes
# on aquestes sub llistes el que representen son les col·lumnes del fitxer csv. El que fa aquesta funció
# es agafar un valor de cada subllista i juntarlos amb una altra llista, d'aquesta manera tornem a tindre
# una representacio del fitxer original. On cada subllista de la llista representara una fila del fitxer csv
def orderLists(list):
    orderedList = []
    recicleList = []
    for i in range (len(list[0])):
        for x in range(10):
            recicleList.append(list[x][i])
        orderedList.append(recicleList)
        recicleList = []

    return orderedList



#Aquesta funció elimina els duplicats de una llista, es fa crean un diccionari i passant
# els valor de la llista com a clau. Aixo elimina els duplicats perquè un diccionari no pot tindre
# claus repetides. Finalment retornem el diccionari com a llista.
def deleteDuplicates(x):
    return list(dict.fromkeys(x))



# Aquesta funció es la que s'encarrega de transformar els valors reals a un rang discret.
# Funciona de tal manera que s'agafen les subllistes per ordre, osigui les col·lumnes de el fitxer
# csv, s'ordenen per valor i s'eliminen els valors repetits. Tot seguit els elements de la subllista 
# seran dividits en tantes subsubllistes com el valor que ens donen per paramentre al executar el
# script. D'aquesta manera cada subsub llista representara un valor del rang ente 1 i el nombre d'entrada.
# Per assignar el el valor discret a un numero, el que es fa es deprés de tot lo anterior es mira si 
# per cada element de la subllista original(la que no s'ha processat amb tot lo anterior) es mira a quina
# subsub llista es troba ell mateix, ex: el numero 1.52101 de RI esta en la subllista 4, llavors 
# 1.52101 passara a ser 4. Aquest numero 4 s'afegeix en una nova llista anomenada discret list
# la qual al final contindra tots els valors reals transformats a discrets. 
def discreetDomain(atributs,argval):
    discreetList = [[] for _ in range(9)]
    i = 0
    for list in atributs:
        sortedList = list.copy() # copiar una llista
        sortedList.sort() # ordenar
        sortedList = deleteDuplicates(sortedList) #eliminar repetits
        # dividir la list en tantes subllistes com el numero argval
        dividedList= [sortedList[i:i+int(len(sortedList)/int(argval))+1] for i in range(0, len(sortedList), int(len(sortedList)/int(argval))+1)]
        for elem in list:
            x = 1
            for dlist in dividedList: 
                if elem in dlist:     # si el element pertany a la subllista assginem el valor x a el numero corresponent
                    discreetList[i].append(x)  # sent x la subsub llista al qual pertany el element
                    break
                else:
                    x +=1
        i+=1
    return discreetList

# El que fa aquesta funció es llegir el fitxer csv i afegir cada columna en una llista
# de manera que tots els valors RI estan en una llista Na en una altra llista etc.
# I finalment retorna una llista on hi ha els valors de la col·lumna type, ja que aqueta no s'ha de 
# transformar en domini discret. Tambe retorna una llista amb els elements de la primera linea del
# fitxer csv, el qual sera una llista amb els element RI,Na,Mg,Al,Si,K,Ca,Ba,Fe,Type,  i finalment 
# tambe retorna una llista de llistes amb els elemens de cada columna en sent aquesta la subllista.
# exemple [[elements de la col RI][elements de la col Na][elements de la col Mg][]...]
def openAndRead(css_path):
    with open(css_path) as css:
        RI,Na,Mg,Al,Si,K,Ca,Ba,Fe,Type, atributs= ([] for i in range(11))
        
        instances = css.readline().split(',') # split es per separar per el parametre dins del parentesis
        for line in css:
            values = line.strip().split(',') # strip es per remoure els espais al començament i al final de una string
            RI.append(values[0])
            Na.append(values[1])
            Mg.append(values[2])
            Al.append(values[3])
            Si.append(values[4])
            K.append(values[5])
            Ca.append(values[6])
            Ba.append(values[7])
            Fe.append(values[8])
            Type.append(int(values[9]))
        atributs.append(RI)
        atributs.append(Na)
        atributs.append(Mg)
        atributs.append(Al)
        atributs.append(Si)
        atributs.append(K)
        atributs.append(Ca)
        atributs.append(Ba)
        atributs.append(Fe)
    return atributs, instances, Type



        
if __name__ == '__main__':
    if len(sys.argv) != 5: # sys.argv controla els arguments que es passen per parametre
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 4.\n" %
                         len(sys.argv))
    
    csv_path = sys.argv[1]
    if not os.path.isfile(csv_path):
        sys.exit("ERROR: CSV file %s does not exist." % csv_path)
    learnig_path = sys.argv[2]
    if not os.path.isfile(learnig_path):
        sys.exit("ERROR: arff file %s does not exist." % learnig_path)
    testing_path = sys.argv[3]
    if not os.path.isfile(testing_path):
        sys.exit("ERROR: arff file %s does not exist." % testing_path)
    argval = sys.argv[4]       

    atributs, instances, Type= openAndRead(csv_path)
    discretList = discreetDomain(atributs,argval)
    discretList.append(Type)
    finalDiscretList = orderLists(discretList)
    split7525(finalDiscretList,learnig_path,testing_path,argval,instances)