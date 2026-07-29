class ThemeInterpreter:

    @staticmethod
    def describe(value, labels):

        if value < 0.2:
            return labels[0]

        if value < 0.4:
            return labels[1]

        if value < 0.6:
            return labels[2]

        if value < 0.8:
            return labels[3]

        return labels[4]