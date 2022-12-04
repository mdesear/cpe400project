from manim import *
from random import *
import networkx as nx
import math




class ShowPoints(Scene):
    def construct(self):

        # configure the frame height and width do the graph fits on the screen
        self.camera.frame_height = 9
        self.camera.frame_width = 16


        seed(0xDEADBEAF)

        n = 14
        p = 3 / n

        VISITED_COLOR = GREEN
        NEIGHBOUR_COLOR = BLUE
        PATH_COLOR = RED

        graph = None
        while graph is None or not nx.is_connected(graph):
            graph = nx.generators.random_graphs.gnp_random_graph(n, p)

        g = (
            Graph(graph.nodes, graph.edges, layout_config={"seed": 0}, labels=True)
            .scale(2.7)
            .rotate(PI / 12)
        )

        # add random weights to the edges of the graph

        Velocity = 210000000 # m/s for optical fiber
        packet_size = 12000 # bits

        for u, v in graph.edges:          
            

            # get the distance between the two nodes 
            x1 = g._layout[u][0]
            y1 = g._layout[u][1]
            x2 = g._layout[v][0]
            y2 = g._layout[v][1]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) # distance is in meters

            bandwidth = randint(1500, 2500) # bandwidth is in bps

            Transmission_delay = (packet_size / bandwidth) # in sec
            Propogation_delay = (distance / Velocity) # in sec
            Queue_delay = 0.0000001 # in sec (arbitrary)

            Processing_delay= Transmission_delay + Propogation_delay + Queue_delay


            graph.edges[u, v]['weight'] = (Processing_delay)


   

        # display the edge weights on the graph
        edge_labels = nx.get_edge_attributes(graph, 'weight')

        # change the size of the labeled dots in the graph to 0.2
        for v in g.vertices:
            g.vertices[v].scale(0.3)


        # calculate the midpoint for each edge lines for g 
        edge_midpoints = {}
        for edge in g.edges:
            edge_midpoints[edge] = g.edges[edge].get_center()


        # Add Tex edge labels to the graph at the midpoint of each edge manim line
        for edge in edge_midpoints:
            g.add(
                 #fill the sqaure with black
                Square(fill_opacity=1, fill_color=BLACK, color=BLACK).scale(0.2).move_to(edge_midpoints[edge]).set_color(BLACK),
                Tex(round(edge_labels[edge],2), color =PINK).scale(0.5).move_to(edge_midpoints[edge]),
            )

        # quickfix for a bug in AniomationGroup's handling of z_index
        for v in g.vertices:
            g.vertices[v].set_z_index(1)

        self.play(Write(g))        


        
        #create a function tha runs dijkstra's algorithm on the graph
        def dijkstra(start, end):

            # Add Text in the upper right corner of the screen to display the start and end nodes and packet size
            start_text = Text("Start Node: " + str(start), color = PINK).scale(0.5).move_to(UP * 2.5 + RIGHT * 6.5)
            end_text = Text("End Node: " + str(end), color = PINK).scale(0.5).move_to(UP * 2.5 + RIGHT * 6.5 + UP * 0.5)
            packet_size_text = Text("Packet Size: " + str(packet_size), color = PINK).scale(0.5).move_to(UP * 2.5 + RIGHT * 6.5 + UP * 1)

            self.play(
                Write(start_text),
                Write(end_text),
                Write(packet_size_text),
            )


            # create a list of nodes that have been visited
            visited = []

            # create a list of nodes that have not been visited
            unvisited = []

            # create a dictionary that stores the distance from the start node to each node
            distance = {}

            # create a dictionary that stores the previous node for each node
            previous = {}

            # for each node in the graph
            for node in graph.nodes:

                # if the node is the start node
                if node == start:

                    # set the distance to the start node to 0
                    distance[node] = 0

                # otherwise
                else:

                    # set the distance to infinity
                    distance[node] = math.inf

                # add the node to the unvisited list
                unvisited.append(node)

                # set the previous node to None
                previous[node] = None

            current_node_text = Text("Unvisted Node with Smallest Delay:", color = WHITE).scale(0.5).move_to(UP * 3.5 + LEFT * 5.3)
            self.play(Write(current_node_text))


            # while there are still nodes to visit
            while unvisited:

                # get the node with the smallest distance
                current = min(unvisited, key=distance.get)

                # Display the current node number next to current_node_text
                current_node_number = Text(str(current), color = WHITE).scale(0.5).move_to(UP * 3.5 + LEFT * 5.3 + RIGHT * 2.7)
                self.play(Write(current_node_number))





                # if the current node is the end node
                if current == end:
                    break

                # remove the current node from the unvisited list
                unvisited.remove(current)

                # add the current node to the visited list
                visited.append(current)

                # # animate a dot moving along the edge path from the previously visted node to the current node
                # if current != start:
                #     d1 = Dot(color=VISITED_COLOR).move_to(g.vertices[previous[current]].get_center())

                #     self.play(
                #         d1.animate.move_to(g.vertices[current].get_center()),
                #         FadeOut(d2),
                #     )
                    

                # Flash the current node with an indication manim animation, and color the current node Green
                self.play(
                    Flash(g.vertices[current], color = VISITED_COLOR, line_length=0.45, flash_radius=0.1),
                    ReplacementTransform(g.vertices[current], LabeledDot(label = str(current), color = VISITED_COLOR).move_to(g.vertices[current].get_center()), run_time=0.3),
                )
                
                list_of_tuples = []
                # for each neighbour of the current node
                for neighbour in graph.neighbors(current):
                    
                    # color the edge between the current node and the neighbour node Blue
                    if current < neighbour:
                        edge_tup = current, neighbour
                    else:
                        edge_tup = neighbour, current

              
                    d2 = Dot(color=NEIGHBOUR_COLOR).move_to(g.vertices[current].get_center())

                    self.play(
                        g.edges[edge_tup].animate.set_color(NEIGHBOUR_COLOR),
                        # slightly ofset the dot from the start of edge path
                        d2.animate.move_to(g.vertices[neighbour].get_center()),
                        Wiggle(g.vertices[neighbour], color = NEIGHBOUR_COLOR, line_length=0.35, flash_radius=0.1, run_time=0.7),
                    )


                    list_of_tuples.append(edge_tup)

                    # if the neighbour has not been visited
                    if neighbour not in visited:

                        # calculate the new distance to the neighbour
                        new_distance = distance[current] + graph.edges[current, neighbour]['weight']

                        # if the new distance to the neighbour is less than the current distance to the neighbour
                        if new_distance < distance[neighbour]:

                            # set the distance to the neighbour to the new distance
                            distance[neighbour] = new_distance

                            # set the previous node of the neighbour to the current node
                            previous[neighbour] = current

                # set all the edges in the list_of_tuples to their original color simultaneously
                self.play(
                    *[
                        g.edges[edge].animate.set_color(WHITE)
                        for edge in list_of_tuples
                    ]
                )
                self.play(Unwrite(current_node_number))

            self.play(
                Unwrite(current_node_number),
                Unwrite(current_node_text),
                )
                                           
            # initialize the path to the end node
            path = [end]

            # while the previous node of the current node is not None
            while previous[path[-1]] is not None:
                # add the previous node to the path
                path.append(previous[path[-1]])

            # reverse the path
            path.reverse()


            # Add Text in the upper left corner of the screen to display the path
            path_text = Text("Path: " + str(path), color = WHITE).scale(0.5).to_corner(UL)
            self.play(Write(path_text))


            # animate a dot moving through each node in the path from the start node through intermediary nodes/edges and ending at the end node
            for i in range(len(path) - 1):
                d1 = Dot(color=PATH_COLOR).move_to(g.vertices[path[i]].get_center())

                self.play(
                    d1.animate.move_to(g.vertices[path[i + 1]].get_center()),
                    Flash(g.vertices[path[i]], color = PATH_COLOR, line_length=0.45, flash_radius=0.1),
                    ReplacementTransform(g.vertices[path[i]], LabeledDot(label = str(path[i]), color = PATH_COLOR).move_to(g.vertices[path[i]].get_center()), run_time=0.3),
                    FadeOut(d2),
                )
                d2 = d1

            # Color the End Node Red
            self.play(
                ReplacementTransform(g.vertices[path[-1]], LabeledDot(label = str(path[-1]), color = PATH_COLOR).move_to(g.vertices[path[-1]].get_center()), run_time=0.3),
                Flash(g.vertices[path[-1]], color = PATH_COLOR, line_length=0.45, flash_radius=0.1),

            )

            self.wait(5)


        # Get User Input for the Graph
        # print the range of nodes the user can choose from
        print("Enter a number between 0 and " + str(len(graph.nodes) - 1) + " for the start/end node.")

        # Ask the user to pick a start node with in the range of nodes we have
        start = int(input("Enter a start node: "))
        while start not in range(1, len(graph.nodes) + 1):
            start = int(input("Enter a start node: "))
        # Ask the user to pick an end node with in the range of nodes we have
        end = int(input("Enter an end node: "))
        while end not in range(1, len(graph.nodes) + 1):
            if start == end:
                print("The start node and end node cannot be the same.")
                end = int(input("Enter an end node: "))
            else:
                end = int(input("Enter an end node: "))

        print("The Video will take about 2 minutes to render")
        dijkstra(start,end)