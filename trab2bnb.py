#Usando branch and bound para resolver o problema

'''
Usar heuristica pra solução inicial(tipo cidade mais proxima)

node selection... ver...  enfatizar a otimalidade, enfatizar a factibilidade??

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
from graphviz import Digraph
import timeit

start = timeit.default_timer()


def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )

solver = pywraplp.Solver.CreateSolver('GLOP')
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
    x[j] = solver.NumVar(0,1,'x[%i]' % j)


for j in range(n-1):
    u[j] = solver.NumVar(1,n-1, 'u[%i]' % j)


#garante que todas as variaveis Xij, com i fixo e j variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    res = [0] * (n*n)
    for i in range(n):
        res[k*n + i] = 1

    constraint = solver.Constraint(1, 1)
    for j in range(n*n):
        constraint.SetCoefficient(x[j], res[j])
    for j in range(n-1):
        constraint.SetCoefficient(u[j], 0)

#garante que todas as variaveis Xij, com j fixo e i variando, somadas sejam igual a 1
for k in range(n): #k é numero de restriçoes
    res = [0] * (n*n)
    for i in range(n):
    	res[i*n + k] = 1

    constraint = solver.Constraint(1, 1)
    for j in range(n*n):
        constraint.SetCoefficient(x[j], res[j])
    for j in range(n-1):
        constraint.SetCoefficient(u[j], 0)

for i in range(1,n):
    for j in range(1,n):
        resX = [0] * (n*n)
        resU = [0] * (n-1)
        resX[i*n + j] = (n-1)

        resU[i-1] += 1
        resU[j-1] -= 1

        constraint = solver.Constraint(-infinity,n-2)
        for j in range(n*n):
            constraint.SetCoefficient(x[j], resX[j])
        for j in range(n-1):
            constraint.SetCoefficient(u[j], resU[j])

for k in range(n):
	constraint = solver.Constraint(0, 0)
	for j in range(n*n):
		constraint.SetCoefficient(x[j], 0)
	constraint.SetCoefficient(x[k*n + k], 1)
	for j in range(n-1):
		constraint.SetCoefficient(u[j], 0)

#print('Number of variables =', solver.NumVariables())
#print('Number of constraints =', solver.NumConstraints())

#arruma função objetivo
objective = solver.Objective()
for j in range(n*n):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j]) #coloca coeficientes da func objetivo
for j in range(n-1):
    objective.SetCoefficient(u[j], 0) #coloca coeficientes da func objetivo
objective.SetMinimization() #coloca para minimizar a func obj


def respostaInteira(x):
	for i in range(n*n):
		if(x[i].solution_value() > 0.00000000001 and x[i].solution_value() < 0.9999999999):
		#if(int(x[i].solution_value()) != math.ceil(x[i].solution_value())):
			#print("fim igual")
			return i
	#print("fim -1")
	return -1


def printRes(x):
	for j in range(n*n):
		indFrom = (int)(j/n)
		indTo = j%n
		if(x[j].solution_value()):
			plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
	#for j in range(n-1):
		#print('U ', str(j+1),' = ', u[j].solution_value())
		#print('X ' + str(indFrom) + ' ' +str(indTo)  , ' = ', x[j].solution_value())
	plt.show()

def printRes2(res):
	for j in range(n*n):
		indFrom = (int)(j/n)
		indTo = j%n
		if(res[j] >= 0.999999):
			plt.plot([points[indFrom][0],points[indTo][0]],[points[indFrom][1],points[indTo][1]],'ro-')
		print('X ' + str(indFrom) + ' ' +str(indTo)  , ' = ', res[j])
	plt.show()

primal = infinity
res = []
#dual = 0

#dot = Digraph(comment='testVizu', format='png')

#count = 0

tempoExc=0

def bnb(solver):
	global x
	global res
	#global u

	global primal
	#global dual

	#global count
	#my_id = count
	#count += 1

	#stop = timeit.default_timer()

	#if(stop - start >= 20):
	#	tempoExc = 1
	#	return

	status = solver.Solve()
	if status == pywraplp.Solver.OPTIMAL:
		objval = solver.Objective().Value()
		#print(objval)
		if(objval >= primal):
			print("poda por qualidade: " + str(objval))
			#dot.node(f"{my_id}", f"Poda por qualidade", color="blue")
			#count += 1
			return # my_id
		else:
			idx = respostaInteira(x)
			if(idx == -1):
				primal = objval
				res = [x[i].solution_value() for i in range(n*n)]
				print("Resposta: " + str(objval) )
				#dot.node(f"{my_id}", f"{primal}, {objval:.2f}", color="green")
				#printRes(x)
			else:
				#dot.node(f"{my_id}", f"{primal}, {objval:.2f}")
				x[idx].SetBounds(0,0)
				child_id = bnb(solver)
				#dot.edge(f"{my_id}", f"{child_id}", label=f"x{int(idx/n)},{idx%n} = 0")

				x[idx].SetBounds(1,1)
				child_id = bnb(solver)
				#dot.edge(f"{my_id}", f"{child_id}", label=f"x{int(idx/n)},{idx%n} = 1")

				x[idx].SetBounds(0,1) #volta ao normal
	else:
		print("Poda por infactibilidade")
		#dot.node(f"{my_id}", f"Poda por infactibilidade", color="red")
		#count += 1
	return #my_id

bnb(solver)

if(tempoExc):
	print("Tempo Excedido, Resposta encontrada:")
print(primal)
printRes2(res)

#dot.render('kipling', view=True)
#status = solver.Solve()# resolve
#print(respostaInteira(x))

'''
x[0*n + 0].SetBounds(0,0)
x[2*n + 2].SetBounds(0,0)
x[2*n + 3].SetBounds(1,1)

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
    print('The problem does not have an optimal solution.')
'''