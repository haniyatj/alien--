import random 
import networkx as nx
import matplotlib.pyplot as plt
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

    def dfs(self,start,end): #under consrtuciton gpted
        if start not in self.nodes or end not in self.nodes:
           print("No such start and end node found in graph")
           return None
        
         # Reset visited flags
        for node in self.nodes.values():
            node.visited = False

        path = self.dfs_helper(start, end, [])
        return path

    def dfs_helper(self, current, end, path):
        if current == end:
            return path + [current]

        self.nodes[current].visited = True

        for neighbor, _ in self.nodes[current].actions:
            if not self.nodes[neighbor].visited:
                new_path = self.dfs_helper(neighbor, end, path + [current])
                if new_path:
                    return new_path

        return None

    def spawn_aliens(self,route): #spawn random aliens bw 10-80 on dfs path nodes
        for node in route:
         self.nodes[node].aliens=random.randint(10,80)


    def set_militarybase(self, percentage=100):
        num_militaryBases = int(len(self.nodes) * (percentage / 100))
    
        cities = [city for city_name, city in self.nodes.items() if city_name != 'Alexandria']
    
        cities_having_militaryBases = random.sample(cities, min(num_militaryBases, len(cities)))

        for city in cities_having_militaryBases:
            city.military = True  

    def print_all_nodes_data(self):
        for city_name, city_obj in self.nodes.items():
            print(f"City: {city_name}")
            print(f"  Civilans: {city_obj.civilans}")
            print(f"  Military: {city_obj.military}")
            print(f"  Aliens: {city_obj.aliens}")
            print(f"  Actions (Connections): {city_obj.actions}")
            print("----------")
city_list = {
    'Ismailia': city('Ismailia'),
    'Suez': city('Suez'),
    'Asyut': city('Asyut'),
    'Sohag': city('Sohag'),
    'Beni Suef': city('Beni Suef'),
    'Port Said': city('Port Said'),
    'Cairo': city('Cairo'),
    'Luxor': city('Luxor'),
    'Giza': city('Giza'),
    'Alexandria': city('Alexandria'),
    'Aswan': city('Aswan'),
    'Sharm El-Sheikh': city('Sharm El-Sheikh'),
    'Hurghada': city('Hurghada'),
    'Marsa Matruh': city('Marsa Matruh'),
    }


graph = graph()

for node in  city_list.values():
    graph.add_node(node)

graph.add_edge('Cairo', 'Asyut', 5)
graph.add_edge('Luxor', 'Aswan', 3)
graph.add_edge('Giza', 'Beni Suef', 2)
graph.add_edge('Alexandria', 'Marsa Matruh', 4)
graph.add_edge('Suez', 'Ismailia', 1)
graph.add_edge('Port Said', 'Ismailia', 2)
graph.add_edge('Sharm El-Sheikh', 'Hurghada', 5)
graph.add_edge('Aswan', 'Sohag', 4)
graph.add_edge('Marsa Matruh', 'Alexandria', 3)  
graph.add_edge('Sohag', 'Asyut', 3)


graph.set_militarybase()
graph.print_all_nodes_data()


"""# Create a NetworkX graph
G = nx.Graph()

# Add nodes to the graph
for node in graph.nodes.values():
    G.add_node(node.state)

# Add edges to the graph
for node_state, node in graph.nodes.items():
    for neighbor, distance in node.actions:
        G.add_edge(node_state, neighbor, weight=distance)

# Draw the graph
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=10, font_weight="bold")

# Add edge labels
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the graph
plt.title('Graph Visualization')
plt.show()"""










