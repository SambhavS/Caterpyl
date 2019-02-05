from utils import *

def ast_to_IL(ast, master_lookup):
    """Sets up register counter and initializes lists to hold IL. 
    Calls helper with 'main' to recursively generate IL and process output"""

    def get_count(counter):
        """ Increments counter"""
        counter[0] += 1
        return counter[0]

    def convert_body(parent_func, body):
        """Recursively traverses tree and generates IL based on node type"""
        nonlocal lines_dict
        lines = lines_dict[parent_func]
        lookup = master_lookup[parent_func]

        for statement in body.statements:
            if node_type(statement) == "return":
                last_reg, sublines = exp_to_IL(r_count, statement.ret_val)
                lines += sublines
                if parent_func == "main":
                    if int(memory):
                        lines.append("end {}".format(memory))
                    lines.append("retmain {}".format(last_reg))
                else:
                    if int(memory):
                        lines.append("end {}".format(memory))
                    lines.append("ret {}".format(last_reg))
                break

            elif node_type(statement) == "assign":
                last_reg, sublines = exp_to_IL(r_count, statement.exp)
                if last_reg[:2] == "_t" and last_reg[2:] and is_int(last_reg[2:]):
                    r_count[0] -= 1
                lines += sublines
                lines.append("{} = {}".format(statement.var_name.name, last_reg))

            elif node_type(statement) == "if":
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                truth_header = "--> T{}:".format(get_count(counter))
                after_header = "--> A{}:".format(get_count(counter))
                lines.append("ifTrue {} goto {}".format(cond_reg, truth_header[:-1]))
                if statement.else_body.statements:
                    else_header = "--> E{}:".format(get_count(counter))
                    lines.append("ifFalse {} goto {}".format(cond_reg, else_header[:-1]))
                if cond_reg[:2] == "_t" and cond_reg[2:] and is_int(cond_reg[2:]):
                    r_count[0] -= 1
                lines.append("goto {}".format(after_header[:-1]))
                lines.append(truth_header)
                convert_body(parent_func, statement.true_body)
                lines.append("goto {}".format(after_header[:-1]))
                if statement.else_body.statements:
                    lines.append(else_header)
                    convert_body(parent_func, statement.else_body)
                    lines.append("goto {}".format(after_header[:-1]))
                lines.append(after_header)
                
            elif node_type(statement) == "while":
                while_header = "--> W{}:".format(get_count(counter))
                lines.append(while_header)
                cond_reg, sublines = exp_to_IL(r_count, statement.cond)
                lines += sublines
                after_header = "--> A{}:".format(get_count(counter))
                lines.append("ifFalse {} goto {}".format(cond_reg, after_header[:-1]))
                if cond_reg[:2] == "_t" and cond_reg[2:] and is_int(cond_reg[2:]):
                    r_count[0] -= 1
                convert_body(parent_func, statement.true_body)
                lines.append("goto {}".format(while_header[:-1]))
                lines.append(after_header)
            elif node_type(statement) in ("expression", "unaryexpression", "fnccall"):
                last_reg, sublines = exp_to_IL(r_count, statement)
                if last_reg[:2] == "_t" and last_reg[2:] and is_int(last_reg[2:]):
                    r_count[0] -= 1
                lines += sublines
            elif node_type(statement) == "body":
                convert_body(parent_func, statement)

    memory_locations = dict()
    counter = [0]
    lines_dict= dict()
    r_count = [1]
    for function in ast.children:
        memory = len([i for i in master_lookup[function.name] if "::" not in i]) * 4
        lines_dict[function.name] = ["{}:".format(function.name)]
        for param_name, param_type in function.params[::-1]:
            lines_dict[function.name].append("param {}".format(param_name))    
        if int(memory):
            lines_dict[function.name].append("start {}".format(memory))
        convert_body(function.name, function.body)
        if int(memory):
            lines_dict[function.name].append("end {}".format(memory))
        if function.name != "main":
            lines_dict[function.name].append("ret 0")
        else:
            lines_dict["main"].append("retmain 0")

    return lines_dict

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
        elif node_type(exp) == "unaryexpression":
            r = helper(exp.oper)
            if r[:2] == "_t" and r[2:] and is_int(r[2:]):
                r_count[0] -= 1
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {} {}".format(r_name, exp.op_name, r))
            return r_name
        elif node_type(exp) == "const":
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = {}".format(r_name, exp.val))
            return r_name
        elif node_type(exp) == "var":
            return exp.name
        elif node_type(exp) == "fnccall":
            regs = [helper(arg) for arg in exp.arguments]
            for reg in regs[::-1]:
                lines.append("pushParam {}".format(reg))
            for reg in regs[::-1]:
                r_count[0] -= 1
            # allocate space for variables, push variables to registers?
            func_name = exp.called_func
            param_space = len(regs) * 4
            r_count[0] += 1
            r_name = "_t{}".format(r_count[0])
            lines.append("{} = call {}".format(r_name, func_name))
            if param_space:
                lines.append("popParamSpace {}".format(param_space))
            return r_name
        else:
            raise Exception("BAD IL")
    last_reg = helper(expression)
    return last_reg, lines
