import math


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
    
depot_x = 0
depot_y = 1

#dummy data
loc_data = [[-3,3], [3,-3], [-3,-3], [3,3], [2,3],[2,2]]
loc_weight = [2,2,2,2,2,2]

node_arr = []
print("Angle UNSORTED")
#populate nodes objects
for i in range(len(loc_weight)):
    node_arr.append(Location(i, loc_data[i][0], loc_data[i][1], loc_weight[i]))
    node_arr[i].angle = angle_of_vectors(depot_x, depot_y, loc_data[i][0], loc_data[i][1])
    print(node_arr[i].angle)
    
print()
print("Angle sorted")

sort_nodes = sort_locations(node_arr)

for i in range(len(loc_weight)):
    print(sort_nodes[i].angle)
    
#assigning vehicles
#vehicle capacity, ask for the input later
veh_input = 5
veh_cap = veh_input

veh_agnmt = []
one_veh = []
counter = 0

for i in range(len(loc_weight)):
    
    if((veh_cap - sort_nodes[i].weight < 0)):
        
        veh_agnmt.append(one_veh)
        veh_cap = veh_input
        one_veh.clear()
        counter += 1
        
        one_veh.append(sort_nodes[i])
        veh_cap -= sort_nodes[i].weight
        
        print("one_veh ", one_veh)
        print("veh_cap: ", veh_cap, " weight of one node: ", sort_nodes[i].weight, "\n")
        
    elif(veh_cap - sort_nodes[i].weight >= 0 or (i == len(loc_weight)-1)):
        
        one_veh.append(sort_nodes[i])
        veh_cap -= sort_nodes[i].weight
        
        print("veh_cap: ", veh_cap, " weight of one node: ", sort_nodes[i].weight, "\n")
        
        if((veh_cap - sort_nodes[i].weight == 0) or (i == len(loc_weight)-1)):
            
            veh_agnmt.append(one_veh)
            veh_cap = veh_input
            one_veh.clear()
            counter += 1
            
            print("one_veh ", one_veh)
    
print(len(veh_agnmt))

#check if it is correct

