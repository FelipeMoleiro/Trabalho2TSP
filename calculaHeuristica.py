import math
import matplotlib.pyplot as plt

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )

#le numero de galaxias
n = int(input())

data = {}

points = []

#se receber n == -1 gera pontos aleatorios
if(n == -1):
    n = int(input())
    for i in range(n):
        points.append(np.random.random(size=(2,1)))

else:
    #le matriz de distancia
    for i in range(n):
        inp = input().strip().split(" ")
        point = []
        point.append(float(inp[2]))
        point.append(float(inp[1]))
        points.append(point)

#calcula matriz de distancia a partir dos pontos
mat = []   
for i in range(n):
    l = []
    for j in range(n):
        if(i != j):
            l.append(dist(points[i][0],points[i][1],points[j][0],points[j][1]))
        else:
            l.append(0)
    mat.append(l)

#heuristica do vizinho mais proximo
def heuristicaFunc():
    resposta = 0
    respostaVet = [0] * (n*n)
    respostaU = [0] * (n-1)
    order = [0] * (n)
    visitados = [0] * n
    numVisitados = 1

    cnt = 0
    i = 0
    visitados[0] = 1
    order[cnt] = 0
    while (True):
        minValue = 0x7fffffff
        idx = -1
        for j in range(n):
            if( (visitados[j] == 0) and (i != j) ):
                if(mat[i][j] < minValue):
                    minValue = mat[i][j]
                    idx = j

        #print(idx)
        cnt += 1
        respostaU[idx-1] = cnt
        order[cnt] = idx
        respostaVet[i*n + idx] = 1
        visitados[idx] = 1
        numVisitados += 1
        resposta += mat[i][idx]
        i = idx
        if(numVisitados == n):
            respostaVet[i*n + 0] = 1
            resposta += mat[i][0]
            break

    return resposta, respostaVet, respostaU, order


def calc_value_sol(order):
    res = 0
    for i in range(n):
        res += mat[order[i]][order[(i+1)%n]]
    return res

def swp2OPT(route,i,k):
    newRoute = [0]*n
    for j in range(i):
        newRoute[j] = route[j]
    for j in range(k,i-1,-1):
        newRoute[k-j+i] = route[j]
    for j in range(k+1,n):
        newRoute[j] = route[j]
    return newRoute

def OPT_2(routeP):
    route = routeP
    resAtual = calc_value_sol(route)
    achouNovo = 1

    while(achouNovo == 1):
        print(resAtual)
        achouNovo = 0
        for i in range(1,n-1):
            for j in range(i+1,n):
                diff = 0
                diff -= mat[route[i-1]][route[i]]
                diff -= mat[route[j]][route[(j+1)%n]]
                diff += mat[route[i-1]][route[j]]
                diff += mat[route[i]][route[(j+1)%n]]
                
                if(diff < 0):
                    newRoute = swp2OPT(route,i,j)
                    route = newRoute
                    resAtual = calc_value_sol(newRoute)
                    achouNovo = 1
                    break
            if(achouNovo == 1):
                break

    return route, resAtual

def criaResFromRoute(route):
    resX = [0] * (n*n)
    resU = [0] * (n-1)
    posZero = -1
    for i in range(n):
        resX[route[i]*n + route[(i+1)%n]] = 1
        if(route[i] == 0):
            posZero = i

    posZero = (posZero + 1) %n
    for j in range(n-1):
        resU[route[(posZero+j)%n]-1] = (j+1)

    return resX,resU

def plot_route(route):
    for i in range(n):
        plt.plot([points[route[i]][0],points[route[(i+1)%n]][0]],[points[route[i]][1],points[route[(i+1)%n]][1]],'ro-')
    plt.show()

primal, resX, resU, order = heuristicaFunc()#heurustuca vizinhança

newRoute, newPrimal = OPT_2(order)#melhora da heuristica
resX,resU = criaResFromRoute(newRoute)
#newResX = 



print("Valor da heuristica inicial: " + str(newPrimal) )
print()
for i in range(n):
    print(newRoute[i])
plot_route(newRoute)