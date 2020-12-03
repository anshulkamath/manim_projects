from manimlib.imports import *

class mathFinalProj(Scene):

    def construct(self):
        intro = TexMobject("\\text{Math 19} ", "\\text{ Final Project: }", "\\text{Taylor Approximations}")
        author = TexMobject("\\text{by: }", "\\text{Anshul Kamath}")
        section = TexMobject("\\text{Section: }", "\\text{1}")

        intro.set_color_by_tex("Math", BLUE)
        intro.set_color_by_tex("Taylor", GREEN)
        author.set_color_by_tex("Anshul", RED)
        section.set_color_by_tex("1", PURPLE)

        author.shift(DOWN)
        section.shift(DOWN * 2)

        self.play(Write(intro))
        self.wait(1)
        self.play(Write (author))
        self.play(Write(section))
        self.wait(2)
        self.play(FadeOut(intro), FadeOut(author), FadeOut(section))
        Scene.construct(self)



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

        approx_graphs = [
            self.get_graph(graph, self.approximation_color)
            for graph in self.taylor]

        term_num = [
                    TexMobject("n = " + str(n), aligned_edge=TOP+RIGHT)
                    for n in range(0, len(self.taylor))]

        equation_num = [
                TexMobject("P_{", str(n), "}(x) = ", self.generate_e_taylor(n))
                for n in range(0, len(self.taylor))]

        approx_graphs.append(func_graph)
        term_num.append(TexMobject("n \\rightarrow \\infty", aligned_edge = TOP + RIGHT))
        equation_num.append(TexMobject("P_{n} = e^{x}", aligned_edge = BOTTOM + RIGHT))

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

        self.play(ShowCreation(func_graph), FadeIn(real_function))

        for n, graph in enumerate(approx_graphs):
            if graph == func_graph:
                self.play(FadeOut(real_function))
            self.play(
                        Transform(approx_graph, graph),
                        Transform(term, term_num[n]),
                        Transform(equation, equation_num[n]))
            self.wait(1)

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

        approx_graphs = [
            self.get_graph(graph, self.approximation_color)
            for graph in self.taylor]

        term_num = [
            TexMobject("n = ", str(n))
            for n in range(1, len(self.taylor) + 1)]

        equation_num = [
            TexMobject("P_{", str(n), "}(x) = ", self.generate_ln_taylor(n))
            for n in range(1, len(self.taylor) + 1)]

        approx_graphs.append(func_graph)
        term_num.append(TexMobject("n \\rightarrow \\infty", aligned_edge = TOP + RIGHT))
        equation_num.append(TexMobject("P_{n} = \\ln(1 + x)", aligned_edge = BOTTOM + RIGHT))

        for term in term_num:
            term.move_to(UP * 3.25 + RIGHT * 6.25)

        for equation in equation_num:
            equation.set_color(self.approximation_color)
            equation.to_edge(BOTTOM + RIGHT, buff = SMALL_BUFF)

        approx_graph = VectorizedPoint(self.input_to_graph_point(self.center, func_graph))
        term = VectorizedPoint(UP * 3.25 + RIGHT * 6.25)
        equation = VectorizedPoint(3 * DOWN)

        real_function = TexMobject("f(x)=\\ln(1+x)", color = BLUE)
        real_function.to_edge(BOTTOM+RIGHT)

        self.play(ShowCreation(func_graph), FadeIn(real_function))

        for n, graph in enumerate(approx_graphs):
            if graph == func_graph:
                self.play(FadeOut(real_function))
            self.play(
                        Transform(approx_graph, graph),
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

class outro(Scene):
    def construct(self):
        heading = TexMobject("\\text{Credit: }")
        credit = TexMobject("\\text{This was made using }", "\\text{3Blue}", "\\text{1Brown}", "\\text{'s manim library.}")
        heading.align_to(credit, UP+LEFT)
        credit.shift(DOWN)
        heading.set_color(GRAY)
        credit.set_color_by_tex("Blue", BLUE)
        credit.set_color_by_tex("Brown", LIGHT_BROWN)

        self.play(Write(heading, run_time = 1), Write(credit, run_time = 1))
        self.wait(2)
        self.play(FadeOut(heading, run_time = 1), FadeOut(credit, run_time = 1))
