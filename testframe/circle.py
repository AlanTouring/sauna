"""This module is an example of a class, which is used in a unit test."""


class Circle:
    """This class is an examples, which for which test cases are written.
        The class is class calculates area and outline of a circle."""
    def __init__(self):
        self.radius = 1

    def get_area(self):
        """This is function calculates the area of the circle."""
        return 3.14 * self.radius * self.radius

    def set_radius(self, radius):
        """This is a simple setter function."""
        self.radius = radius

    def get_radius(self):
        """This is a simple getter function."""
        return self.radius

    def get_outline(self):
        """This is function calculates the outline of the circle."""
        return 2 * 3.14 * self.radius


if __name__ == '__main__':
    circle = Circle()
    circle.set_radius(2)
    area = circle.get_area()
    LABEL = '>> The area of a circle is :='
    print(LABEL, area, "<<", sep=" ", end='')
