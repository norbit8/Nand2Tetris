class Parser:
    """
    This class will generate a list of commands.
    """

    def __init__(self, file):
        """
        Constructor of the parser class
        :param file: .vm file.
        """
        self.__file = file

    def get_list(self):
        """
        :return: return parsed list
        """
        cleaned_lst = []
        list_of_lines = self.__file.readlines()
        for item in list_of_lines:
            cleaned_line = []
            item = item.replace("\r", "")
            item = item.replace("\n", "")
            item = item.replace("\t", " ")
            tmp_str = item.split("//")[0]  # ignore comments
            if tmp_str == "":
                continue
            tmp_str = tmp_str.split(" ")
            for string in tmp_str:
                if string != "":
                    cleaned_line.append(string)
            if len(cleaned_line) > 0:
                cleaned_lst.append(cleaned_line)
        return cleaned_lst

