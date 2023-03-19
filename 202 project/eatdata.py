from bs4 import BeautifulSoup
#make array of distancess
def distance_array(arr, n):
    dist = [[0 for x in range(n)] for y in range(n)] 
    print(dist)
    
    return 0

#THIS IS MAIN, READS XML
# Reading the data inside the xml
# file to a variable under the name
# data
with open('n030-k03.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")
n = len(Bs_data.find_all('node'))
# Finding all instances of tag
# `node`
# b_node = Bs_data.find_all('node')

# print(b_node)
node_table = [None]*n
for i in range(1, n+1):
    node = Bs_data.find('node', {'id': i})
    id = node.get('id')
    x = node.find('cx').text
    y = node.find('cy').text
    if i > 1:
        request = Bs_data.find('request', {'node': i})
        weight = request.find('quantity').text
        node_table[i-1] = (id, x, y, weight)
    else:
        node_table[i-1] = (id, x, y, None)
    
    #print(node_table[i-1])
distance_array(node_table, n)
