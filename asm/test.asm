  # Setup stack/base pointer
.global start
start:
  movq %rsp, %rbp
  subq $40, %rsp
  # Assignment
  movl $15, %ebx
  # Assignment
  movl %ebx, 0(%rbp)
  # Assignment
  movl $0, %ebx
  # Assignment
  movl %ebx, -8(%rbp)
  # Assignment
  movl $1, %ebx
  # Assignment
  movl %ebx, -16(%rbp)
  # Assignment
  movl $0, %ebx
  # Assignment
  movl %ebx, -24(%rbp)
  # Assignment
  movl $0, %ebx
  # Assignment
  movl %ebx, -32(%rbp)
W1:
  # Checking comparison
  movl -32(%rbp), %r15d
  cmp 0(%rbp), %r15d
  jl e12
  movl $0, %ebx
  jmp aft12
e12:
  movl $1, %ebx
aft12:
  # IfFalse branch
  cmpl $0, %ebx
  je A2
  # Assignment
  movl -8(%rbp), %r15d
  movl %r15d, -24(%rbp)
  # Assignment
  movl -16(%rbp), %r15d
  movl %r15d, -8(%rbp)
  # Arithmetic operation
  movl -24(%rbp), %r15d
  add  -16(%rbp), %r15d
  movl %r15d, %ecx
  # Assignment
  movl %ecx, -16(%rbp)
  # Assignment
  movl $1, %ecx
  # Arithmetic operation
  movl -32(%rbp), %r15d
  add  %ecx, %r15d
  movl %r15d, %ecx
  # Assignment
  movl %ecx, -32(%rbp)
  # Goto
  jmp W1
A2:
  # Return out of `main`
  movl -8(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  # Return out of `main`
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
  addq $40, %rsp
