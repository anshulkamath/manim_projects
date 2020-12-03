from manimlib.imports import *

class Shapes(Scene):
    #A few simple shapes
    def construct(self):
        circle = Circle()
        square = Square()
        line=Line(np.array([3,0,0]),np.array([5,0,0]))
        triangle=Polygon(np.array([0,0,0]),np.array([1,1,0]),np.array([1,-1,0]))

        self.play(ShowCreation(circle))
        self.play(FadeOut(circle))
        self.play(GrowFromCenter(square))
        self.add(line)
        self.play(Transform(square,circle))

class MoreShapes(Scene):
    def construct(self):
        circle = Circle(color=PURPLE_A)
        square = Square(fill_color=GOLD_B, fill_opacity=0.5, color=GOLD_A)
        square.move_to(UP+LEFT)
        circle.surround(square)
        rectangle = Rectangle(height=2, width=3)
        ellipse=Ellipse(width=3, height=1, color=RED)
        ellipse.shift(2*DOWN+2*RIGHT)
        pointer = CurvedArrow(5*RIGHT,2*RIGHT,color=MAROON_C)
        arrow = Arrow(LEFT,UP)
        arrow.next_to(circle,DOWN+LEFT)
        rectangle.next_to(arrow,DOWN+LEFT)
        ring=Annulus(inner_radius=.5, outer_radius=1, color=BLUE)
        ring.next_to(ellipse, RIGHT)

        self.add(pointer)
        self.play(FadeIn(square))
        self.play(Rotating(square),FadeIn(circle))
        self.play(GrowArrow(arrow))
        self.play(GrowFromCenter(rectangle), GrowFromCenter(ellipse), GrowFromCenter(ring))

class Rhombus(Scene):
    def construct(self):
        rhombus = Polygon(2*UP, LEFT, 2*DOWN, RIGHT, color = PURPLE_A, fill_color=PURPLE_A, fill_opacity=1)
        circle = Circle(color = MAROON_D)
        circle.surround(rhombus)
        h_line = Line(LEFT, RIGHT, color=BLACK)
        v_line = Line(2*DOWN, 2*UP, color=WHITE)

        self.add(rhombus)
        self.play(FadeIn(circle))
        self.play(Rotating(rhombus), Rotating(h_line), Rotating(v_line))

class AddingText(Scene):
    #Adding text on the screen
    def construct(self):
        my_first_text=TextMobject("Writing with manim is fun")
        second_line=TextMobject("and easy to do!")
        second_line.next_to(my_first_text,DOWN)
        third_line=TextMobject("for me and you!")
        third_line.next_to(my_first_text,DOWN)

        self.add(my_first_text, second_line)
        self.wait(2)
        self.play(Transform(second_line,third_line))
        self.wait(2)
        second_line.shift(3*DOWN)
        self.play(ApplyMethod(my_first_text.shift,3*UP))

class AddingMoreText(Scene):
    def construct(self):
        quote = TextMobject("Imagination is more important than knowledge.")
        quote.set_color(RED)
        quote.to_edge(UP)
        quote2 = TextMobject("A person who never made a mistake never tried anything new.")
        quote2.set_color(YELLOW)
        author = TextMobject("- Albert Einstein")
        author2 = TextMobject("Albert Einstein")
        author.set_color(RED)
        author.scale(0.75)
        author2.scale(1.5)
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN)

        self.add(quote)
        self.add(author)
        self.wait(2)

        self.play(Transform(quote, quote2), ApplyMethod(author.move_to, quote2.get_corner(DOWN + RIGHT)+DOWN+2*LEFT))
        self.play(ApplyMethod(author.match_color, quote2))
        self.play(ApplyMethod(author.scale, 1.5))
        self.wait(2)
        self.play(FadeOut(quote))
        self.play(Transform(author, author2))
        self.play(ApplyMethod(author2.move_to, [0,0,0]))
        self.wait(2)
        self.play(FadeOut(author))

class SpinningSquare(Scene):
    def construct(self):
        square = Square(fill_color=GOLD_B, fill_opacity=1, color=GOLD_B)
        circle = Circle(radius=1, color=MAROON_C)
        circle.surround(square)

        text = TextMobject("This is a spinning square inscribed in a circle")
        text.to_edge(UP)
        text.set_color(RED)

        self.play(FadeIn(text))
        self.wait(1)
        self.play(FadeIn(circle), FadeIn(square))
        self.play(Rotating(square))

class RotateAndHighlight(Scene):
    #Rotation of text and highlighting with surrounding geometries
    def construct(self):
        square=Square(side_length=5,fill_color=YELLOW, fill_opacity=1)
        label=TextMobject("Text at an angle")
        label.bg=BackgroundRectangle(label,fill_opacity=1)
        label_group=VGroup(label.bg,label) #Order matters
        label_group.rotate(TAU/8)
        label2=TextMobject("Boxed text",color=BLACK)
        label2.bg=SurroundingRectangle(label2,color=BLUE,fill_color=RED, fill_opacity=.5)
        label2_group=VGroup(label2,label2.bg)
        label2_group.next_to(label_group,DOWN)
        label3=TextMobject("Rainbow")
        label3.scale(2)
        label3.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        label3.to_edge(DOWN)

        self.add(square)
        self.play(FadeIn(label_group))
        self.play(FadeIn(label2_group))
        self.play(FadeIn(label3))

class BasicEquations(Scene):
    #A short script showing how to use Latex commands
    def construct(self):
        eq1=TextMobject("$\\vec{X}_0 \\cdot \\vec{Y}_1 = 3$")
        eq1.shift(2*UP)
        eq2=TexMobject("\\vec{F}_{net} = \\sum_i \\vec{F}_i")
        eq2.shift(2*DOWN)

        self.play(Write(eq1))
        self.play(Write(eq2))

class GreensTheoremTitle(Scene):
    def construct(self):
        ## Line Integral Form
        title = TexMobject("\\text{Green's}", "\\text{ Theorem:}")
        title.set_color_by_tex("Green's", GREEN)
        eq1 = TexMobject("\\oint \\limits_{\gamma}", " \\vec{f}(x)", " \\cdot  \\mathrm{d}\\vec{S}")
        eq1.set_color_by_tex("\\vec{f}", BLUE)
        equals = TexMobject("=")
        ## Double Integral Form
        eq2 = TexMobject("\\iint_R (\\nabla \\times", " \\vec{f}", ") \\cdot \\vec{k} \\, \\mathrm{dR}")
        eq2.set_color_by_tex("\\vec{f}", BLUE)

        self.play(Write(title))
        self.wait(1 )
        self.play(ApplyMethod(title.to_edge, UP))
        self.play(Write(eq1))
        self.wait(2)
        self.play(ApplyMethod(eq1.shift, UP*2))
        self.play(Write(eq2))
        self.wait(2)
        self.play(ApplyMethod(eq1.shift, DOWN), ApplyMethod(eq2.shift, DOWN))
        self.play(FadeIn(equals), ApplyMethod(eq1.next_to, equals, LEFT), ApplyMethod(eq2.next_to, equals, RIGHT))
        self.wait(3)

        equations = VGroup(eq1, equals, eq2)

        self.play(ApplyMethod(equations.shift, UP*2))

class UsingBracesConcise(Scene):
    #A more concise block of code with all columns aligned
    def construct(self):
        eq1_text=["4","x","+","3","y","=","0"]
        eq2_text=["5","x","-","2","y","=","3"]
        eq1_mob=TexMobject(*eq1_text)
        eq2_mob=TexMobject(*eq2_text)
        eq1_mob.set_color_by_tex_to_color_map({
            "x":RED_B,
            "y":GREEN_C
            })
        eq2_mob.set_color_by_tex_to_color_map({
            "x":RED_B,
            "y":GREEN_C
            })
        for i,item in enumerate(eq2_mob):
            item.align_to(eq1_mob[i],LEFT)
        eq1=VGroup(*eq1_mob)
        eq2=VGroup(*eq2_mob)
        eq2.shift(DOWN)
        eq_group=VGroup(eq1,eq2)
        braces=Brace(eq_group,LEFT)
        eq_text = braces.get_text("A pair of equations")

        self.play(Write(eq1),Write(eq2))
        self.play(GrowFromCenter(braces),Write(eq_text))
