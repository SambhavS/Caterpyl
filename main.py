from utils import *

"""
TODO:
-add type checking
-namespace for variables vs function?

Program Summary:
We go through the program, checking for independent trees. Each tree is a 
return statement, an if/else statement, a variable assignment, or a function declaration.
We should distinguish between a series of statements, a single statement, and an expression.

We skip non-parsable tokens proactively - that is each function assumes they need not skip any
tokens and skips any remaining non-parseable ones before returning.
"""

def test_run(fname):
    """ Load and run program"""
    with open(fname) as f:
        contents = f.read()
        ast = main_AST(contents)
        print_tree(ast)

def print_tree(tree, depth=0):
    dt_str = " ({})".format(tree.data_type) if hasattr(tree, "data_type") else ""
    op_str = " ({})".format(tree.op_name) if hasattr(tree, "op_name") else ""
    val_str = " ({})".format(tree.val) if hasattr(tree, "val") else ""
    print("{}{}{}{}{}".format("{}{}".format("   "*depth,"|"), tree.__class__.__name__, op_str, val_str, dt_str))
    if hasattr(tree, "children"):
        children = tree.children            
        for child in children:
            print_tree(child, depth+1)

def main_AST(program):
    tokens = tokenize(program)
    subtrees, _ = parse_statements(tokens, 0, func_dec=True)  
    return Prog(subtrees)

def parse_statements(tokens, ind, func_dec=False):
    statements = []
    while ind != len(tokens) and typ(tokens[ind]) != Tkn.rbrack:
        if ind >= len(tokens):
            raise Exception("Syntax Error")
        statement, ind = statement_AST(tokens, ind, func_dec)
        
        statements.append(statement)
    # Parse `}`
    ind += 1
    return statements, ind


def statement_AST(tokens, ind, func_dec=False):
    root = tokens[ind]
    root_type = typ(root)
    if root_type in Tkn.prog_keywords:
        """Special Language Construct"""
        if root_type is Tkn.ifx:
            ind = check_skip(tokens[ind], ind, Tkn.ifx, "Check `if`")
            ind = check_skip(tokens[ind], ind, Tkn.lparen, "Check `(`")
            expression, ind = expression_AST(tokens, ind)
            ind = check_skip(tokens[ind], ind, Tkn.lbrack, "Check `{`")     
            true_statements, ind = parse_statements(tokens, ind)
            if tokens[ind] == "else":
                ind = check_skip(tokens[ind], ind, Tkn.elsex, "Check `else`")
                ind = check_skip(tokens[ind], ind, Tkn.lbrack, "Check `{`")
                else_statements, ind = parse_statements(tokens, ind)
            else:
                ind = check_skip(tokens[ind], Tkn.rbrack, "Check `}`")
                else_statements = None
            subtree = If(cond=expression, true_body=Body(true_statements), else_body=Body(else_statements))
        elif root_type is Tkn.returnx:
            ind = check_skip(tokens[ind], ind, Tkn.returnx, "Check `return`")
            ret_expression, ind = expression_AST(tokens, ind)
            subtree = Return(ret_expression)

    elif root_type in Tkn.type_keys:
        type_dec = root
        ind = check_skip(tokens[ind], ind, Tkn.type_keys, "Check type keyword")
        if func_dec:
            """ Function Declaration -- needs type checking"""
            print(tokens[ind])
            ind = check_skip(tokens[ind], ind, Tkn.var, "Check function var name")
            func_name = tokens[ind]
            ind = check_skip(tokens[ind], ind, Tkn.lparen, "Check `(`")
            ind = check_skip(tokens[ind], ind, Tkn.rparen, "Check `)`")
            ind = check_skip(tokens[ind], ind, Tkn.lbrack, "Check `{`")
            statements, ind = parse_statements(tokens, ind, func_dec=False)
            subtree = Func(ret_type=type_dec, func_name=func_name, body=Body(statements))
        else:
            """ Variable Assignment -- needs type checking"""
            variable = Var(root)
            ind = check_skip(tokens[ind], ind, Tkn.var, "Check var name")
            ind = check_skip(tokens[ind], ind, Tkn.equal, "Check `=`")
            expression, ind = expression_AST(tokens, ind)
            subtree = Assign(var_name=variable, data_type=type_dec, exp=expression)
    return subtree, ind

def expression_AST(tokens, ind):
    start_ind = ind
    tok_list = []
    """This part finds the ending index. 
    This means that we find one extra parenthesis or semicolon.

    We have the following cases:
    1) We just find a constant - we return it
    2) We find a constant followed by an operator - we return an
     expression with our findings and recursively figure out the rest






    """
    p_lev = 0
    # Find ending index of overall expression
    while typ(tokens[ind]) is not Tkn.semicolon: 
        curr_type = typ(tokens[ind])
        if curr_type is Tkn.lparen:
            p_lev -=1
        elif curr_type is Tkn.rparen:
            p_lev += 1
        if  p_lev > 0:
            break
        tok_list.append(tokens[ind])
        ind += 1

    lst_ind = 0
    first_tkn_type = typ(tok_list[lst_ind])
    if first_tkn_type in Tkn.constants or first_tkn_type is Tkn.var:
        if first_tkn_type is Tkn.var:
            value = Var(tok_list[lst_ind])
        else:
            value = Const(tok_list[lst_ind], first_tkn_type)
        lst_ind += 1
        if len(tok_list) == 1:
            expression = value
        elif typ(tok_list[lst_ind]) is Tkn.binop:
            operator = tok_list[lst_ind]
            lst_ind += 1
            second_expression, _ = expression_AST(tokens, start_ind + lst_ind)
            expression = Expression(op_name = operator, oper1=value, oper2=second_expression)
        else:
            raise Exception("Constant followed by nonterminary token that is not nonbinary operator")

    elif first_tkn_type is Tkn.lparen:
        lst_ind += 1
        # We find the first complete expression and parse it
        p_lev = -1
        while p_lev < 0:
            if typ(tok_list[lst_ind]) is Tkn.rparen:
                p_lev += 1
            elif typ(tok_list[lst_ind]) is Tkn.lparen:
                p_lev -= 1
            lst_ind += 1
        if len(tok_list) == lst_ind:
            expression, _ = expression_AST(tokens, start_ind+1)
        elif typ(tok_list[lst_ind]) is tkn.binop:
            operator = typ(tok_list[lst_ind])
            expression1, _ = expression_AST(tokens, start_ind+1)
            expression2, _ = expression_AST(tokens, start_ind+lst_ind)
            expression = Expression(op_name=operator, oper1=expression1, oper2=expression2)
    
    ind = check_skip(tokens[ind], ind, [Tkn.rparen, Tkn.semicolon], "Check `)` or `;`" )
    return expression, ind

def get_final_index(tokens, ind):
    """Finds ending index of expression"""

def tokenize(string):
    """ Returns list of tokens given program as a string"""
    tokens = []
    token = ""
    for i, c in enumerate(string):
        token += c
        if (   c in SPECIAL_CHARS 
            or i+1 == len(string) 
            or string[i+1] in SPECIAL_CHARS + WHITESPACE):
            tokens.append(token)
            token = ""
    if token:
        tokens.append(token)
        token = ""
    return [t.strip() for t in tokens if t.strip()]  

def check_skip(val, ind, exp, msg):
    """Checks that value matches a certain type and skips it"""
    if typ(val) not in exp:
        raise Exception(msg)   
    return ind + 1


# Call test run        
test_run("ex.c")
