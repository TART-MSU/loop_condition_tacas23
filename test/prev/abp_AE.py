from z3 import *
import numpy as np
import time


start = time.time()
#get n
print('Generate SAT query for Simulation Relation')

print('Model Sizes:')
n=int(11)
k=int(14)

sys.stdout.write('n='+str(n)+", ")
sys.stdout.write('k='+str(k)+"\nAllocating variables...")

# sys.stdout.write("Allocating variables...")

### The SOLVER ###
# Solver().MODEL_COMPLETION = True
solver=Solver()



a_states = []
b_states = []
x_states = []
x_labels = []
y_states = []
y_labels = []


for i in range(n):
    a_states.append(Bool("s"+ str(i)))
    x_states.append(Bool("x"+ str(i)))
    x_labels.append(Bool("L(x"+ str(i)+")"))


for i in range(k):
    b_states.append(Bool("q"+ str(i)))
    y_states.append(Bool("y"+ str(i)))
    y_labels.append(Bool("L(y"+ str(i)+")"))


# def var_str(i,j):
#     return "sim" + str(i) + str(j)
sim_states = []
sim_labels = []
for i in range(n):
    props = ""
    labels = ""
    for j in range(k):
        props += "sim" + str(i) + str(j)
        labels += "L(sim" + str(i) + str(j) + ")"
        if j != k:
            props += " "
            labels += " "
    sim_states.append(Bools(props))
    sim_labels.append(Bools(labels))

# print("done.")

# print(a_states)
# print(b_states)
# print(x_states)
# print(y_states)
# print(sim_states)
# print(sim_labels)
# print()

#####################################
# == Helper Functions ==
def Q(x_i):
    return Or([x_i == a for a in a_states])

def P(y_i):
    return Or([y_i == b for b in b_states])
#####################################


# print('Construct Transition Relations...', end = '')
R1 = []
R2 = []
Rsim = []
def construct_R_1():
    for i in range(n):
        tr = ""
        for j in range(n):
            tr += "R1(x" + str(i) + "-x" + str(j) + ") "
        R1.append(Bools(tr))

def construct_R_2():
    for i in range(k):
        tr = ""
        for j in range(k):
            tr += "R2(y" + str(i) + "-y" + str(j) + ") "
        R2.append(Bools(tr))


temp_sim_R = [] ##temp...not a good solution
def construct_R_sim():
    for i in range(n):
        for j in range(n):
            temp_tr = ""
            for t in range (k):
                tr = ""
                for r in range (k):
                    tr += ("R(sim" + str(i) + str(t) + "-sim" + str(j) + str(r) + ") ")
                Rsim.append(Bools(tr))
                temp_tr += tr
            temp_sim_R.append(Bools(temp_tr))
                    # tr += "R(sim" + str(i) + str(count) + ",sim" + str(i+j) + str(count) + ") "

construct_R_1()
construct_R_2()
construct_R_sim()


sys.stdout.write("done.\nBuilding user defined models...")
# print("done.")
################################# USER DEFINED ######################################

# print("Building user defined models...", end = "")

# print('== User Defined Propositions')
S_send_p0 = Bool("S_send_p0")
S_send_p1 = Bool("S_send_p1")
S_recv_a0 = Bool("S_recv_a0")
S_recv_a1 = Bool("S_recv_a1")

R_recv_p0 = Bool("R_recv_p0")
R_recv_p1 = Bool("R_recv_p1")
R_send_a0 = Bool("R_send_a0")
R_send_a1 = Bool("R_send_a1")

packet_loss = Bool("packet_loss")
ack_loss = Bool("ack_loss")
timeout = Bool("timeout")

# print('== User Defined Labeling Functions and  Model Transitions ==')
x_labels = {}
# def define_L_1():
x_labels[0] = [S_send_p0]
x_labels[1] = [R_recv_p0]
x_labels[2] = [R_send_a0]
x_labels[3] = [S_recv_a0]
x_labels[4] = [S_send_p1]
x_labels[5] = [packet_loss]
x_labels[6] = [timeout]
x_labels[7] = [R_recv_p1]
x_labels[8] = [R_send_a1]
x_labels[9] = [ack_loss]
x_labels[10] = [S_recv_a1]

# user define R1
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


y_labels = {}
# def define_L_2():
y_labels[0] = [S_send_p0]
y_labels[1] = [packet_loss]
y_labels[2] = [timeout]
y_labels[3] = [S_recv_a0]
y_labels[4] = [S_send_p1]
y_labels[5] = [packet_loss]
y_labels[6] = [timeout]
y_labels[7] = [S_recv_a1]

y_labels[8] = [R_recv_p0]
y_labels[9] = [R_send_a0]
y_labels[10] = [ack_loss]
y_labels[11] = [R_recv_p1]
y_labels[12] = [R_send_a1]
y_labels[13] = [ack_loss]

input_R2 = np.zeros((k,k), dtype=bool)

#sender
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

#
#
#
# input_R2[2][1] = True
# input_R2[2][3] = True
# input_R2[3][2] = True
# print(input_R2)

# model defined
# define_L_1()
# define_L_2()
# define_L_sim()

# print(x_labels)
# print(y_labels)

# print('== User Defined Model Transitions ==')
# # user define R1
# input_R1 = np.zeros((n,n), dtype=bool)
# input_R1[0][1] = True
# input_R1[1][0] = True
# # print(input_R1)



############################################################################
def define_R_1():
    for i in range(n):
        for j in range(n):
            if(input_R1[i][j]):
                solver.add(R1[i][j] == True)
            else:
                solver.add(R1[i][j] == False)


def define_R_2():
    for i in range(k):
        for j in range(k):
            if(input_R2[i][j]):
                solver.add(R2[i][j] == True)
            else:
                solver.add(R2[i][j] == False)

def define_R_sim():
    solver.add(And([And([And([Rsim[t+(i*k)][r] == R2[t][r] for r in range (k)]
        ) for t in range(k)]
        ) for i in range(n*n)]))



def define_R_Transition():
    for a in range(n):
        for b in range(k):
            for i in range(n):
                for j in range(k):
                    # solver.add(And(sim_states[a][b], sim_states[i][j]) == R2[b][j])
                    solver.add(And(sim_states[a][b], sim_states[i][j], R2[b][j], R1[a][i])
                        == Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"))


# print(Rsim)

# print(And([And([And([(Rsim[t+(i*k)][r] == R2[t][r]) for r in range (k)]
#         ) for t in range(k)]
#         ) for i in range(n*n)]))

# print(And([And([And([(Rsim[t+(i*k)][r] == R2[t][r]) for r in range (k)]
#         ) for t in range(k)]
#         ) for i in range(n*n)]))

# def define_R_Transition():
#     for a in range(n):
#         for b in range(k):
#             for i in range(n):
#                 for j in range(k):
#                     # solver.add(And(sim_states[a][b], sim_states[i][j]) == R2[b][j])
#                     solver.add(And(sim_states[a][b], sim_states[i][j], R2[b][j], R1[a][i]) == Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"))
#                     # solver.add(Implies(R2[b][j], Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")")))
                    # GOOD: solver.add(And(sim_states[a][b], sim_states[i][j]) == Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"))

                    # solver.add(And(sim_states[a][b], sim_states[i][j]) == Or(Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"), R2[b][j]))

                    # solver.add(Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")") == And(sim_states[a][b], sim_states[i][j]))
                    # print((Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")") == And(sim_states[a][b], sim_states[i][j])))
                    # print(str(sim_states[a][b]) + "-" + str(sim_states[i][j]) + " " + str(Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")")))
# solver.add(sim_states[1][0] == False)
# solver.add(sim_states[0][0] == True)
# solver.add(sim_states[1][0] == False)
# solver.add(sim_states[2][0] == False)
# solver.add(sim_states[3][0] == False)
# solver.add(sim_states[4][0] == False)
# def define_R_Transition():
#     solver.add(And([And([And([Implies((And(sim_states[t//k][t],sim_states[i%n][r])), Rsim[(i*k)+t][r]
#         ) for r in range(k)]
#         ) for t in range(k)]
#         ) for i in range(n)]))

# print("done.")


sys.stdout.write("done.\nSolving simulation formulas...")

start_solving = time.time()

# print("done.\n","Solving simulation formulas...",end = "")
# print("Solving simulation formulas...", end = "")

# print(And([And([And([Implies(((sim_states[(t//k)+(i//n)][t] == sim_states[i%n][r])), Rsim[(i*k)+t][r]
#         ) for r in range(k)]
#         ) for t in range(k)]
#         ) for i in range(n)]))

# print(sim_states)


# print('== SAT Formula for Simulation Relation ==')
alpha_1 = And(And([Q(x) for x in x_states]), And([P(y) for y in y_states]))

alpha_2 = And([And([Implies(sim_states[i][j],Or([y_states[t] for t in range(k)])
    ) for j in range(k)]
    ) for i in range(n)])

# alpha_3 = And([And([ Implies(sim_states[i][j], x_labels[i] == sim_labels[i][j]) for j in range(k)]
# ) for i in range(n)])

alpha_3 = And([And([ Implies(sim_states[i][j], (x_labels[i] == y_labels[j])
    ) for j in range(k)]
    ) for i in range(n)])

# print(alpha_3)

# Good
alpha_4 = And([And(
        [Implies(R1[i][j],
            Or([Or([Rsim[(j*k)+(i*k*n)+t][r] for r in range(k)]
            ) for t in range(k)])
        ) for j in range(n)]
        ) for i in range(n)])


# New
alpha_4_new = And([And(
        [(R1[i][j] == And([Implies(sim_states[i][t], Or([Bool("R(sim"+str(i)+str(t)+"-sim"+str(j)+str(r)+")")
             for r in range(k) ])) for t in range(k)])
            ) for j in range(n)]
            ) for i in range(n)])



# print(alpha_4)
# alpha_4 = And([And(
#         [Implies(R1[i][j],
#             Or([Or([Rsim[((j+i)*k)+t+(i*k*k)][r] for r in range(k)]
#             ) for t in range(k)])
#         ) for j in range(n)]
#         ) for i in range(n)])
# print(Rsim)
# alpha_4 = And([And(
#         [Implies(R1[i][j],
#             And([Implies(sim_states[i][t],Or([Rsim[((j+i)*k)+t+(i*k*k)][r] for r in range(k)])
#             ) for t in range(k)])
#         ) for j in range(n)]
#         ) for i in range(n)])


# print('== Z3 Solve ==')
# print("solving alpha_1 to alpha_4 with user defined models")
# model defined


define_R_1()
define_R_2()
define_R_Transition()
# solver.push()
solver.add(alpha_1)
solver.add(alpha_2)
solver.add(alpha_3)
# solver.add(alpha_4)
solver.add(alpha_4_new) #better

# initial state matches
# print(sim_states[0][0])
solver.add((sim_states[0][0]))

# print(alpha_4)

solver.add(And([a_states[i] == True for i in range(len(a_states))]))
solver.add(And([b_states[i] == True for i in range(len(b_states))]))
solver.add(And([x_states[i] == True for i in range(len(x_states))]))
solver.add(And([y_states[i] == True for i in range(len(y_states))]))



result = solver.check()

print("done.")



# solver.add()
# checkthis = Exists(sim_states[0][0], True)
# solver.add(checkthis)
# print(solver.check())


print('\n== Summary ==')

print("z3 solve result: " + str(result))

if (str(solver.check()) != "unsat"):
    # m = solver.model().sexpr()
    m = solver.model()
    # print(m)

    # for t in range(n):

    print()
    for i in range(n):
        for j in range(k):
            if "True" in str(m.evaluate(sim_states[i][j], model_completion=True)):
                print("simulate s"+str(i)+ " to q" +str(j) + " : " + str(m.evaluate(sim_states[i][j], model_completion=True)))


    # print(R1)
    # for i in range(n):
    #     for j in range(n):
    #         print("R1("+str(i)+str(j) + "): "+str(m.evaluate(R1[i][j], model_completion=True)))


    # print(R2)
    # for i in range(k):
    #     for j in range(k):
    #         print("R2("+str(i)+str(j) + "): "+str(m.evaluate(R2[i][j], model_completion=True)))


    # for a in range(n):
    #         for b in range(k):
    #             for i in range(n):
    #                 for j in range(k):
    #                     print("Rsim("+str(a)+str(b) + "," +  str(i)+str(j) + "): " + str(m.evaluate(Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"), model_completion=True)))
    #


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
    print("\nSAT, above is the simulation relation.")
else:
    print("\nUNSAT, simulation relation unavailable.")

# print(solver.model())

end = time.time()

print('\nsolving time took: ', str(round(end-start_solving, 3)))

print('total time took: ', str(round(end-start, 3)))

print('\n(END)')
