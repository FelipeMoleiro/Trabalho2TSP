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

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )

solver = pywraplp.Solver.CreateSolver('SCIP')
infinity = solver.infinity()

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

x = {}
u = {}
for j in range(n*n):
    x[j] = solver.BoolVar('x[%i]' % j)


for j in range(n-1):
    u[j] = solver.IntVar(1.0,n-1, 'u[%i]' % j)


#garante que todas as variaveis Xij, com i fixo e j variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    res = [0] * (n*n)
    for i in range(n):
        res[k*n + i] = 1

    constraint = solver.RowConstraint(1, 1, '')
    for j in range(n*n):
        constraint.SetCoefficient(x[j], res[j])
    for j in range(n-1):
        constraint.SetCoefficient(u[j], 0)

#garante que todas as variaveis Xij, com j fixo e i variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    res = [0] * (n*n)
    for i in range(n):
    	res[i*n + k] = 1

    constraint = solver.RowConstraint(1, 1, '')
    for j in range(n*n):
        constraint.SetCoefficient(x[j], res[j])
    for j in range(n-1):
        constraint.SetCoefficient(u[j], 0)


''' Implementação Naive
#para cada subconjuntos de tamanho 2 a n-1
for tam in range(2,n):
    combinationsR = combinations(list(range(n)), tam)
    for comb in combinationsR:
        #coloca a restrição somatorio de Xij, com i e j pertencente ao subconj e i!=j, tem que ser <= |subconjunto|-1
        #print(comb)
        res = [0] * data['num_vars']
        for i in comb:
            for j in comb:
            	res[i*n + j] = 1

        constraint = solver.RowConstraint(0,len(comb)-1, '')
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], res[j])
'''

for i in range(1,n):
    for j in range(1,n):
        resX = [0] * (n*n)
        resU = [0] * (n-1)
        resX[i*n + j] = (n-1)

        resU[i-1] += 1
        resU[j-1] -= 1

        constraint = solver.RowConstraint(-infinity,n-2, '')
        for j in range(n*n):
            constraint.SetCoefficient(x[j], resX[j])
        for j in range(n-1):
            constraint.SetCoefficient(u[j], resU[j])
'''
for i in range(n):
    resX = [0] * (n*n)
    resX[i*n + i] = 1

    constraint = solver.RowConstraint(0,0, '')
    for j in range(n*n):
        constraint.SetCoefficient(x[j], resX[j])
    for j in range(n-1):
        constraint.SetCoefficient(u[j], 0)
'''


print('Number of variables =', solver.NumVariables())
print('Number of constraints =', solver.NumConstraints())

#arruma função objetivo
objective = solver.Objective()
for j in range(n*n):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j]) #coloca coeficientes da func objetivo
for j in range(n-1):
    objective.SetCoefficient(u[j], 0) #coloca coeficientes da func objetivo

objective.SetMinimization() #coloca para minimizar a func obj


status = solver.Solve() # resolve

if status == pywraplp.Solver.OPTIMAL: #se achou resposta
    print('Objective value =', solver.Objective().Value()) #print valor da função objetivo minimizada

    #para cada variavel
    for j in range(n*n):
        indFrom = (int)(j/n)
        indTo = j%n

        if(x[j].solution_value()):
            plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')

        print('X ' + str(indFrom) + ' ' +str(indTo)  , ' = ', x[j].solution_value())
    for j in range(n-1):
        print('U ', str(j+1),' = ', u[j].solution_value())
    plt.show()
else: #se nao tem resposta
    print(solver.nodes())
    print('The problem does not have an optimal solution.')
