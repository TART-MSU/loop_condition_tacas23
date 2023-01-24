from z3 import *
import numpy as np

#get n
print('Generate SAT query for Simulation Relation')

print('== Models')
### number of state in M_a
# n=input('n: ')
# while not n.isdigit() or int(n)<1:
#     print('Try again.')
#     n=input('n: ')
n=int(2)


### number of state in M_b
# k=input('k: ')
# while not k.isdigit() or int(n)<1:
#     print('Try again.')
#     k=input('k: ')
k=int(4)

print('n =', n)
print('k =', k)


### The SOLVER ###
# Solver().MODEL_COMPLETION = True
solver=Solver()


print('== Initialize Propositions')
prop1    = Bool("a")
prop2    = Bool("b")

print(prop1)

# prop1 = True
# prop2 = True



print('== Build State Variables ==')

## forall model
# a_states = []
x_states = []
for i in range(n):
    # a_states.append(Bool("s"+ str(i)))
    x_states.append(Bool("x"+ str(i)))
    # x_labels.append(Bool("L(x"+ str(i)+")"))



## exists model
# b_states = []
y_states = []
# y_labels = []
for i in range(k):
    # b_states.append(Bool("q"+ str(i)))
    y_states.append(Bool("y"+ str(i)))
    # y_labels.append(Bool("L(y"+ str(i)+")"))
    # y_labels.add("L(y"+ str(i)+")")




# def var_str(i,j):
#     return "sim" + str(i) + str(j)
sim_states = []
sim_labels = []
for i in range(n):
    props = ""
    labels = ""
    for j in range(k):
        props += "sim" + str(i) +"-"+ str(j)
        labels += "L(sim" + str(i) +"-"+ str(j) + ")"
        if j != (k-1):
            props += " "
            labels += " "
    sim_states.append(Bools(props))
    sim_labels.append(Bools(labels))


# print(a_states)
# print(b_states)
print(x_states)
print(y_states)
print(sim_states)
print(sim_labels)
print()


print('== Construct Transition Relations ==')

# def trans_x(pre, post):
#     return "R1(x" + str(pre) + "-x" + str(post) + ")"
#
# def trans_y(pre, post):
#     return "R2(y" + str(pre) + "-y" + str(post) + ")"

# R1.append(Bool(trans_x(0, 1)))
# R1.append(Bool(trans_x(1, 0)))
#
#
# R2.append(Bool(trans_y(0, 1)))
# R2.append(Bool(trans_y(1, 2)))
# R2.append(Bool(trans_y(2, 1)))
# R2.append(Bool(trans_y(2, 3)))
# R2.append(Bool(trans_y(3, 3)))


R1 = []
R2 = []
Rsim = []
def construct_R_1():
    tr.append("R1(x" + str(i) + "-x" + str(j) + ")")
    for i in range(n):
        tr = []
        for j in range(n):
            tr.append("R1(x" + str(i) + "-x" + str(j) + ")")
        R1.append(Bools(tr))

def construct_R_2():
    for i in range(k):
        tr = []
        for j in range(k):
            tr.append("R2(y" + str(i) + "-y" + str(j) + ")")
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

# construct_R_1()
# print(R1)
# construct_R_2()
# print(R2)
# construct_R_sim()
# print(Rsim)
# print(Rsim)




print('== User Define Labeling Functions ==')
x_labels = {}
def define_L_1():
    x_labels[0] = [prop1]
    x_labels[1] = []
    # x_labels[2] = [prop1, prop2]
    # x_labels[3] = [prop1, prop2]
    # x_labels[4] = [prop1, prop2]
    # x_labels["L(x"+ str(0)+")"] = [prop1, prop2]
    # x_labels["L(x"+ str(1)+")"] = [prop1, prop2]
    # x_labels["L(x"+ str(2)+")"] = [prop1, prop2]
    # x_labels["L(x"+ str(3)+")"] = [prop1, prop2]
    # x_labels["L(x"+ str(4)+")"] = [prop1, prop2]


y_labels = {}
def define_L_2():
    y_labels[0] = [prop1]
    y_labels[1] = []
    y_labels[2] = [prop1]
    y_labels[3] = []
    # y_labels["L(y"+ str(0)+")"] = [prop1, prop2]
    # y_labels["L(y"+ str(1)+")"] = [prop1, prop2]
    # y_labels["L(y"+ str(2)+")"] = [prop1, prop2]
    # y_labels["L(y"+ str(3)+")"] = [prop1, prop2]


# def define_L_sim():
#     solver.add(And([And([ sim_labels[i][j] == y_labels[j] for j in range(k)])
#         for i in range(n)]))



# model defined
define_L_1()
define_L_2()
# define_L_sim()

print(x_labels)
print(y_labels)




print('== User Define Transitions ==')
# user define R1
input_R1 = np.zeros((n,n), dtype=bool)
input_R1[0][1] = True
input_R1[1][0] = True


input_R2 = np.zeros((k,k), dtype=bool)
input_R2[0][1] = True
input_R2[1][2] = True
input_R2[2][1] = True
input_R2[2][3] = True
input_R2[3][3] = True



def define_R_1():
    for i in range(n):
        for j in range(n):
            if(input_R1[i][j]):
                solver.add(Bool("R1["+str(i)+"]["+str(j)+"]") == True)
            else:
                solver.add(Bool("R1["+str(i)+"]["+str(j)+"]") == False)


def define_R_2():
    for i in range(k):
        for j in range(k):
            if(input_R2[i][j]):
                solver.add(Bool("R2["+str(i)+"]["+str(j)+"]") == True)
            else:
                solver.add(Bool("R2["+str(i)+"]["+str(j)+"]") == False)
#
# def define_R_sim():
#     solver.add(And([And([And([Rsim[t+(i*k)][r] == R2[t][r] for r in range (k)]
#         ) for t in range(k)]
#         ) for i in range(n*n)]))
#
#
#
# def define_R_Transition():
#     for a in range(n):
#         for b in range(k):
#             for i in range(n):
#                 for j in range(k):
#                     # solver.add(And(sim_states[a][b], sim_states[i][j]) == R2[b][j])
#                     solver.add(And(sim_states[a][b], sim_states[i][j], R2[b][j], R1[a][i])
#                         == Bool("R(sim"+str(a)+str(b)+"-sim"+str(i)+str(j)+")"))

define_R_1()
define_R_2()

# define_R_Transition()



#####################################
# == Helper Functions ==
# def Q(x_i):
#     return Or([x_i == a for a in a_states])
#
# def P(y_i):
#     return Or([y_i == b for b in b_states])
#####################################



# print('== SAT Formula for Simulation Relation ==')
# alpha_1 = And(And([Q(x) for x in x_states]), And([P(y) for y in y_states]))
# solver.add(alpha_1)
# print(alpha_1)

alpha_2 = And([And([Implies(sim_states[i][j],Or([y_states[t] for t in range(k)])
    ) for j in range(k)]
    ) for i in range(n)])
solver.add(alpha_2)
# print(alpha_2)

alpha_3 = And([And([ Implies(sim_states[i][j], (x_labels[i] == y_labels[j])
    ) for j in range(k)]
    ) for i in range(n)])
solver.add(alpha_3)
# print(alpha_3)


# New
# alpha_4 = And([And(
#     [(R1[i][j] == And([Implies(sim_states[i][t], Or([Bool("R(sim"+str(i)+str(t)+"-sim"+str(j)+str(r)+")")
#          for r in range(k) ])) for t in range(k)])
#         ) for j in range(n)]
#         ) for i in range(n)])
# alpha_4 = And([And(
#     [(R1[i][j] == And([Implies(sim_states[i][t],
#         Or([Bool("sim"+str(i)+"-"+str(j))] for j in range(k)))]))])])
# print(alpha_4)


# # Good
# alpha_4 = And([And(
#         [Implies(R1[i][j],
#             Or([Or([Rsim[(j*k)+(i*k*n)+t][r] for r in range(k)]
#             ) for t in range(k)])
#         ) for j in range(n)]
#         ) for i in range(n)])

# # New
# alpha_4_new = And([And(
#         [(R1[i][j] == And([Implies(sim_states[i][t], Or([Bool("R(sim"+str(i)+str(t)+"-sim"+str(j)+str(r)+")")
#              for r in range(k) ])) for t in range(k)])
#             ) for j in range(n)]
#             ) for i in range(n)])


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

# print("solver: ", solver)
print("check: ", solver.check())
# print("model: ", solver.model())


# quit()

# print('== Z3 Solve ==')
# print("solving alpha_1 to alpha_4 with user defined models")

# define_R_1()
# define_R_2()
# define_R_Transition()
# # solver.push()
# solver.add(alpha_1)
# solver.add(alpha_2)
# solver.add(alpha_3)
# # solver.add(alpha_4)
# solver.add(alpha_4_new) #better

# # print(alpha_4)

# solver.add(And([a_states[i] == True for i in range(len(a_states))]))
# solver.add(And([b_states[i] == True for i in range(len(b_states))]))
# solver.add(And([x_states[i] == True for i in range(len(x_states))]))
# solver.add(And([y_states[i] == True for i in range(len(y_states))]))



print("z3 solve result: " + str(solver.check()))


# solver.add()
# checkthis = Exists(sim_states[0][0], True)
# solver.add(checkthis)
# print(solver.check())


print('\n==Evaluation==')
if (str(solver.check()) != "unsat"):
    # m = solver.model().sexpr()
    m = solver.model()
    # print(m)

    # for t in range(n):

    print()
    for i in range(n):
        for j in range(k):
            if "True" in str(m.evaluate(sim_states[i][j], model_completion=True)):
                print("simulate p"+str(i)+ " to q" +str(j) + " : " + str(m.evaluate(sim_states[i][j], model_completion=True)))

    print()
    for i in range(n):
        for j in range(k):
            if "False" in str(m.evaluate(sim_states[i][j], model_completion=False)):
                print("simulate p"+str(i)+ " to q" +str(j) + " : " + str(m.evaluate(sim_states[i][j], model_completion=True)))


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
    print("SAT, simulation relation is as shown above.")
else:
    print("UNSAT, simulation relation unavailable.")

# print(solver.model())

print('\n(END)')
