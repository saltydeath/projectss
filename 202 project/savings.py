class Location:
    weight = 0
    angle = 0.0
    
    def __init__(self, id, x, y, weight):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight


def compute_savings(D):
    N = len(D)
    n = N-1
    savings_table = [None]*int((n*n-n)/2) #create array for exact no of savings calculated
    idx = 0
    for i in range(1,N):
        for j in range(i+1,N):
            saving = D[i,0]+D[0,j]-D[i,j]
            savings_table[idx] = (saving,-D[i,j],i,j)
            idx+=1
    savings_table.sort(reverse=True)
    return savings_table

# D is a array  of the full 2D distance matrix.
# d is a list of demands. d[0] should be 0.0 as it is the depot.
# C is the capacity constraint limit for the identical vehicles.
# N is the number of nodes including the depot

def parallel_savings_init(D, d, C):
    N = len(D)
    
    ## 1. make route for each customer
    routes = [[i] for i in range(1,N)] #(N-1)x(N-1) "2D array"
    route_demands = d[1:] if C else [0]*N
    route_costs = [D[0,i]+D[i,0] for i in range(1,N)] 
    
    ## 2. compute initial savings 
    savings_table = compute_savings(D)
        
    # zero based node indexing!
    endnode = [0]+list(range(0,N-1))#create list[0, 0, 1, 2, 3, ...., N-2]
    #indicates last node in a route            
        
    ## 3. merge
    # Get potential merges best savings first (second element is secondary sorting criterion, and it it ignored)
    for best_saving, _, i, j in savings_table:
            
        if best_saving<0:
            break
            
        left_route = endnode[i]
        right_route = endnode[j]
        
        # the node is already an internal part of a longer segment
        if ((left_route is None) or
            (right_route is None) or
            (left_route==right_route)):
            continue
        
        # check capacity constraint validity
        merged_demand = route_demands[left_route]+route_demands[right_route]
        if merged_demand > C:
            continue

        merged_cost = route_costs[left_route]-D[0,i]+route_costs[right_route]-D[0,j]+D[i,j]

        # update bookkeeping only on the recieving (left) route
        route_demands[left_route] = merged_demand
        route_costs[left_route] = merged_cost
            
        # merging is done based on the joined endpoints, reverse the 
        #  merged routes as necessary
        if routes[left_route][0]==i:
            routes[left_route].reverse()
        if routes[right_route][-1]==j:
            routes[right_route].reverse()

        # the nodes that become midroute points cannot be merged
        if len(routes[left_route])>1:
            endnode[ routes[left_route][-1] ] = None
        if len(routes[right_route])>1:
            endnode[ routes[right_route][0] ] = None
        
        # all future references to right_route are to merged route
        endnode[ routes[right_route][-1] ] = left_route
        
        # merge with list concatenation
        routes[left_route].extend( routes[right_route] )
        routes[right_route] = None    
        
    return routes