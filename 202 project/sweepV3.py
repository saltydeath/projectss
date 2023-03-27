import math
import eatdata
from sys import maxsize
from itertools import permutations
from typing import DefaultDict

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

INT_MAX = 2147483647
 
# Function to find the minimum
# cost path for all the paths
def findMinRoute(tsp):
    sum = 0
    counter = 0
    j = 0
    i = 0
    min = INT_MAX
    visitedRouteList = DefaultDict(int)
 
    # Starting from the 0th indexed
    # city i.e., the first city
    visitedRouteList[0] = 1
    route = [0] * len(tsp)
 
    # Traverse the adjacency
    # matrix tsp[][]
    while i < len(tsp) and j < len(tsp[i]):
 
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if j != i and (visitedRouteList[j] == 0):
            if tsp[i][j] < min:
                min = tsp[i][j]
                route[counter] = j + 1
 
        j += 1
 
        # Check all paths from the
        # ith indexed city
        if j == len(tsp[i]):
            sum += min
            min = INT_MAX
            visitedRouteList[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    # Update the ending city in array
    # from city which was last visited
    i = route[counter - 1] - 1
 
    for j in range(len(tsp)):
 
        if (i != j) and tsp[i][j] < min:
            min = tsp[i][j]
            route[counter] = j + 1
    
    print(route)
    sum += min
 
    # Started from the node where
    # we finished as well.
    print("Minimum Cost is :", sum)


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


print("Travelling Salesman Sample: Incomplete")
min_perm = 0

minDist = []
nodestoRemove = []
new_graph = []

for i in range(len(veh_agnmt)):
    
    # POPULATE THE NODES TO REMOVE
    for j in range(1, eatdata.n+1):
        if(not (j in veh_agnmt[i])):
            nodestoRemove.append(j-1)
    #nodestoRemove = [2,4]       
    #print(nodestoRemove)
    
    new_graph = [[D[a][b] for b in range(len(D[a])) if b not in nodestoRemove] for a in range(len(D)) if a not in nodestoRemove]
    
    #print(new_graph)
    findMinRoute(new_graph)
    print()
    
    nodestoRemove = []
    


