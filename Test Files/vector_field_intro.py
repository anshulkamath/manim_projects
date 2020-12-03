from manimlib.imports import *

class DrawAnAxis(Scene):
    CONFIG = {
        "plane_kwargs" : {
            "x_line_frequency": 1,
            "y_line_frequency": 1
        }
    }

    def construct(self):
        my_plane = NumberPlane(**self.plane_kwargs)
        my_plane.add(my_plane.get_axis_labels())
        self.add(my_plane)
        self.wait(2)

class SimpleVectorField(Scene):
    CONFIG = {
        "plane_kwargs": {
            "color": RED
        }
    }

    def construct(self):
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.add(plane)

        points = [
            x*RIGHT + y*UP
            for x in np.arange(-5, 5, 1)
            for y in np.arange(-5, 5, 1)
        ]

        vec_field = []

        for point in points:
            field = 0.5 * RIGHT + 0.5 * UP
            result = Vector(field).shift(point)
            vec_field.append(result)

        draw_field = VGroup(*vec_field)

        self.play(ShowCreation(draw_field))

class FieldWithAxes(Scene):
    CONFIG = {
        "plane_kwargs": {
            "color": RED_B
        },
        "point_charge_loc": 0.5 * RIGHT - 1.5 * UP
    }
    def construct(self):
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.add(plane)

        field = VGroup(*[
            self.calcField(x * RIGHT + y * UP)
            for x in np.arange(-9, 9, 1)
            for y in np.arange(-5, 5, 1)
        ])

        self.play(ShowCreation(field))

    def calcField(self, point):
        ## Calculating the field at a single point
        x, y = point[:2]

        Rx, Ry = self.point_charge_loc[:2]

        ## Calculating the distance from the point charge
        r = math.sqrt((x - Rx) ** 2 + (y - Ry) ** 2)

        efield = (point - self.point_charge_loc) / r ** 3
        # efield = np.array((-y,x,0))/math.sqrt(x**2+y**2)  #Try one of these two fields
        # efield = np.array(( -2*(y%2)+1 , -2*(x%2)+1 , 0 ))/3  #Try one of these two fields
        return Vector(efield).shift(point)
