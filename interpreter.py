import re

class Token:
    INTEGER = "int"
    VARIABLE = "variable"
    ASSIGNMENT = "iz"
    CONDITIONAL = "wtf"
    END = "brb"
    EQ = "liek"
    GT = "uber"
    NEG = "nope"
    WHILE = "rtfm"
    BREAK = "tldr"
    INPUT = "stfw"
    OUTPUT = "rofl"
    PUSH = "n00b"
    POP = "l33t"
    DEQUEUE = "haxor"
    INCREMENT = "lmao"
    DECREMENT = "roflmao"
    EXIT = "stfu"
    WAIT = "afk"
    TO = "to"
    CLEAR = "/dev/null"

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.type)

class Integer(Token):
    def __init__(self, value):
        super().__init__(Token.INTEGER)
        self.value = value

    def __str__(self):
        return str(self.value)

class VariableToken(Token):
    def __init__(self, name):
        super().__init__(Token.VARIABLE)
        self.name = name

class Lexer:
    def __init__(self, text, iterable=False):
        self.text = text
        self.iterable = iterable

    def __str__(self):
        return self.text

    def __repr__(self):
        return "{}({})".format(self.__class__, self.text)

    def tokens(self):
        RE_LOL = re.compile("^lo(o)*l$")
        if not self.iterable:
            self.text = self.text.splitlines()
        for line in self.text:
            print("line is")
            print(line)
            for word in line.split():
                print("word is:")
                print(word)
                if word.isdigit():
                    yield Integer(int(word))
                elif RE_LOL.match(word):
                    yield VariableToken(word)
                elif word == "iz":
                    yield Token(Token.ASSIGNMENT)
                elif word == "wtf":
                    yield Token(Token.CONDITIONAL)
                elif word == "brb":
                    yield Token(Token.END)
                elif word == "uber":
                    yield Token(Token.GT)
                elif word == "liek":
                    yield Token(Token.EQ)
                elif word == "nope":
                    yield Token(Token.NEG)
                elif word == "rtfm":
                    yield Token(Token.WHILE)
                elif word == "tldr":
                    yield Token(Token.BREAK)
                elif word == "stfw":
                    yield Token(Token.INPUT)
                elif  word == "rofl":
                    yield Token(Token.OUTPUT)
                elif word == "n00b":
                    yield Token(Token.PUSH)
                elif word == "l33t":
                    yield Token(Token.POP)
                elif word == "haxor":
                    yield Token(Token.DEQUEUE)
                elif word == "stfu":
                    yield Token(Token.EXIT)
                elif word == "afk":
                    yield Token(Token.WAIT)
                elif word == "w00t":
                    #yiel Comment(word)
                    break
                elif word == "lmao":
                    yield Token(Token.INCREMENT)
                elif word == "roflmao":
                    yield Token(Token.DECREMENT)
                elif word == "to":
                    yield Token(Token.TO)
                elif word == "/dev/null":
                    yield Token(Token.CLEAR)
#        yield None

###############################################################################

class AST:
    pass

class BinCond(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For(AST):
    def __init__(self, var, end, body):
        self.variable = var
        self.end = end
        self.afterthought = 1 if var.value < end else (
                0 if var.value == end else -1)
        self.body = body

    def __repr__(self):
        #testing only
        return "for {} {} b={}".format(self.variable.name, self.end, self.body)

class If(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Variable(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{} {} {}".format(self.name, "iz", self.value)

    def __repr__(self):
        return "{}({}, {})".format(
                self.__class__.__name__, self.name, self.value)

    @classmethod
    def from_token(cls, x):
        return cls(Token.name, token.value)

class End(AST):
    pass

class ParserException(Exception):
    pass
class StatementError(ParserException):
    pass
class LoopError(ParserException):
    pass
class AssignmentError(ParserException):
    pass

class Parser:
    def __init__(self, token_generator):
        self.tokens = token_generator

    def loop_for(self):
        """
        for: 4 <var> iz <int> 2 <int> <statement>* <end>
        """
        variable = next(self.tokens)
        if variable.type is not Token.VARIABLE:
            raise LoopError("Expected variable")
        ass = next(self.tokens)
        if ass.type is not Token.ASSIGNMENT:
            raise Exception
        initial_value = next(self.tokens)
        if initial_value.type is not Token.INTEGER: #or expr?
            raise Exception
        to = next(self.tokens)
        if to.type is not Token.INTEGER:
            raise Exception
        end_value = next(self.tokens)
        if end_value.type is not Token.INTEGER: #again, or expr?
            raise Exception
        
        body = []
        while True:
            try:
                next_statement = self.statement()
            except StopIteration:
                raise LoopError("No {} found!".format(Token.END))
            except:
                raise
            else:
                if next_statement is None:
                    return For(
                            Variable(variable.name, initial_value.value),
                            end_value.value,
                            body)
                else:
                    body.append(next_statement)

    def loop_while(self):
        """
        while: <statement>* <end>
        """
        body = []
        while True:
            try:
                next_statement = self.statement()
            except StatementError:
                raise LoopError("{} expected!".format(Token.END))
            else:
                if next_statement:
                    body.append(next_statement)
                else:
                    return While(True, body)

    def expr(self):
        """
        expr: VARIABLE | INTEGER
        """
        token = next(self.tokens)
        if token.type is Token.VARIABLE:
            return Variable(Token.name, token.value)
        elif token.type is Token.INTEGER:
            return Token.value
        else:
            raise ExprError("Expected variable or integer")

    def cond_if(self):
        """
        if: <expr> "iz" ("nope") "uber"|"liek" <expr> statement* end
        """
        #Get the left side of the condition
        left = self.expr()
        
        #Get operator
        ass = next(self.tokens)
        if ass.type is not Token.ASSIGNMENT:
            raise Exception
        op = next(self.tokens)
        if op.type is Token.NEG:
            op = next(self.tokens)
            if op.type in (Token.EQ, Token.GT):
                operator = "not" + op.type
            else:
                raise Exception
        elif op.type in (Token.EQ, Token.GT):
            operator = op.type
        else:
            raise Exception

        #Get the right side of the condition
        right = self.expr()

        #Get the body
        body = []
        next_statement = self.statement()
        if next_statement:
            body.append(next_statement)
        else:
            return If(BinOp(left, operator, right), body, None)

    def unary_var(self, cls, token):
        if token is Token.VARIABLE:
            return cls(Variable.from_token(token))

    def nullary(self, cls):
        return cls()

    def assignment(self, token):
        name = token.name
        ass = next(self.tokens)
        if ass.type is not Token.ASSIGNMENT:
            raise AssignmentError("Expected {}".format(Token.ASSIGNMENT))
        value = next(self.tokens)
        if value.type is not Token.INTEGER:
            raise AssignmentError("Expected integer")
        return Variable(name, value)

    def statement(self):
        """
        statement: assignment | conditional_if | while | for | input | output |
                   push | pop | dequeue | wait | increment | decrement | exit |
                   end | break
        """
        try:
            token = next(self.tokens)
#        except StopIteration:
#            return
        except StopIteration:
            raise
        if not token:
            raise StatementError
        if token.type is Token.CONDITIONAL:
            return self.cond_if()
        if token.type is Token.VARIABLE:
            return self.assignment(token)
        elif token.type is Token.WHILE:
            return self.loop_while()
        elif token.type is Token.INTEGER and token.value == 4:
            print("FOR LOOP")
            return self.loop_for()
        elif token.type is Token.INPUT:
            return self.unary_var(Input, next(self.tokens))
        elif token.type is Token.OUTPUT:
            return self.unary_var(Output, next(self.tokens))
        elif token.type is Token.PUSH:
            return self.unary_var(Push, next(self.tokens))
        elif token.type is Token.POP:
            return self.unary_var(Pop, next(self.tokens))
        elif token.type is Token.DEQUEUE:
            return self.unary_var(Dequeue, next(self.tokens))
        elif token.type is Token.WAIT:
            return self.unary_var(Wait, next(self.tokens))
        elif token.type is Token.INCREMENT:
            return self.unary_var(Increment, next(self.tokens))
        elif token.type is Token.DECREMENT:
            return self.unary_var(Decrement, next(self.tokens))
        elif token.type is Token.EXIT:
            return self.nullary(Exit)
        elif token.type is Token.END:
#            return self.nullary(End)
            return
        elif token.type is Token.BREAK:
            return self.nullary(Break)
#        elif token.type is Token.COMMENT:
#            return #?
        else:
            print("NO MATCHING statement")
            print(token)
            raise StatementError

    def parse(self, statements=[]):
        """
        program:    <statement>*
        statement:  <assignment> | <while> | <for> | <if> |
                    <input> | <output> | <increment> | <decrement> | <clear>
                    <push> | <pop> | <dequeue> | <wait> |
                    <exit> | <end> | <break>
        assignment: VARIABLE "iz" INTEGER
        while:      "rtfm"
                        <statement>*
                    <end>
        for:        4 VARIABLE iz INTEGER 2 INTEGER
                        <statement>*
                    <end>
        if:         <expr> "iz" ("nope") "uber" | "liek" <expr>
                        <statement>*
                    <end>
        push:       "n00b" <expr>
        pop:        "l33t" VARIABLE
        dequeue:    "haxor" VARIABLE
        wait:       "afk" <expr>
        input:      "stfw" VARIABLE
        output:     "rofl" VARIABLE
        increment:  "lmao" VARIABLE
        decrement:  "rolfmao" VARIABLE
        clear:      VARIABLE to /dev/null
        exit:       "stfu"
        end:        "brb"
        break:      "tldr"
        expr:       VARIABLE | INT
        """
#        statements = []
        
        while True:
            try:
                next_statement = self.statement()
            except StopIteration:
                return statements
            else:
                if next_statement:
                    statements.append(next_statement)
#            else:
#                return statements
#        while True:
#            try:
#                statements.append(self.statement())
#            except StatementError:
#                return statements
#            except:
#                raise

def main():
    text ="""4 lol iz 4 2 8
lool iz 3
lol iz 4
brb
loool iz 5"""
    lexer = Lexer(text)
    parser = Parser(lexer.tokens())
    print(parser.parse())

if __name__ == '__main__':
    main()
