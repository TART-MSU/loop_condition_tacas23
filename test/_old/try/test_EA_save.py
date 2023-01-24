from z3 import *
import numpy as np
import sys

#get n
print('Generate SAT query for Simulation Relation')

# number of state in M_a
# n=input('n: ')
# while not n.isdigit() or int(n)<1:
#     print('Try again.')
#     n=input('n: ')
n=int(5)

# number of state in M_b
# k=input('k: ')
# while not k.isdigit() or int(n)<1:
#     print('Try again.')
#     k=input('k: ')
k=int(4)


### The SOLVER ###
# Solver().MODEL_COMPLETION = True
solver=Solver()


print('== Build variables ==')

a_states = []
b_states = []

x_states = []
x_labels = []
y_states = []
y_labels = []


for i in range(n):
    # a_states.append(Bool("s"+ str(i)))
    # x_states.append(Bool("x"+ str(i)))
    a_states.append(Int("s"+ str(i)))
    x_states.append(Bool("x"+ str(i)))
    # x_labels.append(Bool("L(x"+ str(i)+")"))
    x_labels.append(str(""))


for i in range(k):
    # b_states.append(Bool("q"+ str(i)))
    # y_states.append(Bool("y"+ str(i)))
    b_states.append(Int("q"+ str(i)))
    y_states.append(Bool("y"+ str(i)))
    # y_labels.append(Bool("L(y"+ str(i)+")"))
    y_labels.append(str(""))


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
    # sim_labels.append(str(labels))

#
# print(a_states)
# print(b_states)
# print(x_states)
# print(x_labels)
# print(y_states)
# print(y_labels)
# print(sim_states)
# print(sim_labels)
# print()


#####################################


print('== Construct Transition Relations ==')
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


print('== User Define Labeling Functions ==')
def define_L_1():
    # solver.add(And((x_labels[0] == ('a' == False)),
    #         (x_labels[1] == ('a' == False)),
    #         (x_labels[2] == ('a' == False)),
    #         (x_labels[3] == ('a' == True)),
    #         (x_labels[4] == ('a' == True))))
    x_labels[0] = ('(empty)');
    x_labels[1] = ('(empty)');
    x_labels[2] = ('(empty)');
    x_labels[3] = ('a');
    x_labels[4] = ('(empty)');


def define_L_2():
    # solver.add(And((y_labels[0] == ('a' == False)),
    #         (y_labels[1] == ('a' == False)),
    #         (y_labels[2] == ('a' == True)),
    #         (y_labels[3] == ('a' == True))))
    y_labels[0] = ('(empty)');
    y_labels[1] = ('(empty)');
    y_labels[2] = ('a');
    y_labels[3] = ('a');


def define_L_sim():
    solver.add(And([And([sim_labels[i][j] == y_labels[j] for j in range(k)])
        for i in range(n)]))


define_L_1()
define_L_2()


# print(x_labels)
# print(y_labels)
# print(sim_labels)
# print('???')


"""
Define transitions, all the undefined transitions will be detault to 'fault'
"""
print('== User Define Transitions ==')
########## user define ##########
input_R1 = np.zeros((n,n), dtype=bool)
input_R1[0][1] = True
input_R1[0][2] = True
input_R1[1][3] = True
input_R1[2][4] = True
input_R1[3][0] = True
input_R1[4][0] = True


input_R2 = np.zeros((k,k), dtype=bool)
input_R2[0][1] = True
input_R2[1][2] = True
input_R2[1][3] = True
input_R2[2][0] = True
input_R2[3][0] = True

###############################

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

def define_R_Transition():
    for a in range(n):
        for b in range(k):
            for i in range(n):
                for j in range(k):
                    solver.add((Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")") ==
                        And(sim_states[a][b], sim_states[i][j], R1[a][i], R2[b][j])))



# print(input_R1)
# print(input_R2)




print('== SAT Formula for Simulation Relation ==')
# Good
# alpha_1 = And(And([Q(x) for x in x_states]), And([P(y) for y in y_states]))


# alpha_2 = And([And([Implies(sim_states[i][j],Or([y_states[t] for t in range(k)])
#     ) for j in range(k)]
#     ) for i in range(n)])

# alpha_3 = And([And([Implies(sim_states[i][j], x_labels[i] == sim_labels[i][j]) for j in range(k)]
# ) for i in range(n)])

# # Good
# alpha_4 = And([And(
#         [(R2[i][j] ==
#             Or([Bool("R(sim"+str(r)+str(i)+"-sim"+str(t)+str(j)+")") for r in range(n)
#              for t in range(n)])
#         ) for j in range(k)]
#         ) for i in range(k)])



#####################################
# == Helper Functions ==
def Q(x_i):
    return Or([x_i == (x) for x in a_states])

def P(y_i):
    return Or([y_i == (y) for y in b_states])




##### • All states are legal states. #####
all_states = And(And([Q(x) for x in x_states]),
                 And([P(y) for y in y_states]))

# print(all_states)
##### • Exhaustive exploration #####
exhausive_explore = And([And([ (Implies(Not(j == r),Not(y_states[j] == y_states[r]))
    ) for j in range(k)]
    ) for r in range(k)])


##### • The initial P state simulates all initial Q states. #####
### initial conditions
init_conidiont = And(And([x_states[i] == True for i in range(len(x_states))]),
                     And([y_states[i] == True for i in range(len(y_states))]),
                     (sim_states[0][0] == True))


##### • Successors in Q are simulated by successors in P. #####
# Good
## all R2 transitions are simulated as a transition in the simulation
# forall_R2 = And([And(
#         [(R2[i][j] ==
#             Or([Bool("R(sim"+str(r)+str(i)+"-sim"+str(t)+str(j)+")") for r in range(n)
#              for t in range(n)])
#         ) for j in range(k)]
#         ) for i in range(k)])

# successors_R2 = And([And(Implies(sim_states[i][j],
#                     (Implies(R2[j][t], sim_states[i+1][t])
#                             for t in range(k)
#                             for j in range(k))
#                             ) for i in range(n)]))

# successors_R2 = ([Implies(R2[j][t],
#                             And([sim_states[i+1][t] for i in range(n-1)
#                             ])
#                             ) for t in range(k)
#                             for j in range(k)])

# all_successors = And([And([Implies(sim_states[i][j],
#                             Implies(R2[i][1], sim_states[i+1][1])
#                             )
#                             for j in range(k)])
#                             for i in range(n-1)])
# print(all_successors)


def all_successors(i, l):
    # print(i, l)
    return And([And([Implies(sim_states[i][j],
    Implies(R2[j][t], sim_states[i+1][t]))
    for j in range(k)])
    for t in range(k)])


# print(all_successors(2, 3))

x_plus_one = [And(R1[i][i+1], all_successors(i, i+1)) for i in range(n-1)]


# print(x_plus_one)


x_jump_back = [Or(R1[n-1][i], all_successors(i, i+1)) for i in range(n-1)]

# x_jump_back = Or( [And([ ((R1[n-1][r]))
#       for j in range(n)]
#     ) for r in range(n)])

# print(x_jump_back)


# print(successors_R2)

# sys.exit()

forall_R2 = And([And(
        [(R2[i][j] ==
            Or([Bool("R(sim"+str(r)+str(i)+"-sim"+str(t)+str(j)+")")
             for r in range(n)
             for t in range(n)])
        ) for j in range(k)]
        ) for i in range(k)])

# print(forall_R2)

# x must be a trace
# update!!
for i in range(n):
    for j in range(n):
        for t in range(n):
            if(j != t):
                solver.add(Implies(Not(x_states[i] == x_states[j]), Not(And(R1[i][j], R1[i][t]))))



##### • Relational state predicates are fulfilled by simulation. #####
# relational_pred = And([And([Implies(sim_states[i][j], x_labels[i] == sim_labels[i][j]) for j in range(k)]
# ) for i in range(n)])
relational_pred = And([And([Implies(sim_states[i][j],
                    x_labels[i] == y_labels[j])
                            for j in range(k)])
                            for i in range(n)])




print("\n\n(debug)")
# print(all_states)

print("\n\n")


print('== Z3 Solve ==')
print("solving alpha_1 to alpha_4 with user defined models")
# model defined
define_L_1()
define_L_2()
# define_L_sim()

define_R_1()
define_R_2()
define_R_Transition()


# solver.push()
solver.add(all_states)
# solver.add(exhausive_explore)
solver.add(relational_pred)
solver.add(forall_R2)
solver.add(init_conidiont)
# solver.add(x_plus_one)
# solver.add(x_jump_back)

# print(alpha_4)

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

    print()
    for i in range(n):
        for j in range(k):
            if "True" in str(m.evaluate(sim_states[i][j], model_completion=True)):
                print("simulate s"+str(i)+ " to q" +str(j) + " : "
                    + str(m.evaluate(sim_states[i][j], model_completion=True)))

    # print(x_states)
    # for i in range(n):
    #         print("x("+str(i) + "): "+str(m.evaluate(x_states[i], model_completion=True)))


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
    print("SAT, simulation relation is as shown above.")
else:
    print("UNSAT, simulation relation unavailable.")

# print(solver.model())

print('\n(END)')

# And([a_states[i] == True for i in range(len(a_states))]),
#                      And([b_states[i] == True for i in range(len(b_states))]),
# (not necessary to check, removed)
# solver.add(one_of_y)
# one_of_y = And([And([Implies(sim_states[i][j],Or([y_states[t] for t in range(k)])
#     ) for j in range(k)]
#     ) for i in range(n)])
