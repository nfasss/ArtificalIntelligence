# NAME: NUR FASIHAH AYUNI BINTI MOHD YAHYA
# NIM : 1301213670
# CLASS : IF-44-1NT
# GROUP : 5

import random
import math
import matplotlib.pyplot as plt

class Chromosome:   
# Initialization                 
    def __init__(self, bin = None):
        if bin == None:
            b=[0,1] 
            self.bin = random.choices(b, k=6)
        else:
            self.bin = bin
        self.x = self.decode(dmin_x, dmax_x, self.bin[:3])
        self.y = self.decode(dmin_y, dmax_y, self.bin[3:])

# using binary encoding
    def decode(self, dmax, dmin, g):        
        tp = [2**-i for i in range(1, len(g) + 1)]
        return dmin + ((dmax - dmin) / sum(tp) * sum([g[i] * tp[i] for i in range(len(g))]))  
        
# output          
    def __repr__(self):        
        return '{} min(x,y): ({}, {})  Heuristic value : {}  Fitness value : {}'.format(self.bin, self.x, self.y, HeuristicValue(self.x, self.y), fitness_value(self.x, self.y))

def found(a, ch):        
    choose = False      
    for i in a:
        if i.bin == ch.bin:
            choose = True
            break
    return choose

def fitness_value (x,y):   # Minimization Heuristic 
    return 1/(((math.cos(x) + math.sin(y))*(math.cos(x) + math.sin(y)))/((x*x) + (y*y) + 0.0000000000000000000000001))

# Parent Selection using method Roullete Wheel Selection
def roulleteWheel(k):
    parent=[] #create an array/list for parent 

    # create lambda function as an anonymous function inside other function to sort
    fitness_list = list(map(lambda ch: fitness_value (ch.x , ch.y), Population))
    w_list = [fitness_list[i] / sum (fitness_list) for i in range (len (Population))]

    while len(parent) != k:
        select_p = random.choices(Population, weights=w_list)[0] 
        if not found (parent,select_p): # not have same chromosome within 2 parents
            parent.append(select_p)
    return parent

def crossover (parent1, parent2):
# Randomly choose 1 cutting point
    cuttingpoint= random.randint(1, len(parent1.bin) - 1) 

# The parent 1 and parent 2 will randomly cross between one cutting point
    Child1 = parent1.bin[:cuttingpoint] + parent2.bin[cuttingpoint:]
    Child2 = parent1.bin[:cuttingpoint] + parent2.bin[cuttingpoint:]


# Mutation Child 1 and Child 2
    Mutation = random.uniform (0,9) #choose random value from 0 to 9
# Probability mutation < 0.4
    if Mutation < 0.4:
        Mutation_size = random.randint(0, len(Child1)-1)
        if (Child1[Mutation_size] == 0 and Child2[Mutation_size] == 0):
            Child1[Mutation_size] = 1
            Child2[Mutation_size] = 1
        elif (Child1[Mutation_size] == 1 and Child2[Mutation_size] == 1):
            Child1[Mutation_size]= 0
            Child2[Mutation_size]= 0
        elif (Child1[Mutation_size] == 0 ):
            Child2[Mutation_size] = 1
        elif (Child1[Mutation_size] == 1 ):
            Child2[Mutation_size] = 0
        elif (Child2[Mutation_size] == 0 ):
            Child1[Mutation_size] = 1
        else:
            Child1[Mutation_size] =0


# Append the result crossover and mutation in population          
    Population.append(Chromosome(Child1))
    Population.append(Chromosome(Child2))

def selection_survivor():
    Population.sort(key= lambda ch: HeuristicValue (ch.x , ch.y), reverse = True)

def BestChromosome():
    while len(Population) != 50: # remove the worst chromosome by using pop function
        Population.pop()

# Main Function

# GA parameter
dmin_x = -5   # Minimum value of X
dmax_x = 5    # Maximum value of x
dmin_y = -5   # Minimum value of y
dmax_y = 5    # Maximum value of y

# Heuristic Value
def HeuristicValue (x,y):  
    return  (((math.cos(x) + math.sin(y))*(math.cos(x) + math.sin(y)))/((x*x) + (y*y) ))# Formula of heuristic value 

Generation = 1
Population = []

# Population = 50
while len(Population) != 50:
    ch = Chromosome()

    if not found(Population, ch):
        Population.append(ch)

selection_survivor()
BestChromosome()
print('Generation', Generation)
print('Best Chromosome', Population[4])

li = [0]*100
li[Generation-1] = fitness_value(Population[4].x, Population[4].y)

while Generation < 100:
    parent = roulleteWheel(2)
    crossover(parent[0], parent[1])
    selection_survivor()
    BestChromosome()

    Generation += 1

    li[Generation-1] = fitness_value(Population[4].x, Population[4].y)
    print('Generation', Generation)
    print('Best Chromosome', Population[4]) 

# Graph labeling and representation
plt.plot(range(1, Generation + 1), li)
plt.xlim(left=0.0)
plt.ylim(bottom=0.0)
plt.title("Fitness Value Growth")
plt.ylabel("Fitness")
plt.xlabel("Generation")
plt.show()
