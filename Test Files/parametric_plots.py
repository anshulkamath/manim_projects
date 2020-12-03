from manimlib.imports import *

class ParameterizedCurve(GraphScene):
    CONFIG = {
        "t_min": 0,
        "t_max":  6 * TAU,
        "function": lambda u: np.array([4 * np.sin((math.pi + u) / 5) - 1, -3 * np.cos(u/4), 0]),
        "function_color": BLUE,
        "vector_field": lambda p: np.array([-p[1], p[0], 0]),
        "x_min": -10,
        "x_max": 10,
        "y_min": -10,
        "y_max": 10,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-10, 11, 2),
        "y_labeled_nums": range(-6, 6, 2),
        "x_axis_width": 24,
        "y_axis_height": 20,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-10, 11, 2),
        "y_labeled_nums": range(-6, 6, 2),
        "x_axis_width": 24,
        "y_axis_height": 20,

        "vector_field_kwargs": {
            "delta_x": .5,
            "delta_y": .5,
            "max_magnitude": 5
        },

        "plane_kwargs": {
            "x_line_frequency": 1,
            "y_line_frequency": 1
        }
    }

    def construct(self):
        ## Setting up axes
        self.setup_axes(animate = True)

        ## Creating graph objects
        plane = NumberPlane(**self.plane_kwargs)
        vector_field = VectorField(self.vector_field, **self.vector_field_kwargs)

        ## Creating parametric/function objects
        func_graph= ParametricFunction(self.function, t_min = 0, t_max = self.t_max)
        trace_function = Dot()
        func_graph.set_color(BLUE)

        test_dot = Dot()
        # move_points_along_vector_field(test_dot, self.vector_field)

        arrow = Arrow(trace_function.get_arc_center(), )
        # print(trace_function.get_arc_center())

        ## Adding an updater to the dot to trace the function
        trace_function.add_updater(lambda u: u.move_to(func_graph.get_end()))

        ## Animate everything
        self.add(plane)
        self.wait(1)
        self.add(trace_function)
        self.play(ShowCreation(func_graph), run_time = 2.5)

        self.play(ShowCreation(vector_field))
        self.play(ShowCreation(test_dot))
