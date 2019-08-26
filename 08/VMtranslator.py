####### imports ########
import os
import sys
import parser
import coder

########################
##################
#    CONSTANTS   #
##################


def pre_output(argv):
    """
    This function will create new file (.hack file),
    and will output the compiled assembley file to it.
    :param argv: the users input
    :return: None
    """
    BOOT_STRAP = [["call", "Sys.init", "0"]]  # bootstrap initialization
    boot_strap_code = coder.Coder(BOOT_STRAP, "")
    boot_strap_coded_lines = boot_strap_code.get_list()
    for i in range(1, len(argv)):
        # This loop iterates over the user's inputs (or arguments).
        if os.path.isdir(argv[i]):
            if argv[i][-1] != "/":
                dir_name = argv[i].split("/")[-1]
            else:
                dir_name = argv[i].split("/")[-2]
            asm_file = open(argv[i] + "/" + dir_name + ".asm", "w")
            asm_file.writelines(["@256\n", "D=A\n", "@SP\n", "M=D\n"])
            asm_file.writelines(boot_strap_coded_lines[0])
            for file in os.listdir(argv[i]):
                if file.endswith(".vm"):
                    # This if statement verifies that the argument is actually a dir.
                    final_output(argv[i] + "/" + file, asm_file)
            asm_file.close()
        elif argv[i].endswith(".vm"):
            asm_file = open(argv[i][:-2] + "asm", "w")
            asm_file.writelines(["@256\n", "D=A\n", "@SP\n", "M=D\n"])
            asm_file.writelines(boot_strap_coded_lines[0])
            # Enter's if the specific argument is an assembly file only.
            final_output(argv[i], asm_file)
            asm_file.close()


def final_output(file_name, asm_file):
    """
    The input generator
    :param file_name: The VM file to be complied.
    :param asm_file: The asm file to be written on.
    :return: None
    """
    # calling the vm file
    vm_file = open(file_name, "r")
    parsed_file = parser.Parser(vm_file)
    parsed_lines = parsed_file.get_list()
    code = coder.Coder(parsed_lines, file_name.split("/")[-1][:-2])
    coded_lines = code.get_list()
    vm_file.close()
    for command in coded_lines:
        # writing the complied lines into the new file (.hack)
        asm_file.writelines(command)


def main(argv):
    pre_output(argv)
    return 0


if __name__ == "__main__":
    main(sys.argv)
