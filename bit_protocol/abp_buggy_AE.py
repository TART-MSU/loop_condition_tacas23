from z3 import *
import numpy as np
import sys
import re

# print('Generate SAT query for Simulation Relation')
print('\n\n[ case: (A_small, E_big) ABP w bug ]')

size_A=int(11)
size_B=int(14)
n=int(11)
k=int(14)

# size_A=int(3)
# size_B=int(2)
# n=int(3)
# k=int(2)

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
        sim_vars.append(Bool("sim" + str(i) + "-"+ str(j)))


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

# print('== User Define Labeling Functions and Transitions ==')




########## user define ##########
solver.add(a_labels[0] == "S_send_p0")
solver.add(a_labels[1] == "R_recv_p0")
solver.add(a_labels[2] == "R_send_a0")
solver.add(a_labels[3] == "S_recv_a0")
solver.add(a_labels[4] == "S_send_p1")
solver.add(a_labels[5] == "packet_loss")
solver.add(a_labels[6] == "timeout")
solver.add(a_labels[7] == "R_recv_p1")
solver.add(a_labels[8] == "R_send_a1")
solver.add(a_labels[9] == "ack_loss")
solver.add(a_labels[10] == "S_recv_a1")



solver.add(y_labels[0] == "S_send_p0")
solver.add(y_labels[1] == "packet_loss")
solver.add(y_labels[2] == "packet_loss") # no timeout
solver.add(y_labels[3] == "S_recv_a0")
solver.add(y_labels[4] == "S_send_p1")
solver.add(y_labels[5] == "packet_loss")
solver.add(y_labels[6] == "packet_loss") # no timeout
solver.add(y_labels[7] == "S_recv_a1")

solver.add(y_labels[8] == "R_recv_p0")
solver.add(y_labels[9] == "R_send_a0")
solver.add(y_labels[10] == "ack_loss")
solver.add(y_labels[11] == "R_recv_p1")
solver.add(y_labels[12] == "R_send_a1")
solver.add(y_labels[13] == "ack_loss")



### Define transitions, all the undefined transitions will be detault to 'fault'
input_R1 = np.zeros((n,n), dtype=bool)
input_R1[0][1] = True
input_R1[1][2] = True
input_R1[2][3] = True
input_R1[3][4] = True

input_R1[4][5] = True
input_R1[4][6] = True
input_R1[4][7] = True

input_R1[5][4] = True
input_R1[6][4] = True
input_R1[7][8] = True

input_R1[8][9] = True
input_R1[8][10] = True

input_R1[9][4] = True

input_R1[10][0] = True


input_R2 = np.zeros((k,k), dtype=bool)
input_R2[0][1] = True
input_R2[0][2] = True
input_R2[0][3] = True
input_R2[0][8] = True
input_R2[0][9] = True
input_R2[0][10] = True
input_R2[0][11] = True
input_R2[0][12] = True
input_R2[0][13] = True

input_R2[1][0] = True
input_R2[1][8] = True
input_R2[1][9] = True
input_R2[1][10] = True
input_R2[1][11] = True
input_R2[1][12] = True
input_R2[1][13] = True

input_R2[2][0] = True
input_R2[2][8] = True
input_R2[2][9] = True
input_R2[2][10] = True
input_R2[2][11] = True
input_R2[2][12] = True
input_R2[2][13] = True

input_R2[3][4] = True
input_R2[3][8] = True
input_R2[3][9] = True
input_R2[3][10] = True
input_R2[3][11] = True
input_R2[3][12] = True
input_R2[3][13] = True

input_R2[4][5] = True
input_R2[4][6] = True
input_R2[4][7] = True
input_R2[4][8] = True
input_R2[4][9] = True
input_R2[4][10] = True
input_R2[4][11] = True
input_R2[4][12] = True
input_R2[4][13] = True

input_R2[5][4] = True
input_R2[5][8] = True
input_R2[5][9] = True
input_R2[5][10] = True
input_R2[5][11] = True
input_R2[5][12] = True
input_R2[5][13] = True

input_R2[6][4] = True
input_R2[6][8] = True
input_R2[6][9] = True
input_R2[6][10] = True
input_R2[6][11] = True
input_R2[6][12] = True
input_R2[6][13] = True

input_R2[7][0] = True
input_R2[7][8] = True
input_R2[7][9] = True
input_R2[7][10] = True
input_R2[7][11] = True
input_R2[7][12] = True
input_R2[7][13] = True


### receiver
input_R2[8][9] = True
input_R2[8][0] = True
input_R2[8][1] = True
input_R2[8][2] = True
input_R2[8][3] = True
input_R2[8][4] = True
input_R2[8][5] = True
input_R2[8][6] = True
input_R2[8][7] = True

input_R2[9][10] = True
input_R2[9][11] = True
input_R2[9][0] = True
input_R2[9][1] = True
input_R2[9][2] = True
input_R2[9][3] = True
input_R2[9][4] = True
input_R2[9][5] = True
input_R2[9][6] = True
input_R2[9][7] = True

input_R2[10][9] = True
input_R2[10][0] = True
input_R2[10][1] = True
input_R2[10][2] = True
input_R2[10][3] = True
input_R2[10][4] = True
input_R2[10][5] = True
input_R2[10][6] = True
input_R2[10][7] = True

input_R2[11][12] = True
input_R2[11][0] = True
input_R2[11][1] = True
input_R2[11][2] = True
input_R2[11][3] = True
input_R2[11][4] = True
input_R2[11][5] = True
input_R2[11][6] = True
input_R2[11][7] = True

input_R2[12][13] = True
input_R2[12][8] = True
input_R2[12][0] = True
input_R2[12][1] = True
input_R2[12][2] = True
input_R2[12][3] = True
input_R2[12][4] = True
input_R2[12][5] = True
input_R2[12][6] = True
input_R2[12][7] = True

input_R2[13][12] = True
input_R2[13][4] = True
input_R2[13][0] = True
input_R2[13][1] = True
input_R2[13][2] = True
input_R2[13][3] = True
input_R2[13][4] = True
input_R2[13][5] = True
input_R2[13][6] = True
input_R2[13][7] = True


# solver.add(a_labels[0]=='(empty)')
# solver.add(a_labels[1]=='a')
# solver.add(a_labels[2]=='a')
#
# solver.add(y_labels[0]=='(empty)')
# solver.add(y_labels[1]=='a')
# # solver.add(y_labels[2]=='(empty)')
#
#
# ########## user define ##########
# input_R1 = np.zeros((n,n), dtype=bool)
# input_R1[0][1] = True
# input_R1[1][0] = True
# input_R1[0][2] = True
# input_R1[2][0] = True
# # input_R1[1][3] = True
# # input_R1[2][4] = True
# # input_R1[3][0] = True
# # input_R1[4][0] = True
#
#
# input_R2 = np.zeros((k,k), dtype=bool)
# input_R2[0][1] = True
# input_R2[1][0] = True
# # input_R2[1][2] = True
# # input_R2[2][1] = True
# # input_R2[1][3] = True
# # input_R2[2][0] = True
# # input_R2[3][0] = True

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
    return And( [ And((Implies( And((curr == i), (next == r)) , And(Bool('R2(q'+str(i)+'-q'+str(r)+')'),Bool('sim'+str(x_t)+"-"+str(r)) ) )))
                        for i in range(size_B) for r in range (size_B) ])

def exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+"-"+str(j)),
            (Or([ check_Relation_R2_and_sim(y_states[j], y_states[r], x_t)for r in range(k)])))
                            for j in range(k)] )

# print(exists_one_matching_succ(1, 1))
# all_succ = And([ Implies(check_Relation_R1(x_states[i], x_states[t]) , exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])

def simple_exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+"-" +str(j)),
            (Or([ And(Bool('R2(q'+str(j)+'-q'+str(r)+')'), Bool('sim'+str(x_t)+"-" +str(r)))
                            for r in range(k)])))
                            for j in range(k)] )

### A simplified version, don't allow full freedom of allocating states
all_succ = And([ Implies( Bool('R1(s'+str(i)+'-s'+str(t)+')') , simple_exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])



# all_succ = And([check_Relation_R1(x_states[i], x_states[i+1]) for i in range(n-1)])
# print(all_succ)
##### Relational state predicates are fulfilled by simulation. #####
# a helper to check if (x, j) are having same labels
def check_Labels(x, j):
    return And([Implies( (x == (i)), (a_labels[i] == y_labels[j])) for i in range(size_A) ])

relational_pred = And([Implies( sim_vars[(i*k) + j],
                    check_Labels(x_states[i], j))for i in range(n) for j in range(k)])

# print(relational_pred)
# print('############ (debug) ############')
# print(solver.check())
# m = solver.model()
# print(m)
# sys.exit()

# print('== Z3 Solve ==')
print("building formulas...")

solver.add(all_states)
solver.add(exhausive_explore)
solver.add(init_condition)
solver.add(all_succ)
solver.add(relational_pred)


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
                ystate = re.findall('-(\d+)', str(sim_vars[i]))
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
