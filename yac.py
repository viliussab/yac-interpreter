from sly import Lexer
from sly import Parser

def add(lhs, rhs):
    lhs_type, lhs_value = lhs[0], lhs[1]
    rhs_type, rhs_value = rhs[0], rhs[1]
    if lhs_type == 'int' and rhs_type == 'int':
        return 'int', lhs_value + rhs_value
    elif lhs_type == 'dbl' and rhs_type == 'dbl':
        return 'dbl', lhs_value + rhs_value
    elif lhs_type == 'str' and rhs_type == 'str':
        return 'str', lhs_value + rhs_value
    else:
        print("Type mismatch! addition operation of type '" + lhs_type + "' and '" + rhs_type + "' not supported!")
        return None


def sub(lhs, rhs):
    lhs_type, lhs_value = lhs[0], lhs[1]
    rhs_type, rhs_value = rhs[0], rhs[1]
    if lhs_type == 'int' and rhs_type == 'int':
        return 'int', lhs_value - rhs_value
    elif lhs_type == 'dbl' and rhs_type == 'dbl':
        return 'dbl', lhs_value - rhs_value
    else:
        print("Type mismatch! subtraction operation of type '" + lhs_type + "' and '" + rhs_type + "' not supported!")
        return None


def mul(lhs, rhs):
    lhs_type, lhs_value = lhs[0], lhs[1]
    rhs_type, rhs_value = rhs[0], rhs[1]
    if lhs_type == 'int' and rhs_type == 'int':
        return 'int', lhs_value * rhs_value
    elif lhs_type == 'dbl' and rhs_type == 'dbl':
        return 'dbl', lhs_value * rhs_value
    else:
        print("Type mismatch! multiplication operation of type '" + lhs_type + "' and '" + rhs_type + "' not supported!")
        return None


def div(lhs, rhs):
    lhs_type, lhs_value = lhs[0], lhs[1]
    rhs_type, rhs_value = rhs[0], rhs[1]
    if lhs_type == 'int' and rhs_type == 'int':
        return 'int', int(lhs_value / rhs_value)
    elif lhs_type == 'dbl' and rhs_type == 'dbl':
        return 'dbl', lhs_value / rhs_value
    else:
        print("Type mismatch! division operation of type '" + lhs_type + "' and '" + rhs_type + "' not supported!")
        return None


def var_create(envs, var):
    keyword, var_name = var[0], var[1]
    found_env = False
    for env in envs:
        if var_name in env:
            print("yra?")
            found_env = True
            break
    if found_env == False:
        if keyword == 'keyword_int':
            var_type = 'int'
        elif keyword == 'keyword_dbl':
            var_type = 'dbl'
        else:
            var_type = 'str'

        # print("sukurtas " + str(var_name) + " su tipu " + var_type)
        envs[len(envs) - 1][var_name] = var_type, None
    else:
        print("ERROR: variable " + str(var_name) + " already exists!")
    return var_name


class YacLexer(Lexer):
    tokens = { PRINT,
               NAME,
               INT_VALUE, DBL_VALUE, STR_VALUE,
               KEYWORD_INT, KEYWORD_DBL, KEYWORD_STR,
               CONVERTER_INT, CONVERTER_DBL, CONVERTER_STR,
               IF, ELSE,
               AND, OR, EQS, LTE, GTE,
               WHILE, FOR,
               FUNC}

    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ';' , '>', '<', '{', '}', ':', ','}

    # tokens
    PRINT = r'print'
    KEYWORD_INT = r'int '
    KEYWORD_DBL = r'dbl '
    KEYWORD_STR = r'str '
    CONVERTER_INT = r'int\('
    CONVERTER_DBL = r'dbl\('
    CONVERTER_STR = r'str\('
    FUNC = r'func '

    IF = r'if'
    ELSE = r'else'
    AND = r'\|\|'
    OR = r'\&\&'
    EQS = r'=='
    LTE = r'<='
    GTE = r'>='
    WHILE = r'while'
    FOR = r'for'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\".*?\"')
    def STR_VALUE(self, t):
        t.value = str(t.value)
        t.value = t.value[1:-1]
        return t

    @_(r'\d*[.]\d+')
    def DBL_VALUE(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT_VALUE(self, t):
        t.value = int(t.value)
        return t

    @_(r'\/\/.*')
    def COMMENT_ONELINE(self, t):
        pass

    @_(r'\/\*([\s\S]*?)\*\/')
    def COMMENT_INLINE(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


class YacParser(Parser):
    tokens = YacLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statements(self, p):
        pass

    @_('full_statement statements')
    def statements(self, p):
        return p[0], p[1]

    @_('func_declaration')
    def full_statement(self, p):
        return p

    @_('FUNC NAME "(" params ")" ":" "(" params ")" "{" statements "}"')
    def func_declaration(self, p):
        return 'func', p.NAME, ('new_vars', p.params0), ('new_vars', p.params1), p.statements

    @_('new_vars')
    def params(self, p):
        return p.new_vars

    @_('')
    def params(self, p):
        pass

    @_('statement ";"')
    def full_statement(self, p):
        return p.statement

    @_('if_statement')
    def full_statement(self, p):
        return p.if_statement

    @_('WHILE "(" condition ")" "{" statements "}"')
    def full_statement(self, p):
        return 'loop_while', p.condition, p.statements

    @_('FOR "(" var_init ";" condition ";" var_assign ")" "{" statements "}"')
    def full_statement(self, p):
        return 'loop_for', p.var_init, p.condition, p.var_assign, p.statements

    @_('IF "(" condition ")" "{" statements "}"')
    def if_statement(self, p):
        return 'if', p.condition, p.statements

    @_('IF "(" condition ")" "{" statements "}" ELSE "{" statements "}"')
    def if_statement(self, p):
        return 'if_else', p.condition, p.statements0, p.statements1

    @_('bool_cond AND bool_cond')
    def condition(self, p):
        return 'and', p.bool_cond0, p.bool_cond1

    @_('bool_cond OR bool_cond')
    def condition(self, p):
        return 'or', p.bool_cond0, p.bool_cond1

    @_('bool_cond')
    def condition(self, p):
        return p.bool_cond

    @_('expr EQS expr')
    def bool_cond(self, p):
        return '==', p.expr0, p.expr1

    @_('expr LTE expr')
    def bool_cond(self, p):
        return '<=', p.expr0, p.expr1

    @_('expr GTE expr')
    def bool_cond(self, p):
        return '>=', p.expr0, p.expr1

    @_('expr "<" expr')
    def bool_cond(self, p):
        return '<', p.expr0, p.expr1

    @_('expr ">" expr')
    def bool_cond(self, p):
        return '>', p.expr0, p.expr1

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('var_init')
    def statement(self, p):
        return p.var_init

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('func_call')
    def statement(self, p):
        return p.func_call

    @_('KEYWORD_INT')
    def keyword(self, p):
        return 'keyword_int'

    @_('KEYWORD_DBL')
    def keyword(self, p):
        return 'keyword_dbl'

    @_('KEYWORD_STR')
    def keyword(self, p):
        return 'keyword_str'

    @_('new_var "," new_vars')
    def new_vars(self, p):
        return p.new_var, p.new_vars

    @_('new_var')
    def new_vars(self, p):
        return p.new_var

    @_('keyword NAME')
    def new_var(self, p):
        return p.keyword, p.NAME

    @_('NAME "," names')
    def names(self, p):
        return p.NAME, p.names

    @_('NAME')
    def names(self, p):
        return p.NAME

    @_('expr "," exprs')
    def exprs(self, p):
        return p.expr, p.exprs

    @_('expr')
    def exprs(self, p):
        return p.expr

    @_('new_vars "=" exprs')
    def var_init(self, p):
        return 'vars_assign', ('new_vars', p.new_vars), ('exprs', p.exprs)

    @_('new_vars "=" func_call')
    def var_init(self, p):
        return 'vars_assign', ('new_vars', p.new_vars), p.func_call

    @_('new_vars')
    def var_init(self, p):
        return 'new_vars', p.new_vars

    @_('PRINT "(" expr ")"')
    def statement(self, p):
        return 'internal', p.PRINT, p.expr

    @_('names "=" func_call')
    def var_assign(self, p):
        return 'vars_assign', ('vars', p.names), p.func_call

    @_('names "=" exprs')
    def var_assign(self, p):
        return 'vars_assign', ('vars', p.names), ('exprs', p.exprs)

    @_('CONVERTER_INT expr ")"')
    def expr(self, p):
        return 'convert', 'int', p.expr

    @_('CONVERTER_DBL expr ")"')
    def expr(self, p):
        return 'convert', 'dbl', p.expr

    @_('CONVERTER_STR expr ")"')
    def expr(self, p):
        return 'convert', 'str', p.expr

    @_('expr "+" expr')
    def expr(self, p):
        return 'add', p.expr0, p.expr1

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr "-" expr')
    def expr(self, p):
        return 'sub', p.expr0, p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return 'mul', p.expr0, p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return 'div', p.expr0, p.expr1

    @_('')
    def call_params(self, p):
        pass

    @_('exprs')
    def call_params(self, p):
        return p.exprs

    @_('NAME "(" call_params ")"')
    def func_call(self, p):
        return 'func_call', p.NAME, ('exprs', p.call_params)

    @_('NAME')
    def expr(self, p):
        return 'var', p.NAME

    @_('INT_VALUE')
    def expr(self, p):
        return 'int', p.INT_VALUE

    @_('DBL_VALUE')
    def expr(self, p):
        return 'dbl', p.DBL_VALUE

    @_('STR_VALUE')
    def expr(self, p):
        return 'str', p.STR_VALUE


class YacInterpret:

    def __init__(self, tree, envs, funcs):
        self.envs = envs
        self.funcs = funcs
        if len(envs) == 0:
            self.current_env = {}
            self.envs.append(self.current_env)
        else:
            self.current_env = envs[-1]
        result = self.walkTree(tree)

    def enter_scope(self):
        # print("scoped entered ;))")
        new_environment = {}
        self.envs.append(new_environment)
        self.current_env = new_environment
        # print(len(self.envs))

    def exit_scope(self):
        # print("scoped exited ;))")
        self.envs.pop()
        self.current_env = self.envs[len(self.envs) - 1]
        # print(len(self.envs))


    def eval_expr(self, expr):
        if expr[0] in ['int', 'dbl', 'str']:
            return expr
        else:
            return self.walkTree(expr)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'int':
            return node[0], node[1]

        if node[0] == 'dbl':
            return node[0], node[1]

        if node[0] == 'str':
            return node[0], node[1]

        if node[0] == 'func':
            # print('func ' + node[1])
            self.funcs[node[1]] = node
            return None

        if node[0] == 'func_call':
            name = node[1]

            if name not in self.funcs:
                print("ERROR: no such function with name '" + str(node[1]) + "' found")
                return None

            #call parameters
            call_param_list = self.walkTree(node[2])
            if call_param_list is None:
                call_param_list = []

            function_node = self.funcs[name]

            #create new envinroment

            old_envs = self.envs
            old_current_env = self.current_env

            self.envs = []
            self.current_env = {}
            self.envs.append(self.current_env)

            #input parameters
            in_params = function_node[2]

            if in_params[1] is None:
                in_params_list = []
            else:
                in_params_list = self.walkTree(in_params)

            if len(call_param_list) != len(in_params_list):
                print("ERROR: the function '" + str(node[1]) + "' was called with " + str(len(call_param_list)) +
                      " parameters when in fact the function takes " + str(len(in_params_list)) + ".")
                self.envs = old_envs
                self.current_env = old_current_env
                return None
            else:
                for i in range(0, len(in_params_list)):
                    self.current_env[in_params_list[i]] = call_param_list[i]

            #output parameters
            out_params = function_node[3]

            if out_params[1] is None:
                out_params_list = []
            else:
                out_params_list = self.walkTree(out_params)

            #statements
            self.walkTree(function_node[4])

            return_params = []
            for param in out_params_list:
                tupl = 'var', param
                parameter = self.walkTree(tupl)
                return_params.append(parameter)

            self.envs = old_envs
            self.current_env = old_current_env
            #
            # print(return_params)
            return return_params

        if node[0] == 'if':
            cond = self.walkTree(node[1])
            if cond[1]:
                self.enter_scope()
                self.walkTree(node[2])
                self.exit_scope()
            return

        if node[0] == 'if_else':
            # print(node)
            cond = self.walkTree(node[1])
            if cond[1]:
                self.enter_scope()
                self.walkTree(node[2])
                self.exit_scope()
            else:
                self.enter_scope()
                self.walkTree(node[3])
                self.exit_scope()
            return

        if node[0] == 'loop_while':
            while True:
                condition = self.walkTree(node[1])
                if not condition[1]:
                    break
                self.enter_scope()
                self.walkTree(node[2])
                self.exit_scope()
            return

        if node[0] == 'loop_for':
            self.enter_scope()
            self.walkTree(node[1])
            while True:
                condition = self.walkTree(node[2])
                if not condition[1]:
                    break
                self.enter_scope()
                self.walkTree(node[4])
                self.exit_scope()
                self.walkTree(node[3])
            self.exit_scope()
            return

        if node[0] == 'and':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] and rhs[1]

        if node[0] == 'or':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] or rhs[1]

        if node[0] == '==':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] == rhs[1]

        if node[0] == '<=':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] <= rhs[1]

        if node[0] == '>=':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] >= rhs[1]

        if node[0] == '<':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] < rhs[1]

        if node[0] == '>':
            lhs = self.walkTree(node[1])
            rhs = self.walkTree(node[2])
            return 'bool', lhs[1] > rhs[1]

        if node[0] == 'add':
            return add(self.walkTree(node[1]), self.walkTree(node[2]))

        elif node[0] == 'sub':
            return sub(self.walkTree(node[1]), self.walkTree(node[2]))

        elif node[0] == 'mul':
            return mul(self.walkTree(node[1]), self.walkTree(node[2]))

        elif node[0] == 'div':
            return div(self.walkTree(node[1]), self.walkTree(node[2]))

        # if node[0] == 'keyword_int':
        #     self.current_env[node[1][1]] = 'int', 0
        #     if self.walkTree(node[1]) is None:
        #         del env[node[1][1]]
        #         return None
        #     return self.current_env[node[1][1]]
        #
        # if node[0] == 'keyword_dbl':
        #     self.current_env[node[1][1]] = 'dbl', 0.0
        #     if self.walkTree(node[1]) is None:
        #         del env[node[1][1]]
        #         return None
        #     return self.current_env[node[1][1]]
        #
        # if node[0] == 'keyword_str':
        #     self.current_env[node[1][1]] = 'str', ""
        #     if self.walkTree(node[1]) is None:
        #         del env[node[1][1]]
        #         return None
        #     return self.current_env[node[1][1]]

        if node[0] == 'convert':
            if node[1] == 'int':
                return 'int', int((self.walkTree(node[2]))[1])
            if node[1] == 'dbl':
                return 'dbl', float((self.walkTree(node[2]))[1])
            if node[1] == 'str':
                return 'str', str((self.walkTree(node[2]))[1])

        if node[0] == 'new_vars':
            varname_list = []
            tupl = node[1]
            if type(tupl[1]) != tuple:
                var = tupl
                ans = var_create(self.envs, var)
                varname_list.append(ans)
            else:
                while type(tupl[1]) == tuple:
                    var = tupl[0]
                    ans = var_create(self.envs, var)
                    varname_list.append(ans)
                    tupl = tupl[1]
                var = tupl
                ans = var_create(self.envs, var)
                varname_list.append(ans)
                
            return varname_list

        if node[0] == 'vars':
            var_list = []
            var_tree = node[1]
            # print(var_tree)
            if type(var_tree) != tuple:
                var_list.append(var_tree)
            else:
                var_list = list(var_tree)
            # print(var_list)

            return var_list

        if node[0] == 'exprs':
            expr_list = []
            tupl = node[1]
            if tupl is None:
                return []
            if type(tupl[0]) != tuple:
                expr_list.append(self.walkTree(tupl))
            else:
                while type(tupl[1]) == tuple:
                    expr_list.append(self.walkTree(tupl[0]))
                    tupl = tupl[1]
                expr_list.append(self.walkTree(tupl))
            # values = node[1]
            # tupl = values
            # while type(tupl) == tuple:
            #     print(tupl)
            #     expr_list.append(self.walkTree(tupl))
            #     tupl = tupl[1]
            # if type(tupl) != tuple:
            #     print(tupl)
            #     expr_list.append(self.walkTree(tupl))
            # # elif type(tupl[1]) != tuple:
            # #     tupl = tupl[0]
            # #     print(tupl)
            # #     expr_list.append(self.walkTree(tupl))
            # else:
            #     tupl = tupl[0]
            #     while type(tupl[1]) == tuple:
            #         print(tupl)
            #         expr_list.append(self.walkTree(tupl[0]))
            #         tupl = self.eval_expr(tupl[1])
            #     print(tupl)
            #     expr_list.append(self.eval_expr(tupl))
            # print(expr_list)
            return expr_list

        # if node[0] == 'new_vars_assign':
        #     variables = self.walkTree(node[1])
        #     values = self.walkTree(node[2])
        #     if len(variables) == len(values):
        #         for i in range(0, len(variables)):
        #             self.walkTree(('var_assign', variables[i], values[i]))
        #     else:
        #         print("ERROR: tuple assign length mismatch!")
        #     return None

        if node[0] == 'vars_assign':
            variables = self.walkTree(node[1])
            values = self.walkTree(node[2])
            if len(variables) == len(values):
                for i in range(0, len(variables)):
                    self.walkTree(('var_assign', variables[i], values[i]))
            else:
                print("Variables:")
                print(variables)
                print(len(variables))
                print("Values")
                print(len(values))
                print(values)
                print("ERROR: tuple assign length mismatch!")
            return None

        if node[0] == 'var_assign':
            try:
                variable = None
                idx = 0
                for i in range(0, len(self.envs)):
                    checkenv = self.envs[i]
                    if node[1] in checkenv:
                        variable = checkenv[node[1]]
                        idx = i
                expected_type = variable[0]
                answer = self.walkTree(node[2])
                answer_type = answer[0]
                if expected_type == answer_type:
                    self.envs[idx][node[1]] = answer
                    return node[1]
                else:
                    print("ASSIGN ERROR: Type mismatch! Variable '" + node[1] + "' of type '" + expected_type + "' can not be assigned to '" + answer_type + "'" )
                    return None
            except KeyError:
                print("ASSIGN ERROR: Undefined variable '" + node[1] + "' found! sitam")
                return None


        if node[0] == 'var':
            for i in range(0, len(self.envs)):
                checkenv = self.envs[i]
                if node[1] in checkenv:
                    return checkenv[node[1]]

            #Error
            print("Undefined variable '" + node[1] + "' found!")
            return None
            # if not found_env:
            # try:
            #     return self.current_env[node[1]]
            # except LookupError:


        if node[0] == 'internal':
            if node[1] == 'print':
                ans = self.walkTree(node[2])
                if ans is not None:
                    if ans[1] is not None:
                        print(ans[1])
                    else:
                        print("PRINT ERROR: " + str(node[2][1]) + " value is created but not assigned!")
                else:
                    print("PRINT ERROR: Could not print that value")
                    return None

        if node is not None:
            for child_node in node:
                self.walkTree(child_node)
            return


if __name__ == '__main__':
    envs = []
    funcs = {}
    lexer = YacLexer()
    parser = YacParser()
    # INLINE INTERPRETATORIUS
    # while True:
    #     try:
    #         text = input('=> ')
    #     except EOFError:
    #         break
    #     if text:
    #         lex = lexer.tokenize(text)
    #         # print("************")
    #         # print("** LEXER  **")
    #         for token in lex:
    #             print(token)
    #         tree = parser.parse(lexer.tokenize(text))
    #         print("** PARSER **")
    #         print(tree)
    #         print("************")
    #         YacInterpret(tree, envs, funcs)
    # FAILO INTERPRETAVIMAS
    import sys

    if len(sys.argv) != 2:
        raise SystemExit(f'Netinkami argumentai! : {sys.argv[0]} reikalauja tik vieno duomenų failo')
    text = open(sys.argv[1]).read()

    lex = lexer.tokenize(text)
    tree = parser.parse(lex)
    # print("tree:")
    # print(tree)
    # print("*****\n")
    YacInterpret(tree, envs, funcs)


