####### imports ########
import os
import sys
import CompilationEngine as Cn
########################


def compileJack(argv):
    """
    This function will run the process of compiling the jack programs.
    :param argv: the users input
    """
    # This loop iterates over the user's inputs (or arguments).
    for i in range(1, len(argv)):
        # DIR:
        # This if statement verifies that the argument is actually a dir.
        if os.path.isdir(argv[i]):
            if argv[i][-1] != "/":
                argv[i] += "/"
            for file in os.listdir(argv[i]):
                if file.endswith(".jack"):
                    analyzed_file = Cn.CompilationEngine(argv[i]+file, file[:-5])
                    analyzed_file.CompileClass()
        # FILE:
        # Enter's if the specific argument is an xml file only.
        elif argv[i].endswith(".jack"):
            analyzed_file = Cn.CompilationEngine(argv[i], argv[i].split("/")[-1][:-5])
            analyzed_file.CompileClass()


def main(argv):
    compileJack(argv)
    return 0


if __name__ == "__main__":
    main(sys.argv)
