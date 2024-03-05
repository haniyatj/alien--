import random
import networkx as nx
import matplotlib.pyplot as plt
import heapq  
class City:
    def __init__(self, state, civilians=0, aliens=0, military=False):
        self.state = state
        self.civilians = civilians
        self.aliens = aliens
        self.military = military
        self.actions = []  # List of (neighbor, distance) tuples
        self.heuristic_val = float('inf')  # Initialize with infinity

    def __lt__(self, other):
        return self.heuristic_val < other.heuristic_val

class Graph:
    def __init__(self):
        self.nodes = {}  # state: City object
        self.military_resources = 0

    def add_node(self, city):
        self.nodes[city.state] = city

    def add_edge(self, city1, city2, distance):
        if city1 in self.nodes and city2 in self.nodes:
            self.nodes[city1].actions.append((city2, distance))
            self.nodes[city2].actions.append((city1, distance))
       

    def dfs(self,start,end):
        if start not in self.nodes or end not in self.nodes:
           print("No such start and end node found in graph")
           return None
        
         # Reset visited flags
        for node in self.nodes.values():
            node.visited = False

        path = self.dfs_helper(start, end, [])
        return path

    def dfs_helper(self, current, end, route):  
        if current == end:
            return route + [current]

        self.nodes[current].visited = True

        for neighbor, _ in self.nodes[current].actions:
            if not self.nodes[neighbor].visited:
                new_route = self.dfs_helper(neighbor, end, route + [current])
                if new_route:
                    return new_route

        return None  

    def calculate_heuristic(self, city, goal):
        # Initialize heuristic value
        heuristic = 0
        
        # Priority for civilians under alien attack
        if city.aliens > 0 and city.civilians > 0:
            heuristic += 3  # Adjust weight as needed
        
        # Priority for military bases under alien attack
        if city.aliens > 0 and city.military:
            heuristic += 2  # Adjust weight as needed
        
        # Priority for civilians with no alien attack
        if city.aliens == 0 and city.civilians > 0:
            heuristic += 1  # Adjust weight as needed
        
        # Update the heuristic value for the city
        city.heuristic_val = heuristic
        # military_factor = 0.5 * city.aliens if city.military else 0
        # if city.aliens ==0:
        #    city.heuristic_val =3 * city.civilians
        # else:
        #     city.heuristic_val = city.aliens + 2 * city.civilians + military_factor


    def find_path(self, start, goal):
        extra_resource = self.nodes['Alexandria'].aliens * 3
        frontier = []
        heapq.heapify(frontier)
        heapq.heappush(frontier, (0, self.nodes[start]))  # (priority, city)

        came_from = {start: None}
        cost_so_far = {start:0 }
        resources_so_far = {start:extra_resource}  

        while frontier:
            current_priority, current_city = heapq.heappop(frontier)
            if (current_city.aliens):
              resources_so_far[current_city.state] = extra_resource-current_city.aliens
            if current_city.aliens > extra_resource:
                break
            if current_city.state == goal:
                break
            print('current city:',current_city.state, resources_so_far[current_city.state] )
            for next_state, distance in current_city.actions:
                new_cost = cost_so_far[current_city.state] + distance
                #  potential remaining resources if move to nextcity
                potential_remaining_resources = resources_so_far[current_city.state] - self.nodes[next_state].aliens
                print('next-satte',next_state,'potential_remaining_resources:',potential_remaining_resources)
                # Skip  neighbor / use too many resources before reaching Alex
                if potential_remaining_resources < 0 and next_state != goal:
                    continue

                if (next_state ==goal and potential_remaining_resources < 0):
                    continue

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    self.calculate_heuristic(self.nodes[next_state], goal)
                    priority = new_cost + self.nodes[next_state].heuristic_val
                    heapq.heappush(frontier, (priority, self.nodes[next_state]))
                    came_from[next_state] = current_city.state
                    resources_so_far[next_state] = resources_so_far[current_city.state] - self.nodes[next_state].aliens
                    print('resourceso currentcity',current_city.state,resources_so_far[current_city.state],'resources_so_far next state:',next_state,resources_so_far[next_state])
        print('resourcessofar',resources_so_far)
        if goal not in came_from:
            print("No path found due to exceeding alien count limit and limited resources.")
            return []  
        return self.reconstruct_path(came_from, start, goal)
    
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def spawn_aliens(self, route): #spawn random aliens dfs path nodes
        for node_state in route:
            self.nodes[node_state].aliens = random.randint(100, 900)   
            if (node_state == 'Alexandria'):
                self.military_resources = self.nodes[node_state].aliens + (self.nodes[node_state].aliens*3)#setting military resource
      
    def set_military_bases(self, percentage=70):
        num_militaryBases = int(len(self.nodes) * (percentage / 100))
        cities = [city for city_name, city in self.nodes.items() if city_name != 'Alexandria']
        cities_having_militaryBases = random.sample(cities, min(num_militaryBases, len(cities)))
        for city in cities_having_militaryBases:
            city.military = True  

    def set_civilians(self):
        for city in self.nodes.values():
            city.civilians = random.randint(100, 900)


    def print_all_nodes_data(self):
        for name, city_obj in self.nodes.items():
            print(f"State: {name}")
            print(f"Number of Civilians: {city_obj.civilians}")
            if city_obj.military:
                print(f"State has a military base")
            if city_obj.aliens > 0:
                print(f"Number of Aliens attacking: {city_obj.aliens}")
            print('Neighbouring cities:',city_obj.actions)
            print("---------------------------------------")

    def print_alien_attack_patter(self, path,start,end):
        print("Alien attack pattern:",path)
        print("---------------------------------------")
        print("Troops movement starts from ",start,"and ends at ",end)
        print("---------------------------------------")

    def print_result(self,path2):
        if(path2!=[]):
            print("Optimised path for troops till Alexendria:", path2)
            print("---------------------------------------")
            # Update military resources tracking
            remaining_resources = self.military_resources
            for city_name in path2:
                city = self.nodes[city_name]
                if(city_name=='Alexandria'):
                    print("Alexandria has been saved.Troops have successfully defeated the aliens!")
                    break
                print("Troops are in ",city_name,'(',city.aliens,"aliens).Military resource:",remaining_resources)
                remaining_resources -= city.aliens
                if (city.aliens != 0 ):
                    print(city_name," saved.Troops remaining military resources:",remaining_resources)
                else :
                    print("Troops are moving to next city.")
            
            #print("Remaining military resources upon reaching Alexandria:", remaining_resources)



G = Graph()
city_list = {
    'Cairo': City('Cairo'),
    'Luxor': City('Luxor'),
    'Giza': City('Giza'),
    'Alexandria': City('Alexandria'),
    'Suez': City('Suez'),
    'Cara': City('Cara'),
    'Tobuk': City('Tobuk'),
    'Derna': City('Derna'),
    'Asyut': City('Asyut'),
    'Sohag': City('Sohag'),
    }


for node in  city_list.values():
    G.add_node(node)


G.add_edge('Cairo', 'Luxor', 6)
G.add_edge('Cairo', 'Giza', 9)
G.add_edge('Cairo', 'Suez', 10)
G.add_edge('Cairo', 'Cara', 18)
G.add_edge('Luxor', 'Giza', 4)
G.add_edge('Luxor', 'Tobuk', 20)
G.add_edge('Suez', 'Cara', 10)
G.add_edge('Suez', 'Asyut', 12)
G.add_edge('Cara', 'Asyut', 13)
G.add_edge('Tobuk', 'Derna', 16)
G.add_edge('Tobuk', 'Sohag', 20)
G.add_edge('Sohag', 'Asyut', 22)
G.add_edge('Asyut', 'Alexandria', 22)
G.add_edge('Sohag', 'Alexandria', 22)
G.add_edge('Derna', 'Alexandria', 22)
G.add_edge('Cairo', 'Sohag', 28)



G.set_military_bases()
G.set_civilians()
G.print_all_nodes_data()
path=G.dfs('Cairo', 'Alexandria')
G.spawn_aliens(path)
G.print_alien_attack_patter(path,start='Luxor',end='Alexandria')
path2 = G.find_path('Luxor', 'Alexandria')
G.print_result(path2)

# Create a NetworkX graph
Gp = nx.Graph()

# Add nodes to the graph
for node in G.nodes:
    Gp.add_node(node)

# Add edges to the graph
for node_state, node in G.nodes.items():
    for neighbor, distance in node.actions:
        Gp.add_edge(node_state, neighbor, weight=distance)

# Draw the graph
pos = nx.spring_layout(Gp)  # Positions for all nodes
nx.draw(Gp, pos, with_labels=True, node_size=600, node_color="skyblue", font_size=6, font_weight="bold")

# Add node labels
node_labels = {node_state: f"{node_state}\nCivilians: {G.nodes[node_state].civilians}\nAliens: {G.nodes[node_state].aliens}\nMilitary Base: {G.nodes[node_state].military}" for node_state in G.nodes}
nx.draw_networkx_labels(Gp, pos, labels=node_labels)

# Add edge labels
edge_labels = {(u, v): d['weight'] for u, v, d in Gp.edges(data=True)}
nx.draw_networkx_edge_labels(Gp, pos, edge_labels=edge_labels)

# Show the graph
plt.title('Graph Visualization')
plt.show()