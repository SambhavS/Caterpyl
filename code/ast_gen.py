from utils import *
"""
------------------------------------------------------------
C Grammar (Notation: [leaf], <branch>, UNKNOWN, `literal`)
------------------------------------------------------------
program := [<func>, <func>, <func>, ...]
func := [ret_type] [func_name] `(` ARGS + `)` `{` <body> `}`
ARGS := ?
body := [<statement>, <statement>, <statement>, ...]
statement := `return` <expression> `;` | [ret_type]  [var name] = <expression> `;`
                                      | `if` `(` <expression> `)` `{` <body> `}`
                                      | `if` `(` <expression> `)` `{` <body> `}` 
                                           `else` `{` <statement_series> `}`
expression := [parenthetical expression (PE) / const-var (CV)] [binary operator] 
                ... [PE/CV] [binary operator] ... [PE/CV]
*unary operators
"""

def main_AST(program, master_lookup):
    """ Creates token stream, parses tokens, 
        and returns AST given program as a string."""

    def parse_statements(tokens, lookup, func_dec=False):
        statements = []
        while len(tokens) and typ(tokens[0]) != Tkn.rbrack:
            statement = statement_AST(tokens, lookup, func_dec)
            statements.append(statement)
        # Parse `}`
        if tokens:
            tokens.pop(0)
        return statements

    def statement_AST(tokens, lookup, func_dec=False):
        nonlocal master_lookup
        root = tokens[0]
        root_type = typ(root)
        if root_type in Tkn.prog_keywords:
            """Special Language Construct"""
            if root_type is Tkn.ifx:
                check_skip(tokens, Tkn.ifx, "Check `if`")
                check_skip(tokens, Tkn.lparen, "Check `(`")
                expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.rparen, "Check `)`")
                check_skip(tokens, Tkn.lbrack, "Check `{`")
                true_statements = parse_statements(tokens, lookup)
                if tokens[0] == "else":
                    check_skip(tokens, Tkn.elsex, "Check `else`")
                    check_skip(tokens, Tkn.lbrack, "Check `{`")
                    else_statements = parse_statements(tokens, lookup)
                else:
                    else_statements = []
                subtree = If(cond=expression, true_body=Body(
                    true_statements), else_body=Body(else_statements))
            elif root_type is Tkn.whilex:
                check_skip(tokens, Tkn.whilex, "Check `while`")
                check_skip(tokens, Tkn.lparen, "Check `(`")
                expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.rparen, "Check `)`")
                check_skip(tokens, Tkn.lbrack, "Check `{`")
                true_statements = parse_statements(tokens, lookup)
                subtree = While(cond=expression, true_body=Body(true_statements))
            elif root_type is Tkn.returnx:
                check_skip(tokens, Tkn.returnx, "Check `return`")
                ret_expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.semicolon, "Check `;`")
                subtree = Return(ret_expression)

        elif root_type in Tkn.type_keys:
            type_dec = root
            check_skip(tokens, Tkn.type_keys, "Check type keyword")
            if func_dec:
                """ Function Declaration"""
                func_name = tokens[0]
                check_skip(tokens, Tkn.var, "Check function var name")
                check_skip(tokens, Tkn.lparen, "Check `(`")
                params = parse_params(tokens)
                check_skip(tokens, Tkn.rparen, "Check `)`")
                check_skip(tokens, Tkn.lbrack, "Check `{`")
                lookup = master_lookup[func_name]
                for param_name, param_type in params:
                    lookup[param_name] = {"type_dec": param_type, "type":"var"}
                statements = parse_statements(tokens, lookup, func_dec=False)
                subtree = Func(ret_type=type_dec, name=func_name, body=Body(statements), params=params, lookup=lookup)
            elif typ(tokens[1]) is Tkn.equal:
                """ Variable Declaration + Assignment"""
                variable = Var(name=tokens[0])
                check_skip(tokens, Tkn.var, "Check var name")
                check_skip(tokens, Tkn.equal, "Check `=`")
                expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.semicolon, "Check `;`")
                decl = Decl(var=variable, type_dec=type_dec, lookup=lookup)
                assign = Assign(var_name=variable, exp=expression)
                subtree = Body([decl, assign])

            elif typ(tokens[1]) is Tkn.semicolon:
                """ Variable Declaration"""
                variable = Var(name=tokens[0])
                check_skip(tokens, Tkn.var, "Check var name")
                check_skip(tokens, Tkn.semicolon, "Check `;`")
                subtree = Decl(var=variable, type_dec=type_dec, lookup=lookup)
            else:
                raise Exception("Bad syntax after type keyword")
        elif root_type is Tkn.var:
            if typ(tokens[1]) is Tkn.op_eq:
                """Assignment + Operation """
                variable = Var(name=tokens[0])
                check_skip(tokens, Tkn.var, "Check var name")
                operator = tokens[0][0]
                check_skip(tokens, Tkn.op_eq, "Check `?=`")
                expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.semicolon, "Check `;`")
                mod_expression = Expression(op_name=operator, oper1=variable, oper2=expression, lookup=lookup)
                subtree = Assign(var_name=variable, exp=mod_expression)

            elif typ(tokens[1]) is Tkn.equal:
                """ Assignment"""
                variable = Var(name=tokens[0])
                check_skip(tokens, Tkn.var, "Check var name")
                check_skip(tokens, Tkn.equal, "Check `=`")
                expression = exp_AST(tokens, lookup)
                check_skip(tokens, Tkn.semicolon, "Check `;`")
                subtree = Assign(var_name=variable, exp=expression)
            else:
                print(typ(tokens[1]))
        else:
            raise Exception("Invalid first term in statement {}".format(root))
        return subtree

    def parse_params(tokens):
        """ Parse the parameters in a function declaration """
        params = []
        while True:
            next_tok = tokens[0]
            if typ(next_tok) == Tkn.rparen:
                return params
            else:
                param_type = tokens[0]
                check_skip(tokens, Tkn.type_keys, "Check param type")
                param_name = tokens[0]
                check_skip(tokens, Tkn.var, "Check var name")
                params.append((param_name, param_type))
                if typ(tokens[0]) == Tkn.rparen:
                    continue
                check_skip(tokens, Tkn.comma, "Check `,`")
                
    def exp_AST(tokens, lookup):
        """Creates and converts list of expressions to proper expression AST"""
        def list_to_tree(exp_lst):
            while any([isinstance(exp, list) for exp in exp_lst]):
                i = 0
                while i < len(exp_lst):
                    if isinstance(exp_lst[i], list):
                        exp_lst[i] = list_to_tree(exp_lst[i])
                    i += 1
            ordered_operators = ORDERED_OPS
            for op in ordered_operators:
                while op in exp_lst:
                    ind = exp_lst.index(op)
                    if op in UNOPS:
                        exp_lst[ind:ind+2] = [UnaryExpression(op_name=op, oper=exp_lst[ind-1], lookup=lookup)]
                    else:
                        exp_lst[ind-1:ind+2] = [Expression(op_name=op, oper1=exp_lst[ind-1], oper2=exp_lst[ind+1], lookup=lookup)]
            return exp_lst[0]

        exp_lst, drops = raw_expression_list(tokens, lookup)
        exp_ast = list_to_tree(exp_lst)
        for i in range(drops):
            tokens.pop(0)
        return exp_ast

    def raw_expression_list(tokens, lookup, ind=0):
        """Returns a list of expression terms that need to be combined to form an AST"""
        def last_ind(tokens, start):
            """Helper function that returns the index corresponding to the end of an expression"""
            final_ind = start+1
            if typ(tokens[start]) in Tkn.constants or typ(tokens[start]) is Tkn.var:
                return final_ind
            p_lvl = 1
            while True:
                tok_type = typ(tokens[final_ind])
                if tok_type is Tkn.lparen:
                    p_lvl += 1
                if tok_type is Tkn.rparen:
                    p_lvl -= 1
                if p_lvl == 0 or tok_type is Tkn.semicolon or tok_type is Tkn.comma:
                    break
                final_ind += 1
            return final_ind
        
        # First expression is parenthetical
        if typ(tokens[ind]) is Tkn.lparen:
            final_ind = last_ind(tokens, ind)
            children = []
            i = ind+1
            while i < final_ind:
                tok_type = typ(tokens[i])
                if tok_type in Tkn.constants or tok_type is Tkn.var or tok_type is Tkn.binop:
                    children.append(wrapNode(tokens[i]))
                    i += 1
                elif tok_type is Tkn.lparen:
                    expression, _ = raw_expression_list(tokens, lookup, i)
                    children.append(expression)
                    i = last_ind(tokens, i) + 1
            if len(children) % 2 == 0:
                raise Exception("Bad expression: binary operators must alternate")
            final_ind += 1
            if typ(tokens[final_ind]) is Tkn.binop:
                operator = tokens[final_ind]
                final_ind += 1
                second_exp_list, final_ind = raw_expression_list(tokens, lookup, final_ind)
                return [children, operator] + second_exp_list, final_ind
            elif typ(tokens[final_ind]) in [Tkn.semicolon, Tkn.rparen, Tkn.comma]:
                return [children], final_ind
            else:
                raise Exception("Bad expression")

        elif typ(tokens[ind]) in Tkn.var and len(tokens) > ind+1 and typ(tokens[ind+1]) is Tkn.lparen:
            # Function call
            called_func = tokens[ind]
            ind += 1
            subtokens = tokens[ind+1:]
            args = parse_args(subtokens, lookup)
            func_call = FncCall(called_func=called_func, arguments=args, master_lookup=master_lookup)
            ind += len(tokens[ind-1:]) - len(subtokens)
            if typ(tokens[ind]) is Tkn.binop:
                operator = tokens[ind]
                ind += 1
                second_exp_list, ind = raw_expression_list(tokens, lookup, ind)
                return [func_call, operator] + second_exp_list, ind
            elif typ(tokens[ind]) in [Tkn.semicolon, Tkn.rparen, Tkn.comma]:
                return [func_call], ind

        elif typ(tokens[ind]) in Tkn.constants or typ(tokens[ind]) is Tkn.var:
            # First expression is constant/variable
            val = wrapNode(tokens[ind])
            ind += 1
            if typ(tokens[ind]) is Tkn.binop:
                operator = tokens[ind]
                ind += 1
                second_exp_list, ind = raw_expression_list(tokens, lookup, ind)
                return [val, operator] + second_exp_list, ind
            elif typ(tokens[ind]) in [Tkn.semicolon, Tkn.rparen, Tkn.comma]:
                return [val], ind

        elif typ(tokens[ind]) is Tkn.unop or tokens[ind] == "-":
            exp_list = [tokens[ind]] if typ(tokens[ind]) is Tkn.unop else [Const(0, int), tokens[ind]]
            operator = tokens[ind]
            ind += 1
            second_exp_list, ind = raw_expression_list(tokens, lookup, ind)
            return exp_list + second_exp_list, ind
        raise Exception("Bad expression: {} {}".format(tokens[ind], typ(tokens[ind])))

    def parse_args(tokens, lookup):
        args = []
        while True:
            if typ(tokens[0]) is Tkn.rparen:
                return args
            else:
                args.append(exp_AST(tokens, lookup))
                while tokens[0] in ",":
                    tokens.pop(0)
        
    ### AST Utils ###
    def populate_with_funcs(tokens, master_lookup):
        func_names = []
        b_lvl = 0
        curr_func = {}
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok == "{":
                b_lvl += 1
            elif tok == "}":
                b_lvl -= 1
            elif b_lvl == 0:
                if len(curr_func) == 0:
                    curr_func["type_dec"] = tok
                elif len(curr_func) == 1:
                    curr_func["name"] = tok
                    func_names.append(curr_func)
                    curr_func = {}
                    while tokens[i+1] != "{":
                        i += 1
                else:
                    raise SyntaxError("Incorrect function declaration")
            i += 1
        for d in func_names:
            name = d["name"]
            master_lookup[name] = {"{}::TYPE_INFO".format(name) :d["type_dec"]}
        print(master_lookup)

    def wrapNode(val):
        """ Wraps value in proper node class"""
        tok_type = typ(val)
        if tok_type in Tkn.constants:
            return Const(val, tok_type)
        elif tok_type is Tkn.var:
            return Var(val)
        elif tok_type is Tkn.binop:
            return val

    def tokenize(string):
        """ Returns list of tokens given program as a string"""
        tokens = []
        token = ""
        is_comment = False
        for i, c in enumerate(string):
            if is_comment:
                if c == "\n":
                    is_comment = False
            else:
                if c == "/" and (i+1<len(string) and string[i+1]=="/"):
                    is_comment = True
                    continue
                token += c
                terminals  = "(){;},"
                opers = "!+-*/=<>%"
                if c in opers and (i+1<len(string) and string[i+1]=="="):
                    continue
                elif (c in terminals+opers or i+1 == len(string)
                        or string[i+1] in terminals+opers+WHITESPACE):
                    tokens.append(token)
                    token = ""
        if token:
            tokens.append(token)
            token = ""
        return [t.strip() for t in tokens if t.strip()]


    def check_skip(tokens, exp, msg):
        """Checks that value matches a certain type and skips it"""
        if typ(tokens[0]) not in exp:
            raise Exception("{} but got {}".format(msg, tokens[0]))
        tokens.pop(0)

    tokens = tokenize(program)
    populate_with_funcs(tokens, master_lookup)
    subtrees = parse_statements(tokens, master_lookup, func_dec=True)
    return master_lookup, Prog(subtrees)