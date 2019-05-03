class Coder:
    """
    This class is the coder class, it translates each parsed line into
    a 16 bit binary number.
    """
    C_INSTRUCTION_SIGNS = ["=", ";", "+", "-", "<<", ">>", "&", "|", "0", "1", "!", "*"]
    A_INSTRUCTION_SIGN = "@"

    def __init__(self, parsed_lines):
        """
        A constructor for the Coder class.
        :param parsed_lines: A list of lines after they have been parsed and "cleaned"
        """
        self.__parsed_lines = parsed_lines
        self.__symbol_list = {
                              "R0" : 0, "R1" : 1, "R2" : 2, "R3" : 3,
                              "R4" : 4, "R5" : 5, "R6" : 6, "R7" : 7,
                              "R8" : 8, "R9" : 9, "R10" : 10, "R11" : 11,
                              "R12" : 12, "R13" : 13, "R14" : 14, "R15" : 15,
                              "SP" : 0, "LCL" : 1, "ARG" : 2, "THIS" : 3, "THAT" : 4,
                              "SCREEN" : 16384, "KBD" : 24576
                             }
        self.__comp_to_bin = {
                              "0": "1110101010", "1": "1110111111", "-1": "1110111010", "D": "1110001100",
                              "A": "1110110000", "M": "1111110000", "!D": "1110001101", "!A": "1110110001",
                              "!M": "1111110001", "-D": "1110001111", "-A": "1110110011", "-M": "1111110011",
                              "D+1": "1110011111", "A+1": "1110110111", "M+1": "1111110111", "D-1": "1110001110",
                              "A-1": "1110110010", "M-1": "1111110010", "D+A": "1110000010", "D+M": "1111000010",
                              "D-A": "1110010011", "D-M": "1111010011", "A-D": "1110000111", "M-D": "1111000111",
                              "D&A": "1110000000", "D&M": "1111000000", "D|A": "1110010101", "D|M": "1111010101",
                              "D*A": "1100000000", "D*M": "1101000000", "D<<": "1010110000", "A<<": "1010100000",
                              "M<<": "1011100000", "D>>": "1010010000", "A>>": "1010000000", "M>>": "1011000000",
                             }
        self.__dest_to_bin = {
                              "NULL": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110",
                              "AMD": "111"
                             }
        self.__jmp_to_bin = {
                             "NULL": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101",
                             "JLE": "110", "JMP": "111"
                            }

    def get_list(self):
        """
        :return: A list containing the binary code representation of the lines in the file
        """
        bin_lines = []
        line_counter = 0
        new_symbol_counter = 16
        # --- FIRST SCAN ---
        for line in self.__parsed_lines:
            if line[0] == '(':
                self.__symbol_list[line[1:len(line)-1]] = line_counter
                continue
            line_counter += 1
        # -- SECOND SCAN ---
        for line in self.__parsed_lines:
            if self.A_INSTRUCTION_SIGN in line:
                if line[1:] in self.__symbol_list or line[1:].isdigit():
                    continue
                else:
                    self.__symbol_list[line[1:]] = new_symbol_counter
                    new_symbol_counter += 1
        # -- THIRD SCAN ---
        for line in self.__parsed_lines:
            if self.A_INSTRUCTION_SIGN in line:
                bin_lines.append(self.a_ins_translate(line))
            elif line[0] == '(':
                continue
            else:
                bin_lines.append(self.c_ins_translate(line))
        return bin_lines

    def a_ins_translate(self, line):
        """
        In case of a_instruction this function will translate
        the line into the binary code of it.
        :param line:
        :return:
        """
        if line[1:].isdigit():
            dec_number = int(line[1:])
            bin_number = format(dec_number, "015b")
        else:
            dec_number = self.__symbol_list[line[1:]]
            bin_number = format(dec_number, "015b")
        return "0" + bin_number + "\n"

    def c_ins_translate(self, line):
        """
        In case of c_instruction this function will translate
        the line into the binary code of it.
        :param line: an assembly line.
        :return: the binary translation of a c instruction.
        """
        dest = "NULL"
        jmp = "NULL"
        # Enters this block only if a destination expression appears in line
        if "=" in line:
            dest = line.split("=")[0]
            temp = line.split("=")[1]
            # Enters this block only if a jump expression appears as well
            if ";" in temp:
                comp = temp.split(";")[0]
                jmp = temp.split(";")[1]
            # If no jump expression then there is only a computation
            else:
                comp = temp
        # Enters this block if there is no destination, but there is a jump expression
        elif ";" in line:
           comp = line.split(";")[0]
           jmp = line.split(";")[1]
        # Enters this block if there is no destination and no block
        else:
            comp = line
        # These conditions translate the different possible expressions into binary code
        # according to the given table
        if dest in self.__dest_to_bin:
            bin_dest = self.__dest_to_bin[dest]
        elif dest[::-1] in self.__dest_to_bin:
            bin_dest = self.__dest_to_bin[dest]
        else:
            bin_dest = self.__dest_to_bin["AMD"]
        if comp in self.__comp_to_bin:
            bin_comp = self.__comp_to_bin[comp]
        else:
            bin_comp = self.__comp_to_bin[comp[::-1]]
        bin_jmp = self.__jmp_to_bin[jmp]
        c_inst = bin_comp + bin_dest + bin_jmp
        return c_inst + "\n"
