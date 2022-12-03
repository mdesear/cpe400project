from manim import *
from random import *
import networkx as nx


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

        graph = None
        while graph is None or not nx.is_connected(graph):
            graph = nx.generators.random_graphs.gnp_random_graph(n, p)

        # add random weights to the edges of the graph
        for u, v in graph.edges:          # Bandwith           # Distance 
            graph.edges[u, v]['weight'] = (randint(1500, 2500),randint(1, 15))

        # display the edge weights on the graph
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        
        

        g = (
            Graph(graph.nodes, graph.edges, layout_config={"seed": 0}, labels=True)
            .scale(2.7)
            .rotate(PI / 12)
        )

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
                Tex(str(edge_labels[edge]), color =PINK).scale(0.8).move_to(edge_midpoints[edge]),
            )

        # quickfix for a bug in AniomationGroup's handling of z_index
        for v in g.vertices:
            g.vertices[v].set_z_index(1)

        self.play(Write(g))        


        def dijkstra(start, end, packet_size):
            # initialize the distance to all nodes to infinity
            distances = {node: float("inf") for node in graph.nodes}
            # set the distance to the start node to 0
            distances[start] = 0

            # initialize the previous node to None for all nodes
            previous = {node: None for node in graph.nodes}

            # initialize the unvisited nodes to all nodes
            unvisited = set(graph.nodes)

            # while there are still unvisited nodes
            while unvisited:
                # get the node with the smallest distance
                current = min(unvisited, key=lambda node: distances[node])

                # if the current node is the end node, we are done
                if current == end:
                    break

                # mark the current node as visited
                unvisited.remove(current)

                # for each neighbour of the current node
                for neighbour in graph.neighbors(current):
                    # use the edge weight of the current node to the neighbour
                    bandwidth_distance_tup = graph.edges[current, neighbour]['weight']

                    # extract the bandwidth and distance from the tuple
                    bandwidth = bandwidth_distance_tup[0]
                    distance = bandwidth_distance_tup[1]


                    # calculate Processing Delay 



                    # if the distance to the neighbour is smaller than the current distance
                    if weight < distances[neighbour]:
                        # update the distance to the neighbour
                        distances[neighbour] = weight
                        # set the previous node of the neighbour to the current node
                        previous[neighbour] = current

            # initialize the path to the end node
            path = [end]

            # while the previous node of the current node is not None
            while previous[path[-1]] is not None:
                # add the previous node to the path
                path.append(previous[path[-1]])

            # reverse the path
            path.reverse()

            return path


        # dijkstra(0,13, 12000)