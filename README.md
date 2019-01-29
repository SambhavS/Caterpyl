# Caterpyl

Run assembly with:

as -arch x86_64 -o ex.o ex.s ;
ld -o ex ex.o 2> std.err ; ./ex ; echo $?


ASSEMBLY TIPS
Return value in %edi register.
Syscall code in %eax register
movl $0x2000004, %eax   - for syscalls
Use $ for literal values



iffalse:
    movl $0, %edi           # load return value
    movl $0x2000001, %eax    # load exit val for syscall
    syscall                  # make syscall to exit

iftrue:
    movl $1, %edi           # load return value
    movl $0x2000001, %eax    # load exit val for syscall
    syscall                  # make syscall to exit
