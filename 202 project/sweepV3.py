import math
import eatdata
from sys import maxsize
from itertools import permutations
from typing import DefaultDict

maxsize = float('inf')
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



# Function to copy temporary solution
# to the final solution
def copyToFinal(curr_path):
	final_path[:N + 1] = curr_path[:]
	final_path[N] = curr_path[0]

# Function to find the minimum edge cost
# having an end at the vertex i
def firstMin(adj, i):
	min = maxsize
	for k in range(N):
		if adj[i][k] < min and i != k:
			min = adj[i][k]

	return min

# function to find the second minimum edge
# cost having an end at the vertex i
def secondMin(adj, i):
	first, second = maxsize, maxsize
	for j in range(N):
		if i == j:
			continue
		if adj[i][j] <= first:
			second = first
			first = adj[i][j]

		elif(adj[i][j] <= second and
			adj[i][j] != first):
			second = adj[i][j]

	return second

# function that takes as arguments:
# curr_bound -> lower bound of the root node
# curr_weight-> stores the weight of the path so far
# level-> current level while moving
# in the search space tree
# curr_path[] -> where the solution is being stored
# which would later be copied to final_path[]
def TSPRec(adj, curr_bound, curr_weight,
			level, curr_path, visited):
	global final_res
	
	# base case is when we have reached level N
	# which means we have covered all the nodes once
	if level == N:
		
		# check if there is an edge from
		# last vertex in path back to the first vertex
		if adj[curr_path[level - 1]][curr_path[0]] != 0:
			
			# curr_res has the total weight
			# of the solution we got
			curr_res = curr_weight + adj[curr_path[level - 1]]\
										[curr_path[0]]
			if curr_res < final_res:
				copyToFinal(curr_path)
				final_res = curr_res
		return

	# for any other level iterate for all vertices
	# to build the search space tree recursively
	for i in range(N):
		
		# Consider next vertex if it is not same
		# (diagonal entry in adjacency matrix and
		# not visited already)
		if (adj[curr_path[level-1]][i] != 0 and
							visited[i] == False):
			temp = curr_bound
			curr_weight += adj[curr_path[level - 1]][i]

			# different computation of curr_bound
			# for level 2 from the other levels
			if level == 1:
				curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
								firstMin(adj, i)) / 2)
			else:
				curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
								firstMin(adj, i)) / 2)

			# curr_bound + curr_weight is the actual lower bound
			# for the node that we have arrived on.
			# If current lower bound < final_res,
			# we need to explore the node further
			if curr_bound + curr_weight < final_res:
				curr_path[level] = i
				visited[i] = True
				
				# call TSPRec for the next level
				TSPRec(adj, curr_bound, curr_weight,
					level + 1, curr_path, visited)

			# Else we have to prune the node by resetting
			# all changes to curr_weight and curr_bound
			curr_weight -= adj[curr_path[level - 1]][i]
			curr_bound = temp

			# Also reset the visited array
			visited = [False] * len(visited)
			for j in range(level):
				if curr_path[j] != -1:
					visited[curr_path[j]] = True

# This function sets up final_path
def TSP(adj, N):
	
	# Calculate initial lower bound for the root node
	# using the formula 1/2 * (sum of first min +
	# second min) for all edges. Also initialize the
	# curr_path and visited array
	curr_bound = 0
	curr_path = [-1] * (N + 1)
	visited = [False] * N

	# Compute initial bound
	for i in range(N):
		curr_bound += (firstMin(adj, i) +
					secondMin(adj, i))

	# Rounding off the lower bound to an integer
	curr_bound = math.ceil(curr_bound / 2)

	# We start at vertex 1 so the first vertex
	# in curr_path[] is 0
	visited[0] = True
	curr_path[0] = 0

	# Call to TSPRec for curr_weight
	# equal to 0 and level 1
	TSPRec(adj, curr_bound, 0, 1, curr_path, visited)
	





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

print()
print()

minDist = []
nodestoRemove = []
new_graph = []

for i in range(len(veh_agnmt)):
    
    # POPULATE THE NODES TO REMOVE
    for j in range(1, eatdata.n+1):
        if(not (j in veh_agnmt[i])):
            nodestoRemove.append(j-1)
    #nodestoRemove = [2,4]    

    new_graph = [[D[a][b] for b in range(len(D[a])) if b not in nodestoRemove] for a in range(len(D)) if a not in nodestoRemove]
    
    #print(new_graph)
    N = len(new_graph)
    
    nodestoRemove = []
    # final_path[] stores the final solution
    # i.e. the // path of the salesman.
    final_path = [None] * (N + 1)

    # visited[] keeps track of the already
    # visited nodes in a particular path
    visited = [False] * N

    # Stores the final minimum weight
    # of shortest tour.
    final_res = maxsize

    TSP(new_graph, N)
    veh_agnmt[i].sort()
    ascList = veh_agnmt[i]

    final_node_path = []
    for m in final_path:
        final_node_path.append(ascList[m])

    print("Minimum total distance cost :", final_res)
    print("Path Taken : ", end = ' ')
    for n in range(N + 1):
        print(final_node_path[n], end = ' ')
    print("\n")
    
    


