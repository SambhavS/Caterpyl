.global start
start:
  movq %rsp, %rbp
  subq $12, %rsp
  movl $10, %ebx
  movl %ebx, 0(%rbp)
  movl 0(%rbp), %r15d
  movl %r15d, -4(%rbp)
  movl -4(%rbp), %r15d
  movl %r15d, -8(%rbp)
  movl -8(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
  addq $12, %rsp