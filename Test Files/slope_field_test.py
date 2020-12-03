from manimlib.imports import *

## Functions
def divergence(vector_func, dt=1e-7):
    def result(point):
        value = vector_func(point)
        return sum([
            (vector_func(point + dt * RIGHT) - value)[i] / dt
            for i, vect in enumerate([RIGHT, UP, OUT])
        ])
    return result

def two_d_curl(vector_func, dt=1e-7):
    def result(point):
        value = vector_func(point)
        return op.add(
            (vector_func(point + dt * RIGHT) - value)[1] / dt,
            -(vector_func(point + dt * UP) - value)[0] / dt,
        )
    return result


def cylinder_flow_vector_field(point, R=1, U=1):
    z = R3_to_complex(point)
    # return complex_to_R3(1.0 / derivative(joukowsky_map)(z))
    return complex_to_R3(derivative(joukowsky_map)(z).conjugate())

def four_swirls_function(point):
    x, y = point[:2]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result

## Scenes

class Introduction(MovingCameraScene):
    CONFIG = {
        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 1.0 / 8,
                "delta_y": 1.0 / 8,
                "y_min": -8.5,
                "y_max": 8.5,
            }
        },
        "vector_field_config": {},
        "virtual_time": 3,
    }

    def construct(self):
        # Divergence
        def div_func(p):
            return p / 3
        
        div_vector_field = VectorField(
            div_func, **self.vector_field_config
        )
        
        stream_lines = StreamLines(
            div_func, **self.stream_lines_config
        )
        
        stream_lines.shuffle()
        
        div_title = self.get_title("Divergence")

        self.add(div_vector_field)
        
        self.play(
            LaggedStartMap(ShowPassingFlash, stream_lines),
            FadeIn(div_title[0]),
            *list(map(GrowFromCenter, div_title[1]))
        )

        # Curl
        def curl_func(p):
            return rotate_vector(p / 3, 90 * DEGREES)

        curl_vector_field = VectorField(
            curl_func, **self.vector_field_config
        )
        stream_lines = StreamLines(
            curl_func, **self.stream_lines_config
        )
        stream_lines.shuffle()
        curl_title = self.get_title("Curl")

        self.play(
            ReplacementTransform(div_vector_field, curl_vector_field),
            ReplacementTransform(
                div_title, curl_title,
                path_arc=90 * DEGREES
            ),
        )
        self.play(ShowPassingFlash(stream_lines, run_time=3))
        self.wait()

    def get_title(self, word):
        title = TextMobject(word)
        title.scale(2)
        title.to_edge(UP)
        title.add_background_rectangle()
        return title

class TestVectorField(Scene):
    CONFIG = {
        "func": cylinder_flow_vector_field,
        "flow_time": 15,
    }

    def construct(self):
        lines = StreamLines(
            four_swirls_function,
            virtual_time=3,
            min_magnitude=0,
            max_magnitude=2,
        )
        self.add(AnimatedStreamLines(
            lines,
            line_anim_class=ShowPassingFlash
        ))
        self.wait(10)