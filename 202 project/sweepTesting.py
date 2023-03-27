import math
import eatdata
from sys import maxsize
from itertools import permutations

D = eatdata.dist_arr
d = [0]*eatdata.n
node_t = eatdata.node_table
for i in range(0,eatdata.n):
    d[i] = eatdata.node_table[i]

#print(D) 

def angle_of_vectors(depot_x, depot_y, loc_x ,loc_y):
    
     dotProduct = depot_x*loc_x + depot_y*loc_y
     modOfVector1 = math.sqrt(depot_x*depot_x + depot_y*depot_y)*math.sqrt(loc_x*loc_x + loc_y*loc_y) 
    
     angle = dotProduct/modOfVector1
     
     angleInDegree = math.degrees(math.acos(angle))
     
     if(loc_x < 0):
         angleInDegree = 360 - angleInDegree

     return angleInDegree 

class Location:
    weight = 0
    angle = 0.0
    
    def __init__(self, id, x, y, weight):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight

def sort_locations(node_arr):
    node_arr.sort(key=lambda x: x.angle)
    return node_arr

def travellingSalesmanProblem(dist_arr, indexes, start):

    retArray = [0,[]]
    vertex = indexes
    min_path = maxsize
    
    next_permutation=permutations(vertex)
    for i in next_permutation:
        #print(i)
        current_pathweight = 0
        k = start
        for j in i:
            current_pathweight += dist_arr[k - 1][j - 1]
            k = j
        current_pathweight += dist_arr[k - 1][start-1]
        min_path = min(min_path, current_pathweight)
        retArray[0] = min_path
        
        if (min_path == current_pathweight):
            retArray[1] = i
            #print(i)
    return retArray


# #dummy data
# loc_data = [[-3,3], [3,-3], [-3,-3], [3,3], [2,3],[2,2]]
# loc_weight = [2,2,2,2,2,2]

node_arr = []
source_node = int(eatdata.source_node)
node_arr.append(Location(node_t[source_node - 1][0], node_t[source_node - 1][1], node_t[source_node - 1][2], 0))
depot_x = node_arr[0].x
depot_y = node_arr[0].y

# print(node_arr[0].x, " y: ", node_arr[0].y, " id", node_arr[0].id, " int(eatdata.source_node): ", int(eatdata.source_node))


for i in range(1,len(eatdata.node_table)):

    if(i != source_node - 1): # this is the source node id
        node_arr.append(Location(node_t[i][0], node_t[i][1], node_t[i][2], float(node_t[i][3]))) 
        # print(node_arr)
        # print(i)
        node_arr[i].angle = angle_of_vectors(depot_x, depot_y, node_t[i][1], node_t[i][2])

sort_nodes = sort_locations(node_arr)

veh_input = float(eatdata.veh_cap)
veh_cap = veh_input

veh_agnmt = []
one_veh = []
counter = 0

for i in range(1, len(node_t)):
    
    if((veh_cap - sort_nodes[i].weight < 0)):
        
        one_veh.append(source_node)
        veh_agnmt.append(one_veh)
        veh_cap = veh_input
        one_veh = []
        counter += 1
        
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight
        
        # print("one_veh ", one_veh)
        # print("veh_cap: ", veh_cap, " weight of one node: ", sort_nodes[i].weight, "\n")
        
    elif(veh_cap - sort_nodes[i].weight >= 0 or (i == len(node_t)-1)):
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight
        
        #print("veh_cap: ", veh_cap, " weight of one node: ", sort_nodes[i].weight, "\n")
        
        if((veh_cap - sort_nodes[i].weight == 0) or (i == len(node_t)-1)):
            #print(veh_agnmt)
            one_veh.append(source_node)
            veh_agnmt.append(one_veh)
            veh_cap = veh_input
            one_veh = []
            counter += 1
            
            #print("one_veh ", one_veh)
    
print("Minimum Number of Vehicles is:")
print(len(veh_agnmt))
for i in range(len(veh_agnmt)):
    print("One Vehicle carries:")
    print(veh_agnmt[i])



graph = [[0,1,2,3], [1,0,2,3], [2,2,0,3], [3,3,3,0]]  # Given 2D array representing a graph
node_to_remove = 1  # Index of the node to be removed

# Create a new 2D array without the node to be removed
new_graph = [[graph[i][j] for j in range(len(graph[i])) if j != node_to_remove] for i in range(len(graph)) if i != node_to_remove]

print(new_graph)  # Output: [[0, 2], [2, 0]]
