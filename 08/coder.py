class Coder:
    """
    This class is the coder class, it translates each parsed line into
    the correspond asm lines.
    """
    ##################
    #    GLOBAL      #
    ##################
    call_counter = 0

    ##################
    #    CONSTANTS   #
    ##################

    C_INSTRUCTION_SIGNS = ["=", ";", "+", "-", "<<", ">>", "&", "|", "0", "1", "!", "*"]
    A_INSTRUCTION_SIGN = "@"
    SET_A_TO_D = ["D=A\n"]
    STORE_R13 = ["@R13\n", "M=D\n"]
    STORE_R14 = ["@R14\n", "M=D\n"]
    STORE_R15 = ["@R15\n", "M=D\n"]
    ADD_VALUES_R14 = ["@R14\n", "D=D+M\n"]
    AND_VALUES_R14 = ["@R14\n", "D=D&M\n"]
    OR_VALUES_R14 = ["@R14\n", "D=D|M\n"]
    NOT_VALUES_R14 = ["@R14\n", "D=!D\n"]
    SUB_VALUES_R14 = ["@R14\n", "D=D-M\n"]
    NEG = ["@SP\n", "A=M-1\n", "M=-M\n"]  # Negates the value in the stack.
    PUSH_LINES_TRANS = ["@SP\n", "A=M\n", "M=D\n", "@SP\n", "M=M+1\n"]  # Pushes the value stored in D into the stack.
    POP_LINES_TRANS = ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n"]  # Pops the value from the stack and stores it in D.
    LCL_ARG_THIS_THAT = ["local", "argument", "this", "that"]
    LCL_ARG_THIS_THAT_FIRST_TRANS = ["D=D+A\n", "@R15\n", "M=D\n"]
    LCL_ARG_THIS_THAT_SECOND_TRANS = ["@R15\n", "A=M\n", "M=D\n"]  # R15 = D
    SET_MIN1_TO_D = ["@1\n", "D=-A\n"]  # D = -1.
    SET_ZERO_TO_D = ["D=0\n"]  # Sets D to zero.
    STATIC_TEMP_POINTER = ["static", "temp", "pointer"]  # The structure of the memory command.
    D_PLUS_TWO = ["@2\n", "D=D+A\n"]  # D = D + 2.


    ##################
    #   CONSTRUCTOR  #
    ##################

    def __init__(self, parsed_lines, file_name):
        """
        A constructor for the Coder class.
        :param parsed_lines: A list of lines after they have been parsed and "cleaned"
        """
        self.__parsed_lines = parsed_lines
        self.__arithmetic_logic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.__mem_access_commands = ["pop", "push"]
        self.__goto = ["if-goto", "goto", "label"]
        self.__function = ["call", "function", "return"]
        self.__file_name = file_name
        self.__eq = 0
        self.__gt = 0
        self.__lt = 0
        self.__func_name = ""

    def get_list(self):
        """
        :return: A list containing the asm code representation of the lines in the file
        """
        asm_total_lst = []
        for index, command in enumerate(self.__parsed_lines):
            if command[0] in self.__arithmetic_logic:
                # If the command is a STACK OPERATION OF ARITHMETIC/LOGICAL COMMAND
                asm_total_lst.append(self.arithmet_logic_lst(command[0]))
            elif command[0] in self.__mem_access_commands:
                # If the command is a MEMORY ACCESS COMMAND:
                asm_total_lst.append(self.write_push_pop(command[0], command[1], command[2]))
            elif command[0] in self.__goto:
                # That's a goto command
                asm_total_lst.append(self.write_branching(command[0], command[1]))
            elif command[0] in self.__function:
                # --- FUNCTIONS ---
                # function foo nVars
                # call foo nArgs
                # return
                asm_total_lst.append(self.func_mux(command))
        return asm_total_lst
        # --------- HERE MORE FUNCTIONS WILL APPEAR WHEN WE IMPLEMENT PROJECT 8 ------------

    def func_mux(self, command):
        """
        This function determines what kind of "function command" wer'e dealing with
        and it will execute the corresponding function.
        :param command: function foo nVars, call foo nArgs, return.
        :return: List of asm commands.
        """
        lst = []
        if command[0] == "function":
            self.__func_name = command[1]
            lst = self.write_function(command[1], command[2])
        elif command[0] == "call":
            self.__func_name = command[1]
            lst = self.write_call(command[1], command[2])
        elif command[0] == "return":
            lst = self.write_return()
        return lst

    def write_function(self, func_name, nvars):
        """
        :param func_name: function name.
        :param nvars: number of vars.
        :return: asm list.
        """
        lst = ["//function " + func_name + nvars + "\n"]
        lst.extend(["(" + self.__func_name + ")\n"])
        for i in range(int(nvars)):
            lst.extend(["@0\n", "D=A\n"] + self.PUSH_LINES_TRANS)
        return lst

    def write_call(self, func_name, nargs):
        """
        :param func_name: The name of the function.
        :param nargs: number of arguments.
        :return: asm list.
        """
        Coder.call_counter += 1
        # ---- PUSH returnAddress ----
        lst = [
                "//call " + func_name + " " + nargs + " " + str(Coder.call_counter) + "\n",
                "@" + func_name + "$" + "ret" + "." + str(Coder.call_counter) + '\n',
                "D=A\n"
              ]
        lst.extend(self.PUSH_LINES_TRANS)
        # ---- PUSH LCL -----
        lst.extend(["@LCL\n", "D=M\n"] + self.PUSH_LINES_TRANS)
        # ---- PUSH ARG -----
        lst.extend(["@ARG\n", "D=M\n"] + self.PUSH_LINES_TRANS)
        # ---- PUSH THIS -----
        lst.extend(["@THIS\n", "D=M\n"] + self.PUSH_LINES_TRANS)
        # ---- PUSH THAT -----
        lst.extend(["@THAT\n", "D=M\n"] + self.PUSH_LINES_TRANS)
        # ---- Repositions ARG -----
        lst.extend(["@SP\n", "D=M\n", "@5\n", "D=D-A\n", "@" + str(nargs) + "\n", "D=D-A\n", "@ARG\n", "M=D\n"])
        # ---- Repositions LCL -----
        lst.extend(["@SP\n", "D=M\n", "@LCL\n", "M=D\n"])
        # ---- goto functionName -----
        lst.extend(["@" + func_name + "\n", "0;JMP\n"])
        # ----- LABELING: ------
        lst.extend(["(" + func_name + "$" + "ret" + "." + str(Coder.call_counter) + ")\n"])
        return lst

    def write_return(self):
        """
        Handles the return request
        :return: asm list.
        """
        lst = (["//return\n", "@LCL\n", "D=M\n", "@R13\n", "M=D\n"])  # endFrame = LCL
        lst.extend(["@5\n", "D=D-A\n", "A=D\n", "D=M\n", "@R14\n", "M=D\n"])  # now R14 is retAddr
        # *ARG = pop()
        lst.extend(self.POP_LINES_TRANS + ["@ARG\n", "A=M\n", "M=D\n"])
        # SP = ARG + 1
        lst.extend(["@ARG\n", "D=M+1\n", "@SP\n", "M=D\n"])
        # setting the endFrame to D again
        lst.extend(["@R13\n", "D=M\n"])
        lst.extend(["@1\n", "D=D-A\n", "A=D\n", "D=M\n", "@THAT\n", "M=D\n"])  # restores THAT
        # setting the endFrame to D again
        lst.extend(["@R13\n", "D=M\n"])
        lst.extend(["@2\n", "D=D-A\n", "A=D\n", "D=M\n", "@THIS\n", "M=D\n"])  # restores THIS
        # setting the endFrame to D again
        lst.extend(["@R13\n", "D=M\n"])
        lst.extend(["@3\n", "D=D-A\n", "A=D\n", "D=M\n", "@ARG\n", "M=D\n"])  # restores ARG
        # setting the endFrame to D again
        lst.extend(["@R13\n", "D=M\n"])
        lst.extend(["@4\n", "D=D-A\n", "A=D\n", "D=M\n", "@LCL\n", "M=D\n"])  # restores LCL
        # goto retAddr
        lst.extend(["@R14\n", "A=M\n", "0;JMP\n"])
        return lst

    def write_branching(self, command, label_name):
        """
        A function which determines what type of branching we are dealing with.
        :param command: A string which represent the command
        :param label_name: A string which represent the label to jump/not to jump to.
        :return: A list representing the assembly code that was
                  translated from the given vm line.
        """
        lst_to_return = []
        if command == "label":
            lst_to_return = self.writeLabel(label_name)
        if command == "goto":
            lst_to_return = self.writeGoto(label_name)
        if command == "if-goto":
            lst_to_return = self.writeIf(label_name)
        return lst_to_return

    def writeLabel(self, label_name):
        """
        This function returns a list of asm code representing a label command.
        :param label_name: A string which represent the label to jump/not to jump to.
        :return: A list representing the assembly code that was
                  translated from the given vm line.
        """
        lst = ["(" + self.__func_name + "$" + label_name + ")\n"]
        return lst

    def writeGoto(self, label_name):
        """
        This function returns a list of asm code representing a goto-command.
        :param label_name: A string which represent the label to jump/not to jump to.
        :return: A list representing the assembly code that was
                  translated from the given vm line.
        """
        lst = [
               "// goto " +label_name + "\n",
               "@" + self.__func_name + "$" + label_name + "\n",
               "0;JMP\n"
              ]
        return lst

    def writeIf(self, label_name):
        """
        This function returns a list of asm code representing an if goto-command.
        :param label_name: A string which represent the label to jump/not to jump to.
        :return: A list representing the assembly code that was
                  translated from the given vm line.
        """
        lst = [
                "//if-goto " + label_name + "\n",
                "@" + self.__func_name + "$" + label_name + "\n",
                "D;JNE\n"
              ]
        lst = self.POP_LINES_TRANS + lst
        return lst

    def arithmet_logic_lst(self, command):
        """
        This function deals with arithmetic part of the IL language.
        :param command: eq add sub neg gt lt and or not.
        :return: List of ASM commands.
        """
        asm_commands = []
        if command == "eq":
            # TRUE OR FALSE
            # Before each label we concatenate the file name and number to the name of the loop so
            # there will not be multiple loops with the same name
            asm_commands += ["//eq\n"] + self.POP_LINES_TRANS + self.STORE_R14 + \
                            self.POP_LINES_TRANS + self.SUB_VALUES_R14 + \
                            ["@" + self.__file_name[:-1] + "TRUEEQ" + str(self.__eq) + "\n", "D;JEQ\n"] + \
                            ["@" + self.__file_name[:-1] + "FALSEEQ" + str(self.__eq) + "\n", "0;JMP\n"] + \
                            ["(" + self.__file_name[:-1] + "TRUEEQ" + str(self.__eq) + ")\n"] + self.SET_MIN1_TO_D + \
                            self.PUSH_LINES_TRANS + ["@" + self.__file_name[:-1] +
                                                     "ENDEQ" + str(self.__eq) + "\n", "0;JMP\n"] + \
                            ["(" + self.__file_name[:-1] + "FALSEEQ" + str(self.__eq) + ")\n"] + self.SET_ZERO_TO_D + \
                            self.PUSH_LINES_TRANS + ["(" + self.__file_name[:-1] + "ENDEQ" + str(self.__eq) + ")\n"]
            self.__eq += 1

        elif command == "add":
            # ADDS A VALUE
            asm_commands += ["//add\n"] + self.POP_LINES_TRANS + self.STORE_R14 + \
                            self.POP_LINES_TRANS + self.ADD_VALUES_R14 + \
                            self.PUSH_LINES_TRANS

        elif command == "sub":
            # ADDS A VALUE
            asm_commands += ["//sub\n"] + self.POP_LINES_TRANS + self.STORE_R14 + \
                            self.POP_LINES_TRANS + self.SUB_VALUES_R14 + \
                            self.PUSH_LINES_TRANS

        elif command == "neg":
            # ADDS A VALUE
            asm_commands += ["//neg\n"] + self.NEG

        elif command == "gt":
            # TRUE OR FALSE
            # Before each label we concatenate the file name and number to the name of the loop so
            # there will not be multiple loops with the same name
            asm_commands += ["//gt\n"] + self.POP_LINES_TRANS + self.STORE_R13 + \
                            [
                                '@' + self.__file_name[:-1] + 'YNEGGT' + str(self.__gt) + '\n', 'D;JLT\n',
                                '@' + self.__file_name[:-1] + 'YNOTNEGGT' + str(self.__gt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'YNEGGT' + str(self.__gt) + ')\n', '@R15\n',
                                'M=0\n', '@' + self.__file_name[:-1] + 'STOREXSIGNGT' + str(self.__gt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'YNOTNEGGT' + str(self.__gt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@R15\n', 'M=D\n',
                                '(' + self.__file_name[:-1] + 'STOREXSIGNGT' + str(self.__gt) + ')\n', '@SP\n',
                                'A=M-1\n', 'D=M\n',
                                '@R13\n', 'M=D-M\n',
                                '@' + self.__file_name[:-1] + 'XNEGGT' + str(self.__gt) + '\n', 'D;JLT\n',
                                '@' + self.__file_name[:-1] + 'XNOTNEGGT' + str(self.__gt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'XNEGGT' + str(self.__gt) + ')\n', '@R14\n',
                                'M=0\n', '@' + self.__file_name[:-1] + 'CHECKSIGNSGT' + str(self.__gt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'XNOTNEGGT' + str(self.__gt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@R14\n', 'M=D\n',
                                '(' + self.__file_name[:-1] + 'CHECKSIGNSGT' + str(self.__gt) + ')\n', '@R14\n',
                                'D=M\n', '@R15\n',
                                'D=D+M\n', 'D=D+1\n',
                                '@' + self.__file_name[:-1] + 'DIFFSIGNSGT' + str(self.__gt) + '\n', 'D;JEQ\n',
                                '@' + self.__file_name[:-1] + 'SAMESIGNSGT' + str(self.__gt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'DIFFSIGNSGT' + str(self.__gt) + ')\n', '@R14\n',
                                'D=M\n', '@' + self.__file_name[:-1] + 'TRUEGT' + str(self.__gt) + '\n',
                                'D;JLT\n', '@' + self.__file_name[:-1] + 'FALSEGT' + str(self.__gt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'TRUEGT' + str(self.__gt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@SP\n', 'A=M-1\n',
                                'M=D\n', '@' + self.__file_name[:-1] + 'ENDGT' + str(self.__gt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'FALSEGT' + str(self.__gt) + ')\n',
                                '@0\n', 'D=A\n',
                                '@SP\n', 'A=M-1\n',
                                'M=D\n', '@' + self.__file_name[:-1] + 'ENDGT' + str(self.__gt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'SAMESIGNSGT' + str(self.__gt) + ')\n',
                                '@R13\n', 'D=M\n',
                                '@' + self.__file_name[:-1] + 'TRUEGT' + str(self.__gt) + '\n', 'D;JGT\n',
                                '@' + self.__file_name[:-1] + 'FALSEGT' + str(self.__gt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'ENDGT' + str(self.__gt) + ')\n'
                            ]
            self.__gt += 1
        elif command == "lt":
            # TRUE OR FALSE
            # Before each label we concatenate the file name and number to the name of the loop so
            # there will not be multiple loops with the same name
            asm_commands += ["//lt\n"] + self.POP_LINES_TRANS + self.STORE_R13 + \
                            [
                                '@' + self.__file_name[:-1] + 'YNEGLT' + str(self.__lt) + '\n', 'D;JLT\n',
                                '@' + self.__file_name[:-1] + 'YNOTNEGLT' + str(self.__lt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'YNEGLT' + str(self.__lt) + ')\n', '@R15\n',
                                'M=0\n', '@' + self.__file_name[:-1] + 'STOREXSIGNLT' + str(self.__lt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'YNOTNEGLT' + str(self.__lt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@R15\n', 'M=D\n',
                                '(' + self.__file_name[:-1] + 'STOREXSIGNLT' + str(self.__lt) + ')\n', '@SP\n',
                                'A=M-1\n', 'D=M\n',
                                '@R13\n', 'M=D-M\n',
                                '@' + self.__file_name[:-1] + 'XNEGLT' + str(self.__lt) + '\n', 'D;JLT\n',
                                '@' + self.__file_name[:-1] + 'XNOTNEGLT' + str(self.__lt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'XNEGLT' + str(self.__lt) + ')\n', '@R14\n',
                                'M=0\n', '@' + self.__file_name[:-1] + 'CHECKSIGNSLT' + str(self.__lt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'XNOTNEGLT' + str(self.__lt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@R14\n', 'M=D\n',
                                '(' + self.__file_name[:-1] + 'CHECKSIGNSLT' + str(self.__lt) + ')\n', '@R14\n',
                                'D=M\n', '@R15\n',
                                'D=D+M\n', 'D=D+1\n',
                                '@' + self.__file_name[:-1] + 'DIFFSIGNSLT' + str(self.__lt) + '\n', 'D;JEQ\n',
                                '@' + self.__file_name[:-1] + 'SAMESIGNSLT' + str(self.__lt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'DIFFSIGNSLT' + str(self.__lt) + ')\n', '@R14\n',
                                'D=M\n', '@' + self.__file_name[:-1] + 'TRUELT' + str(self.__lt) + '\n',
                                'D;JEQ\n', '@' + self.__file_name[:-1] + 'FALSELT' + str(self.__lt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'TRUELT' + str(self.__lt) + ')\n',
                                '@1\n', 'D=-A\n',
                                '@SP\n', 'A=M-1\n',
                                'M=D\n', '@' + self.__file_name[:-1] + 'ENDLT' + str(self.__lt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'FALSELT' + str(self.__lt) + ')\n',
                                '@0\n', 'D=A\n',
                                '@SP\n', 'A=M-1\n',
                                'M=D\n', '@' + self.__file_name[:-1] + 'ENDLT' + str(self.__lt) + '\n',
                                '0;JMP\n', '(' + self.__file_name[:-1] + 'SAMESIGNSLT' + str(self.__lt) + ')\n',
                                '@R13\n', 'D=M\n',
                                '@' + self.__file_name[:-1] + 'TRUELT' + str(self.__lt) + '\n', 'D;JLT\n',
                                '@' + self.__file_name[:-1] + 'FALSELT' + str(self.__lt) + '\n', '0;JMP\n',
                                '(' + self.__file_name[:-1] + 'ENDLT' + str(self.__lt) + ')\n'
                            ]
            self.__lt += 1
        elif command == "and":
            # TRUE OR FALSE
            asm_commands += ["//and\n"] + self.POP_LINES_TRANS + self.STORE_R14 + \
                            self.POP_LINES_TRANS + self.AND_VALUES_R14 + \
                            self.PUSH_LINES_TRANS

        elif command == "or":
            # TRUE OR FALSE
            asm_commands += ["//or\n"] + self.POP_LINES_TRANS + self.STORE_R14 + \
                            self.POP_LINES_TRANS + self.OR_VALUES_R14 + \
                            self.PUSH_LINES_TRANS

        elif command == "not":
            # VALUE
            asm_commands += ["//not\n"] + ["@SP\n"] + ["A=M-1\n"] + \
                            ["M=!M\n"]

        return asm_commands

    def write_push_pop(self, command, segment, index):
        """
        :param command: the command that appears in vm A.K.A "push" or "pop"
        :param segment: what memory segment is involved in the command
        :param index: the specific register we would like to access within
        the memory segment
        :return: A list with string where each string represents a hack assembly
        command, while the whole lists represents a vm command translation to assembly
        """
        asm_line = []
        if command == "push":
            asm_line = self.write_push(segment, index)
        elif command == "pop":
            asm_line = self.write_pop(segment, index)
        return asm_line

    def write_push(self, segment, index):
        """
        writes the command: "push segment index" to ASM
        :param segment: LOCAL ARGUMENT THIS THAT STATIC TEMP POINTER
        :param index: integer i.
        :return: List of ASM commands.
        """
        # enters a comment into the translation describing what
        # was the equivalent expression in vm
        asm_line = ["// push " + segment + " " + index + "\n"]
        if segment in self.LCL_ARG_THIS_THAT:
            if segment == "local":
                asm_line.append("@LCL\n")
            elif segment == "argument":
                asm_line.append("@ARG\n")
            elif segment == "this":
                asm_line.append("@THIS\n")
            elif segment == "that":
                asm_line.append("@THAT\n")

            # store the base address of the segment in D
            asm_line.append("A=M\n")
            asm_line.append("D=A\n")

            # access the specific register within the segment
            # that is determined by the index
            asm_line.append("@" + index + "\n")
            asm_line.append("D=D+A\n")
            asm_line.append("A=D\n")
            asm_line.append("D=M\n")
        elif segment in self.STATIC_TEMP_POINTER:
            if segment == "static":
                asm_line.append("@" + self.__file_name + index + "\n")
            elif segment == "temp":
                asm_line.append("@R" + str(int(index) + 5) + "\n")
            elif segment == "pointer":
                if index == "0":
                    asm_line.append("@THIS\n")
                elif index == "1":
                    asm_line.append("@THAT\n")
            asm_line.append("D=M\n")
        elif segment == "constant":
            asm_line.append("@" + index + "\n")
            asm_line.append("D=A\n")
        asm_line.extend(self.PUSH_LINES_TRANS)
        return asm_line

    def write_pop(self, segment, index):
        """
        writes the command: "pop segment index" to ASM
        :param segment: LOCAL ARGUMENT THIS THAT STATIC TEMP POINTER
        :param index: integer i.
        :return: List of ASM commands
        """
        asm_line = ["// pop " + segment + " " + index + "\n"]
        if segment in self.LCL_ARG_THIS_THAT:
            if segment == "local":
                asm_line.append("@LCL\n")
            elif segment == "argument":
                asm_line.append("@ARG\n")
            elif segment == "this":
                asm_line.append("@THIS\n")
            elif segment == "that":
                asm_line.append("@THAT\n")
            asm_line.append("D=M\n")
            asm_line.append("@" + index + "\n")
            asm_line.extend(self.LCL_ARG_THIS_THAT_FIRST_TRANS)
            asm_line.extend(self.POP_LINES_TRANS)
            asm_line.extend(self.LCL_ARG_THIS_THAT_SECOND_TRANS)
        elif segment in self.STATIC_TEMP_POINTER:
            asm_line.extend(self.POP_LINES_TRANS)
            if segment == "static":
                asm_line.append("@" + self.__file_name + index + '\n')
            elif segment == "temp":
                asm_line.append("@R" + str(int(index) + 5) + "\n")
            elif segment == "pointer":
                if index == "0":
                    asm_line.append("@THIS\n")
                elif index == "1":
                    asm_line.append("@THAT\n")
            asm_line.append("M=D\n")
        return asm_line
