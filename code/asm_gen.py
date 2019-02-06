from utils import *

def gen_assembly(interm_lines, master_lookup):
    """Converts TAC representation into valid x86_64 assembly. Returns lines of assembly"""
    def to_asm(tok):
        if last_func == "main":
            offset = 0
        else:
            offset = -8
        """ Converts individual TAC token to assembly equivelent"""
        if tok in reg_dict:     return reg_dict[tok]
        elif tok in opers:      return opers[tok]
        elif tok in log_ops:    return log_ops[tok]
        elif tok in comps:      return comps[tok]
        elif tok in un_ops:     return un_ops[tok]
        elif is_int(tok):       return "${}".format(tok)
        elif tok in mem_dict:   return "{}(%rbp)".format(mem_dict[tok] * -4 + offset)
        else:
            raise Exception("TypeError: Variable `{}` not declared".format(tok))

    def qpush(string):
        if not string:
            return
        if string[-1] == ":":
            assembly.append(string)
        else:
            assembly.append("  {}".format(string))
    func_stack = ["main"]
    params = []
    # Define equivalent register names and set up start of assembly file
    assembly = []
    qpush("#   Setup stack/base pointer, base offset")
    qpush(".global start")
    qpush("start:")
    qpush("movq %rsp, %rbp")

    reg_dict = {"_t1": "%r8d", "_t2": "%r9d", "_t3": "%r10d", "_t4": "%r11d",
                "_t5": "%r12d", "_t6": "%r13d", "_t7": "%r14d"}
    opers = {"*":"imul", "-":"sub", "+":"add", "/":"div", "%":"div"}
    log_ops = {"&&":"and", "||":"or"}
    un_ops = {"!": "not"}
    comps = {"==": "je", "!=": "jne", ">=": "jge", "<=": "jle", "<":  "jl", ">":  "jg"}

    # Convert TAC line by line, by type of statement
    # (False == 0, True != 0)
    for i, line in enumerate(interm_lines):
        tokens = line.split()
        if len(tokens) == 5:
            if tokens[0] == "ifTrue":
                cond_reg, dest = tokens[1], tokens[-1]
                qpush("cmpl $0, {}".format(to_asm(cond_reg)))
                qpush("jne {}".format(dest))
            elif tokens[0] == "ifFalse":
                cond_reg, dest = tokens[1], tokens[-1]
                qpush("cmpl $0, {}".format(to_asm(cond_reg)))
                qpush("je {}".format(dest))

            elif tokens[3] in opers:
                dest, source1, source2 = to_asm(tokens[0]), to_asm(tokens[2]), to_asm(tokens[4])
                instr = to_asm(tokens[3])
                if instr == "div":
                    qpush("movl $0, %edx")
                    qpush("movl {}, %eax".format(source1))
                    qpush("movl {}, %ecx".format(source2))
                    qpush("div %ecx")
                    value = "%edx" if tokens[3] == "%" else "%eax"
                    qpush("movl {}, {}".format(value, dest))
                else:
                    qpush("movl {}, %r15d".format(source1))
                    qpush("{}  {}, %r15d".format(instr, source2))
                    qpush("movl %r15d, {}".format(dest))

            elif tokens[3] in log_ops:
                operator = to_asm(tokens[3])
                dest, source1, source2 = to_asm(tokens[0]), to_asm(tokens[2]), to_asm(tokens[4])
                if operator == "and":
                    instr, match, fall_through = "je", 0, 1
                elif operator == "or":
                    instr, match, fall_through = "jne", 1, 0
                qpush("movl {}, %r15d".format(source1))
                qpush("cmp $0, %r15d")
                qpush("{} e{}".format(instr, i))
                qpush("movl {}, %r15d".format(source2))
                qpush("cmp $0, %r15d")
                qpush("{} e{}".format(instr, i))
                qpush("movl ${}, {}".format(fall_through, dest))
                qpush("jmp aft{}".format(i))
                qpush("e{}:".format(i))
                qpush("movl ${}, {}".format(match, dest))
                qpush("aft{}:".format(i))
                    
            elif tokens[3] in comps:
                dest, oper, oper1, oper2 = to_asm(tokens[0]), to_asm(tokens[3]), to_asm(tokens[2]), to_asm(tokens[4])
                qpush("movl {}, %r15d".format(oper1))
                qpush("cmp {}, %r15d".format(oper2))
                qpush("{} e{}".format(oper, i))
                qpush("movl $0, {}".format(dest))
                qpush("jmp aft{}".format(i))
                qpush("e{}:".format(i))
                qpush("movl $1, {}".format(dest))
                qpush("aft{}:".format(i))

        elif len(tokens) == 4:
            if tokens[2] in un_ops:
                operator = to_asm(tokens[2])
                dest, operand = to_asm(tokens[0]), to_asm(tokens[3])
                qpush("movl {}, %r15d".format(operand))
                qpush("cmp $0, %r15d")
                qpush("je e{}".format(i))
                qpush("movl $0, {}".format(dest))
                qpush("jmp aft{}".format(i))
                qpush("e{}:".format(i))
                qpush("movl $1, {}".format(dest))
                qpush("aft{}:".format(i))

            elif tokens[2] == "call":
                qpush("#----------")
                func_name = tokens[3]
                ret_address = to_asm(tokens[0])
                # Push base pointer
                qpush("subq $4, %rsp")
                qpush("movq %rbp, -4(%rsp)")
                # Change base pointer
                qpush("subq $4, %rsp")
                qpush("movq %rsp, %rbp")
                for param in params:
                    asm_param = to_asm(param)
                    qpush("subq $4, %rsp")
                    qpush("movl {}, %r15d".format(asm_param))
                    qpush("movl %r15d, 0(%rsp)".format(asm_param))
                func_stack.append(func_name)
                qpush("call {}".format(func_name))
                func_stack.pop()
                # Clean by moving stack up to child base pointer
                qpush("movq %rbp, %rsp")
                # Restore old base
                qpush("addq $4, %rsp")
                qpush("movq -4(%rsp), %rbp")
                # Get stack back to original place
                qpush("addq $4, %rsp")
                # Move edi to register
                qpush("movl %edi, {}".format(ret_address))
                # Clean pushed parameters
                for param in params:
                    qpush("subq $4, %rsp")
                params = []
                qpush("#----------")

        elif len(tokens) == 3:
            if tokens[1] == "=":
                source, dest = to_asm(tokens[2]), to_asm(tokens[0])
                if "(" in source and "(" in dest:
                    qpush("movl {}, %r15d".format(source))
                    qpush("movl %r15d, {}".format(dest))
                else:
                    qpush("movl {}, {}".format(source, dest))
            elif tokens[0] == "goto":
                dest = tokens[-1]
                qpush("jmp {}".format(dest))

        elif len(tokens) == 2:
            if tokens[0] == "retmain":
                source = to_asm(tokens[1])
                qpush("movl {}, %edi".format(source))
                qpush("movl $0x2000001, %eax")
                qpush("syscall")
            elif tokens[0] == "ret":
                source = to_asm(tokens[1])
                qpush("movl {}, %edi".format(source))
                qpush("ret")
            elif tokens[0] == "-->":
                label = tokens[1]
                qpush(label)
            elif tokens[0] == "start":
                stack_space = tokens[1]
                qpush("subq ${}, %rsp".format(stack_space))
                for arg in lookup:
                    if "::" not in arg and arg not in mem_dict:
                        mem_dict[arg] = len(mem_dict)

            elif tokens[0] in ("end","popParamSpace"):
                stack_space = tokens[1]
                qpush("addq ${}, %rsp".format(stack_space))
            elif tokens[0] == "pushParam":
                reg = tokens[1]
                params.append(reg)
            elif tokens[0] == "param":
                param = tokens[1]
                mem_dict[param] = len(mem_dict) - 1


        elif len(tokens) == 1:
            qpush(tokens[0])
            # Move base pointer to stack pointer
            func_name = tokens[0][:-1]
            last_func = func_name
            lookup = master_lookup[func_name]
            mem_dict = {}
    
                    
    return assembly