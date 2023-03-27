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


# Branch and Bound TSP code
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
	

start_time = time.perf_counter()
node_arr = []
source_node = int(eatdata.source_node)
node_arr.append(Location(node_t[source_node - 1][0], node_t[source_node - 1][1], node_t[source_node - 1][2], 0))
depot_x = node_arr[0].x
depot_y = node_arr[0].y


for i in range(1,len(eatdata.node_table)):

    if(i != source_node - 1):
        node_arr.append(Location(node_t[i][0], node_t[i][1], node_t[i][2], float(node_t[i][3]))) 
        node_arr[i].angle = angle_of_vectors(depot_x, depot_y, node_t[i][1], node_t[i][2])

sort_nodes = sort_locations(node_arr)

veh_input = float(eatdata.veh_cap)
veh_cap = veh_input

veh_agnmt = []
one_veh = []
counter = 0
veh_weight = []

for i in range(1, len(node_t)):
    
    if((veh_cap - sort_nodes[i].weight < 0)):
        
        one_veh.append(source_node)
        veh_agnmt.append(one_veh)
        veh_weight.append(veh_input-veh_cap)
        veh_cap = veh_input
        one_veh = []
        counter += 1
        
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight
        
        
    elif(veh_cap - sort_nodes[i].weight >= 0 or (i == len(node_t)-1)):
        one_veh.append(int(sort_nodes[i].id))
        veh_cap -= sort_nodes[i].weight    
        
        if((veh_cap - sort_nodes[i].weight == 0) or (i == len(node_t)-1)):
            one_veh.append(source_node)
            veh_agnmt.append(one_veh)
            veh_weight.append(veh_input-veh_cap)
            veh_cap = veh_input
            one_veh = []
            counter += 1

nodestoRemove = []
new_graph = []

for i in range(len(veh_agnmt)):
    
    for j in range(1, eatdata.n+1):
        if(not (j in veh_agnmt[i])):
            nodestoRemove.append(j-1)

    new_graph = [[D[a][b] for b in range(len(D[a])) if b not in nodestoRemove] for a in range(len(D)) if a not in nodestoRemove]
    
    N = len(new_graph)
    
    nodestoRemove = []
    final_path = [None] * (N + 1)
    visited = [False] * N

    final_res = maxsize

    TSP(new_graph, N)
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
    
    


