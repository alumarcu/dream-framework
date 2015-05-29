def toss_coin(sides):
    """
    Choose a value from a given list of values
    [the coin can have more than two sides]
    """
    from random import choice
    return choice(sides)


def line_count(self, file_path):
    """
    Count the number of lines in a file with given path
    """
    with open(file_path) as file:
        return sum(1 for ln in file)