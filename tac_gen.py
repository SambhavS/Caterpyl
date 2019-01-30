from utils import *

def ast_to_IL(ast):
    """Sets up register counter and initializes lists to hold IL. 
    Calls helper with 'main' to recursively generate IL and process output"""

    def convert_body(parent_func, body, lines):
        """Recursively traverses tree and generates IL based on node type"""
        for statement in body.statements:
            if node_type(statement) == "return":
                last_reg, sublines = exp_to_IL(r_count, statement.ret_val)
                lines += sublines
                if parent_func == "main":
                    lines += ["retmain {}".format(last_reg)]
                else:
                    lines += ["ret {}".format(last_reg)]
                break
            elif node_type(statement) == "assign":
                last_reg, sublines = exp_to_IL(r_count, statement.exp)
                r_count[0] -= 1
                lines += sublines
                lines += ["{} = {}".format(statement.var_name.name, last_reg)]
            elif node_type(statement) == "if":
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                truth_header = "--> {}:".format(line_counter[0])
                line_counter[0] += 1
                lines += ["ifT {} goto {}".format(cond_reg, truth_header[:-1])]
                truth_lines = [truth_header]
                all_lines.append(truth_lines)
                convert_body(parent_func, statement.true_body, truth_lines)
                if statement.else_body.statements:
                    else_header = "--> {}:".format(line_counter[0])
                    line_counter[0] += 1
                    lines += ["ifF {} goto {}".format(cond_reg, else_header[:-1])]
                    else_lines = [else_header]
                    all_lines.append(else_lines)
                    convert_body(parent_func, statement.else_body, else_lines)
            elif node_type(statement) == "body":
                convert_body(parent_func, statement, lines)

    line_counter = [0]
    main_lines = ["Main:"]
    all_lines = [main_lines]
    r_count = [0]
    for function in ast.children:
        if function.name == "main":
            convert_body("main", function.body, main_lines)
    main_lines.append("retmain 0")
    interm_lines = [line for lst in all_lines for line in lst]
    return interm_lines

def exp_to_IL(r_count, expression):
    """Returns tuple of generated intermediate-language lines that evaluate
     an expression and name of the register that stores the final value"""
    lines = []
    def helper(exp):
        if node_type(exp) == "expression":
            r1 = helper(exp.oper1)
            r2 = helper(exp.oper2)
            for r in (r1, r2):
                if r[:2] == "_t" and r[2:] and is_int(r[2:]):
                    r_count[0] -= 1
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {} {} {}".format(r_name, r1, exp.op_name, r2))
            return r_name
        elif node_type(exp) == "const":
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {}".format(r_name, exp.val))
            return r_name
        elif node_type(exp) == "var":
            return exp.name
        else:
            raise Exception("BAD IL")
    last_reg = helper(expression)
    return last_reg, lines
