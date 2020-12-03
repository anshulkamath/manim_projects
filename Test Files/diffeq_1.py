from manimlib.imports import *

def y1(t):
    return math.exp(-t) * ((t - 5) ** 5 - 12500) / (5 * (t - 5) ** 5)


def y2(t):
    return 2 - 4 * math.tan(1) / math.tan(t/2)

def y3(t, c):
    return - 1 / (3 * t + c)

## Defining the differential equations
# def differentialEquation1(point):
#     t, y, z = point

#     dy = (-t * y + math.exp(-t)) / (t - 5)

#     if math.isnan(dy):
#         dy = 0
#     elif dy == float("-inf"):
#         dy = 50
#     elif dy == float("+inf"):
#         dy = -50

#     return np.array([1., dy, 0.])

def differentialEquation3(point):
    t, y, z = point

    dy = 3 * y ** 2 ## Do not have to worry aobut domain restrictions

    return np.array([1., dy, 0.])


class IntroScene(Scene):
    def construct(self):
        intro = TexMobject("\\text{Math 82} ", "\\text{ Final Project: }", "\\text{Slope Field Fun}")
        author = TexMobject("\\text{by: }", "\\text{Anshul Kamath}")

        intro.set_color_by_tex("Math", BLUE)
        intro.set_color_by_tex("Slope", GREEN)
        author.set_color_by_tex("Anshul", RED)

        author.shift(DOWN)

        self.play(Write(intro))
        self.wait(1)
        self.play(FadeIn(author))
        self.wait(2)
        self.play(FadeOut(intro), FadeOut(author))
        Scene.construct(self)

class FirstDE(GraphScene):
    CONFIG = {
        "vector_field_config": {
            ## Function to scale length for the vector field color gradient
            "length_func": lambda norm: 0.45 * sigmoid(norm/3),
            "min_magnitude": 0,
            "max_magnitude": 10
        },
        "plane_kwargs" : {
            "x_line_frequency": 1,
            "y_line_frequency": 1
        },
        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 0.5,
                "delta_y": 0.5,
                "y_min": -8.5,
                "y_max": 8.5,
            },
            "dt": 5e-2,
            "virtual_time": 3,
            "n_anchors_per_line": 100
        }

        ## Parametric Equation
        # "x_min": -10,
        # "x_max": 10,
        # "y_min": -10,
        # "y_max": 10,

        # "function": lambda t: 1 / math.tan(t/2) + 2,
        # "t_min": -10,
        # "t_max":  10,
    }

    ## DE: (t-5) y'' + ty = e^(-t), y(0) = 1
    ## Soln: e^(-t) [(t-5)^5 - 12500] / 5(t - 5) ^ 5
    # def y1(t):
    #     if t is not 5:
    #         y = math.exp(-t) * ((t - 5) ** 5 - 12500) / (5 * (t - 5) ** 5)
    #     else:
    #         y = 1e6

    ## DE: sin (t) y' + y = 2
    ## Soln: y = C1 * cot(t/2) + 2
    def y2(t):
        tan = math.tan(t/2)
        
        if (tan == 0):
            tan = 1e-2
        elif (tan == float('+inf')):
            tan = 1e2
        elif (tan == float('-inf')):
            tan = -1e2
        
        y = 1 / tan + 2
        return [t, float("%.2f"%y), 0.]

    def construct(self):

        ## Defining our function from above
        differentialEquation = differentialEquation3

        ## Creating the graph
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.play(FadeIn(plane))

        ## Creating the slope field and adding it to the scene
        slope_field1 = VectorField(
            differentialEquation1, **self.vector_field_config
            )
        
        slope_field2 = VectorField(
            differentialEquation2, **self.vector_field_config
            )

        slope_field3 = VectorField(
            differentialEquation3, **self.vector_field_config
            )
        
        # stream_lines = StreamLines(
        #     differentialEquation, **self.stream_lines_config
        # )
        
        ## Creating the graph of our generic equation
        # func_graph = ParametricFunction(self.function, t_min = self.t_min, t_max = self.t_max)
        # func_graph.set_color(BLUE)
        # tracing_dot = Dot()

        # tracing_dot.add_updater(lambda u: u.move_to(func_graph.get_end()))

        self.play(LaggedStartMap(GrowArrow, slope_field1))
        self.wait(3)
        self.play(ReplacementTransform(slope_field1, slope_field2))
        self.wait(3)
        self.play(ReplacementTransform(slope_field2, slope_field3))
        self.wait(3)
        # stream_lines.shuffle()
        # self.play(LaggedStartMap(ShowPassingFlash, stream_lines))
        # self.add(tracing_dot)
        # self.play(ShowCreation(func_graph), run_time=2)


class SecondScene(GraphScene):    

    CONFIG = {
        "function1": lambda t : np.array([t, y3(t, -19/3), 0.]),
        "function2": lambda t : np.array([t, y3(t, -61/4), 0.]),
        "vector_field_config": {
            ## Function to scale length for the vector field color gradient
            "length_func": lambda norm: 0.45 * sigmoid(norm/3),
            "min_magnitude": 0,
            "max_magnitude": 10
        },

        "plane_kwargs" : {
            "x_line_frequency": 1,
            "y_line_frequency": 1
        },

        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 0.5,
                "delta_y": 0.5,
                "y_min": -8.5,
                "y_max": 8.5,
            },
            "dt": 5e-2,
            "virtual_time": 3,
            "n_anchors_per_line": 100
        },

        ## Parametric Equation
        "parametric_kwargs_1": {
            "t_min": -8,
            "t_max":  2.1,
        },
        "parametric_kwargs_2": {
            "t_min": -8,
            "t_max":  5,
        },
    }

    def construct(self):

        ## Define our Number Plane
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())

        slope_field = VectorField(
            differentialEquation3, **self.vector_field_config
        )

        de_textbox = TexMobject("y' = 3y^{2}")
        de_textbox.add_background_rectangle()
        de_textbox.to_corner(TOP+LEFT)
        de_textbox.shift(2*UP)

        ## First set of ICs
        de_soln_1 = ParametricFunction(self.function1, **self.parametric_kwargs_1)
        tracer_a = Dot()
        de_soln_1.set_color(PURPLE_A)

        first_IC = TexMobject("\\text{Initial Condition: }", "(2, 3)")
        first_IC.set_color_by_tex("(2, 3)", PURPLE_A)
        first_IC.add_background_rectangle()
        first_IC.to_corner(TOP+LEFT)
        first_IC.shift(1.25 * UP)

        ## Second set of ICs
        de_soln_2 = ParametricFunction(self.function2, **self.parametric_kwargs_2)
        tracer_b = Dot()
        de_soln_2.set_color(GREEN_A)

        second_IC = TexMobject("\\text{Initial Condition: }", "(5, 4)")
        second_IC.set_color_by_tex("(5, 4)", GREEN_A)
        second_IC.add_background_rectangle()
        second_IC.to_corner(TOP+LEFT)
        second_IC.shift(0.5 * UP)
        
        tracer_a.add_updater(lambda u: u.move_to(de_soln_1.get_end()))
        tracer_b.add_updater(lambda u: u.move_to(de_soln_2.get_end()))

        ## Now adding a square to show tangency (conformation to DE)
        square = Square(side_length = .75).set_color(YELLOW_A)
        square.shift(0.5 * UP + 1.5 * RIGHT)

        explanation = TextMobject("Notice how our solution is ", "tangent to the slope field")
        
        explanation[0].next_to(square, DOWN, buff = .5)
        explanation[1].next_to(explanation[0], DOWN, buff=.5)


        ## Adding these elements since the flow of the video will have scene before
        self.add(plane)
        self.add(slope_field)

        ## Now writing all of the equations and graphing the two curves with ICs
        self.play(Write(de_textbox))
        self.play(Write(first_IC))
        self.play(ShowCreation(de_soln_1), run_time = 2)
        self.wait(2)
        self.play(Write(second_IC))
        self.play(ShowCreation(de_soln_2), run_time = 2)
        self.add(de_soln_1)
        self.wait(2)

        self.play(FadeIn(square))
        self.play(Write(explanation))

        self.wait(4)

        self.play(FadeOut(de_textbox), FadeOut(first_IC), FadeOut(second_IC))
        self.wait()
        self.play(FadeOut(de_soln_2))
        self.wait()
        self.play(FadeOut(explanation), FadeOut(square), FadeOut(de_soln_1))
        self.remove(de_textbox, first_IC, second_IC, de_soln_2, explanation, square, de_soln_1)


class TestingStreamLines(GraphScene):

    CONFIG = {

        "vector_field_config": {
            ## Function to scale length for the vector field color gradient
            "length_func": lambda norm: 0.45 * sigmoid(norm/3),
            "min_magnitude": 0,
            "max_magnitude": 10
        },

        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 0.5,
                "delta_y": 0.5,
                "y_min": -8,
                "y_max": 8,
                "x_min": -8,
                "x_max": 8
            },
            "dt": 5e-3,
            "virtual_time": 3,
            "n_anchors_per_line": 100
        },
        "plane_kwargs" : {
            "x_line_frequency": 1,
            "y_line_frequency": 1
        },

    }

    def construct(self):
        
        ## First create the plane:
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())

        ## Next, create the vector field:
        vector_field = VectorField(
            differentialEquation3, **self.vector_field_config
        )

        ## Now that we have the vector field, create the stream lines:
        stream_lines = StreamLines(
            differentialEquation3, **self.stream_lines_config
        )

        ## Finally, add all elements to the scene:
        self.play(FadeIn(plane))
        self.play(LaggedStartMap(GrowArrow, vector_field), run_time = 3)
        stream_lines.shuffle()
        self.play(LaggedStartMap(ShowPassingFlash, stream_lines))