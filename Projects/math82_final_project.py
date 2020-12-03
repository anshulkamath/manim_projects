from manimlib.imports import *

## Necessary functions
def firstSoln(t, c):
    return - 1 / (3 * t + c)

def secondSoln(t, c):
    return c / math.tan(t/2) + 2

def firstDifferentialEquation(point):
    t, y, z = point

    dy = 3 * y ** 2 ## Do not have to worry about domain restrictions

    ## If the streamlines are off of the screen, get rid of them
    if (abs(dy) > 100):
        return np.array([0, 0, 0])

    return np.array([1., dy, 0.])

def secondDifferentialEquation(point):
    t, y, z = point

    ## Checking to see if we are diving by 0
    ## If we are, then go to the correct signed infinity
    ## Check where sin(t) tends to with sin'(t)
    if (math.cos(t) == 1):
        dy = -np.sign(2 - y) * 1e3
    elif (math.cos(t) == -1):
        dy = np.sign(2 - y) * 1e3
    else:
        dy = (2 - y) / math.sin(t)
    
    ## If the streamlines are off of the screen, get rid of them
    if (abs(dy) > 100):
        return np.zeros(3)

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

class FirstScene(GraphScene):    

    CONFIG = {
        "function1": lambda t : np.array([t, firstSoln(t, -19/3), 0.]),
        "function2": lambda t : np.array([t, firstSoln(t, -31/2), 0.]),
        "vector_field_config_1": {
            ## Function to scale length for the vector field color gradient
            "length_func": lambda norm: 0.45 * sigmoid(norm/3),
            "min_magnitude": 0,
            "max_magnitude": 30
        },
        "vector_field_config_2": {
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
            "delta_x": 0.5,
            "delta_y": 0.5,
            "dt": 5e-2,
            "virtual_time": 4,
            "n_anchors_per_line": 10,
            "min_magnitude": 0,
            "max_magnitude": 1,
            "stroke_width": 2,
        },

        "stream_line_animation_config": {
            "line_anim_class": ShowPassingFlashWithThinningStrokeWidth,
        },

        ## Parametric Equation
        "parametric_kwargs_1": {
            "t_min": -8,
            "t_max":  2.1,
        },
        "parametric_kwargs_2": {
            "t_min": -8,
            "t_max":  5.1,
        },
    }

    def construct(self):

        ## Define our number plane
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels()).add_to_back()

        ## Next, create the vector field:
        slope_field = VectorField(
            firstDifferentialEquation, **self.vector_field_config_1
        )

        ## Now that we have the vector field, create the stream lines:
        stream_lines = StreamLines(
            firstDifferentialEquation, **self.stream_lines_config
        )
        stream_lines_animation = AnimatedStreamLines(stream_lines, **self.stream_line_animation_config)

        ## Define the Differential Equation textbox
        de_textbox = TexMobject("\\text{DE: }y' = 3y^{2}")
        de_textbox.add_background_rectangle()
        self.add_foreground_mobject(de_textbox) ## Add to foreground so it doesn't get animated over

        ## First set of ICs
        de_soln_1 = ParametricFunction(self.function1, **self.parametric_kwargs_1)
        tracer_a = Dot()
        IC_point_1 = Dot(2 * RIGHT + 3 * UP, color = PURPLE_A)
        de_soln_1.set_color(PURPLE_A)

        ## Text for general solution:
        general_soln = TexMobject("\\text{General solution: }", "y(t) = \\frac{-1}{3t + C}").add_background_rectangle()

        ## Disclaimer text (for stream_lines)
        disclaimer = TextMobject(
            "\\scriptsize Disclaimer: Some stream lines do not behave \\newline ",
            "\\scriptsize properly due to a mix of floating point \\newline ",
            "\\scriptsize precision and Euler's Approximation errors.")
        
        disclaimer[0].to_corner(DOWN + RIGHT).shift(UP).add_background_rectangle(opacity = 1)
        disclaimer[1].next_to(disclaimer[0], DOWN).add_background_rectangle(opacity = 1)
        disclaimer[2].next_to(disclaimer[1], DOWN).add_background_rectangle(opacity = 1)

        ## Text for first set of ICs
        first_IC = TexMobject("\\text{Initial Condition: }", "(2, 3)")
        first_IC.set_color_by_tex("(2, 3)", PURPLE_A)
        first_IC.add_background_rectangle()

        ## Second set of ICs
        de_soln_2 = ParametricFunction(self.function2, **self.parametric_kwargs_2)
        tracer_b = Dot()
        IC_point_2 = Dot(5 * RIGHT + 2 * UP, color = GREEN_A)
        de_soln_2.set_color(GREEN_A)

        ## Text for second set of ICs
        second_IC = TexMobject("\\text{Initial Condition: }", "(5, 2)")
        second_IC.set_color_by_tex("(5, 2)", GREEN_A)
        second_IC.add_background_rectangle()
        
        ## Adding updater points to trace out the solutions
        tracer_a.add_updater(lambda u: u.move_to(de_soln_1.get_end()))
        tracer_b.add_updater(lambda u: u.move_to(de_soln_2.get_end()))

        ## Now adding a box to show tangency (conformation to DE)
        tangent_box = Square(side_length = .75).set_color(YELLOW_D)
        tangent_box.shift(0.5 * UP + 1.5 * RIGHT)

        ## Adding a box to show the initial condition for druve 1
        IC_box_1 = Square(side_length = 0.75).set_color("#ff5a4e")
        IC_box_1.shift(2 * RIGHT + 3 * UP)

        ## Same for thes second curve
        IC_box_2 = Square(side_length = 0.75).set_color("#ff5a4e")
        IC_box_2.shift(5 * RIGHT + 2 * UP)

        ## Creating our tex explanations for each of the boxes
        tangent_explanation = TextMobject("Notice how our solution is ", "tangent to the slope field")
        tangent_explanation[0].next_to(tangent_box, DOWN, buff = .5).add_background_rectangle()
        tangent_explanation[1].next_to(tangent_explanation[0], DOWN, buff=.25).add_background_rectangle()

        IC_explanation = TextMobject("These are our ICs").add_background_rectangle()
        IC_explanation.next_to(IC_box_1, RIGHT, buff = .5)

        ## For later:
        next_de = TexMobject("\\text{DE: }y' = \\frac{2 - y}{\\sin(t)}")
        next_de.add_background_rectangle()

        new_slope_field = VectorField(
            secondDifferentialEquation, **self.vector_field_config_2
        )

        ## Start Animations
        
        
        # ## First is the textbox
        self.play(Write(de_textbox))
        self.wait()
        self.play(de_textbox.shift, 3.5 * UP + 5.5 * LEFT)

        # # ## Adding these elements since the flow of the video will have scene before
        self.play(FadeIn(plane))
        self.play(LaggedStartMap(GrowArrow, slope_field), run_time = 3)

        # ## Stream lines with disclaimer
        self.add_foreground_mobject(disclaimer)
        self.add(stream_lines_animation)
        self.play(FadeIn(disclaimer))
        self.wait(5)
        self.play(FadeOut(disclaimer))
        self.remove(stream_lines_animation, disclaimer)
        self.wait(1)
        
        ## Showing general solution:
        general_soln.align_to(de_textbox, UP + LEFT)
        general_soln.shift(0.75 * DOWN)
        self.play(
            FadeIn(general_soln),
            run_time = 2)
        self.add_foreground_mobject(general_soln)

        ## Graphing first curve
        first_IC.align_to(general_soln, UP + LEFT)
        first_IC.shift(1.25 * DOWN)
        self.play(Write(first_IC))
        self.add_foreground_mobject(first_IC) ## Adding it to the foreground here to preserve next animation
        self.play(ShowCreation(de_soln_1), run_time = 2)
        self.play(FadeIn(IC_point_1))
        self.wait(2)

        ## Graphing second curve
        second_IC.align_to(first_IC, UP + LEFT)
        self.play(second_IC.shift, 0.75 * DOWN)
        self.play(ShowCreation(de_soln_2), run_time = 2)
        self.play(FadeIn(IC_point_2))
        self.wait(2)

        ## Explaining ICs
        self.play(FadeIn(IC_box_1), FadeIn(IC_box_2))
        self.play(Write(IC_explanation))
        self.wait(2)

        ## Explaining conformity to slope field
        self.play(FadeIn(tangent_box))
        self.play(Write(tangent_explanation), run_time=3)
        self.wait(2)

        ## Fading everything out except the plane and vector field
        self.play(FadeOut(first_IC), FadeOut(second_IC), FadeOut(general_soln))
        self.wait()
        self.play(FadeOut(IC_explanation), FadeOut(IC_box_1), FadeOut(IC_box_2))
        self.wait()
        self.play(
            FadeOut(de_soln_2), FadeOut(IC_point_2), 
            FadeOut(tangent_explanation), FadeOut(tangent_box), 
            FadeOut(de_soln_1), FadeOut(IC_point_1))
        self.wait(2)
        
        ## Removing all elements from the scene
        self.remove(first_IC, second_IC, tangent_explanation, IC_explanation)
        self.remove(tangent_box, IC_box_1, IC_box_2)
        self.remove(de_soln_1, de_soln_2, IC_point_1, IC_point_2)
        self.remove(general_soln)

        next_de.align_to(de_textbox, UP + LEFT)
        self.play(ReplacementTransform(de_textbox, next_de))
        self.add_foreground_mobject(next_de)
        self.play(ReplacementTransform(slope_field, new_slope_field), run_time = 3)
        self.remove(de_textbox)

class SecondScene(GraphScene):
    CONFIG = {
        "function_1": lambda t: np.array([t, secondSoln(t, 1), 0.]),
        "function_2": lambda t: np.array([t, secondSoln(t, -5), 0.]),

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
            "delta_x": 0.5,
            "delta_y": 0.5,
            "dt": 5e-2,
            "virtual_time": 4,
            "n_anchors_per_line": 10,
            "min_magnitude": 0,
            "max_magnitude": 1,
            "stroke_width": 2,
        },

        "stream_line_animation_config": {
            "line_anim_class": ShowPassingFlashWithThinningStrokeWidth,
        },

        ## Parametric Equation
        "parametric_kwargs_1": {
            "discontinuities": [0],
            "t_min": 0.2,
            "t_max":  6,
        },
        "parametric_kwargs_2": {
            "discontinuities": [0],
            "t_min": 1,
            "t_max": 6,
        },
    }

    def construct(self):
        
        ## Defining constants for ease of coding:
        IC_1 = np.array([math.pi / 2, 3, 0])
        IC_2 = np.array([math.pi / 2, -3, 0])

        ## Reconstructing old scene
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())

        old_de_textbox = TexMobject("\\text{DE: }y' = 3y^{2}")
        old_de_textbox.shift(3.5 * UP + 5.5 * LEFT)

        de_textbox = TexMobject("\\text{DE: }y' = \\frac{2 - y}{\\sin(t)}")
        de_textbox.add_background_rectangle()
        de_textbox.align_to(old_de_textbox, UP + LEFT)
        self.add_foreground_mobject(de_textbox) ## Make sure this is over the background

        ## Next, create the vector field:
        slope_field = VectorField(
            secondDifferentialEquation, **self.vector_field_config
        )

        stream_lines = StreamLines(
            secondDifferentialEquation, **self.stream_lines_config
        )
        stream_lines_animation = AnimatedStreamLines(
            stream_lines,
            **self.stream_line_animation_config
        )

        ## Text for general solution:
        general_soln = TexMobject("\\text{General solution: }", "y(t) = \\cot(\\frac{t}{2}) + 2").add_background_rectangle()

        ## Disclaimer text (for stream_lines)
        disclaimer = TextMobject(
            "\\scriptsize Disclaimer: Some stream lines do not behave \\newline ",
            "\\scriptsize properly due to a mix of floating point \\newline ",
            "\\scriptsize precision and Euler's Approximation errors.")
        
        disclaimer[0].to_corner(DOWN + RIGHT).shift(UP).add_background_rectangle(opacity = 1)
        disclaimer[1].next_to(disclaimer[0], DOWN).add_background_rectangle(opacity = 1)
        disclaimer[2].next_to(disclaimer[1], DOWN).add_background_rectangle(opacity = 1)

        ## Now we plot two parametric curves again:
        
        ## First set of ICs
        de_soln_1 = ParametricFunction(self.function_1, **self.parametric_kwargs_1)
        de_soln_1.set_color(PURPLE_A)
        tracer_a = Dot()
        IC_point_1 = Dot(IC_1, color = PURPLE_A)

        ## Second set of ICs
        de_soln_2 = ParametricFunction(self.function_2, **self.parametric_kwargs_2)
        de_soln_2.set_color(GREEN_A)
        tracer_b = Dot()
        IC_point_2 = Dot(IC_2, color = GREEN_A)

        ## Creating the tracer updaters:
        tracer_a.add_updater(lambda u: u.move_to(de_soln_1.get_end()))
        tracer_b.add_updater(lambda u: u.move_to(de_soln_2.get_end()))

        ## Text for first set of ICs
        first_IC = TexMobject("\\text{Initial Condition: }", "(\\frac{\\pi}{2}, 3)")
        first_IC.set_color_by_tex("(\\frac{\\pi}{2}, 3)", PURPLE_A)
        first_IC.add_background_rectangle()

        ## Text for second set of ICs
        second_IC = TexMobject("\\text{Initial Condition: }", "(\\frac{\\pi}{2}, -3)")
        second_IC.set_color_by_tex("(\\frac{\\pi}{2}, -3)", GREEN_A)
        second_IC.add_background_rectangle()

        ## Boxes around ICs to identify
        IC_box_1 = Square(side_length = 0.75, color = "#ff5a4e").shift(IC_1)
        IC_box_2 = Square(side_length = 0.75, color = "#ff5a4e").shift(IC_2)

        ## Text for boxes
        IC_flag_1 = TextMobject("This is an IC").shift(IC_1 + 2 * LEFT).add_background_rectangle()
        IC_flag_2 = TextMobject("And this is an IC").shift(IC_2 + 2.5 * RIGHT).add_background_rectangle()

        ## Identifying all places where E & U fails
        EU_box = Square(side_length = 0.75, color = YELLOW_D).shift(math.pi * RIGHT + 2 * UP) ## Special case
        EU_boxes = [
            Square(side_length = 0.75, color = YELLOW_D).shift(i * math.pi * RIGHT + 2 * UP)
            for i in range(-2, 3)]
        
        ## Making text to explain this
        EU_explanation = TextMobject(
            "\\small Notice how our solution is no longer unique. \\newline",
            "\\small The DE is not continuous at $t=\\pi$, so the E\\&U \\newline",
            "\\small Thrm does not guarantee a unique solution."
            )
        
        EU_explanation[0].next_to(EU_box, LEFT).add_background_rectangle()
        EU_explanation[1].next_to(EU_explanation[0], DOWN).add_background_rectangle()
        EU_explanation[2].next_to(EU_explanation[1], DOWN).add_background_rectangle()

        ## Identifying all discontinuous points:
        overall_text = TextMobject(
            "\\small These are all points where the E \\& U Theorem \\newline",
            "\\small does not guarantee unique solutions. Note that \\newline ",
            "\\small $\\sin(t) = 0$, thus the DE is not continuous.")
        overall_text[0].move_to(ORIGIN + 2 * DOWN).add_background_rectangle()
        overall_text[1].next_to(overall_text[0], DOWN).add_background_rectangle()
        overall_text[2].next_to(overall_text[1], DOWN).add_background_rectangle()

        ## Creating arrows to indicate what the text is referring to
        arrows = [
            Arrow(start = overall_text[0].get_top(), end = box.get_bottom(), color = RED_C)
            for box in EU_boxes]

        integer_multiples = TextMobject("\\small *Boxes placed at integer multiples of $\\pi$ apart")
        integer_multiples.to_corner(UP+RIGHT).add_background_rectangle()

        ## Animation

        ## Reconstructing old scene
        self.add(plane, de_textbox, slope_field)
        general_soln.align_to(de_textbox, UP + LEFT)
        general_soln.shift(1.25 * DOWN)

        ## Stream lines
        self.wait(2)
        self.add_foreground_mobject(disclaimer)
        self.add(stream_lines_animation)
        self.play(FadeIn(disclaimer))
        self.wait(5)
        self.play(FadeOut(disclaimer))
        self.remove(stream_lines_animation, disclaimer)

        # Show general solution:
        self.play(FadeIn(general_soln))
        self.wait(2)

        # Show the creation of the solutions:
        first_IC.align_to(general_soln, UP + LEFT).add_background_rectangle()
        first_IC.shift(1.25 * DOWN)
        self.play(ShowCreation(de_soln_1), FadeIn(first_IC), run_time=2)
        self.play(FadeIn(IC_point_1))
        self.add_foreground_mobject(first_IC) ## Add to foreground so the next IC doesn't overlap
        self.wait()
        
        second_IC.align_to(first_IC, UP + LEFT).add_background_rectangle()
        self.play(ShowCreation(de_soln_2), FadeIn(second_IC), second_IC.shift, 1.2 * DOWN, run_time = 2)
        self.play(FadeIn(IC_point_2))
        self.wait()

        ## Now identify ICs
        self.play(FadeIn(IC_box_1), Write(IC_flag_1))
        self.wait(2)
        self.play(
            ReplacementTransform(IC_box_1, IC_box_2), 
            ReplacementTransform(IC_flag_1, IC_flag_2),
            run_time = 2)
        self.wait(2)
        self.play(
            FadeOut(IC_box_2), FadeOut(IC_flag_2), 
            FadeOut(first_IC), FadeOut(second_IC),
            FadeOut(general_soln))
        self.remove(IC_box_1, IC_box_2, IC_flag_1, IC_flag_2, first_IC, second_IC, general_soln)

        ## Now we will identify discontinuous points

        self.play(ShowCreation(EU_box))
        self.wait()
        self.play(Write(EU_explanation))
        self.wait(5)

        del EU_boxes[3] ## Making sure that original EU_box is not being retransformed
        self.play(
            *[FadeIn(square) for square in EU_boxes],
            EU_explanation.shift, 3 * DOWN + 1.8 * RIGHT,
            ReplacementTransform(EU_explanation, overall_text))
        
        self.play(*[FadeIn(arrow) for arrow in arrows], FadeIn(integer_multiples))

        self.wait(5)
        
        ## Removing all elements from the scene
        self.play(
            FadeOut(EU_box),
            *[FadeOut(box) for box in EU_boxes],
            *[FadeOut(arrow) for arrow in arrows],
            FadeOut(de_soln_1), FadeOut(de_soln_2),
            FadeOut(IC_point_1), FadeOut(IC_point_2),
            FadeOut(de_textbox), FadeOut(overall_text),
            FadeOut(integer_multiples))
        
        self.play(FadeOut(plane), FadeOut(slope_field), run_time = 4)

class Outro(Scene):
    def construct(self):
        heading = TextMobject("Credit: ")
        credit = TextMobject("This was made using ", "3Blue", "1Brown", "'s manim library.")
        source_code = TextMobject(
            "Source code can be found at: \\newline ", 
            "github.com/", "anshulkamath", "/", "manim\\_projects")
        
        heading.align_to(credit, UP + LEFT)
        credit.shift(DOWN)
        heading.set_color(GRAY)

        credit.set_color_by_tex("Blue", BLUE)
        credit.set_color_by_tex("Brown", LIGHT_BROWN)

        source_code[1:].move_to(ORIGIN + DOWN) ## Shifting all the elements of the second line down
        source_code[0].align_to(source_code[1], UP + LEFT).shift(UP) ## Setting the first line relative and shifting up
        
        source_code.set_color_by_tex("Source", GRAY)
        source_code.set_color_by_tex("anshul", BLUE)
        source_code.set_color_by_tex("manim", LIGHT_BROWN)

        self.play(Write(heading), Write(credit), run_time = 2)
        self.wait(2)
        self.play(FadeOut(heading), FadeOut(credit), run_time = 2)
        self.play(Write(source_code), run_time = 2)
        self.wait(2)
        self.play(FadeOut(source_code), run_time = 3)

