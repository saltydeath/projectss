from bs4 import BeautifulSoup
import math

#create array of distances between each pair of nodes
def distance_array(arr, n):
    dist_arr = [[0 for x in range(n)] for y in range(n)] 
    
    for i in range(0, n):
        for j in range(0, n):
            #euclidean distance
            dist_arr[i][j] = math.sqrt((node_table[j][1]- node_table[i][1])**2 + (node_table[j][2]- node_table[i][2])**2)

    print(dist_arr)

    return dist_arr

#THIS IS MAIN, READS XML
# Reading the data inside the xml
with open('n030-k03.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside the beautifulsoup parser, storing the returned object
Bs_data = BeautifulSoup(data, "xml")
n = len(Bs_data.find_all('node'))

# print(b_node)
node_table = [None]*n
for i in range(1, n+1):
    node = Bs_data.find('node', {'id': i})
    id = node.get('id')
    x = float(node.find('cx').text)
    y = float(node.find('cy').text)
    if i > 1:
        request = Bs_data.find('request', {'node': i})
        weight = request.find('quantity').text
        node_table[i-1] = (id, x, y, weight)
    else:
        node_table[i-1] = (id, x, y, None)
    
    print(node_table[i-1])
distance_array(node_table, n)
