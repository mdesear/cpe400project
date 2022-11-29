from manim import *
import math
import random


# Function to dectect if any range radiuses are overlapping 
def isOverlap(x1, y1, x2, y2,r1, r2):
    d = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    if(d <= r1+r2):
        return True
    else:
        return False

def findOverap(node_list, num_nodes):
    # Find the Edges 
    # Here edges are defined by overlapping range_radiuses
    # TODO: This could be optimized by leveraging symmetry
    i = 0

    while i < num_nodes:
        x1 = node_list[i].coordinates[0,0]
        y1 = node_list[i].coordinates[0,1]
        r1 = node_list[i].radius

        j = 0
        while j < num_nodes:
            if j != i:
                x2 = node_list[j].coordinates[0,0]
                y2 = node_list[j].coordinates[0,1]
                r2 = node_list[j].radius

                is_overlap = isOverlap(x1, y1, x2, y2,r1, r2)

                if is_overlap == True: # then the circles are overlapping & are edges
                    node_list[i].edges.append(node_list[j].ID)# Save the Node's ID in the other node's edge list
            j += 1
        i +=1

    return node_list



# Define Node Class
class Node:
    def _init_(self, ID,distanceDict, bandwidth, radius, coordinates,edges):
        self.ID = ID
        self.distanceDict = distanceDict
        self.bandwidth = bandwidth
        self.radius = radius
        self.coordinates = coordinates
        self.edges = edges

    def genRandomCoordinates(self):
        # Generate Random Coordinates   
        temp_coords = np.random.uniform(-2, 2, size=(1,3)) # create random 3D coords b/c manim requires 3D coords
        temp_coords[0,2] = 0 # write Z axis to zero b/c we're working in 2D
        self.coordinates = temp_coords
        
    def genRandomBandwidth(self):
        # Generate Random Bandwidth
        self.bandwidth = random.randint(1, 30)
        



# ~~ Create a list of Nodes ~~
node_list = []

num_nodes = 5
range_radius = 0.75

# Set Up Default Node Attributes
for i in range(0, num_nodes):
    current_node = Node() # declare node object

    current_node.ID = i
    current_node.radius = range_radius # assign all nodes the same radius... for now?

    current_node.genRandomCoordinates() # generate random coordinates for the node

    current_node.genRandomBandwidth() # generate random bandwidth for the node

    current_node.edges = []

    node_list.append(current_node)

# Find All the circles that overlap
node_list = findOverap(node_list, num_nodes)


# Prepare node information so that graph can recognize it

#NOTE FORMAT FOR EDGES: (Source Node, Connected Node)
# so (1,3) Means node 1 is connected to 3.
# This is not expandable so if multiple connections: 1->3 & 1 ->4
# We need (1,3) and (1,4)

node_vertices = []
node_edges = []
node_lt = {}

for i in range(0, num_nodes):
    node_vertices.append(node_list[i].ID)

    for j in range(0, len(node_list[i].edges)): # SEE Note above for explaination
        tup = node_list[i].ID,node_list[i].edges[j]
        node_edges.append(tup)

    node_lt[node_list[i].ID] = node_list[i].coordinates[0,:].tolist()


print(node_vertices)
print(node_edges)
print(node_lt)



class ShowPoints(Scene):
    def construct(self):

        # Graph the Nodes
        G = Graph(node_vertices, node_edges, layout=node_lt, labels=True)
        self.add(G)


        # This bit makes the circles        
        circles = VGroup()
        for i in range(0, num_nodes):
            coords = node_list[i].coordinates

            # Color the circles GREEN if they overlap RED if they don't
            if not node_list[i].edges: # if edges is empty
                range_circle = Circle(radius=node_list[i].radius, color = RED)
                range_circle.shift(coords) # move circle from orgin to dot coords
                circles.add(range_circle) # Adds the "range_circle" to the group "circles"
            else:
                range_circle = Circle(radius=node_list[i].radius, color = GREEN)
                range_circle.shift(coords)
                circles.add(range_circle) 


        # Add to the Scene
        self.add(circles)








# class GraphManualPosition(Scene):
#     def construct(self):
#         vertices = [1, 2, 3, 4]
#         edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
#         lt = {1: [0, 0, 0], 2: [1, 1, 0], 3: [1, -1, 0], 4: [-1, 0, 0]}
#         G = Graph(vertices, edges, layout=lt, labels=True)
#         self.add(G)