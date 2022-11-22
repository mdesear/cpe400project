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


# Define Node Class
class Node:
  def _init_(self, ID,distanceDict, bandwidth, radius, coordinates,edges):
    self.ID = ID
    self.distanceDict = distanceDict
    self.bandwidth = bandwidth
    self.radius = radius
    self.coordinates = coordinates
    self.edges = edges
    

# ~~ Create a list of Nodes ~~
node_list = []

num_nodes = 5
range_radius = 0.5

# Set Up Default Node Attributes
for i in range(0, num_nodes):
    current_node = Node() # declare node object

    current_node.ID = i
    current_node.radius = range_radius # assign all nodes the same radius... for now?

    temp_coords = np.random.uniform(-1, 1, size=(1,3)) # create random 3D coords b/c manim requires 3D coords
    temp_coords[0,2] = 0 # write Z axis to zero b/c we're working in 2D
    current_node.coordinates = temp_coords

    temp_bandwidth = random.randint(0,30) # assigns random bandwidth to each node (Mbps)
    current_node.bandwidth = temp_bandwidth

    current_node.edges = []

    node_list.append(current_node)


# Find the Edges 
# Here edges are defined by overlapping range_radiuses
# TODO: This could be optimized by leveraging symmetry
i = 0
while i < num_nodes:

    x1 = node_list[i].coordinates[0,0]
    y1 = node_list[i].coordinates[0,1]
    r1 = node_list[i].radius

    j = i+1
    while j < num_nodes-1:
        x2 = node_list[j].coordinates[0,0]
        y2 = node_list[j].coordinates[0,1]
        r2 = node_list[j].radius

        is_overlap = isOverlap(x1, y1, x2, y2,r1, r2)

        if is_overlap == True: # then the circles are overlapping & are edges
            print(node_list[i].edges)
            node_list[i].edges.append(node_list[j].ID)# Save the Node's ID in the other node's edge list

        j += 1
    i +=1


class ShowPoints(Scene):
    def construct(self):

        # This Bit Creates The Axes
        axes = Axes(x_range=[-5,5,1], y_range = [-3,3,1],tips=False)
        
        # This Bit Displays the Dots from the coords array
        dots = VGroup() # This groups all the dots together
        circles = VGroup()
       
        for i in range(0, num_nodes):
            coords = node_list[i].coordinates
            dot = Dot(coords,radius=0.08, color = BLUE)
            dots.add(dot) # This adds the "dot" to the group "dots"

            # Color the Circle Green for overlap Blue else
            if not node_list[i].edges: # if edges is empty
                range_circle = Circle(radius=node_list[i].radius, color = RED)
                range_circle.shift(coords) # move circle from orgin to dot coords
                circles.add(range_circle) # Adds the "range_circle" to the group "circles"
            else:
                range_circle = Circle(radius=node_list[i].radius, color = GREEN)
                range_circle.shift(coords)
                circles.add(range_circle) 


        # Add to the Scene
        self.add(axes)
        self.add(circles)
        self.add(dots)