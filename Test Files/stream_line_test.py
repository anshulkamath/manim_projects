from manimlib.imports import *

def firstDifferentialEquation(point):
    t, y, z = point

    dy = 3 * y ** 2 ## Do not have to worry aobut domain restrictions

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


class StreamLineTesting(GraphScene):
    CONFIG = {
        "vector_field_kwargs": {
            ## Function to scale length for the vector field color gradient
            "length_func": lambda norm: 0.45 * sigmoid(norm/3),
            "min_magnitude": 0,
            "max_magnitude": 30
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
            "max_magnitude": 30,
            "stroke_width": 2,

        },
        "stream_line_animation_config": {
            "line_anim_class": ShowPassingFlashWithThinningStrokeWidth,
        },
    }

    def construct(self):

        ## Defining our new plane:
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())

        ## Creating our slopefield
        slope_field = VectorField(firstDifferentialEquation, **self.vector_field_kwargs)

        ## Creating streamlines:
        stream_lines = StreamLines(firstDifferentialEquation, **self.stream_lines_config)
        stream_line_animation = AnimatedStreamLines(stream_lines, **self.stream_line_animation_config)
        
        ## Creating everything:
        self.add(plane).bring_to_back()
        self.add(slope_field)

        ## Stream Lines
        stream_lines.shuffle()
        self.add(stream_line_animation)
        self.wait(4)