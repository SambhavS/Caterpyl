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

def main_AST(program):
    """ Creates token stream, parses tokens, 
        and returns AST given program as a string."""
    tokens = tokenize(program)
    print(tokens)
    subtrees = parse_statements(tokens, func_dec=True)
    return Prog(subtrees)

def parse_statements(tokens, func_dec=False):
    statements = []
    while len(tokens) and typ(tokens[0]) != Tkn.rbrack:
        statement = statement_AST(tokens, func_dec)
        statements.append(statement)
    # Parse `}`
    if tokens:
        tokens.pop(0)
    return statements

def statement_AST(tokens, func_dec=False):
    root = tokens[0]
    root_type = typ(root)
    if root_type in Tkn.prog_keywords:
        """Special Language Construct"""
        if root_type is Tkn.ifx:
            check_skip(tokens, Tkn.ifx, "Check `if`")
            check_skip(tokens, Tkn.lparen, "Check `(`")
            expression = exp_AST(tokens)
            check_skip(tokens, Tkn.rparen, "Check `)`")
            check_skip(tokens, Tkn.lbrack, "Check `{`")
            true_statements = parse_statements(tokens)
            if tokens[0] == "else":
                check_skip(tokens, Tkn.elsex, "Check `else`")
                check_skip(tokens, Tkn.lbrack, "Check `{`")
                else_statements = parse_statements(tokens)
            else:
                else_statements = []
            subtree = If(cond=expression, true_body=Body(
                true_statements), else_body=Body(else_statements))
        elif root_type is Tkn.whilex:
            check_skip(tokens, Tkn.whilex, "Check `while`")
            check_skip(tokens, Tkn.lparen, "Check `(`")
            expression = exp_AST(tokens)
            check_skip(tokens, Tkn.rparen, "Check `)`")
            check_skip(tokens, Tkn.lbrack, "Check `{`")
            true_statements = parse_statements(tokens)
            subtree = While(cond=expression, true_body=Body(true_statements))
        elif root_type is Tkn.returnx:
            check_skip(tokens, Tkn.returnx, "Check `return`")
            ret_expression = exp_AST(tokens)
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
            check_skip(tokens, Tkn.rparen, "Check `)`")
            check_skip(tokens, Tkn.lbrack, "Check `{`")
            statements = parse_statements(tokens, func_dec=False)
            subtree = Func(ret_type=type_dec, name=func_name, body=Body(statements))
        elif typ(tokens[1]) is Tkn.equal:
            """ Variable Declaration + Assignment"""
            variable = Var(name=tokens[0])
            check_skip(tokens, Tkn.var, "Check var name")
            check_skip(tokens, Tkn.equal, "Check `=`")
            expression = exp_AST(tokens)
            check_skip(tokens, Tkn.semicolon, "Check `;`")
            decl = Decl(var=variable, type_dec=type_dec)
            assign = Assign(var_name=variable, exp=expression)
            subtree = Body([decl, assign])

        elif typ(tokens[1]) is Tkn.semicolon:
            """ Variable Declaration"""
            variable = Var(name=tokens[0])
            check_skip(tokens, Tkn.var, "Check var name")
            check_skip(tokens, Tkn.semicolon, "Check `;`")
            subtree = Decl(var=variable, type_dec=type_dec)
        else:
            raise Exception("Bad syntax after type keyword")
    elif root_type is Tkn.var:
        """ Assignment"""
        variable = Var(name=tokens[0])
        check_skip(tokens, Tkn.var, "Check var name")
        check_skip(tokens, Tkn.equal, "Check `=`")
        expression = exp_AST(tokens)
        check_skip(tokens, Tkn.semicolon, "Check `;`")
        subtree = Assign(var_name=variable, exp=expression)
    else:
        raise Exception("Invalid first term in statement {}".format(root))
    return subtree

def exp_AST(tokens):
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
                    exp_lst[ind:ind+2] = [UnaryExpression(op_name=op, oper=exp_lst[ind-1])]
                else:
                    exp_lst[ind-1:ind+2] = [Expression(op_name=op, oper1=exp_lst[ind-1], oper2=exp_lst[ind+1])]
        return exp_lst[0]

    exp_lst, drops = raw_expression_list(tokens)
    exp_ast = list_to_tree(exp_lst)
    for i in range(drops):
        tokens.pop(0)
    return exp_ast

def raw_expression_list(tokens, ind=0):
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
            if p_lvl == 0 or tok_type is Tkn.semicolon:
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
                expression, _ = raw_expression_list(tokens, i)
                children.append(expression)
                i = last_ind(tokens, i) + 1
        if len(children) % 2 == 0:
            raise Exception("Bad expression: binary operators must alternate")
        final_ind += 1
        if typ(tokens[final_ind]) is Tkn.binop:
            operator = tokens[final_ind]
            final_ind += 1
            second_exp_list, final_ind = raw_expression_list(tokens, final_ind)
            return [children, operator] + second_exp_list, final_ind
        elif typ(tokens[final_ind]) in [Tkn.semicolon, Tkn.rparen]:
            return [children], final_ind
        else:
            raise Exception("Bad expression")
    elif typ(tokens[ind]) in Tkn.constants or typ(tokens[ind]) is Tkn.var:
        # First expression is constant/variable
        val = wrapNode(tokens[ind])
        ind += 1
        if typ(tokens[ind]) is Tkn.binop:
            operator = tokens[ind]
            ind += 1
            second_exp_list, ind = raw_expression_list(tokens, ind)
            return [val, operator] + second_exp_list, ind
        elif typ(tokens[ind]) in [Tkn.semicolon, Tkn.rparen]:
            return [val], ind

    elif typ(tokens[ind]) is Tkn.unop or tokens[ind] == "-":
        exp_list = [tokens[ind]] if typ(tokens[ind]) is Tkn.unop else [Const(0, int), tokens[ind]]
        operator = tokens[ind]
        ind += 1
        second_exp_list, ind = raw_expression_list(tokens, ind)
        return exp_list + second_exp_list, ind
    print(tokens[ind], typ(tokens[ind]))
    raise Exception("Bad expression")

### AST Utils ###

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
    for i, c in enumerate(string):
        token += c
        terminals  = "(){;}"
        opers = "!+-*/=<>"
        if c in opers and (i+1<len(string) and string[i+1]=="="):
            pass
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