class ExpandList():
    # method to expand a list with multiple values
    def expand(list: list, *values):
        for value in values:
            list.append(value)
        return list