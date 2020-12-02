'''
Nomes: 
Felipe Guilermmo Santuche Moleiro - 10724010 - felipemoleiro@usp.br
Mateus Prado Santos - 10851707 - mateus.prado@usp.br
Matheus Lopes Rigato - 10260462 - matheus_rigato@usp.br
Victor Vieira Custodio Reis - 10734686 - reisvictor@usp.br
Vinicius Ricardo Carvalho - 10724413 - vinicius_carvalho@usp.br
'''


from __future__ import print_function
from ortools.linear_solver import pywraplp
from itertools import combinations
import math
import matplotlib.pyplot as plt
import numpy as np

DEBUG = 1

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )

solver = pywraplp.Solver.CreateSolver('SCIP')
infinity = solver.infinity()

solver.EnableOutput()

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


#for i in range(n):
#    plt.plot(points[i][0],points[i][1],'ro-')
#plt.show()

#-----------------------------------Nao le mais matriz de dist, ja que le pontos...
#le matriz de distancia
#mat = []
#for i in range(n):
#    mat.append( [int(j) for j in input().strip().split(" ")] )
#----------------------------------------------------------------------------------


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

#coeficientes da func objetivo
data['obj_coeffs'] = []

#adiciona os coeficientes de acordo com a matriz, ou seja, X01,X02,X03,x04,X10,X11,...,X43
for i in range(n):
    for j in range (n):
           data['obj_coeffs'].append(mat[i][j])

#numero de variaveis é n*n de xij + (n-1) informando a ordem de visitação dos nós 2 a n 
data['num_vars'] = n * n + n-1

if(DEBUG): print("Setting up variables")

x = []
u = []
for j in range(n*n):
    x.append( solver.BoolVar('x[%i]' % j) )


for j in range(n-1):
    u.append( solver.IntVar(1.0,n-1, 'u[%i]' % j) )

if(DEBUG): print("Setting up constraints")



#garante que todas as variaveis Xij, com i fixo e j variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    constraint = solver.RowConstraint(1, 1, '')
    for i in range(n):
        constraint.SetCoefficient(x[k*n + i], 1)

#garante que todas as variaveis Xij, com j fixo e i variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    constraint = solver.RowConstraint(1, 1, '')
    for i in range(n):
        constraint.SetCoefficient(x[i*n + k], 1)

for i in range(1,n):
    for j in range(1,n):
        constraint = solver.RowConstraint(-infinity,n-2, '')
        constraint.set_is_lazy(True)
        constraint.SetCoefficient(x[i*n + j],(n-1))

        if(i != j):
            constraint.SetCoefficient(u[i-1], 1)
            constraint.SetCoefficient(u[j-1], -1)


print('Number of variables =', solver.NumVariables())
print('Number of constraints =', solver.NumConstraints())

#arruma função objetivo
objective = solver.Objective()
for j in range(n*n):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j]) #coloca coeficientes da func objetivo
for j in range(n-1):
    objective.SetCoefficient(u[j], 0) #coloca coeficientes da func objetivo

objective.SetMinimization() #coloca para minimizar a func obj


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
temp1 = []
temp2 = []
for i in range(n*n):
    temp1.append( resX[i] )
    temp2.append(x[i])
for i in range(n-1):
    temp1.append( resU[i] )
    temp2.append(u[i])
#primal, res = heuristica()
solver.SetHint(temp2,temp1)
tempoEmSegundos = 10 * 60

solver.set_time_limit(tempoEmSegundos*1000)

#solver.SCIP_LPPAR_TIMING

status = solver.Solve() # resolve


 

if status == pywraplp.Solver.FEASIBLE: #se achou resposta
    #para cada variavel
    for j in range(n*n):
        indFrom = (int)(j/n)
        indTo = j%n
        if(x[j].solution_value()):
            plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
    plt.show()
