class SymbolTable:
    TYPE = 0
    KIND = 1
    INDEX = 2

    def __init__(self):
        """
        creates a new empty symbol table
        """
        self.__class_symbol_table = dict()
        self.__sub_symbol_table = dict()
        self.__static_counter, self.__var_counter, \
        self.__field_counter, self.__arg_counter = 0, 0, 0, 0

    def startSubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names
        in the previous subroutine's scope.)
        """
        self.__sub_symbol_table.clear()
        self.__var_counter, self.__arg_counter = 0, 0

    def define(self, name, var_type, kind):
        """
        Defines a new identifier of a given name, type and kind,
        and assigns it a running index.
        :param name: String
        :param var_type: String
        :param kind: String
        """
        if kind == "STATIC":
            self.__class_symbol_table[name] = (var_type, kind, self.varCount(kind))
            self.__static_counter += 1
            # print(name)
            # print(self.__class_symbol_table[name])
        elif kind == "FIELD":
            self.__class_symbol_table[name] = (var_type, kind, self.varCount(kind))
            self.__field_counter += 1
            # print(name)
            # print(self.__class_symbol_table[name])
        elif kind == "ARGUMENT":
            self.__sub_symbol_table[name] = (var_type, kind, self.varCount(kind))
            self.__arg_counter += 1
            # print(name)
            # print(self.__sub_symbol_table[name])
        elif kind == "VAR":
            self.__sub_symbol_table[name] = (var_type, kind, self.varCount(kind))
            self.__var_counter += 1
            # print(name)
            # print(self.__sub_symbol_table[name])

    def varCount(self, kind):
        """
        :param kind: String
        :return: The number of variables of the given kind already defined in the
        current scope
        """
        if kind == "STATIC":
            return self.__static_counter
        if kind == "FIELD":
            return self.__field_counter
        if kind == "ARGUMENT":
            return self.__arg_counter
        if kind == "VAR":
            return self.__var_counter


    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        :param name: String
        :return: NONE if the identifier in the unknown in the current scope.
        """
        if name in self.__sub_symbol_table:
            return self.__sub_symbol_table[name][self.KIND]
        elif name in self.__class_symbol_table:
            return self.__class_symbol_table[name][self.KIND]
        else:
            return "NONE"

    def typeOf(self, name):
        """
        :param name: String
        :return: The type of the named identifier in the current scope.
        """
        if name in self.__sub_symbol_table:
            return self.__sub_symbol_table[name][self.TYPE]
        elif name in self.__class_symbol_table:
            return self.__class_symbol_table[name][self.TYPE]

    def indexOf(self, name):
        """
        :param name:
        :return: The index assigned to named identifier.
        """
        if name in self.__sub_symbol_table:
            return self.__sub_symbol_table[name][self.INDEX]
        elif name in self.__class_symbol_table:
            return self.__class_symbol_table[name][self.INDEX]

    def print_dicts(self):
        """
        test method. prints the dictionaries
        :return:
        """
        print("class")
        print(self.__class_symbol_table)
        print("sub")
        print(self.__sub_symbol_table)
