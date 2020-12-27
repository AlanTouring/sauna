"""This module is an example of a class, which is used in a unit test."""


# pylint: disable=R0903 # too few methods
class Example:
    """This class is an examples, for which test cases are written.
    The class itself has no real function."""
    def __init__(self):
        self.value = 4

    def get_value(self):
        """This is a simple getter function."""
        return self.value
    # pylint: enable=R0903


if __name__ == '__main__':
    example = Example()
    RESULT = example.get_value()
    LABEL = '>> The value is :='
    print(LABEL, RESULT, "<<", sep=" ", end='')
