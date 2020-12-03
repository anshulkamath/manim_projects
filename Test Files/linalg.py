from manimlib.imports import *

class SimpleLinearTransformation(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : True,
        "transposed_matrix" : [[(1/2) ** 0.5, (1/2) ** 0.5], [-(1/2) ** 0.5, (1/2) ** 0.5]]
    }

    def construct(self):
        self.setup()
        self.wait()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.wait()