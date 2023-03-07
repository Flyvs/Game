class ExpandList():
    def expand(list: list, *values):
        """
        expands a list with multiple values and returns it
        """
        for value in values:
            list.append(value)
        return list