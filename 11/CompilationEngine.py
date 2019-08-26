import JackTokenizer as jt
import VMWriter as vmw
import SymbolTable as st


class CompilationEngine:
    """
    Generates the compiler's output
    """

    STOP_VAR = ["WHILE", "IF", "RETURN", "LET", "DO"]
    UNARY_OP = {"-": "neg", "~": "not"}
    OP = {"+": "add", "-": "sub", "/": "call Math.divide 2",
          "=": "eq", "&lt;": "lt", "*": "call Math.multiply 2",
          "&gt;": "gt", "|": "or", "&amp;": "and"}

    def __init__(self, input_file, file_name):
        """
        ------CONSTRUCTOR------
        :param file_name: the file's name
        :param input_file: Input file.
        :param output_file: Output file.
        """
        self.__file_name = file_name
        self.__in = input_file
        self.__out = vmw.VMWriter(input_file)
        self.__tokenizer = jt.JackTokenizer(input_file)
        self.__commands = []
        self.__rec_counter = 0
        self.__symbol_table = st.SymbolTable()
        self.__void_flag = False
        self.__constructor = False
        self.__method_flag = False
        self.__array_flag = False
        self.__class_name = ""
        self.__arg_counter = 0
        self.__var_counter = 0
        self.__curr_func = ""
        self.__label_index = 0
        self.__method_assign_arg_counter = 0

    def eat(self):
        """
        advances the current token and writes it to the file.
        """
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()

    def CompileClass(self):
        """
        Compiles a complete class
        """
        # eat "class"
        self.eat()
        # eat class name
        self.__class_name = self.__tokenizer.identifier()
        self.eat()
        # eat left! curly bracket
        self.eat()
        self.CompileClassVarDec()
        self.CompileSubroutineDec()
        # eat the "}" !
        self.eat()
        self.__out.close()

    def CompileClassVarDec(self):
        """
        Compiles a static variable declaration or a field declaration
        """
        # checks whether the current token is "field" or "static" and returns if it isn't
        if self.__tokenizer.keyword() != "FIELD" and self.__tokenizer.keyword() != "STATIC":
            return
        # continues eating tokens until encounters ";"
        while True:
            # eats the kind, the type and the name
            kind = self.__tokenizer.keyword()
            self.eat()
            if self.__tokenizer.token_type() == "KEYWORD":
                var_type = self.__tokenizer.keyword()
            else:
                var_type = self.__tokenizer.identifier()
            self.eat()
            name = self.__tokenizer.identifier()
            self.eat()
            self.__symbol_table.define(name, var_type, kind)
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ";":
                    self.eat()
                    break
                elif self.__tokenizer.symbol() == ",":
                    while True:
                        if self.__tokenizer.token_type() == "SYMBOL":
                            if self.__tokenizer.symbol() == ";":
                                self.eat()
                                break
                        #  eats the name of the parameter
                        self.eat()
                        name = self.__tokenizer.identifier()
                        self.__symbol_table.define(name, var_type, kind)
                        self.eat()
                        continue
                    break
        # after finishing handling a specific line which was w a class var declaration we
        # check if the next line is one as well
        self.CompileClassVarDec()


    def CompileSubroutineDec(self):
        """
        Compiles a complete method, function, or constructor
        """
        # checks whether the current token is "method", "function" or "constructor" and returns if it isn't
        if self.__tokenizer.keyword() != "METHOD" and self.__tokenizer.keyword() != "FUNCTION" and \
           self.__tokenizer.keyword() != "CONSTRUCTOR":
            return
        # when we start compiling a new subroutine we have to reset the subroutine symbol table
        self.__symbol_table.startSubroutine()
        # EATS THE KEYWORD:
        kind = self.__tokenizer.keyword()
        self.eat()
        # EATS THE TYPE:
        if self.__tokenizer.token_type() == "KEYWORD":
            ret_type = self.__tokenizer.keyword()
        else:
            ret_type = self.__tokenizer.identifier()
        self.eat()
        # EATS THE NAME OF THE FUNCTION:
        self.__curr_func = self.__tokenizer.identifier()
        self.eat()
        if kind == "METHOD":
            self.__method_flag = True
            self.__symbol_table.define("this", self.__class_name, "ARGUMENT")
        elif kind == "CONSTRUCTOR":
            self.__constructor = True
        if ret_type == "VOID":
            self.__void_flag = True
        # EATS THE OPEN '(':
        self.eat()
        # -------------------------
        self.CompileParameterList()
        # eats the ")"
        self.eat()
        self.__var_counter = 0
        self.CompileSubroutineBody()
        # -------------------------
        # after finishing handling a specific line which was w a class var declaration we
        # check if the next line is one as well
        self.CompileSubroutineDec()

    def CompileParameterList(self):
        """
        Compiles a (possibly empty) parameter
        list. Does not handle the enclosing "()"
        """
        # continues eating tokens until encounters ")"
        while True:
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ")":
                    break
            # eats the type and the name of the parameter
            var_type = self.__tokenizer.keyword()
            self.eat()
            name = self.__tokenizer.identifier()
            self.eat()
            self.__symbol_table.define(name, var_type, "ARGUMENT")
            if self.__tokenizer.get_current_token() == "<symbol> , </symbol>\n":
                self.eat()

    def CompileSubroutineBody(self):
        """
        Compiles a subroutine body.
        """
        # eats the '{'
        self.eat()
        self.CompileVarDec()
        # here we write the function command in VM
        self.__out.writeFunction(self.__class_name + "." + self.__curr_func, str(self.__var_counter))
        if self.__method_flag:
            self.__out.writePush("argument", "0")
            self.__out.writePop("pointer", "0")
        if self.__constructor:
            self.__out.writePush("constant", str(self.__symbol_table.varCount("FIELD")))
            self.__out.writeCall("Memory.alloc", "1")
            self.__out.writePop("pointer", "0")
        self.CompileStatements()
        # eats the '}'
        self.eat()

    def CompileVarDec(self):
        """
        Compiles a var declaration.
        """
        # checks whether the current token is "var" and returns if it isn't
        if self.__tokenizer.keyword() != "VAR":
            return
        # continues eating tokens until encounters ";"
        while True:
            # eats the var
            self.eat()
            #  eats the type
            if self.__tokenizer.token_type() == "KEYWORD":
                var_type = self.__tokenizer.keyword()
            else:
                var_type = self.__tokenizer.identifier()
            self.eat()
            name = self.__tokenizer.identifier()
            #######################################################
            # after assigning type and name we eat to reach the ";"
            #######################################################
            self.eat()
            self.__symbol_table.define(name, var_type, "VAR")
            self.__var_counter += 1
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ";":
                    self.eat()
                    break
                elif self.__tokenizer.symbol() == ",":
                    while True:
                        if self.__tokenizer.token_type() == "SYMBOL":
                            if self.__tokenizer.symbol() == ";":
                                self.eat()
                                break
                        #  eats the name of the parameter
                        self.eat()
                        name = self.__tokenizer.identifier()
                        self.__symbol_table.define(name, var_type, "VAR")
                        self.__var_counter += 1
                        self.eat()
                        continue
                    break

        # after finishing handling a specific line which was a class var declaration we
        # check if the next line is one as well
        self.CompileVarDec()

    def CompileStatements(self):
        """
        Compiles a sequence of statements.
        Does not handle the enclosing "{}"
        """
        while self.__tokenizer.keyword() != "RETURN":
            if self.__tokenizer.get_current_token() == "<symbol> } </symbol>\n":
                # closes the statements tag within if/else/while
                return
            elif self.__tokenizer.keyword() == "LET":
                self.CompileLet()
            elif self.__tokenizer.keyword() == "IF":
                self.CompileIf()
            elif self.__tokenizer.keyword() == "WHILE":
                self.CompileWhile()
            elif self.__tokenizer.keyword() == "DO":
                self.CompileDo()
        if self.__tokenizer.get_current_token() == "<keyword> return </keyword>\n":
            self.CompileReturn()

    def CompileLet(self):
        """
        Compiles a let statement
        """
        # eats "LET"
        self.eat()
        # eats varName
        let_kind = self.__symbol_table.kindOf(self.__tokenizer.identifier())
        if let_kind == "FIELD":
            let_kind = "this"
        if let_kind == "VAR":
            let_kind = "local"
        let_index = str(self.__symbol_table.indexOf(self.__tokenizer.identifier()))
        self.eat()
        if self.__tokenizer.get_current_token() == "<symbol> [ </symbol>\n":
            self.__array_flag = True
            self.__out.writePush(let_kind.lower(), let_index)
            # eats "["
            self.eat()
            # eats expression
            self.CompileExpression()
            self.__out.writeArithmetic("add")
            # eats "]"
            self.eat()
        # eats "="
        self.eat()
        # eats expression until encountering the ;
        self.CompileExpression()
        if not self.__array_flag:
            self.__out.writePop(let_kind.lower(), let_index)
        else:
            self.__out.writePop("temp", "0")
            self.__out.writePop("pointer", "1")
            self.__out.writePush("temp", "0")
            self.__out.writePop("that", "0")
            self.__array_flag = False
        # eats ";"
        self.eat()

    def CompileIf(self):
        """
        Compiles an if statement possibly with a trailing else clause
        """
        # eats the 'if'
        self.eat()
        # eats "("
        self.eat()
        self.CompileExpression()
        # eats ")"
        self.eat()
        # eats "{"
        self.eat()
        self.__out.writeArithmetic("not")
        # IF-GOTO:
        self.__label_index += 1
        self.__out.writeIf("else$" + self.__class_name + "." + str(self.__label_index))
        temp = str(self.__label_index)
        self.CompileStatements()
        # GOTO:
        self.__out.writeGoto("endIf$" + self.__class_name + "." + temp)
        # eats "}"
        self.eat()
        if self.__tokenizer.get_current_token() == "<keyword> else </keyword>\n":
            # eats else
            self.eat()
            # eats "{"
            self.eat()
            # LABEL - ELSE
            self.__out.writeLabel("else$" + self.__class_name + "." + temp)
            self.CompileStatements()
            # eats "}"
            self.eat()
        else:
            self.__out.writeLabel("else$" + self.__class_name + "." + temp)
        # LABEL:
        self.__out.writeLabel("endIf$" + self.__class_name + "." + temp)

    def CompileDo(self):
        """
        Compiles a do statement
        """
        self.__arg_counter = 0
        func_name = ""
        tokens_eaten = 0
        # eats the 'do'
        self.eat()
        # eats until the '('
        while self.__tokenizer.get_current_token() != '<symbol> ( </symbol>\n':
            if tokens_eaten % 2 == 0:
                if self.__tokenizer.peek() == '<symbol> . </symbol>\n' and \
                   self.__symbol_table.kindOf(self.__tokenizer.identifier()) != "NONE":
                    self.__arg_counter = 1
                    instance_name = self.__tokenizer.identifier()
                    func_name += self.__symbol_table.typeOf(instance_name)
                    kind = self.__symbol_table.kindOf(instance_name)
                    if kind == "FIELD":
                        kind = "this"
                    if kind == "VAR":
                        kind = "local"
                    index = str(self.__symbol_table.indexOf(instance_name))
                    self.__out.writePush(kind.lower(), index)
                else:
                    func_name += self.__tokenizer.identifier()
            else:
                func_name += self.__tokenizer.symbol()
            tokens_eaten += 1
            self.eat()
        if "." not in func_name:
            func_name = self.__class_name + "." + func_name
            if self.__constructor:
                self.__out.writePush("pointer", "0")
                self.__arg_counter += 1
            elif self.__method_flag:
                self.__out.writePush("pointer", "0")
                self.__arg_counter += 1
        # eats the '('
        self.eat()
        # eats the inside of the parenthesis
        self.CompileExpressionList()
        # eats the ')'
        self.eat()
        # eats the ';'
        self.eat()
        self.__out.writeCall(func_name, str(self.__arg_counter))
        self.__out.writePop("temp", "0")


    def CompileWhile(self):
        """
        Compiles a while statement
        """
        # eats "while"
        self.eat()
        self.__label_index += 1
        self.__out.writeLabel("while$" + self.__class_name + "." + str(self.__label_index))
        temp = str(self.__label_index)
        # eats "("
        self.eat()
        # eats the expression inside of the parenthesis
        self.CompileExpression()
        self.__out.writeArithmetic("not")
        self.__out.writeIf("endWhile$" + self.__class_name + "." + temp)
        # eats ")"
        self.eat()
        # eats "{"
        self.eat()
        self.CompileStatements()
        self.__out.writeGoto("while$" + self.__class_name + "." + temp)
        # eats "}"
        self.eat()
        self.__out.writeLabel("endWhile$" + self.__class_name + "." + temp)

    def CompileReturn(self):
        """
        Compiles a return statement
        """
        # eats the 'return'
        self.eat()
        while True:
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ";":
                    self.eat()
                    break
            self.CompileExpression()
        if self.__void_flag:
            self.__out.writePush("constant", "0")
            self.__void_flag = False
        if self.__constructor:
            self.__constructor = False
        if self.__method_flag:
            self.__method_flag = False
        self.__out.writeRetun()

    def CompileExpression(self):
        """
        Compiles an expression
        """
        self.CompileTerm()
        while True:
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ";" or self.__tokenizer.symbol() == "," or \
                        self.__tokenizer.symbol() == "]" or self.__tokenizer.symbol() == ")":
                    break
                elif self.__tokenizer.symbol() in self.OP:
                    # eats the op
                    op = self.OP[self.__tokenizer.symbol()]
                    self.eat()
                    # compiling the term
                    self.CompileTerm()
                    self.__out.writeArithmetic(op)

    def CompileTerm(self):
        """
        Compiles a term. If the current token is an identifier, the routine must
        distinguish between a variable, an array entry, or a subroutine call.
        A single look-ahead token, which may be one of "[", "(" or ".", suffices
        to distinguish between the possibilities. Any other token is not part of
        this term and should not be advanced over.
        """
        while True:
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ";" or self.__tokenizer.symbol() == "," or \
                   self.__tokenizer.symbol() == "]" or self.__tokenizer.symbol() == ")":
                        break
                elif self.__tokenizer.symbol() == "(":
                    # IF IT WAS A FUNCTION
                    if self.__tokenizer.wasItIdentifier():
                        # eats the "("
                        self.eat()
                        # eats the expression itself
                        self.CompileExpressionList()
                        # eat the ")"
                        self.eat()
                    # () WITHIN AN EXPRESSION:
                    else:
                        # eats the "("
                        self.eat()
                        # eats the expression itself
                        self.CompileExpression()
                        # eat the ")"
                        self.eat()
                        break
                elif self.__tokenizer.symbol() in self.UNARY_OP and\
                        (self.__tokenizer.wasItSymbol() or self.__tokenizer.wasItReturn()):
                    # eats the unary op
                    unary_op = self.UNARY_OP[self.__tokenizer.symbol()]
                    self.eat()
                    # eats the term
                    self.CompileTerm()
                    self.__out.writeArithmetic(unary_op)
                elif self.__tokenizer.symbol() in self.OP:
                    # we encountered an operator
                    break
                else:
                    # eats the .
                    self.eat()
            # integerConstant
            elif self.__tokenizer.token_type() == "INT_CONST":
                self.__out.writePush("constant", self.__tokenizer.intVal())
                # eats the constant
                self.eat()
            # stringConstant
            elif self.__tokenizer.token_type() == "STRING_CONST":
                # push len(str)
                self.__out.writePush("constant", str(len(self.__tokenizer.stringVal())-1))
                # call String.new 1
                self.__out.writeCall("String.new", "1")
                # iterating over each char inserting : call String.appendChar(c)
                for char in self.__tokenizer.stringVal()[:-1]:
                    self.__out.writePush("constant", str(ord(char)))
                    self.__out.writeCall("String.appendChar", "2")
                # eats the string
                self.eat()
            # keywordConstant
            elif self.__tokenizer.token_type() == "KEYWORD":
                # eats the constant
                if self.__tokenizer.keyword() == "TRUE":
                    self.__out.writePush("constant", "1")
                    self.__out.writeArithmetic("neg")
                elif self.__tokenizer.keyword() == "FALSE":
                    self.__out.writePush("constant", "0")
                elif self.__tokenizer.keyword() == "THIS":
                    self.__out.writePush("pointer", "0")
                elif self.__tokenizer.keyword() == "NULL":
                    self.__out.writePush("constant", "0")
                self.eat()
            # IDENTIFIERConstant
            elif self.__tokenizer.token_type() == "IDENTIFIER":
                # check if its an array or a subroutineCall or a simple variable
                if self.__tokenizer.peek() == "<symbol> [ </symbol>\n":
                    array_name = self.__tokenizer.identifier()
                    array_kind = self.__symbol_table.kindOf(array_name)
                    if array_kind == "VAR":
                        array_kind = "local"
                    elif array_kind == "FIELD":
                        array_kind = "this"
                    array_index = str(self.__symbol_table.indexOf(array_name))
                    self.__out.writePush(array_kind.lower(), array_index)
                    # eat the identifier
                    self.eat()
                    # eat the "["
                    self.eat()
                    # compiles the expression inside the arrays '[]'
                    self.CompileExpression()
                    self.__out.writeArithmetic("add")
                    self.__out.writePop("pointer", "1")
                    self.__out.writePush("that", "0")
                    # eats the "]"
                    self.eat()
                elif self.__tokenizer.peek() != "<symbol> ( </symbol>\n" and\
                     self.__tokenizer.peek() != "<symbol> [ </symbol>\n" and\
                     self.__tokenizer.peek() != "<symbol> . </symbol>\n":
                        # eats the identifier
                        kind = self.__symbol_table.kindOf(self.__tokenizer.identifier())
                        indexOf = str(self.__symbol_table.indexOf(self.__tokenizer.identifier()))
                        if kind == "FIELD":
                            kind = "this"
                        if kind == "VAR":
                            kind = "local"
                        self.__out.writePush(kind.lower(), indexOf)
                        self.eat()
                else:
                    # SUBROUTINE:
                    func_name = ""
                    self.__method_assign_arg_counter = 0
                    tokens_eaten = 0
                    while True:
                        if self.__tokenizer.token_type() == "SYMBOL":
                            if self.__tokenizer.symbol() == "(":
                                # eats the "("
                                self.eat()
                                if "." not in func_name:
                                    func_name = self.__class_name + "." + func_name
                                    if self.__constructor:
                                        self.__out.writePush("pointer", "0")
                                        self.__method_assign_arg_counter += 1
                                    elif self.__method_flag:
                                        self.__out.writePush("pointer", "0")
                                        self.__method_assign_arg_counter += 1
                                # compile the expression inside the ()
                                self.CompileExpressionList()
                                self.__out.writeCall(func_name, str(self.__method_assign_arg_counter))
                                # eats the ")"
                                self.eat()
                                break
                        # eats until the "("
                        if tokens_eaten % 2 == 0:
                            if self.__tokenizer.peek() == '<symbol> . </symbol>\n' and \
                               self.__symbol_table.kindOf(self.__tokenizer.identifier()) != "NONE":
                                self.__method_assign_arg_counter = 1
                                func_name += self.__symbol_table.typeOf(self.__tokenizer.identifier())
                                kind = self.__symbol_table.kindOf(self.__tokenizer.identifier())
                                if kind == "FIELD":
                                    kind = "this"
                                if kind == "VAR":
                                    kind = "local"
                                index = str(self.__symbol_table.indexOf(self.__tokenizer.identifier()))
                                self.__out.writePush(kind, index)
                            else:
                                func_name += self.__tokenizer.identifier()
                        else:
                            func_name += self.__tokenizer.symbol()
                        tokens_eaten += 1
                        self.eat()

    def CompileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions
        """
        # continues eating tokens until encounters ")":
        while True:
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ")":
                    break
            # eats expressionList
            self.CompileExpression()
            self.__arg_counter += 1
            self.__method_assign_arg_counter += 1
            if self.__tokenizer.token_type() == "SYMBOL":
                if self.__tokenizer.symbol() == ",":
                    # eats the "," iff it has another expression.
                    self.eat()