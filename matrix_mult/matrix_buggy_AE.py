from z3 import *
import numpy as np
import sys
import re

# print('Generate SAT query for Simulation Relation')
print('\n\n[ case: (A_small, E_big) MM w/ bug ]')

size_A=int(27)
size_B=int(27)
n=int(27)
k=int(27)


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

# print('== User Define Labeling Functions and Transitions ==')
########## user define ##########
solver.add(a_labels[0]=='a[1,2,3,4],b[5,6],c[?,?]') # i = 0
solver.add(a_labels[1]=='(wait)')
solver.add(a_labels[2]=='while(i<m)') # while (i < m)
solver.add(a_labels[3]=='(wait)')
solver.add(a_labels[4]=='(wait)') # j = 0
solver.add(a_labels[5]=='(wait)')
solver.add(a_labels[6]=='while(j<p)') # while (j < p)
solver.add(a_labels[7]=='(wait)')
solver.add(a_labels[8]=='(wait)') # k = 0
solver.add(a_labels[9]=='a[1,2,3,4],b[5,6],c[0,0]') # c[i*p+j] = 0
solver.add(a_labels[10]=='(wait)')
solver.add(a_labels[11]=='while(k<n)') # while (k < n)
solver.add(a_labels[12]=='(wait)')
solver.add(a_labels[13]=='(wait)')
solver.add(a_labels[14]=='(wait)')
solver.add(a_labels[15]=='(wait)')
solver.add(a_labels[16]=='a[1,2,3,4],b[5,6],c[5,?]') # c[i*p+j] += a[i*n+k] * b[k*p+j]
solver.add(a_labels[17]=='a[1,2,3,4],b[5,6],c[17,?]') # k = k+1
solver.add(a_labels[18]=='a[1,2,3,4],b[5,6],c[17,15]') # c[i*p+j] += a[i*n+k] * b[k*p+j]
solver.add(a_labels[19]=='a[1,2,3,4],b[5,6],c[17,39]') # c[i*p+j] += a[i*n+k] * b[k*p+j]
solver.add(a_labels[20]=='k++') #k++
solver.add(a_labels[21]=='(wait)') # jmp l4
solver.add(a_labels[22]=='j++') # j = j+1
solver.add(a_labels[23]=='(wait)') # jmp l4
solver.add(a_labels[24]=='i++') # j = j+1
solver.add(a_labels[25]=='(wait)') # jump l2
solver.add(a_labels[26]=='return 0') # return 0

input_R1 = np.zeros((n,n), dtype=bool)
input_R1[0][1] = True
input_R1[1][2] = True
input_R1[2][3] = True
input_R1[3][4] = True
input_R1[4][5] = True
input_R1[5][6] = True
input_R1[6][7] = True
input_R1[7][8] = True

# input_R1[8][8] = True
input_R1[8][9] = True
input_R1[9][10] = True
input_R1[10][11] = True
input_R1[11][12] = True
input_R1[12][13] = True
input_R1[13][14] = True
input_R1[14][15] = True
input_R1[15][16] = True
input_R1[15][17] = True
input_R1[15][18] = True
input_R1[15][19] = True

input_R1[16][20] = True
input_R1[17][20] = True
input_R1[18][20] = True
input_R1[19][20] = True
# input_R1[20][20] = True
input_R1[20][11] = True

input_R1[11][21] = True
input_R1[21][22] = True

input_R1[22][6] = True
input_R1[6][24] = True
input_R1[24][25] = True
input_R1[25][1] = True
input_R1[1][26] = True
input_R1[26][26] = True




solver.add(y_labels[0]=='a[1,2,3,4],b[5,6],c[?,?]') # i = 0
solver.add(y_labels[1]=='(wait)') # set i_l2 = i, set j_l2 = j, set k_l2 = k, set c_l2 = c
solver.add(y_labels[2]=='while(i<m)') # cjmp i < m_lo2
solver.add(y_labels[3]=='(wait)') # jmp_l2
solver.add(y_labels[4]=='(wait)') # j = 0
solver.add(y_labels[5]=='(wait)') # set j_l4 = j, set k_l4 = k, set c_l4 = c
solver.add(y_labels[6]=='while(j<p)') # cjmp j < p_lo4
solver.add(y_labels[7]=='(wait)') # jmp l4
solver.add(y_labels[8]=='(wait)') # k = 0, r1 = i*p, r2 = r1 + j
solver.add(y_labels[9]=='a[1,2,3,4],b[5,6],c[0,0]') # c[r2] = 0
solver.add(y_labels[10]=='(wait)') # set k_l7 = k, set c_l7 = c
solver.add(y_labels[11]=='while(k<n)') # cjmp k < n_l07, jmp l7
solver.add(y_labels[12]=='(wait)') # jmp_l7
solver.add(y_labels[13]=='(wait)') # r3 = i*p, r4 = r3 + j
solver.add(y_labels[14]=='(wait)') # r5 = c[r4]
solver.add(y_labels[15]=='(wait)') # r6 = i*n, r7 = r6 + k
solver.add(y_labels[16]=='a[1,2,3,4],b[5,6],c[5,?]') # r8 = a[r7]
solver.add(y_labels[17]=='a[1,2,3,4],b[5,6],c[17,?]') # r9 = k*p, r10 = r9 + j, r11 = b[r10], r12 = r8 * r11, r13 = r5 + r12, r14 = i*p, r15 = r14 + j
solver.add(y_labels[18]=='a[1,2,3,4],b[5,6],c[17,15]') # c[r16] = r15
solver.add(y_labels[19]=='a[1,2,3,4],b[5,6],c[17,39]') # c[r16] = r15
solver.add(y_labels[20]=='k++') # k = k+1
solver.add(y_labels[21]=='(wait)') # jmp l4
solver.add(y_labels[22]=='j++') # j = j+1
solver.add(y_labels[23]=='(wait)') # jmp l4
solver.add(y_labels[24]=='i++') # i = i+1
solver.add(y_labels[25]=='(wait)') # jump l2
solver.add(y_labels[26]=='return 0') # return 0

input_R2 = np.zeros((k,k), dtype=bool)
input_R2[0][1] = True
input_R2[1][2] = True
input_R2[2][3] = True
input_R2[3][4] = True
input_R2[4][5] = True
input_R2[5][6] = True
input_R2[6][7] = True
input_R2[7][8] = True

# input_R2[8][8] = True

input_R2[8][9] = True
input_R2[9][10] = True
input_R2[10][11] = True
input_R2[11][12] = True
input_R2[12][13] = True
input_R2[13][14] = True
input_R2[14][15] = True
input_R2[15][16] = True
input_R2[15][17] = True
input_R2[15][18] = True
input_R2[15][19] = True

input_R2[16][20] = True
input_R2[17][20] = True
input_R2[18][20] = True
input_R2[19][20] = True
input_R2[20][20] = True # bug, loop is not correctly updated

# input_R2[20][11] = True

input_R2[11][21] = True
input_R2[21][22] = True

input_R2[22][6] = True
input_R2[6][24] = True
input_R2[24][25] = True
input_R2[24][25] = True
input_R2[25][1] = True
input_R2[1][26] = True
input_R2[26][26] = True

### Define transitions, all the undefined transitions will be detault to 'fault'






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


##### (1) All states are legal states. #####
def P(x_i):
    return Or([x_i == (x) for x in a_states])
def Q(y_i):
    return Or([y_i == (y) for y in b_states])
all_states = And(And([P(x) for x in x_states]),
                 And([Q(y) for y in y_states]))
solver.add(all_states)

##### (2) Exhaustive exploration for Model_A #####
exhausive_explore = And([And([ (Implies(Not(j == r),Not(x_states[j] == x_states[r]))
    ) for j in range(n)]
    ) for r in range(n)])
solver.add(exhausive_explore)


##### (3) All initial P states should be simulated by some initial Q states. #####
init_condition = And([Implies(x_states[i] == 0,
                 Or( [ And((y_states[j] == 0),
                 (sim_vars[(0*k)+j] == True)) for j in range(k) ] ) ) for i in range(n)])
solver.add(init_condition)


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
    return And( [ And((Implies( And((curr == i), (next == r)) , And(Bool('R2(q'+str(i)+'-q'+str(r)+')'),Bool('sim'+str(x_t)+"-" + str(r)) ) )))
                        for i in range(size_B) for r in range (size_B) ])

def exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+ "-" + str(j)),
            (Or([ check_Relation_R2_and_sim(y_states[j], y_states[r], x_t)for r in range(k)])))
                            for j in range(k)] )



def simple_exists_one_matching_succ(x_i, x_t):
    return And([ Implies(Bool('sim'+str(x_i)+ "-" + str(j)),
            (Or([ And(Bool('R2(q'+str(j)+'-q'+str(r)+')'), Bool('sim'+str(x_t)+ "-" + str(r)))
                            for r in range(k)])))
                            for j in range(k)] )

# print(exists_one_matching_succ(1, 1))
# all_succ = And([ Implies(check_Relation_R1(x_states[i], x_states[t]) , exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])

### A simplified version, don't allow full freedom of allocating states
all_succ = And([ Implies( Bool('R1(s'+str(i)+'-s'+str(t)+')') , simple_exists_one_matching_succ(i, t)) for i in range(n) for t in range(n)])
# print(all_succ)
solver.add(all_succ)

# all_succ = And([check_Relation_R1(x_states[i], x_states[i+1]) for i in range(n-1)])
# print(all_succ)
##### Relational state predicates are fulfilled by simulation. #####
# a helper to check if (x, j) are having same labels
def check_Labels(x, j):
    return And([Implies( (x == (i)), (a_labels[i] == y_labels[j])) for i in range(size_A) ])


relational_pred = And([Implies( sim_vars[(i*k) + j],
                    check_Labels(x_states[i], j))for i in range(n) for j in range(k)])
solver.add(relational_pred)

# print(relational_pred)
# print('############ (debug) ############')
# print(solver.check())
# m = solver.model()
# print(m)
# sys.exit()

# print('== Z3 Solve ==')
print("building formulas...")

# solver.add(all_states)
# solver.add(exhausive_explore)
# solver.add(init_condition)
# solver.add(all_succ)
# solver.add(relational_pred)


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
    print('|P|  = ' + str(size_A))
    print('|Q|  = ' + str(size_B))



print('\n(END)')
