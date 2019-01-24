# Caterpyl

Run assembly with:

as -arch x86_64 -o hello_as_64.o hello_as_64.asm ; 
ld -o hello_as_64 hello_as_64.o ; 
./hello_as_64


ASSEMBLY TIPS
Return value in %edi register.
Syscall code in %eax register
movl $0x2000004, %eax   - for syscalls
Use $ for literal values
