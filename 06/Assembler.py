####### imports ########
import os
import sys
import parser
import coder

########################

###### constants #######
FIRST_ARGUMENT = 1

########################


def final_output(file_name):
    """
    This function will create new file (.hack file),
    and will output the compiled assembley file to it.
    :param file_name: the file to be complied
    :return: None
    """
    # calling the asm file
    asm_file = open(file_name, "r")
    parsed_file = parser.Parser(asm_file)
    parsed_lines = parsed_file.get_list()
    code = coder.Coder(parsed_lines)
    coded_lines = code.get_list()
    asm_file.close()
    # writing the complied lines into the new file (.hack)
    new_file = open(file_name[:-3]+"hack", "w")
    new_file.writelines(coded_lines)
    new_file.close()


def main(argv):
    for i in range(1, len(argv)):
        # This loop iterates over the user's inputs (or arguments).
        if os.path.isdir(argv[i]):
            # This if statement verifies that the argument is actually a dir.
            for j in os.listdir(argv[i]):
                if j.endswith(".asm"):
                    final_output(argv[i]+"/"+j)

        elif argv[i].endswith(".asm"):
            # Enter's if the specific argument is an assembly file only.
            final_output(argv[i])
    return 0


if __name__ == "__main__":
    main(sys.argv)
