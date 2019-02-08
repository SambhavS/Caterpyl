  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  subq $16, %rsp
  movl $10, %r9d
  movl %r9d, 0(%rbp)
  movl $0, %r9d
  movl %r9d, -4(%rbp)
  movl $0, %r9d
  movl %r9d, -8(%rbp)
  movl $1, %r9d
  movl %r9d, -12(%rbp)
W1:
  movl $0, %r9d
  movl 0(%rbp), %r15d
  cmp %r9d, %r15d
  jg e12
  movl $0, %r9d
  jmp aft12
e12:
  movl $1, %r9d
aft12:
  cmpl $0, %r9d
  je A2
  movl -8(%rbp), %r15d
  movl %r15d, -4(%rbp)
  movl -12(%rbp), %r15d
  movl %r15d, -8(%rbp)
  movl -8(%rbp), %r15d
  add  -4(%rbp), %r15d
  movl %r15d, %r9d
  movl %r9d, -12(%rbp)
  movl $1, %r9d
  movl 0(%rbp), %r15d
  sub  %r9d, %r15d
  movl %r15d, %r9d
  movl %r9d, 0(%rbp)
  jmp W1
A2:
  addq $16, %rsp
  movl -8(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  addq $16, %rsp
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
