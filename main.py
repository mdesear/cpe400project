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

    # Static coordinates for testing
    # test_coords = np.array([[[-1.85189646,  0.068516190,  0.0        ]],
    #                             [[ 0.85934519, -0.562825780,  0.0        ]],
    #                             [[-0.57849630,   1.43011906,  0.0        ]],
    #                             [[ 1.59875145, -1.321039930,  0.0        ]],
    #                             [[0.854475090,  0.276723650,  0.0        ]] ])
    # current_node.coordinates = test_coords[i]


    current_node.genRandomBandwidth() # generate random bandwidth for the node

    current_node.edges = [] # initialize empty list of edges


    node_list.append(current_node)

# Find All the circles that overlap
node_list = findOverap(node_list)






class ShowPoints(Scene):
    def construct(self):

        # ~~ Initalize the Base Graph ~~
        # Make the Graph

        # Prepare node information so that graph can recognize it
        base_vertices = []
        base_edges = []
        base_lt = {}
        base_vertices, base_edges, base_lt = cleanGraphVars(node_list)


        G = Graph(base_vertices, base_edges, layout=base_lt, labels=True)

        # Make the Circles 
        circles = updateCircles(node_list)

        # Animate the Graph and Circles appearing
        self.play(FadeIn(circles))
        self.play(Create(G))
        self.wait()
        self.play(FadeOut(circles))

        # Generate random coordinates for the nodes

        # Static coordinates for testing
        test_coords = np.array([[[-1.85189646,  0.068516190,  0.0        ]],
                                [[ 0.85934519, -0.562825780,  0.0        ]],
                                [[-0.57849630,   1.43011906,  0.0        ]],
                                [[ 1.59875145, -1.321039930,  0.0        ]],
                                [[0.854475090,  0.276723650,  0.0        ]] ])
                        

        for i in range(0, num_nodes):
            node_list[i].coordinates = test_coords[i]
            node_list[i].edges = [] # reset the edges

        # Find All the circles that overlap
        new_node_list = findOverap(node_list)

        # Prepare node information so that graph can recognize it
        new_node_vertices = [] # these are new becuase I get scopin errors if I don't
        new_node_edges = []
        new_node_lt = {}
        new_node_vertices, new_node_edges, new_node_lt = cleanGraphVars(new_node_list)

        # Make the Graph
        new_G = Graph(new_node_vertices, new_node_edges, layout=new_node_lt, labels=True)

        # Make the Circles
        new_circles = updateCircles(new_node_list)

        # Animate the Graph and Circles appearing
        self.play(FadeIn(new_circles))
        self.play(Transform(G, new_G))
        self.wait()
        self.play(FadeOut(new_circles))


print("Hi")











            

        


        
        
     

    


                    
            




















# class GraphManualPosition(Scene):
#     def construct(self):
#         vertices = [1, 2, 3, 4]
#         edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
#         lt = {1: [0, 0, 0], 2: [1, 1, 0], 3: [1, -1, 0], 4: [-1, 0, 0]}
#         G = Graph(vertices, edges, layout=lt, labels=True)
#         self.add(G)