from io import open_code
from posixpath import split
import sys
import os
import random

def classify(list,learnig_path,testing_path):
    learning_list = []
    testing_list = []
    random.seed(42287)
    for sublist in list:
        if random.randint(1,100) < 75: 
            learning_list.append(sublist)
        else:
            testing_list.append(sublist)

    with open(learnig_path, "w") as learning:
        learning.write("@RELATION learning\n")
        learning.write("\n")
        learning.write("@ATTRIBUTE RI {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Na {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Mg {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Al {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Si {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE K {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Ca {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Ba {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Fe {1,2,3,4,5,6,7,8}\n")
        learning.write("@ATTRIBUTE Type {1,2,3,4,5,6,7,8}\n")
        learning.write("\n")
        
        learning.write("@DATA\n")
        for line in learning_list:
            line = str(line)[1 : -1]
            learning.write("%s\n" % line)
            
    learning.close()

    with open(testing_path, "w") as testing:
        testing.write("@RELATION testing\n")
        testing.write("\n")
        testing.write("@ATTRIBUTE RI {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Na {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Mg {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Al {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Si {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE K {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Ca {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Ba {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Fe {1,2,3,4,5,6,7,8}\n")
        testing.write("@ATTRIBUTE Type {1,2,3,4,5,6,7,8}\n")
        testing.write("\n")
        testing.write("@DATA\n")

        for line in testing_list:
            line = str(line)[1 : -1]
            testing.write("%s\n" % line)
    
    testing.close()

def orderLists(list):
    orderedList = []
    recicleList = []
    for i in range (len(list[0])):
        for x in range(10):
            recicleList.append(list[x][i])
        orderedList.append(recicleList)
        recicleList = []

    return orderedList


def discreetDomain(atributs):
    discreetList = [[] for _ in range(10)]
    i = 0
    for list in atributs:
        lenl = len(list)/8
        sortedList = list.copy()
        sortedList.sort()
        dividedList= [sortedList[i:i+int(lenl)+1] for i in range(0, len(sortedList), int(lenl)+1)]
        for elem in list:
            x = 1
            for dlist in dividedList:
                if elem in dlist:
                    discreetList[i].append(x)
                    break
                else:
                    x +=1
        i+=1
    return discreetList

def openAndCsstoArff(css_path):
    with open(css_path) as css:
        RI,Na,Mg,Al,Si,K,Ca,Ba,Fe,Type, atributs= ([] for i in range(11))
        
        instances = css.readline().split(',')
        for line in css:
            values = line.strip().split(',')
            RI.append(values[0])
            Na.append(values[1])
            Mg.append(values[2])
            Al.append(values[3])
            Si.append(values[4])
            K.append(values[5])
            Ca.append(values[6])
            Ba.append(values[7])
            Fe.append(values[8])
            Type.append(values[9])
        atributs.append(RI)
        atributs.append(Na)
        atributs.append(Mg)
        atributs.append(Al)
        atributs.append(Si)
        atributs.append(K)
        atributs.append(Ca)
        atributs.append(Ba)
        atributs.append(Fe)
        atributs.append(Type)
    
    return atributs



        
if __name__ == '__main__':
    """if len(sys.argv) != 3:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 3.\n" %
                         len(sys.argv))"""
    
    css_path = sys.argv[1]
    if not os.path.isfile(css_path):
        sys.exit("ERROR: CNF file %s does not exist." % css_path)
    learnig_path = sys.argv[2]
    testing_path = sys.argv[3]

    
    atributs= openAndCsstoArff(css_path)
    discretList = discreetDomain(atributs)
    finalDiscretList = orderLists(discretList)
    classify(finalDiscretList,learnig_path,testing_path)