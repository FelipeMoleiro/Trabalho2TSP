#!/usr/bin/env python
# coding: utf-8

# In[2]:


from ortools.linear_solver import pywraplp
from math import ceil
from graphviz import Digraph


# In[3]:


dot = Digraph(comment='Mochila Mochila, yay!', format='png')


# In[4]:


solver = pywraplp.Solver.CreateSolver('GLOP')


# In[5]:


def f(a1, a2, a3, a4):
    return 10*a1 + 12*a2 + 7*a3 + 3/2*a4


# In[6]:


def get_diff(l1, l2):
    for idx, (v1, v2)  in enumerate(zip(l1, l2)):
        if v1 != v2:
            return idx
    return -1


# In[7]:


x1 = solver.NumVar(0, 1e6, 'x1')
x2 = solver.NumVar(0, 1e6, 'x2')
x3 = solver.NumVar(0, 1, 'x3')
x4 = solver.NumVar(0, 1, 'x4')
x = [x1, x2, x3, x4]


# In[8]:


solver.Add(4*x1 + 5*x2 + 3*x3 + x4 <= 10)
solver.Maximize(10*x1 + 12*x2 + 7*x3 + 3/2*x4)


# In[9]:


count = 0
best = -1


# In[10]:


def bnb(solver):
    global count
    global best
    status = solver.Solve()
    my_id = count
    count += 1
    if status == pywraplp.Solver.OPTIMAL:
        dual = solver.Objective().Value()
        if dual < best:
            dot.node(f"{my_id}", f"Poda por qualidade", color="blue")
            print(dual)
            count += 1
            return my_id

        print("Dual: ", dual)
        
        x_lower = [int(xi.solution_value()) for xi in x]
        x_upper = [ceil(xi.solution_value()) for xi in x]
        
        primal = f(*x_lower)
        
        
        non_int = get_diff(x_lower, x_upper)
        if non_int == -1:
            dot.node(f"{my_id}", f"{primal}, {dual:.2f}", color="green")
            best = max(best, primal)
            return my_id
        else:
            dot.node(f"{my_id}", f"{primal}, {dual:.2f}")
            lower = x_lower[non_int]
            upper = x_upper[non_int]
            x_branch = solver.variables()[non_int]
            lb, ub = x_branch.lb(), x_branch.ub()
            x_branch.SetUb(lower)
            child_id = bnb(solver)
            x_branch.SetUb(ub)
            dot.edge(f"{my_id}", f"{child_id}", label=f"x{non_int+1} <= {lower}")
            
            x_branch.SetLb(upper)
            child_id = bnb(solver)
            x_branch.SetLb(lb)
            dot.edge(f"{my_id}", f"{child_id}", label=f"x{non_int+1} >= {upper}")
        return my_id
    else:
        dot.node(f"{my_id}", f"Poda por infactibilidade", color="red")
        count += 1
        return my_id


# In[11]:


bnb(solver)


# In[12]:


best


# In[13]:


dot.render('kipling', view=True)  


# In[ ]:




