# Todo
HIGH PRIORITY
- fix broken recursion
- fix broken parsing for function calls 

After
- which data types?
- user definable functions
- printing
- type checking (actually)
- optimization
- deal with many variables in ASM_gen (insufficient registers)
-fix gross master lookup format

# Tokens
We skip non-parsable tokens proactively for parse_statements & statement_AST, but not for expression_AST


# Call assembly
as -arch x86_64 -o test.o test.asm ;
ld -o test test.o 2> std.err ; ./test ; echo $?

# Register allocation
special registers: rbp (base), rsp (stack), eax (syscall?), edi (return?), r15d(for double memory references), rsi ()
others: ebx, ecx, edx, r8d, r9d, r10d, r11d, r12d, r13d, r14d

