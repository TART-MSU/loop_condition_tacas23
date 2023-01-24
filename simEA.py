from z3 import *
import numpy as np
import sys

print('Generate SAT query for Simulation Relation')


size_A=int(2)
size_B=int(3)
n=int(2)
k=int(3)

### The SOLVER ###
# Solver().MODEL_COMPLETION = True
solver=Solver()


print('== allocate variables ==')

a_states = []
a_labels = []
b_states = []
b_labels = []
x_states = []
x_labels = []
y_states = []
y_labels = []

for i in range(size_A):
    a_states.append(Int("s"+ str(i)))
    solver.add(Int("s"+ str(i)) == i)
    a_labels.append(String('L(s'+str(i)+')'))

for i in range(size_B):
    b_states.append(Int("q"+ str(i)))
    solver.add(Int("q"+ str(i)) == i)
    b_labels.append(String('L(q'+str(i)+')'))

for i in range(n):
    x_states.append(Int("x"+ str(i)))
    x_labels.append(String('L(x'+str(i)+')'))

for i in range(k):
    y_states.append(Int("y"+ str(i)))
    solver.add(Int("y"+ str(i)) == i) ## for now
    y_labels.append(String('L(y'+str(i)+')'))


sim_vars = []
for i in range(n):
    for j in range(k):
        if(j == k):
            break
        sim_vars.append(Bool("sim" + str(i) + "-" + str(j)))


print(a_states)
print(b_states)
print(x_states)
# print(x_labels)
print(y_states)
# print(y_labels)
# print(sim_states)
print(sim_vars)
# print(sim_labels)
# print()
#####################################


print('== Construct Transition Relations ==')
R1 = []
R2 = []
Rx = []
Ry = []

for i in range(size_A):
    for j in range(size_A):
        R1.append(Bool("R1(s" + str(i) + "-s" + str(j) + ")"))

for i in range(k):
    for j in range(k):
        R2.append(Bool("R2(q" + str(i) + "-q" + str(j) + ")"))

# print(R1)
# print(R2)

print('== User Define Labeling Functions and Transitions ==')

solver.add(a_labels[0]=='(empty)')
solver.add(a_labels[1]=='a')

# solver.add(y_labels[0]=='(empty)')
# solver.add(y_labels[1]=='a')
# solver.add(y_labels[2]=='(empty)')

solver.add(y_labels[0]=='b')
solver.add(y_labels[1]=='b')
solver.add(y_labels[2]=='b')

"""
Define transitions, all the undefined transitions will be detault to 'fault'
"""
########## user define ##########
input_R1 = np.zeros((n,n), dtype=bool)
input_R1[0][1] = True
input_R1[1][0] = True
# input_R1[1][3] = True
# input_R1[2][4] = True
# input_R1[3][0] = True
# input_R1[4][0] = True


input_R2 = np.zeros((k,k), dtype=bool)
input_R2[0][1] = True
input_R2[1][2] = True
input_R2[2][1] = True
# input_R2[1][3] = True
# input_R2[2][0] = True
# input_R2[3][0] = True

###############################

# def define_R_1():
for i in range(size_A):
    for j in range(size_A):
        if(input_R1[i][j]):
            solver.add(R1[i*size_A +j] == True)
        else:
            solver.add(R1[i*size_A +j] == False)

# def define_R_2():
for i in range(size_B):
    for j in range(size_B):
        if(input_R2[i][j]):
            solver.add(R2[i*size_B +j] == True)
        else:
            solver.add(R2[i*size_B +j] == False)


print('== SAT Formulas for EA Simulation Relation ==')

##### All states are legal states. #####
def P(x_i):
    return Or([x_i == (x) for x in a_states])
def Q(y_i):
    return Or([y_i == (y) for y in b_states])
all_states = And(And([P(x) for x in x_states]),
                 And([Q(y) for y in y_states]))
solver.add(all_states)

##### Exhaustive exploration for Model_B #####
exhausive_explore = And([And([ (Implies(Not(j == r),Not(y_states[j] == y_states[r]))
    ) for j in range(k)]
    ) for r in range(k)])
solver.add(exhausive_explore)


##### The initial P state simulates all initial Q states. #####
init_condition = And((x_states[0] == 0),
                 And( [ Implies((y_states[j] == 0),
                 (sim_vars[(0*k)+j] == True)) for j in range(k) ] ))
solver.add(init_condition)


# a helper to check if (curr, next) is a valid transition in R1
def check_Relation_R1(curr, next):
    return And( [ (Implies( And((curr == i), (next == j)) , Bool('R1(s'+str(i)+'-s'+str(j)+')')))
                        for i in range(size_A) for j in range (size_A) ])

###### succ_T(x, x') definition #####
def all_successors(curr, next):
    return And([Implies(sim_vars[curr*k + j],
           And([Implies(R2[j*k +t], sim_vars[next*k + t]) for t in range(k) ]))
                                                          for j in range(k)])
##### Two Requirements for EA simulation #####
x_plus_one = And([ And( check_Relation_R1(x_states[i], x_states[i+1]),
                        all_successors(i, i+1)) for i in range(n-1) ])
x_jump_back = Or([ And( check_Relation_R1(x_states[n-1], x_states[i]),
                        all_successors(n-1, i)) for i in range(n-1) ])

solver.add(x_plus_one)
solver.add(x_jump_back)

##### Relational state predicates are fulfilled by simulation. #####
# a helper to check if (x, j) are having same labels
def check_Labels_eq(x, j):
    return And([Implies( (x == (i)), (a_labels[i] == y_labels[j])) for i in range(size_A) ])

def check_Labels_neq(x, j):
    return And([Implies( (x == (i)), Not(a_labels[i] == y_labels[j])) for i in range(size_A) ])


relational_pred = And([Implies(sim_vars[(i*k) + j],
                    check_Labels_neq(x_states[i], j))for i in range(n) for j in range(k)])
solver.add(relational_pred)



# print('############ (debug) ############')
# print(solver.check())
# m = solver.model()
# print(m)
# sys.exit()


print('== Z3 Solve ==')
print("solving formulas...")
print("z3 solve result: " + str(solver.check()))

# solver.add()
# checkthis = Exists(sim_states[0][0], True)
# solver.add(checkthis)
# print(solver.check())
print('\n== Evaluation ==')
if (str(solver.check()) != "unsat"):
    # m = solver.model().sexpr()
    m = solver.model()
    # print(m)

    # for t in range(n):
    print('(simulation relation:)')
    for i in range(n*k):
            if "True" in str(m.evaluate(sim_vars[i], model_completion=True)):
                print(str(sim_vars[i]))

    print('(x states)')
    for i in range(n):
            print("x"+str(i) + ": s"+str(m.evaluate(x_states[i], model_completion=True)))

    print('(y states)')
    for i in range(k):
            print("y"+str(i) + ": q"+str(m.evaluate(y_states[i], model_completion=True)))

    # print(R1)
    # for i in range(n):
    #     for j in range(n):
    #         print("R1("+str(i)+str(j) + "): "+str(m.evaluate(R1[i][j], model_completion=True)))


    # print(R2)
    # for i in range(k):
    #     for j in range(k):
    #         print("R2("+str(i)+str(j) + "): "+str(m.evaluate(R2[i][j], model_completion=True)))


    # print("DEBUG check" + ": " + str(m.evaluate(Bool("R(sim"+str(0)+str(0)+"-sim"+str(1)+str(0)+")"), model_completion=True)))
    # print("DEBUG check" + ": " + str(m.evaluate(Bool("R(sim"+str(1)+str(0)+"-sim"+str(2)+str(0)+")"), model_completion=True)))
    # print("DEBUG check" + ": " + str(m.evaluate(R2[0][0], model_completion=True)))
    # data = str(m)
    # # print(data)
    # data = " " +data[1:len(data)-1]
    # # print(data)
    # data = data.split(",")
    # data = sorted(data)
    # for d in data:s
        # if "False" in d:
            # if "x" in d:
                # if "L" not in d:
                    # print(d + "\n")
    # print()
    print("SAT, simulation relation is as shown above.")
else:
    print("UNSAT, simulation relation unavailable.")



print('\n(END)')
