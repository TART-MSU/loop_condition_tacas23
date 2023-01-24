from z3 import *
import numpy as np
import sys
import re

# print('Generate SAT query for Simulation Relation')
print('\n\n[ case: (A_small, E_big) CBF w/o bug ]')

size_A=int(15)
size_B=int(9)
n=int(15)
k=int(9)


### The SOLVER ###
# Solver().MODEL_COMPLETION = True
solver=Solver()


# print('== Allocate variables ==')

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
    solver.add(Int("x"+ str(i)) == i) ## easy visulization

for i in range(k):
    y_states.append(Int("y"+ str(i)))
    y_labels.append(String('L(y'+str(i)+')'))
    solver.add(Int("y"+ str(i)) == i) ## easy visulization


sim_vars = []
for i in range(n):
    for j in range(k):
        if(j == k):
            break
        sim_vars.append(Bool("sim" + str(i) + "-" + str(j)))


# print(a_states)
# print(b_states)
# print(x_states)
# print(x_labels)
# print(y_states)
# print(y_labels)
# print(sim_states)
# print(sim_vars)
# print(sim_labels)
# print()
#####################################


# print('== Construct Transition Relations ==')
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

# arr = [0, 1, 2, 3, 4] # size=5 j=0..6

# print('== User Define Labeling Functions and Transitions ==')
########## user define ##########
solver.add(a_labels[0]=='a:(null), b:(null)')

solver.add(a_labels[1]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[2]=='a:(0), b:(4), size:(5)')

solver.add(a_labels[3]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[4]=='a:(0), b:(5), size:(5)') # j == size-1

solver.add(a_labels[5]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[6]=='a:(0), b:(5), size:(5)') # j > size-1

solver.add(a_labels[7]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[8]=='a:(0), b:(3), size:(5)')

solver.add(a_labels[9]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[10]=='a:(0), b:(2), size:(5)')

solver.add(a_labels[11]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[12]=='a:(0), b:(1), size:(5)')

solver.add(a_labels[13]=='a:(0), b:(null), size:(5)')
solver.add(a_labels[14]=='a:(0), b:(0), size:(5)')


# solver.add(Bool('sim22') == True)

solver.add(b_labels[0]=='a:(null), b:(null)')

solver.add(b_labels[1]=='a:(0), b:(null), size:(5)')

solver.add(b_labels[2]=='a:(0), b:(4), size:(5)')
solver.add(b_labels[3]=='a:(0), b:(5), size:(5)') # j == size-1
solver.add(b_labels[4]=='a:(0), b:(5), size:(5)') # j > size-1
solver.add(b_labels[5]=='a:(0), b:(3), size:(5)')
solver.add(b_labels[6]=='a:(0), b:(2), size:(5)')
solver.add(b_labels[7]=='a:(0), b:(1), size:(5)')
solver.add(b_labels[8]=='a:(0), b:(0), size:(5)')

### Define transitions, all the undefined transitions will be detault to 'fault'
input_R1 = np.zeros((size_A,size_A), dtype=bool)
input_R1[0][1] = True
input_R1[1][2] = True
input_R1[2][2] = True

input_R1[0][3] = True
input_R1[3][4] = True
input_R1[4][4] = True

input_R1[0][5] = True
input_R1[5][6] = True
input_R1[6][6] = True

input_R1[0][7] = True
input_R1[7][8] = True
input_R1[8][8] = True

input_R1[0][9] = True
input_R1[9][10] = True
input_R1[10][10] = True

input_R1[0][11] = True
input_R1[11][12] = True
input_R1[12][12] = True

input_R1[0][13] = True
input_R1[13][14] = True
input_R1[14][14] = True


input_R2 = np.zeros((size_B,size_B), dtype=bool)
input_R2[0][1] = True
input_R2[1][2] = True
input_R2[1][3] = True
input_R2[1][4] = True
input_R2[1][5] = True
input_R2[1][6] = True
input_R2[1][7] = True
input_R2[1][8] = True

input_R2[2][2] = True
input_R2[3][3] = True
input_R2[4][4] = True
input_R2[5][5] = True
input_R2[6][6] = True
input_R2[7][7] = True
input_R2[8][8] = True


###############################
for i in range(size_A):
    for j in range(size_A):
        if(input_R1[i][j]):
            solver.add(R1[i*size_A +j] == True)
        else:
            solver.add(R1[i*size_A +j] == False)

for i in range(size_B):
    for j in range(size_B):
        if(input_R2[i][j]):
            solver.add(R2[i*size_B +j] == True)
        else:
            solver.add(R2[i*size_B +j] == False)



# print('adding constraints')
# print( And([(Implies( And(('x'+str(1) == i), (next == j)) , Bool('R1(s'+str(i)+'-s'+str(j)+')')))
#                     for i in range(size_A) for j in range (size_A) ]))

# print('== SAT Formulas for AE Simulation Relation ==')


##### All states are legal states. #####
def P(x_i):
    return Or([x_i == (x) for x in a_states])
def Q(y_i):
    return Or([y_i == (y) for y in b_states])
all_states = And(And([P(x) for x in x_states]),
                 And([Q(y) for y in y_states]))

##### Exhaustive exploration for Model_A #####
exhausive_explore = And([And([ (Implies(Not(j == r),Not(x_states[j] == x_states[r]))
    ) for j in range(n)]
    ) for r in range(n)])


##### All initial P states should be simulated by some initial Q states. #####
init_condition = And([Implies(x_states[i] == 0,
                 Or( [ And((y_states[j] == 0),
                 (sim_vars[(0*k)+j] == True)) for j in range(k) ] ) ) for i in range(n)])
# solver.add('sim00' == True)



###### succ_T(x, x') definition #####
# a helper to check if (curr, next) is a valid transition in R1
def check_Relation_R1(curr, next):
    return And( [ (Implies( And((curr == i), (next == j)) , Bool('R1(s'+str(i)+'-s'+str(j)+')')))
                        for i in range(size_A) for j in range (size_A) ])
# a helper to check if (curr, next) is a valid transition in R2
def check_Relation_R2(curr, next):
    return And( [ (Implies( And((curr == i), (next == j)) , Bool('R2(q'+str(i)+'-q'+str(j)+')')))
                        for i in range(size_B) for j in range (size_B) ])


# def check_Relation_R2_and_sim(curr, next, x_t):
#     return And( [ And((Implies( And((curr == i), (next == r)) , And(Bool('R2(q'+str(i)+'-q'+str(j)+')'),Bool('sim'+str(x_t)+str(r)) ) )))
#                         for i in range(size_B) for r in range (size_B) ])

def check_Relation_R2_and_sim(curr, next, x_t):
    return And( [ And((Implies( And((curr == i), (next == r)) , And(Bool('R2(q'+str(i)+'-q'+str(r)+')'),Bool('sim'+str(x_t)+ "-" +str(r)) ) )))
                        for i in range(size_B) for r in range (size_B) ])

def exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+"-" +str(j)),
            (Or([ check_Relation_R2_and_sim(y_states[j], y_states[r], x_t)for r in range(k)])))
                            for j in range(k)] )

def simple_exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+"-" +str(j)),
            (Or([ And(Bool('R2(q'+str(j)+'-q'+str(r)+')'), Bool('sim'+str(x_t)+"-" +str(r)))
                            for r in range(k)])))
                            for j in range(k)] )

# print(exists_one_matching_succ(1, 1))
# all_succ = And([ Implies(check_Relation_R1(x_states[i], x_states[t]) , exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])

### A simplified version, don't allow full freedom of allocating states
all_succ = And([ Implies( Bool('R1(s'+str(i)+'-s'+str(t)+')') , simple_exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])
# print(all_succ)
# solver.add(all_succ)


# all_succ = And([check_Relation_R1(x_states[i], x_states[i+1]) for i in range(n-1)])
# print(all_succ)
##### Relational state predicates are fulfilled by simulation. #####
# a helper to check if (x, j) are having same labels
# def check_Labels(x, j):
#     return And([Implies( (x == (i)), (a_labels[i] == y_labels[j])) for i in range(size_A) ])

def check_Labels(x, j):
    return And([Implies( (x == (i)), (a_labels[i] == b_labels[j])) for i in range(size_A) ]) ### check again

relational_pred = And([Implies( sim_vars[(i*k) + j],
                    check_Labels(x_states[i], j))for i in range(n) for j in range(k)])

# print(relational_pred)


# print('== Z3 Solve ==')
print("building formulas...")

# solver.add(all_states)
solver.add(exhausive_explore)
solver.add(init_condition)
solver.add(all_succ)
solver.add(relational_pred)



# print('############ (debug) ############')
# print(solver.check())
# m = solver.model()
# print(m)
# sys.exit()

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
    y_count=set()
    # for t in range(n):
    print('(simulation relation:)')
    for i in range(n*k):
            if "True" in str(m.evaluate(sim_vars[i], model_completion=True)):
                print(str(sim_vars[i]))
                ystate = re.findall('-(\d)', str(sim_vars[i]))
                y_count.add(ystate[0])
    # print('(x states)')
    # for i in range(n):
    #         print("x"+str(i) + ": s"+str(m.evaluate(x_states[i], model_completion=True)))
    #
    # print('(y states)')
    # for i in range(k):
    #         print("y"+str(i) + ": q"+str(m.evaluate(y_states[i], model_completion=True)))

    print("SAT, simulation relation is as shown above.")

    print('|P|  = ' + str(size_A))
    print('|Q|  = ' + str(size_B))
    print('|Q\'| = ' + str(len(y_count)))
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
    # print("SAT, simulation relation is as shown above.")
else:
    print("UNSAT, simulation relation unavailable.")



print('\n(END)')
