import math
import eatdata
import time
from sys import maxsize

maxsize = float('inf')
D = eatdata.dist_arr
d = [0]*eatdata.n
node_t = eatdata.node_table
for i in range(0,eatdata.n):
    d[i] = eatdata.node_table[i]

# Calculate the degree for one location with regards to the depot
# One method call's time complexity is O(1) as operations are all O(1)
def angle_of_vectors(depot_x, depot_y, loc_x ,loc_y):
    
     dotProduct = depot_x*loc_x + depot_y*loc_y
     modOfVector1 = math.sqrt(depot_x*depot_x + depot_y*depot_y)*math.sqrt(loc_x*loc_x + loc_y*loc_y) 
    
     angle = dotProduct/modOfVector1
     
     angleInDegree = math.degrees(math.acos(angle))
     
     if(loc_x < 0):
         angleInDegree = 360 - angleInDegree

     return angleInDegree 

# Location node that includes all informaiton about the id, x-coordinate, y-coordinate, the weight that a vehicle needs to deliver
class Location:
    weight = 0
    angle = 0.0
    
    def __init__(self, id, x, y, weight):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        
# Step 2: Sorts the locations of all location nodes by their angle to make sure it is in ascending order
# One method call's time complexity is O(nlogn) where n here refers to the number of locations are there in total
def sort_locations(node_arr):
    node_arr.sort(key=lambda x: x.angle)
    return node_arr


# Branch and Bound TSP code consists of copyToFinal, firstMin, secondMin, TSPRec, and TSP
# Worse case time complexity is O(n!) if no nodes are pruned when executing one instance of TSP branch and bound
def copyToFinal(curr_path):
	final_path[:N + 1] = curr_path[:]
	final_path[N] = curr_path[0]

def firstMin(adj, i):
	min = maxsize
	for k in range(N):
		if adj[i][k] < min and i != k:
			min = adj[i][k]

	return min

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

def TSPRec(adj, curr_bound, curr_weight,
			level, curr_path, visited):
	global final_res
	
	if level == N:
		
		if adj[curr_path[level - 1]][curr_path[0]] != 0:
			
			curr_res = curr_weight + adj[curr_path[level - 1]]\
										[curr_path[0]]
			if curr_res < final_res:
				copyToFinal(curr_path)
				final_res = curr_res
		return

	for i in range(N):
		
		if (adj[curr_path[level-1]][i] != 0 and
							visited[i] == False):
			temp = curr_bound
			curr_weight += adj[curr_path[level - 1]][i]

			if level == 1:
				curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
								firstMin(adj, i)) / 2)
			else:
				curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
								firstMin(adj, i)) / 2)

			if curr_bound + curr_weight < final_res:
				curr_path[level] = i
				visited[i] = True
				
				TSPRec(adj, curr_bound, curr_weight,
					level + 1, curr_path, visited)

			curr_weight -= adj[curr_path[level - 1]][i]
			curr_bound = temp

			visited = [False] * len(visited)
			for j in range(level):
				if curr_path[j] != -1:
					visited[curr_path[j]] = True

def TSP(adj, N):
	
	curr_bound = 0
	curr_path = [-1] * (N + 1)
	visited = [False] * N

	for i in range(N):
		curr_bound += (firstMin(adj, i) +
					secondMin(adj, i))

	curr_bound = math.ceil(curr_bound / 2)

	visited[0] = True
	curr_path[0] = 0

	TSPRec(adj, curr_bound, 0, 1, curr_path, visited)
	

# Main portion of code starts here, where data for all locations are extracted
start_time = time.perf_counter()
node_arr = []
source_node = int(eatdata.source_node)
node_arr.append(Location(node_t[source_node - 1][0], node_t[source_node - 1][1], node_t[source_node - 1][2], 0))
depot_x = node_arr[0].x
depot_y = node_arr[0].y

# Step 1: Populate all locations with the Location node and calculate the angle 
# Time Complexity for populating Location node: O(n) (def angle_of_vectors and populating Location node is O(1), for loop runs n times)
for i in range(1,len(eatdata.node_table)):

    if(i != source_node - 1):
        node_arr.append(Location(node_t[i][0], node_t[i][1], node_t[i][2], float(node_t[i][3]))) 
        node_arr[i].angle = angle_of_vectors(depot_x, depot_y, node_t[i][1], node_t[i][2])

# Step 2: Sorts the locations of all location nodes by their angle to make sure it is in ascending order. Location nodes sorted is stored in the sort_nodes array
# Time complexity :O(nlogn)
sort_nodes = sort_locations(node_arr)


# Step 3: Assign locations to different vehicles
# veh_input is the capacity a vehicle can hold
# veh_cap is the capacity ONE vehicle can hold before it is reset for the next vehicle to use
# veh_agmt contains a 2D array of the vehicles and their respective routes
# one_veh contains an array of locations in respect to one vehicle. It will be reused once it is appended to veh_agmt
# veh_weight contains the weight each vehicles have to carry
# Time complexity: O(n) assignment to which vehicles

veh_input = float(eatdata.veh_cap)
veh_cap = veh_input

veh_agnmt = []
one_veh = []
veh_weight = []

for i in range(1, len(node_t)):
    
    # Step 3 Case 1: There is are no more space left to accomodate a location to a vehicle
    # Add one_veh to veh_agmt and append the location to the next vehicle's array
    if((veh_cap - sort_nodes[i].weight < 0)):
        
        one_veh.append(source_node)
        veh_agnmt.append(one_veh)
        veh_weight.append(veh_input-veh_cap)
        veh_cap = veh_input
        one_veh = []
        
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight
        
    # Step 3 Case 2: There are is space to accomodate a location or it is the final node in the list (path needs to end)
    elif(veh_cap - sort_nodes[i].weight >= 0 or (i == len(node_t)-1)):
        
        # Case 2a: If the vehicle has > 0 space, it COULD still accomodate the next location
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight    
        
        # Case 2b: If the vehicle has exactly no space left after accomodating a location ( need to move on to the next vehicle)
        # OR if it is the last node  (last node means theres no more locations after that --> need to close the route)
        if((veh_cap - sort_nodes[i].weight == 0) or (i == len(node_t)-1)):
            one_veh.append(source_node)
            veh_agnmt.append(one_veh)
            veh_weight.append(veh_input-veh_cap)
            veh_cap = veh_input
            one_veh = []


# Step 4: Prepare for TSP for each vehicles
# nodestoRemove is the array of location IDs that are not in a specific one vehicle
# new_graph contains the array of distances that are only relevant to the locations in one vehicle

nodestoRemove = []
new_graph = []

# Overall complexiy of Step 4: s * n! where s is the number of vehicles and n is the number of locations
for i in range(len(veh_agnmt)):
    
	# Finding irrelevant locations' time complexity: O(n)
    for j in range(1, eatdata.n+1):
        if(not (j in veh_agnmt[i])):
            nodestoRemove.append(j-1)

	# Assigning new graph time complexity: n^2
    new_graph = [[D[a][b] for b in range(len(D[a])) if b not in nodestoRemove] for a in range(len(D)) if a not in nodestoRemove]
    
    N = len(new_graph)
    
    nodestoRemove = []
    final_path = [None] * (N + 1)
    visited = [False] * N

    final_res = maxsize

	# Worst case time complexity of one TSP call: O(n!)
    TSP(new_graph, N)
    
    # Time complexity for array sort: O(nlogn)
    veh_agnmt[i].sort()
    ascList = veh_agnmt[i]

    final_node_path = []
    for m in final_path:
        final_node_path.append(ascList[m])

    print("Route : ", final_node_path)
    print("Total distance:",'%.4f'%final_res)
    print("Total weight:", veh_weight[i])
    print()
    
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print('Total elapsed time: %.4f s' % elapsed_time)
print('Total number of vehicles needed: %d' % len(veh_agnmt))

    
    


