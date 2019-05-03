class Parser:
    """
    This class will generate a 2d list which contains the assembly lines
    parsed according to the specification of the exercise.
    """
    C_INSTRUCTION_SIGNS = ["=", ";", "+", "-", "<<", ">>", "&", "|", "0", "1", "!", "*"]
    A_INSTRUCTION_SIGN = "@"

    def __init__(self, file):
        """
        Constructor of the parser class
        :param file: .asm file.
        """
        self.__file = file

    def get_list(self):
        """
        :return: return parsed list
        """
        parsed_list = []
        list_of_lines = self.__file.readlines()
        for item in list_of_lines:
            item = item.replace(" ", "")
            if item[:2] == "//":
                continue
            elif item[0] == self.A_INSTRUCTION_SIGN:
                parsed_list.append(self.clean_line(item))
                continue
            if item[0] == "(":
                parsed_list.append(self.clean_line(item))
                continue
            for sign in self.C_INSTRUCTION_SIGNS:
                if sign in item:
                    parsed_list.append(self.clean_line(item))
                    break
        return parsed_list

    def clean_line(self, item):
        """
        clean the given line
        :param self: ...
        :param item: a given line in a asm file
        :return: cleaned line
        """
        tmp = item.replace("\r", "")  # deletes the "\r" chars
        tmp = tmp.replace("\n", "")  # deletes the "\n" chars
        cleaned_line = tmp.split("//")[0]  # ignore comments
        return cleaned_line
