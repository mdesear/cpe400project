from manim import *

class SecondExample(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        self.add(dot)

        circle2 = Circle(radius=1, color=RED)
        circle.shift(LEFT)
        dot2 = Dot(point=LEFT)
        self.add(dot2)

        self.play(GrowFromCenter(circle))
        self.play(GrowFromCenter(circle2))

        self.wait()
