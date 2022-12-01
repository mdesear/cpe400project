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
        for u, v in graph.edges:
            graph.edges[u, v]['weight'] = randint(1, 10)

        # display the edge weights on the graph
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        

        g = (
            Graph(graph.nodes, graph.edges, layout_config={"seed": 0})
            .scale(2.7)
            .rotate(PI / 12)
        )

        # calculate the midpoint for each edge lines for g 
        edge_midpoints = {}
        for edge in g.edges:
            edge_midpoints[edge] = g.edges[edge].get_center()


        # Add Tex edge labels to the graph at the midpoint of each edge manim line
        for edge in edge_midpoints:
            g.add(
                 #fill the sqaure with black
                Square(fill_opacity=1, fill_color=BLACK, color=BLACK).scale(0.2).move_to(edge_midpoints[edge]).set_color(BLACK),
                Tex(str(edge_labels[edge]), color =PINK).move_to(edge_midpoints[edge], offset=0.1*UP+0.1*RIGHT),
            )


        # quickfix for a bug in AniomationGroup's handling of z_index
        for v in g.vertices:
            g.vertices[v].set_z_index(1)

        self.play(Write(g))        







