from manimlib.imports import *

class PlottingFunctions(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10.3,
        "y_min": -1.5,
        "y_max": 1.5,
        "graph_origin": ORIGIN,
        "function_color": RED,
        "axes_color": GREEN,
        "x_labeled_nums": range(-10, 12, 2)
    }

    def construct(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(lambda x : np.cos(x), self.function_color)
        func_graph2 = self.get_graph(lambda x : np.sin(x))
        vert_line = self.get_vertical_line_to_graph(TAU, func_graph, color=YELLOW)
        graph_lab = self.get_graph_label(func_graph, label = "\\cos(x)")
        graph_lab2= self.get_graph_label(func_graph2,label = "\\sin(x)", x_val=-10, direction=UP/2)
        two_pi = TexMobject("x = 2 \\pi")
        label_coord = self.input_to_graph_point(TAU, func_graph)
        two_pi.next_to(label_coord, RIGHT+UP)

        self.play(ShowCreation(func_graph), ShowCreation(func_graph2))
        self.play(ShowCreation(vert_line), ShowCreation(graph_lab), ShowCreation(graph_lab2), ShowCreation(two_pi))

class TaylorApproximation(GraphScene):
    CONFIG = {
        "function": lambda x : np.cos(x),
        "function_color": BLUE,
        "taylor": [lambda x: 1, lambda x: 1-x**2/2, lambda x: 1-x**2/math.factorial(2)+x**4/math.factorial(4), lambda x: 1-x**2/2+x**4/math.factorial(4)-x**6/math.factorial(6),
                lambda x: 1-x**2/math.factorial(2)+x**4/math.factorial(4)-x**6/math.factorial(6)+x**8/math.factorial(8), lambda x: 1-x**2/math.factorial(2)+x**4/math.factorial(4)-x**6/math.factorial(6)+x**8/math.factorial(8) - x**10/math.factorial(10)],
        "center_point": 0,
        "approximation_color": GREEN,
        "x_min": -10,
        "x_max": 10,
        "y_min": -1,
        "y_max": 1,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-10, 10, 2)
    }

    def construct(self):
        self.setup_axes(animate=True)

        func_graph = self.get_graph(self.function, self.function_color)

        approx_graphs = [
            self.get_graph(graph, self.approximation_color)
            for graph in self.taylor
        ]

        term_num = [
            TexMobject("n = " + str(n), aligned_edge=TOP+RIGHT)
            for n in range (0,8)
        ]

        for t in term_num:
            t.to_edge(BOTTOM, buff=SMALL_BUFF)

        term = VectorizedPoint(3*DOWN)

        approx_graph = VectorizedPoint(
            self.input_to_graph_point(self.center_point, func_graph)
        )

        self.play(ShowCreation(func_graph))

        for n, graph in enumerate(approx_graphs):
            self.play(
                        Transform(approx_graph, graph, run_time = 2),
                        Transform(term, term_num[n])
                        )

        self.wait()

class eApproximation(GraphScene):
    CONFIG = {
        "function": lambda x: np.exp(x),
        "function_color": BLUE,
        # "derivatives": lambda n: x ** n
        "taylor": [lambda x: 1, lambda x: 1 + x, lambda x: 1 + x + x ** 2 / math.factorial(2),
                    lambda x: 1 + x + x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3),
                    lambda x: 1 + x + x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3) + x ** 4 / math.factorial(4),
                    lambda x: 1 + x + x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3) + x ** 4 / math.factorial(4) + x ** 5 / math.factorial(5),
                    lambda x: 1 + x + x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3) + x ** 4 / math.factorial(4) + x ** 5 / math.factorial(5) + x ** 6 / math.factorial(6)],
        "center": 0,
        "approximation_color": GREEN,
        "x_min": -10,
        "x_max": 10,
        "y_min": -10,
        "y_max": 10,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-10, 10, 2)
    }

    def construct(self):
        self.setup_axes(animate=True)

        func_graph = self.get_graph(self.function, self.function_color)

        author = TexMobject("\\text{-Anshul Kamath}", color = RED)
        author.move_to(UP * 3.25 + LEFT * 5)

        approx_graphs = [
            self.get_graph(graph, self.approximation_color)
            for graph in self.taylor]

        term_num = [
                    TexMobject("n = " + str(n), aligned_edge=TOP+RIGHT)
                    for n in range(0, len(self.taylor) + 1)
                    ]

        equation_num = [
                TexMobject("P_{", str(n), "}(x) = ", self.generate_e_taylor(n))
                for n in range(0, len(self.taylor) + 1)
            ]

        for term in term_num:
            term.move_to(UP*3.25+RIGHT*6.25)

        for equation in equation_num:
            equation.set_color(self.approximation_color)
            equation.to_edge(BOTTOM+RIGHT, buff=SMALL_BUFF)

        term = VectorizedPoint(UP*3.25+RIGHT*6.25)

        approx_graph = VectorizedPoint(self.input_to_graph_point(self.center, func_graph))

        equation = VectorizedPoint(3*DOWN)

        real_function = TexMobject("f(x)=e^{x}", color = BLUE)
        real_function.to_edge(BOTTOM + RIGHT)

        self.play(FadeIn(author), ShowCreation(func_graph), FadeIn(real_function))

        for n, graph in enumerate(approx_graphs):
            self.play(
                        Transform(approx_graph, graph),
                        Transform(term, term_num[n]),
                        Transform(equation, equation_num[n]))
            self.wait(1)

        self.wait()

    def generate_e_taylor(self, n, count = 0, string = ""):
        if count == 0:
            return self.generate_e_taylor(n, count + 1, "1")
        elif (count == (n + 1)):
            return string
        elif count == 1:
             return self.generate_e_taylor(n, count + 1, "1 + x")
        else:
            return self.generate_e_taylor(n, count + 1, string + " + \\frac{x^" + str(count) + "}{" + str(count) + "!}")

class lnApproximation(GraphScene):
    CONFIG = {
        "function": lambda x: np.log(1.01 + x),
        "function_color": BLUE,
        "taylor": [lambda x: x, lambda x: x - x ** 2 / math.factorial(2), lambda x: x - x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3),
                    lambda x: x - x ** 2 / math.factorial(2) + x ** 3 / math.factorial(3) - x ** 4 / math.factorial(4)],
        "center": 0,
        "approximation_color": GREEN,
        "x_min": -1,
        "x_max": 1,
        "y_min": -1,
        "y_max": 1,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-1, 2, 1),
        "x_tick_frequency": 0.25,
        "y_labeled_nums": range(-2, 3, 1),
        "y_tick_frequency": 0.5
    }

    def construct(self):
        self.setup_axes(animate = True)

        func_graph = self.get_graph(self.function, self.function_color)

        author = TexMobject("\\text{- Anshul Kamath}", color = RED)
        author.move_to(UP * 3.25 + LEFT * 5)

        approx_graphs = [
            self.get_graph(graph, self.approximation_color)
            for graph in self.taylor]

        term_num = [
            TexMobject("n = ", str(n))
            for n in range(1, len(self.taylor) + 1)]

        equation_num = [
            TexMobject("P_{", str(n), "}(x) = ", self.generate_ln_taylor(n))
            for n in range(1, len(self.taylor) + 1)
        ]

        for term in term_num:
            term.move_to(UP * 3.25 + RIGHT * 6.25)

        for equation in equation_num:
            equation.set_color(self.approximation_color)
            equation.to_edge(BOTTOM + RIGHT, buff = SMALL_BUFF)

        approx_graph = VectorizedPoint(self.input_to_graph_point(self.center, func_graph))
        term = VectorizedPoint(UP * 3.25 + RIGHT * 6.25)
        equation = VectorizedPoint(3 * DOWN)

        real_function = TexMobject("f(x)=ln(1+x)", color = BLUE)
        real_function.to_edge(BOTTOM+RIGHT)

        self.play(ShowCreation(func_graph), FadeIn(author), FadeIn(real_function))

        for n, graph in enumerate(approx_graphs):
            self.play(Transform(approx_graph, graph),
                        Transform(term, term_num[n]),
                        Transform(equation, equation_num[n]),)
            self.wait(1)
        self.wait()

    def generate_ln_taylor(self, n, count = 1, string = ""):
        if count == 1:
            return self.generate_ln_taylor(n, count + 1, "x")
        elif (count == (n + 1)):
            return string
        else:
            return self.generate_ln_taylor(n, count + 1, string + ("+", "-")[count % 2 == 0] + " \\frac{x^" + str(count) + "}{" + str(count) + "!}")
