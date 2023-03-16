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
    
    
depot_x = 0
depot_y = 1

#dummy data
loc_data = [[-3,3], [3,-3], [-3,-3], [3,3]]
loc_weight = [2,2,2,2]

node_arr = []
print("Angle UNSORTED")
#populate nodes objects
for i in range(len(loc_weight)):
    node_arr.append(Location(i, loc_data[i][0], loc_data[i][1], loc_weight[i]))
    node_arr[i].angle = angle_of_vectors(depot_x, depot_y, loc_data[i][0], loc_data[i][1])
    print(node_arr[i].angle)
    
print()
print("Angle sorted")
node_arr.sort(key=lambda x: x.angle)
for i in range(len(loc_weight)):
    print(node_arr[i].angle)
