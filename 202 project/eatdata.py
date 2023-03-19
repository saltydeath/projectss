from bs4 import BeautifulSoup
 
# Reading the data inside the xml
# file to a variable under the name
# data
with open('n030-k03.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag
# `unique`
b_node = Bs_data.find_all('node')
 
print(b_node)