from mip import *
import math
import matplotlib.pyplot as plt
import argparse

#Verifica argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument("-t","--tempo",type=int, help="tempo Em Segundos(deve ser um numero inteiro)")
parser.add_argument("-hr","--heuristica",type=int, help="Seleciona heuristica, 0-sem heuristica, 1-com heuristica de vizinho mais proximo")
parser.add_argument("-se","--searchemphasis",type=int, help="Seleciona a enfase de busca. 0-default, 1-factibilidade, 2-otimalidade")
parser.add_argument("-of", help="Output picture")

args = parser.parse_args()

#cria modelo
m = Model()

#argumentos padrao do algoritmo
m.emphasis = SearchEmphasis.DEFAULT # Default
tempSec = -1# sem limite
heuristicaBool = 1

#modifica argumetnos padrap
if(args.tempo != None):
    tempSec = args.tempo

if(args.searchemphasis != None):
    if(args.searchemphasis == 1): m.emphasis = SearchEmphasis.FEASIBILITY
    elif(args.searchemphasis == 2): m.emphasis = SearchEmphasis.OPTIMALITY

if(args.heuristica != None):
    heuristicaBool = args.heuristica


#informa args
print("Parametros de execução:")
print("Tempo Limite: " + str(tempSec) )
print("Enfase: " + str(m.emphasis) )
print("Heuristica: " + str(heuristicaBool) )
print()


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

#FIM DA LEITURA DA MATRIZ


#coeficientes da func objetivo
data['obj_coeffs'] = []

#adiciona os coeficientes de acordo com a matriz, ou seja, X01,X02,X03,x04,X10,X11,...,X43
for i in range(n):
    for j in range (n):
           data['obj_coeffs'].append(mat[i][j])


#declara variaveis e restriçoes
x = [ m.add_var(var_type=BINARY) for i in range(n*n) ]
u = [ m.add_var(var_type=INTEGER, lb=1, ub=n-1) for i in range(n-1) ]

for i in range(n):
	m += xsum(x[i*n + j] for j in set(range(n))-{i} ) == 1

for i in range(n):
	m += xsum(x[j*n + i] for j in set(range(n))-{i}) == 1

for i in range(1,n):
    for j in range(1,n):
    	if(i != j):
    		m += u[i-1] - u[j-1] + (n-1)*x[i*n + j] <= n-2

#declara func obj
m.objective = xsum(data['obj_coeffs'][i]*x[i] for i in range(n*n))



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

#retorna o valor de uma rota
def calc_value_sol(order):
    res = 0
    for i in range(n):
        res += mat[order[i]][order[(i+1)%n]]
    return res

#função swp do 2-OPT
def swp2OPT(route,i,k):
    newRoute = [0]*n
    for j in range(i):
        newRoute[j] = route[j]
    for j in range(k,i-1,-1):
        newRoute[k-j+i] = route[j]
    for j in range(k+1,n):
        newRoute[j] = route[j]
    return newRoute

#calcula heuristica 2-OPT a partir de uma rota base
def OPT_2(routeP):
    route = routeP
    resAtual = calc_value_sol(route)
    achouNovo = 1

    while(achouNovo == 1):
        #print(resAtual)
        achouNovo = 0
        for i in range(1,n-1):
            for j in range(i+1,n):
                diff = 0
                diff -= mat[route[i-1]][route[i]]
                diff -= mat[route[j]][route[(j+1)%n]]
                diff += mat[route[i-1]][route[j]]
                diff += mat[route[i]][route[(j+1)%n]]
                
                if(diff < -1e-6):
                    #print(diff)
                    #print(i,j)
                    newRoute = swp2OPT(route,i,j)
                    route = newRoute
                    resAtual = calc_value_sol(newRoute)
                    achouNovo = 1
                    break
            if(achouNovo == 1):
                break

    return route, resAtual

#retorna valor das variaveis do modelo a partir de uma rota
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

#retorna rota feita por uma certa resposta do modelo
def criaRouteFromRes(resX):
    tempRoute = [0]
    i = 0
    while (True):
        for j in range(n):
            if(abs(resX[i*n + j]) > 1e-6):
                i = j
                break
        if(i == 0):
            break
        tempRoute.append(i)
    return tempRoute

#retorna rota feita por uma certa resposta do modelo(desta vez verificando as proprias variaveis x e nao recebendo como parametro)
def criaRouteFromResModel():
    tempRoute = [0]
    i = 0
    while (True):
        #print(i)
        for j in range(n):
            if(abs(x[i*n + j].x)  > 1e-6):
                i = j
                break
        if(i == 0):
            break
        tempRoute.append(i)
    return tempRoute

#plot na tela da rota
def plot_route(route):
    for i in range(n):
        plt.plot([points[route[i]][0],points[route[(i+1)%n]][0]],[points[route[i]][1],points[route[(i+1)%n]][1]],'ro-')
    plt.show()


#se a heuristica esta ativada, calcula
if(heuristicaBool == 1):
    primal, resX, resU, order = heuristicaFunc()#heurustuca vizinhança

    newRoute, newPrimal = OPT_2(order)#melhora da heuristica
    resX,resU = criaResFromRoute(newRoute)

    temp = []
    for i in range(n*n):
    	temp.append( (x[i], resX[i]) )
    for i in range(n-1):
    	temp.append( (u[i], resU[i]) )

    m.start = temp
    print("Valor da heuristica inicial: " + str(newPrimal) )
    print()


#se tem limite de tempo executa com limite
if(tempSec < 0):
    status = m.optimize()
else:
    status = m.optimize(max_seconds=tempSec)


print("FIIIM")
print(status)

#print das soluçao final
resFinalX = []
if status == OptimizationStatus.OPTIMAL:

    print('optimal solution cost {} found'.format(m.objective_value))
    for i in range(n*n):
        resFinalX.append(x[i].x)

elif status == OptimizationStatus.FEASIBLE:

    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
    tempOrd = criaRouteFromResModel()
    print('Tentando melhorar solução com OPT-2')
    newRoute, newPrimal = OPT_2(tempOrd)#melhora da heuristica
    resFinalX,resFinalU = criaResFromRoute(newRoute)
    print('sol.cost apos OPT-2 é: ' + str(newPrimal))

elif status == OptimizationStatus.NO_SOLUTION_FOUND:

    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))

if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:

    print('solution:')
    for i in range(n*n):
    	indFrom = (int)(i/n)
    	indTo = i%n
    	if abs(resFinalX[i]) > 1e-6:
    		plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
    if(args.of != None):
        plt.savefig(args.of)
    else:
        plt.show()