from manim import *
import numpy as np
import math
import random


# Function to dectect if any range radiuses are overlapping 
def isOverlap(x1, y1, x2, y2,r1, r2):
    d = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    if(d <= r1+r2):
        return True
    else:
        return False

def findOverap(node_list):
    # Find the Edges 
    # Here edges are defined by overlapping range_radiuses
    # TODO: This could be optimized by leveraging symmetry
    num_nodes = len(node_list)
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
                    tup = node_list[i].ID,node_list[j].ID
                    node_list[i].edges.append(tup)

                    #NOTE FORMAT FOR EDGES: (Source Node, Connected Node)
                    # so (1,3) Means node 1 is connected to 3.
                    # This is not expandable so if multiple connections: 1->3 & 1 ->4
                    # We need (1,3) and (1,4)
            j += 1
        i +=1

    return node_list

def cleanGraphVars(node_list):
    node_vertices = []
    node_edges = []
    node_lt = {}

    for i in range(0, len(node_list)):
        node_vertices.append(node_list[i].ID)
        node_edges.append(node_list[i].edges)
        node_lt[node_list[i].ID] = node_list[i].coordinates[0,:].tolist()

    # Flatten the edge list
    node_edges = sum(node_edges, [])

    return node_vertices, node_edges, node_lt

def updateCircles(node_list):
    # This bit makes the circles        
    circles = VGroup()
    for i in range(0, num_nodes):
        coords = node_list[i].coordinates
        print(coords)

        # Color the circles GREEN if they overlap RED if they don't
        if not node_list[i].edges: # if edges is empty
            range_circle = Circle(radius=node_list[i].radius, color = RED)
            range_circle.shift(coords) # move circle from orgin to dot coords
            circles.add(range_circle) # Adds the "range_circle" to the group "circles"
        else:
            range_circle = Circle(radius=node_list[i].radius, color = GREEN)
            range_circle.shift(coords)
            circles.add(range_circle) 

    return circles

def UpdateGraph(node_list):
    for i in range(0, len(node_list)):
                node_list[i].genRandomCoordinates()
                node_list[i].edges = [] # reset the edges

    # Find All the circles that overlap
    node_list = findOverap(node_list)
    # Prepare node information so that graph can recognize it
    vertices = []
    edges = []
    lt = {}
    vertices, edges, lt = cleanGraphVars(node_list)




    # Make the Graph
    graph = Graph(vertices, edges, layout=lt, labels=True)

    # # Add Edge labels to the graph
    # for i in range(0, len(node_list)):
    #     # find the 


    # Make the Circles 
    circles = updateCircles(node_list)

    return circles, graph 





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
        temp_coords = np.random.uniform(-3, 3, size=(1,3)) # create random 3D coords b/c manim requires 3D coords
        temp_coords[0,2] = 0 # write Z axis to zero b/c we're working in 2D
        self.coordinates = temp_coords
        
    def genRandomBandwidth(self):
        # Generate Random Bandwidth
        self.bandwidth = random.randint(1, 30)
        



# ~~ Create a list of Nodes ~~
og_node_list = []

num_nodes = 8
range_radius = 1

# Set Up Default Node Attributes
for i in range(0, num_nodes):
    current_node = Node() # declare node object

    current_node.ID = i # set ID
    current_node.radius = range_radius # assign all nodes the same radius... for now?
    current_node.genRandomBandwidth() # generate random bandwidth for the node
    current_node.edges = [] # initialize empty list of edges

    og_node_list.append(current_node) # add the node to the list of nodes



class ShowPoints(Scene):
    def construct(self):
        circles, G = UpdateGraph(og_node_list)
       
        # Animate the Graph and Circles appearing
        self.play(FadeIn(circles))
        self.play(Create(G))
        self.wait()

        new_circles, new_G = UpdateGraph(og_node_list)
        
        # Animate the Graph and Circles appearing
        graph_transform = Transform(G, new_G, replace_mobject_with_target_in_scene = True)
        circle_transform = Transform(circles, new_circles, replace_mobject_with_target_in_scene = True)
        self.play(graph_transform,circle_transform)
        self.wait()

print("Hi")











            

        


        
        
     

    


                    
            




















# class GraphManualPosition(Scene):
#     def construct(self):
#         vertices = [1, 2, 3, 4]
#         edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
#         lt = {1: [0, 0, 0], 2: [1, 1, 0], 3: [1, -1, 0], 4: [-1, 0, 0]}
#         G = Graph(vertices, edges, layout=lt, labels=True)
#         self.add(G)