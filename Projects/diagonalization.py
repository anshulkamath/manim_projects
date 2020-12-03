from manimlib.imports import *

def align_with(mob1, mob2):
    '''
    Will align the y component of the center of mob1 with mob2 by moving mob1 or mob2 horizontally
    '''
    mob1_center = mob1.get_center()
    mob2_center = mob2.get_center()
    mob1.shift((mob2_center[0] - mob1_center[0]) * RIGHT)

class IntroScene(Scene):

    def construct(self):
        ## Intro Text
        diagonalization_text = TextMobject("Diagonalization")
        diagonalization_text.set_color(YELLOW)

        formula = TexMobject(
            "\\Large \\text{A} = ", 
            "\\text{X }", 
            "\\text{D } ", 
            "\\text{X}^{-1}")
        
        formula[0].set_color(RED)
        formula[1].set_color(BLUE)
        formula[3].set_color(BLUE)
        formula[2].set_color(GREEN)

        ## Define RHS as a V group for future ease
        rhs = VGroup(*[formula[1:]])

        ## Defining explanation text boxes with arrows pointing to respective elements
        x_explanation = TextMobject("X is the matrix of eigenvectors", color = BLUE).shift(2*DOWN)
        align_with(x_explanation, formula[2])

        d_explanation = TextMobject("D is the diagonal matrix of eigenvalues", color = GREEN).shift(2*UP)
        align_with(d_explanation, formula[2])

        arrows = VGroup(
            *[Arrow(x_explanation.get_top(), formula[i].get_bottom(), color = BLUE) for i in (1, 3)],
            Arrow(d_explanation.get_center(), formula[2].get_top(), color = GREEN))

        ## Now defining the 2x2 matrix which we will diagonalize
        A_matrix = Matrix(np.array([[2, 0], [-2, 1]])).move_to(rhs.get_center() + RIGHT / 2)
        A_matrix.set_color_by_gradient(BLUE, GREEN)

        self.play(Write(diagonalization_text), run_time = 1)
        self.play(diagonalization_text.to_edge, UP)
        self.play(Write(formula))
        self.play(Write(x_explanation), Write(d_explanation))
        self.play(*[FadeIn(arrow) for arrow in arrows])
        self.wait(3)
        self.play(
            *[FadeOut(arrow) for arrow in arrows],
            FadeOut(x_explanation), FadeOut(d_explanation))
        self.wait()
        self.play(ReplacementTransform(rhs, A_matrix))

class ShowNakedTransformation(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": True,
        "transposed_matrix": [[2, 0], [-1, 1]]
    }

    def construct(self):
        self.setup()
        self.wait()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.wait()

class ShowDiagonalizedBasisVectors(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "x_transpose": [[1, 1], [1, 0]],
        "d_transpose": [[1, 0], [0, 2]]
    }

    def construct(self):
        self.setup()
        self.wait()

        evec_1 = Vector([1, 1], color = X_COLOR)
        evec_2 = Vector([1, 0], color = Y_COLOR)
        
        self.add_vector(evec_1)
        self.add_vector(evec_2)

        self.apply_inverse_transpose(self.x_transpose)
        self.apply_transposed_matrix(self.d_transpose)
        self.apply_transposed_matrix(self.x_transpose)

class ShowDecomposedTransformation(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "x_transpose": [[1, 1], [1, 0]],
        "d_transpose": [[1, 0], [0, 2]]
    }

    def construct(self):
        self.setup()
        self.wait()
        i_hat = Vector([1, 0], color = X_COLOR)
        j_hat = Vector([0, 1], color = Y_COLOR)
        self.add_vector(i_hat)
        self.add_vector(j_hat)
        self.apply_inverse_transpose(self.x_transpose)
        self.apply_transposed_matrix(self.d_transpose)
        self.apply_transposed_matrix(self.x_transpose)