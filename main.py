import random 

class city: #each city representing a graph node 
    def __init__(self,state,parent=None,actions=None,military=False,civilians=0,aliens=0):
        self.state=state
        self.civilans=civilians
        self.military=military
        self.actions=actions if actions else []
        self.parent=parent
        self.aliens=aliens

class graph: #will have city nodes with connected edges representing the distance between them
    def __init__(self):
        self.nodes={}

    def add_node(self,node): #add city to graph
        self.nodes[node.state]=node

    def add_edge(self,node1,node2,distance): # add distances bw cities
        if node1 in self.nodes and node2 in self.nodes:
         self.nodes[node1].actions.append((node2,distance))
         self.nodes[node2].actions.append((node1,distance))

    def dfs(self,start,end): #under consrtuciton
        if start not in self.nodes or end not in self.nodes:
           print("No such start and end node found in graph")
           return None
        

    def spawn_aliens(self,route): #spawn random aliens bw 10-80 on dfs path nodes
        for node in route:
         self.nodes[node].aliens=random.randint(10,80)

        
        

city_list = {
'Cairo': city('Cairo'),
'Luxor': city('Luxor'),
'Giza': city('Giza'),
'Alexandria': city('Alexandria'),

    }


graph = graph()

for node in  city_list.values():
    graph.add_node(node)

graph.add_edge('Cairo', 'Luxor', 6)
graph.add_edge('Cairo', 'Giza', 9)
graph.add_edge('Luxor', 'Alexandria', 4)
graph.add_edge('Giza', 'Alexandria', 2)

for node, node in graph.nodes.items():
    print(f"City: {node.state}, Neighbours: {node.actions}")








