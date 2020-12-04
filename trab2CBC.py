from mip import *
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--tempo", help="tempo Em Segundos(deve ser um numero inteiro)")
parser.add_argument("-hr","--heuristica", help="Seleciona heuristica, 0-sem heuristica, 1-com heuristica de vizinho mais proximo")
parser.add_argument("-se","--searchemphasis", help="Seleciona a enfase de busca. 0-default, 1-factibilidade, 2-otimalidade")

args = parser.parse_args()

print(args.t)


#DEFAULT = 0, FEASIBILITY = 1, OPTIMALITY  = 2
SearchEmphasis(1)

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

'''
def subtour(N,edges,node):
	queue = [node]
	visited = [0] * n
	while(queue):
		atual = queue.pop()
		for nxt in edges[atual]

'''

#coeficientes da func objetivo
data['obj_coeffs'] = []

#adiciona os coeficientes de acordo com a matriz, ou seja, X01,X02,X03,x04,X10,X11,...,X43
for i in range(n):
    for j in range (n):
           data['obj_coeffs'].append(mat[i][j])

m = Model()

x = [ m.add_var(var_type=BINARY) for i in range(n*n) ]
u = [ m.add_var(var_type=INTEGER, lb=1, ub=n-1) for i in range(n-1) ]

for i in range(n):
	m += xsum(x[i*n + j] for j in set(range(n))-{i} ) == 1

for i in range(n):
	m += xsum(x[j*n + i] for j in set(range(n))-{i}) == 1

for i in range(1,n):
    for j in range(1,n):
    	if(i != j):
    		#m += u[i-1] - u[j-1] + (n-1)*x[i*n + j] <= n-2
    		m.add_lazy_constr(u[i-1] - u[j-1] + (n-1)*x[i*n + j] <= n-2) #Se for ser lazy constraint


m.objective = xsum(data['obj_coeffs'][i]*x[i] for i in range(n*n))




def heuristica():
    resposta = 0
    respostaVet = [0] * (n*n)
    respostaU = [0] * (n-1)
    visitados = [0] * n
    numVisitados = 1

    cnt = 0
    i = 0
    visitados[0] = 1
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
        respostaVet[i*n + idx] = 1
        visitados[idx] = 1
        numVisitados += 1
        resposta += mat[i][idx]
        i = idx
        if(numVisitados == n):
            respostaVet[i*n + 0] = 1
            resposta += mat[i][0]
            break

    return resposta, respostaVet, respostaU


primal, resX, resU = heuristica()
temp = []
for i in range(n*n):
	temp.append( (x[i], resX[i]) )
for i in range(n-1):
	temp.append( (u[i], resU[i]) )

m.start = temp
print(primal)



tempSec = 30 * 60

status = m.optimize(max_seconds=tempSec)

print("FIIIM")
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for i in range(n*n):
    	indFrom = (int)(i/n)
    	indTo = i%n
    	#print('X ' + str(indFrom) + ' ' +str(indTo)  , ' = ', x[i].x)
    	if abs(x[i].x) > 1e-6:
    		plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
    plt.show()
    '''
    for v in m.vars:
       if abs(v.x) > 1e-6: # only printing non-zeros
        #print('{} : {}'.format(v.name, v.x))
        indFrom = (int)(v.x/n)
        indTo = j%n
       	plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
    plt.show()
    '''
       