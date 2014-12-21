import os
from PIL import Image
from scipy.spatial.distance import mahalanobis
from scipy.linalg import pinv
import numpy as np

def main(path_set_foto, path_nueva_foto):

    #dic_fotos_divididas contiene las fotos en el orden na_*, nb_*, nc_*, nd_*, ne_*
    dic_fotos_divididas = {}
    dic_fotos_divididas['na'] = []
    dic_fotos_divididas['nb'] = []
    dic_fotos_divididas['nc'] = []
    dic_fotos_divididas['nd'] = []
    dic_fotos_divididas['ne'] = []

    #diccionario con
    # - una lista de histogramas de las imagenes en escala de gris
    # - la matrix de covarianza
    # - la distancia de mahalanobis media con la imagen input
    dic_fotos_parseadas = {}
    dic_fotos_parseadas['na'] = [[],None, None]
    dic_fotos_parseadas['nb'] = [[],None, None]
    dic_fotos_parseadas['nc'] = [[],None, None]
    dic_fotos_parseadas['nd'] = [[],None, None]
    dic_fotos_parseadas['ne'] = [[],None, None]
    
    #dividimos las fotos
    for i in os.listdir(path_set_fotos):
        temp = i[:3]
        if temp == 'na_':
            dic_fotos_divididas['na'].append(os.path.join(path_set_fotos, i))
        if temp == 'nb_':
            dic_fotos_divididas['nb'].append(os.path.join(path_set_fotos, i))
        if temp == 'nc_':
            dic_fotos_divididas['nc'].append(os.path.join(path_set_fotos, i))
        if temp == 'nd_':
            dic_fotos_divididas['nd'].append(os.path.join(path_set_fotos, i))
        if temp == 'ne_':
            dic_fotos_divididas['ne'].append(os.path.join(path_set_fotos, i))
    print 'fotos divididas en grupos'

    grupos = dic_fotos_divididas.keys()

    #convertimos las fotos in blanco y negro y luego calculamos el histograma
    for i in grupos:
        for j in dic_fotos_divididas[i]:
            im = None
            im = Image.open(j)
            im = im.convert('L')
            histo = im.histogram()
            maximum = max(histo)
            for l in range(len(histo)):
                histo[l] = histo[l]/maximum
            dic_fotos_parseadas[i][0].append(histo)
        print 'terminado parsear grupo: ' + i
            

    #calculamos la covarianza
    for i in grupos:
        megalist = []
        for j in dic_fotos_parseadas[i][0]:
            megalist.append(j)
        dic_fotos_parseadas[i][1]=np.array(megalist)
        #print 'terminado calcular grupo: ' + i
        #print '(num fotos, num colores) ' + str(dic_fotos_parseadas[i][1].shape)
        dic_fotos_parseadas[i][1] = np.cov(dic_fotos_parseadas[i][1], rowvar = 0)
        print 'terminado de calcular covarianza del grupo: ' + i

    #calculo el histograma de la foto input
    foto_input = Image.open(path_nueva_foto)
    foto_input = foto_input.convert('L')
    input_histo = foto_input.histogram()
    max_input_histo = max(input_histo)
    for l in range(len(input_histo)):
        input_histo[l] = input_histo[l]/max_input_histo

    #calculo la distancia media con la foto input
    #por la matriz inversa utilizo la inversa de Monroe-Pearson que da una pseudo inversa en caso que la matriz sea singular
    for i in grupos:
        suma_dist = 0
        cov_inv = pinv(dic_fotos_parseadas[i][1])
        for j in dic_fotos_parseadas[i][0]:
            suma_dist += mahalanobis(input_histo, j, cov_inv)
        dic_fotos_parseadas[i][2] = suma_dist/len(dic_fotos_parseadas[i][0])
        if np.isnan(dic_fotos_parseadas[i][2]):
            print 'nan encontrado'
            dic_fotos_parseadas[i][2] = np.inf
        print 'dist media: ' + str(dic_fotos_parseadas[i][2])
    
    result = ['A','B','C','D','E'][[dic_fotos_parseadas[i][2] for i in grupos].index(min([dic_fotos_parseadas[i][2] for i in grupos]))]
    return result



if __name__=="__main__":
    path_set_fotos = './set_fotos_todas'
    #path_nueva_foto = './C2.jpg'
    #result = main(path_set_fotos, path_nueva_foto)
    #print result

    result_A = []
    for i in os.listdir('./A'):
        result_A.append(main(path_set_fotos, './A/' + i))
        print 'resultado foto in A:'
        print result_A[-1]
    print 'resultado por A:'
    print result_A

    result_B = []
    for i in os.listdir('./B'):
        result_B.append(main(path_set_fotos, './B/' + i))
        print 'resultado foto in B:'
        print result_B[-1]
    print 'resultado por B:'
    print result_B

    result_C = []
    for i in os.listdir('./C'):
        result_C.append(main(path_set_fotos, './C/' + i))
        print 'resultado foto in C:'
        print result_C[-1]
    print 'resultado por C:'
    print result_C

    result_D = []
    for i in os.listdir('./D'):
        result_D.append(main(path_set_fotos, './D/' + i))
        print 'resultado foto in D:'
        print result_D[-1]
    print 'resultado por D:'
    print result_D

    result_E = []
    for i in os.listdir('./E'):
        result_E.append(main(path_set_fotos, './E/' + i))
        print 'resultado foto in E:'
        print result_E[-1]
    print 'resultado por E:'
    print result_E


    f = open('./mahalanobis.txt', 'a')
    print 'finales'
    f.write('finales\n')
    print 'resultado per A:'
    f.write('resultado per A:\n')
    print result_A
    f.write(str(result_A))
    f.write('\n')
    print 'resultado per B:'
    f.write('resultado per B:\n')
    print result_B
    f.write(str(result_B))
    f.write('\n')
    print 'resultado per C:'
    f.write('resultado per C:\n')
    print result_C
    f.write(str(result_C))
    f.write('\n')
    print 'resultado per D:'
    f.write('resultado per D:\n')
    print result_D
    f.write(str(result_D))
    f.write('\n')
    print 'resultado per E:'
    f.write('resultado per E:\n')
    print result_E
    f.write(str(result_E))
    f.write('\n')
    f.close()



