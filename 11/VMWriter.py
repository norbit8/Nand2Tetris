class VMWriter:
    """
    VMWriter class
    """

    def __init__(self, file):
        """
        creates a new empty symbol table
        """
        self.__output = open(file[:-4] + "vm", "w")

    def writePush(self, segment, index):
        """
        Writes a VM push command
        :param segment: CONST, ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: string
        """
        self.__output.write("push " + segment + " " + index + "\n")

    def writePop(self, segment, index):
        """
        Writes a VM pop command
        :param segment: CONST, ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: string
        """
        self.__output.write("pop " + segment + " " + index + "\n")

    def writeArithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command: ADD , SUB , NEG , EQ , GT , LT , AND , OR , NOT
        """
        self.__output.write(command + "\n")

    def writeLabel(self, label):
        """
        Writes a VM label command
        :param label: String
        """
        self.__output.write("label " + label + "\n")

    def writeGoto(self, label):
        """
        Writes a VM label command
        :param label: String
        """
        self.__output.write("goto " + label + "\n")

    def writeIf(self, label):
        """
        Writes a VM If-goto command
        :param label: String
        """
        self.__output.write("if-goto " + label + "\n")

    def writeCall(self,name, nArgs):
        """
        Writes a VM call command
        :param name: String
        :param nArgs: Int
        """
        self.__output.write("call " + name + " " + nArgs + "\n")

    def writeFunction(self, name, nLocals):
        """
        Writes a VM function command
        :param name: String
        :param nLocals: int
        """
        self.__output.write("function " + name + " " + nLocals + "\n")

    def writeRetun(self):
        """
        Writes a VM return command
        """
        self.__output.write("return\n")

    def close(self):
        """
        Closes the output file
        """
        self.__output.close()
