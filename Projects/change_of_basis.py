from manimlib.imports import *

def align_with(mob1, mob2, horizontal=True):
    '''
    Will align the x or y component of the center of mob1 with mob2 by moving mob1 or mob2 vertically / horizontally.
    Default to y component
    '''
    mob1_center = mob1.get_center()
    mob2_center = mob2.get_center()
    if horizontal:
        mob1.shift((mob2_center[0] - mob1_center[0]) * RIGHT)
    else:
        mob1.shift((mob2_center[1] - mob1_center[1]) * UP)

def create_plane():
    '''
    Returns a VGroup with a foreground and background plane
    '''
    background_plane_kwargs = {
            "color": GREY,
            "axis_config": {
                "stroke_color": LIGHT_GREY,
            },
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        }
    

    foreground_plane_kwargs = {
            "x_max": FRAME_WIDTH / 2,
            "x_min": -FRAME_WIDTH / 2,
            "y_max": FRAME_WIDTH / 2,
            "y_min": -FRAME_WIDTH / 2,
            "faded_line_ratio": 0
        }
        
    
    background_plane = NumberPlane(**background_plane_kwargs)
    foreground_plane = NumberPlane(**foreground_plane_kwargs)
    foreground_plane.add(VectorScene().get_basis_vectors())

    return VGroup(background_plane, foreground_plane)

class IntroScene(VectorScene):
    CONFIG = {
        "transposed_matrix": [[2, -1], [-1, 3]],

        "foreground_plane_kwargs": {
            "x_max": FRAME_WIDTH / 2,
            "x_min": -FRAME_WIDTH / 2,
            "y_max": FRAME_WIDTH / 2,
            "y_min": -FRAME_WIDTH / 2,
            "faded_line_ratio": 0
        },

        "background_plane_kwargs": {
            "color": GREY,
            "axis_config": {
                "stroke_color": LIGHT_GREY,
            },
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        }
    }

    def construct(self):
        
        ## Create our number plane
        plane = create_plane()

        intro = TextMobject("The power of a ", "Change of Basis")
        intro[1].set_color_by_gradient(BLUE, YELLOW)

        ## Defining matrix and styling columns
        matrix = Matrix(np.transpose(self.transposed_matrix)).add_background_rectangle()
        
        col1 = VGroup(*matrix.get_mob_matrix()[:, 0])
        col1.set_color(X_COLOR)
        
        col2 = VGroup(*matrix.get_mob_matrix()[:, 1])
        col2.set_color(Y_COLOR)

        ## Constructing the styled matrix

        matrix_text = TextMobject("A = ")
        matrix.next_to(matrix_text, RIGHT, buff = .25)

        matrix_group = VGroup(matrix_text, matrix).move_to(ORIGIN)

        self.wait()
        self.play(Write(intro), run_time = 1)
        self.play(intro.to_edge, UP)    
        self.play(Write(matrix_group))
        self.add_foreground_mobject(matrix)
        self.wait()
        self.play(FadeOut(intro), FadeOut(matrix_text),
            matrix.to_corner, UP + LEFT,
            FadeIn(plane))
        self.wait()     


class ShowNakedTransforms(LinearTransformationScene):
    CONFIG = {
        "transposed_matrix": [[2, -1], [-1, 3]]
    }

    def construct(self):
        self.setup()
        self.wait()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.wait()
        self.apply_inverse_transpose(self.transposed_matrix)

class TransformOneTwo(LinearTransformationScene):
    CONFIG = {
        "transposed_matrix": [[2, -1], [-1, 3]]
    }

    def construct(self):
        ## Setting up previous scene
        matrix = Matrix(np.transpose(self.transposed_matrix))
        matrix.add_background_rectangle()
        
        col1 = VGroup(*matrix.get_mob_matrix()[:, 0])
        col1.set_color(X_COLOR)
        
        col2 = VGroup(*matrix.get_mob_matrix()[:, 1])
        col2.set_color(Y_COLOR)

        matrix.to_corner(UP+LEFT)
        self.add_foreground_mobject(matrix)

        ## Now setting up all of the second half transforms/explanations
        text = TexMobject("\\frac{1}{5}")
        inv_matrix = Matrix([[3, 1], [1, 2]])
        inv_matrix.next_to(text, RIGHT)

        inv_col1 = VGroup(*inv_matrix.get_mob_matrix()[:, 0])
        inv_col1.set_color(X_COLOR)
        inv_col2 = VGroup(*inv_matrix.get_mob_matrix()[:, 1])
        inv_col2.set_color(Y_COLOR)
        
        inv_matrix_group = VGroup(text, inv_matrix)
        inv_matrix_group.add_background_rectangle()
        inv_matrix_group.to_corner(UP + LEFT)

        ## Create the text at the top right of the screen

        self.setup()
        self.add(matrix)
        self.wait()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.wait()
        
        label_mobs = []
        ## Show coordinates of vectors from matrices
        for vector, color, col in [(self.i_hat, X_COLOR, col1), (self.j_hat, Y_COLOR, col2)]:
            col_copy = col.copy()
            label = vector_coordinate_label(vector, color = color)
            self.play(ReplacementTransform(col_copy, label))
            label_mobs.append(label)

        self.wait(2)

        ## Second part of the animation
        self.play(ReplacementTransform(matrix, inv_matrix_group))
        self.wait()
        self.play(*[FadeOut(label) for label in label_mobs])
        self.apply_inverse_transpose(self.transposed_matrix)

class BreakItDown(Scene):

    CONFIG = {
        "transposed_matrix": [[2, -1], [-1, 3]],
        "inverse_matrix": [[3, 1], [1, 2]]
    }

    def construct(self):
        ## Title
        break_down = TextMobject("Let's break it down: ")
        
        a_equals = TextMobject("A = ")
        a_equals.align_to(ORIGIN, RIGHT)
        a_equals.shift(2 * UP + 5 * LEFT)

        ## Defining all of our matrices
        matrices = [
            Matrix(np.eye(2, dtype=int)),
            Matrix(np.transpose(self.transposed_matrix)),
            Matrix(np.transpose(self.transposed_matrix)),
            Matrix(np.transpose(self.inverse_matrix))
        ]

        ## Placing and styling all the matrices and braces
        for matrix in matrices:
            matrix.next_to(a_equals, RIGHT)
            VGroup(*matrix.get_mob_matrix()[:, 0]).set_color(X_COLOR)
            VGroup(*matrix.get_mob_matrix()[:, 1]).set_color(Y_COLOR)

        ## Have to manually format the two ways of writing the inverse matrix
        matrices[-2] = VGroup( 
                matrices[-2],
                ## Adding a -1 to the top right of the matrix
                TexMobject("-1").move_to(
                    matrices[-2].get_corner(UP + RIGHT), 
                    aligned_edge = LEFT).shift(0.1 * RIGHT)
            ).next_to(a_equals, RIGHT)

        matrices[-1] = VGroup(
                ## Adding the 1/det part of the transformation
                TexMobject("\\frac{1}{5}").next_to(matrices[-1], LEFT),
                matrices[-1]
            ).next_to(a_equals, RIGHT)

        ## Creating all of the braces with the new matrices
        braces = [Brace(matrix, DOWN, buff = SMALL_BUFF) for matrix in matrices]

        ## Defining all of the text boxes
        texts = [
            TextMobject("These are our \\newline ", "original basis vectors"),
            TextMobject("This is our \\newline ", "first transformation"),
            TextMobject("Undoing our \\newline ", "first transformation"),
        ]

        ## Placing all of the text boxes
        for i, text in enumerate(texts):
            text[0].next_to(braces[i], DOWN)
            text[1].next_to(text[0], DOWN)


        ## Start animations
        self.play(Write(break_down))
        self.play(break_down.to_edge, UP)
        self.play(Write(a_equals))

        ## For each matrix, push the previous matrices right, insert the new one, and change the braces
        for i in range(len(matrices)):
            if i == 0:
                self.play(Write(matrices[i]))
                self.play(GrowFromCenter(braces[i]), Write(texts[i]))
            ## For the final transformation of replacing, not adding, a matrix
            elif i == len(matrices) - 1: 
                previous_matrices = VGroup(*matrices[:(i - 1)])
                self.play(
                    previous_matrices.next_to, matrices[i], RIGHT,
                    ReplacementTransform(matrices[i - 1], matrices[i]), 
                    ReplacementTransform(braces[i - 1], braces[i]))
            else:
                previous_matrices = VGroup(*matrices[:i])
                self.play(previous_matrices.next_to, matrices[i], RIGHT)
                self.play(
                    Write(matrices[i]),
                    ReplacementTransform(braces[i - 1], braces[i]),
                    ReplacementTransform(texts[i - 1], texts[i]))
            
            self.wait()

class IntroduceSimilarity(Scene):

    def construct(self):
        ## Create title
        title = TexMobject("\\textbf{Similarity}")
        
        ## Creating the text object for the formula
        formula = [
            "\\Large \\text{A}", 
            " = ", 
            "\\text{P}", 
            "\\text{B}", 
            "\\text{P}^{-1}"
        ]

        formula = TexMobject(*formula)
        formula.set_color_by_tex_to_color_map({
            "A": PURPLE,
            "P": BLUE,
            "B": RED
        })
        formula.shift(UP)

        ## Creating the explanations for each term
        explanations = [
            TextMobject("Shifts us into \"their\" basis"),
            TextMobject("Applies the same \\newline ", "transformation in \"their\" basis"),
            TextMobject("Brings us back to \"our\" basis"),
            TextMobject("Filler"), ## Filler for list comprehension symmetry
            TextMobject("Original transformation \\newline", " in \"our\" basis")
        ]

        ## Need to manually style text that bleeds onto second line
        for i in [1, -1]:
            explanations[i][0].move_to(ORIGIN)
            explanations[i][1].next_to(explanations[i][0], DOWN)

        ## Moving all the explanations down
        for text in explanations:
            text.shift(DOWN)

        arrows = [
            Arrow(explanations[5 - i].get_top(), formula[i - 1].get_bottom(), color = ORANGE)
            for i in range(len(formula), 0, -1) ## Reversing the order of the arrows
        ]
        
        del explanations[-2], arrows[-2] ## We do not need the equal sign nor the text

        self.play(Write(title))
        self.play(title.to_edge, UP)
        self.play(Write(formula))
        self.wait()
        for i in range(len(arrows)):
            if i == 0:
                self.play(GrowArrow(arrows[i]), Write(explanations[i]))
            else:
                self.play(
                    ReplacementTransform(arrows[i - 1], arrows[i]),
                    ReplacementTransform(explanations[i - 1], explanations[i]))
            self.wait(2)

## Show an example of similarity

class SpecialCaseOfSimilarity(Scene):

    CONFIG = {
        "transposed_matrix": [[2.4, 0.2], [1.2, 2.6]],
        "eigenvector_matrix": [[3, -1], [2, 1]],
        "diagonal_matrix": [[2, 0], [0, 3]],
        "inverse_matrix": [[0.2, 0.2], [-0.4, 0.6]]
    }

    def construct(self):

        ## Set up grid
        plane = create_plane()

        ## Similarity analog
        title = TextMobject("Special case of similarity")
        diag_text = TextMobject("Diagonalization", color = LIGHT_BROWN)
        diag_text.to_edge(UP)

        formula = [
            "\\text{A}",
            " = ",
            "\\text{X}",
            "\\text{D}",
            "\\text{X}^{-1}"
        ]

        formula = TexMobject(*formula)
        formula.set_color_by_tex_to_color_map({
            "A": LIGHT_BROWN,
            "X": PURPLE,
            "D": YELLOW
        })
        formula.shift(UP)

        ## Example of diagonalization:
        matrices = [
            Matrix(np.transpose(self.transposed_matrix)),
            Matrix(np.transpose(self.eigenvector_matrix)),
            Matrix(np.transpose(self.diagonal_matrix)),
            Matrix(np.transpose(self.eigenvector_matrix))
        ]

        ## Assigning colors by index tuples
        for index, color in [(0, LIGHT_BROWN), (1, PURPLE), (2, YELLOW), (3, PURPLE)]:
            matrices[index].set_color(color)

        ## Placing and styling all the matrices and braces
        matrices[-1] = VGroup(
            matrices[-1],
            TexMobject("-1").set_color(PURPLE).move_to(matrices[-1].get_corner(UP+RIGHT), aligned_edge=LEFT).shift(0.1 * RIGHT)
        )

        matrices.insert(1, TexMobject(" = "))

        ## Putting all of the matrices into a line
        matrix_group = VGroup(matrices[0])
        for i in range(1, len(matrices)):
            matrices[i].next_to(matrix_group, RIGHT)
            matrix_group.add(matrices[i])

        matrix_group.move_to(ORIGIN)

        ## Formatting braces for each matrix
        braces = [
            Brace(matrix_group[i - 1], DOWN, buff = SMALL_BUFF) 
            for i in range(len(matrix_group), 0, -1) if i not in [2]]

        explanations = [
            TextMobject("Shifts us into \\newline ", "the \"eigenbasis\""),
            TextMobject("Scales the eigenvectors \\newline ", "(now the basis vectors)"),
            TextMobject("Shifts us back into \\newline ", " our original basis"),
            TextMobject("Original \\newline ", "transformation")
        ]

        for i, text in enumerate(explanations):
            text[0].next_to(braces[i], DOWN)
            text[1].next_to(text[0], DOWN)

        ## Brace Text
        rhs = matrix_group[2:]
        big_brace = Brace(rhs, DOWN, buff=SMALL_BUFF)
        brace_text = TexMobject("\\text{These matrices } \\textit{decompose} \\newline ", "\\text{ our linear transformation A}")
        brace_text[0].next_to(big_brace, DOWN)
        brace_text[1].next_to(brace_text[0], DOWN)

        ## First part
        self.play(Write(title))
        self.wait()
        self.play(title.to_edge, UP)
        self.wait()
        self.play(Transform(title, diag_text))
        self.play(Write(formula))
        self.wait()
        self.play(formula.shift, UP)


        ## Make a copy to move the letters in line with matrices
        formula_copy = formula.copy()
        for i, text in enumerate(formula_copy):
            align_with(text, matrix_group[i])
        
        ## Add it here so as to preserve list symmetry
        matrix_group.add_background_rectangle()

        self.play(Write(matrix_group))
        self.play(Transform(formula, formula_copy))
        self.wait(2)

        ## Brace explanations
        ## Point and explain each term in the formula
        for i in range(0, len(explanations)):
            if i == 0:
                self.play(
                    GrowFromCenter(braces[i]),
                    Write(explanations[i])
                )
            else:
                self.play(
                    ReplacementTransform(braces[i - 1], braces[i]),
                    ReplacementTransform(explanations[i - 1], explanations[i])
                )
            self.wait(2)

        self.wait()
        self.play(FadeOut(explanations[-1]), FadeOut(braces[-1]))
        self.wait()

        ## Big Brace explanation
        self.play(GrowFromCenter(big_brace), Write(brace_text))
        self.wait(2)
        self.play(FadeOut(big_brace), FadeOut(brace_text))
        self.wait(2)

        ## Clean up and lead into next scene
        self.play(FadeOut(formula), FadeOut(title))
        self.add_foreground_mobject(matrix_group)
        self.play(
            matrix_group.scale, 0.75,
            matrix_group.to_corner, UP + LEFT
        )
        self.play(FadeIn(plane))

class PlayTransformations(LinearTransformationScene):
    
    CONFIG = {
        "transposed_matrix": [[2.4, 0.2], [1.2, 2.6]],
        "eigenvector_matrix": [[3, -1], [2, 1]],
        "diagonal_matrix": [[2, 0], [0, 3]],
        "inverse_matrix": [[0.2, 0.2], [-0.4, 0.6]]
    }

    def construct(self):
        ## Reconstructing scene
        matrices = [
            Matrix(np.transpose(self.transposed_matrix)),
            Matrix(np.transpose(self.eigenvector_matrix)),
            Matrix(np.transpose(self.diagonal_matrix)),
            Matrix(np.transpose(self.eigenvector_matrix))
        ]

        for index, color in [(0, LIGHT_BROWN), (1, PURPLE), (2, YELLOW), (3, PURPLE)]:
            matrices[index].set_color(color).add_background_rectangle()

        ## Placing and styling all the matrices and braces
        matrices[-1] = VGroup(
            matrices[-1],
            TexMobject("-1").set_color(PURPLE).move_to(matrices[-1].get_corner(UP+RIGHT), aligned_edge=LEFT).shift(0.1 * RIGHT)
        )
        matrices.insert(1, TexMobject(" = "))

        ## Putting all of the matrices into a line
        matrix_group = VGroup(matrices[0])
        for i in range(1, len(matrices)):
            matrices[i].next_to(matrix_group, RIGHT)
            matrix_group.add(matrices[i])

        matrix_group.scale(0.75).to_corner(UP + LEFT)
        matrix_group.add_background_rectangle()

        e1, e2 = self.get_basis_vectors()
        v1 = Vector(self.eigenvector_matrix[0][:], color = PINK)
        v2 = Vector(self.eigenvector_matrix[1][:], color = YELLOW)

        transf_i = Vector(self.transposed_matrix[0][:], color = X_COLOR)
        transf_j = Vector(self.transposed_matrix[1][:], color = Y_COLOR)

        ## Animations

        self.add(matrix_group)
        self.wait()
        self.play(
            *[FadeOut(matrix_group[i]) for i in range(len(matrix_group)) if i not in [1]]
        )
        self.wait()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.wait(3)
        self.apply_inverse_transpose(self.transposed_matrix)
        self.wait()

        ## Put all the matrices in the top corner (except for the first one, already showing)
        for i in range(2, len(matrix_group)):
            matrix_group[i].to_corner(UP + LEFT)

        ## Preparing for the eigenbasis transformation
        self.play(*[FadeOut(basis) for basis in [self.i_hat, self.j_hat]])
        self.moving_vectors.remove(self.i_hat)
        self.moving_vectors.remove(self.j_hat)
        
        self.add_vector(v1)
        self.add_vector(v2)

        ## Create a list of the vectors that are
        animation_matrices = [
            self.inverse_matrix,
            self.diagonal_matrix,
            self.eigenvector_matrix
        ]

        previous_matrix = matrix_group[1].copy()
        self.play(FadeOut(matrix_group[1]))
        for i, matrix in enumerate(animation_matrices):
            self.play(ReplacementTransform(previous_matrix, matrix_group[5 - i]))
            self.wait()
            self.apply_transposed_matrix(matrix)
            self.wait(2)
            
            previous_matrix = matrix_group[5 - i]
        
        self.wait()

        self.play(
            ReplacementTransform(v1, transf_i), 
            ReplacementTransform(v2, transf_j),
            ReplacementTransform(previous_matrix, matrix_group[1])
        )
        self.wait()

## Idea: Show a screenshot of each transformation in the Special Case of Simlarity page