class JackTokenizer:
    """
    This class will generate a list of tokens.
    """

    ###################
    # ---- CONSTS ----#
    ###################
    KEYWORDS = ["class", "constructor", "function", "method", "field", "static",
                "var", "int", "char", "boolean", "void", "true", "false", "null",
                "this", "let", "do", "if", "else", "while", "return"
                ]
    SYMBOL = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*",
              "/", "&", "|", "<", ">", "=", "~"]

    def __init__(self, file):
        """
        Constructor of the parser class
        :param file: .jack file.
        """
        self.__file = open(file, 'r')
        self.__cleaned_lst = []
        self.__index = 0
        self.__stringConstFlag = False
        self.__comment_flag = False
        self.__skip_twice = False
        for line in self.__file:
            self.__token = ""
            for index, char in enumerate(line):
                if (char == '"' or self.__stringConstFlag) and not self.__comment_flag:
                    self.__stringConstFlag = True
                    if char == '"' and len(self.__token) != 0:
                        self.__stringConstFlag = False
                        self.__cleaned_lst.append("<stringConstant> " + self.__token[1:] + " </stringConstant>\n")
                        self.__token = ''
                    else:
                        if char == '<':
                            self.__token += "&lt;"
                        elif char == '>':
                            self.__token += "&gt;"
                        elif char == '&':
                            self.__token += "&amp;"
                        else:
                            self.__token += char
                    continue
                elif self.__skip_twice:
                    self.__skip_twice = False
                    continue
                elif char == "/" and line[index + 1] == "/":
                    break
                elif char == "/" and line[index + 1] == "*":
                    self.__comment_flag = True
                    continue
                elif char == "*" and line[index + 1] == "/":
                    self.__comment_flag = False
                    self.__skip_twice = True
                    continue
                elif self.__comment_flag:
                    continue
                elif char == "\r" or char == '\n':
                    if len(self.__token) != 0:
                        self.__cleaned_lst.append(self.__token)
                        self.__token = ''
                    break
                elif char.isspace() and len(self.__token) == 0:
                    continue
                elif char in self.SYMBOL:
                    if char == '<':
                        self.__cleaned_lst.append("<symbol> &lt; </symbol>\n")
                    elif char == '>':
                        self.__cleaned_lst.append("<symbol> &gt; </symbol>\n")
                    elif char == '&':
                        self.__cleaned_lst.append("<symbol> &amp; </symbol>\n")
                    else:
                        self.__cleaned_lst.append("<symbol> " + char + " </symbol>\n")
                    continue
                elif not (line[index + 1].isspace()) and line[index + 1] not in self.SYMBOL:
                    self.__token += char
                    continue
                elif line[index + 1].isspace() or line[index + 1] in self.SYMBOL:
                    self.__token += char
                    if self.__token in self.KEYWORDS:
                        self.__cleaned_lst.append("<keyword> " + self.__token + " </keyword>\n")
                    elif self.__token.isdigit():
                        self.__cleaned_lst.append("<integerConstant> " + self.__token + " </integerConstant>\n")
                    else:
                        self.__cleaned_lst.append("<identifier> " + self.__token + " </identifier>\n")
                    self.__token = ""
        self.__file.close()

    def has_more_tokens(self):
        """
        :return: bool returns true if there are still anymore tokens false otherwise
        """
        return not(self.__index == (len(self.__cleaned_lst) - 1))

    def advance(self):
        """
        advances the current token in the tokenizer
        :return: None
        """
        self.__index = self.__index + 1

    def get_current_token(self):
        """
        :return: returns the current token
        """
        return self.__cleaned_lst[self.__index]

    def token_type(self):
        """
        :return: string The type of the current token
        """
        if "<keyword>" in self.__cleaned_lst[self.__index]:
            return "KEYWORD"
        elif "<integerConstant>" in self.__cleaned_lst[self.__index]:
            return "INT_CONST"
        elif "<stringConstant>" in self.__cleaned_lst[self.__index]:
            return "STRING_CONST"
        elif "<symbol>" in self.__cleaned_lst[self.__index]:
            return "SYMBOL"
        elif "<identifier>" in self.__cleaned_lst[self.__index]:
            return "IDENTIFIER"

    def keyword(self):
        """
        !!! SHOULD BE CALLED ONLY IF THE TOKENTYPE IS KEYWORD !!!
        <keyword> keyword </keyword>
        :return: the keyword in upper case
        """
        return self.__cleaned_lst[self.__index][10: -12].upper()

    def symbol(self):
        """
        !!! SHOULD BE CALLED ONLY IF THE TOKENTYPE IS SYMBOL !!!
        <symbol> symbol </symbol>
        :return: the symbol
        """
        return self.__cleaned_lst[self.__index][9: -11]

    def identifier(self):
        """
        !!! SHOULD BE CALLED ONLY IF THE TOKENTYPE IS IDENTIFIER !!!
        <identifier> identifier </identifier>
        :return: the identifier.
        """
        return self.__cleaned_lst[self.__index][13: -15]

    def intVal(self):
        """
        !!! SHOULD BE CALLED ONLY IF THE TOKENTYPE IS INT_CONST !!!
        <integerConstant> intConst </integerConstant>
        :return: the integer value of the current token.
        """
        return self.__cleaned_lst[self.__index][18: -20]

    def stringVal(self):
        """
        !!! SHOULD BE CALLED ONLY IF THE TOKENTYPE IS STRING_CONST !!!
        <stringConstant> string </stringConstant>
        :return: the string value of the current token without double quotes.
        """
        return self.__cleaned_lst[self.__index][17: -18]

    def testXML(self):
        """
        export an xml test file.
        :return: .
        """
        f = open("test.xml", "w")
        f.writelines(["<tokens>\n"])
        f.writelines(self.__cleaned_lst)
        f.writelines(["</tokens>\n"])
        f.close()

    def peek(self):
        """
        :return: the next token without advancing the tokenizer
        """
        return self.__cleaned_lst[self.__index + 1]

    def wasItIdentifier(self):
        """
        :return: true if the previous token was an identifier else false
        """
        return self.__cleaned_lst[self.__index - 1][:12] == "<identifier>"

    def wasItSymbol(self):
        """
        :return: true if previous token was symbol except for ")" and "]", else false
        """
        if self.__cleaned_lst[self.__index - 1][9:10] == ")" or self.__cleaned_lst[self.__index - 1][9:10] == "]":
            return False
        return self.__cleaned_lst[self.__index - 1][:8] == "<symbol>"

    def wasItReturn(self):
        """
        :return: true if previous token was return keyword else false
        """
        return self.__cleaned_lst[self.__index - 1][10:16] == "return"
