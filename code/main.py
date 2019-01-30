from utils import *
from ast_gen import *
from tac_gen import *
from asm_gen import *
import subprocess

def main():
    # Read C
    fname = "test.c"
    with open("../asm/{}".format(fname)) as f:
        contents = f.read()

    # Create & print AST
    ast = main_AST(contents)
    print_tree(ast)

    # Convert AST and print resulting IL
    interm_lines = ast_to_IL(ast)   
    print_IL(interm_lines)
    return
    
    # Define dicts for type and memory info
    lookup = make_lookup(ast)
    mem_dict = {var:i for i, var in enumerate(lookup.keys())}
    
    # Generate and print assembly
    assembly = gen_assembly(interm_lines, mem_dict)
    print_lst(assembly)
    
    # Write generated assembly to file
    with open("../asm/{}.asm".format(fname.split(".")[0]), "w") as f_out:
            for line in assembly:
                f_out.write("{}\n".format(line))

    # Run generated assembly
    f_base = fname.split(".")[0] 
    assemble_link_run = """ cd ../asm; as -arch x86_64 -o {0}.o {0}.asm ; 
                            ld -o {0} {0}.o 2> std.err; ./{0} ; echo $? ;""".format(f_base)
    subprocess.call(assemble_link_run, shell=True)  
    return 0

main()