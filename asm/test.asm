  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  subq $8, %rsp
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call foo
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, 0(%rbp)
  #   Call
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call foo
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  addq $4, %rsp
  movl %edi, %r9d
  movl %r9d, -4(%rbp)
  movl 0(%rbp), %r15d
  imul  -4(%rbp), %r15d
  movl %r15d, %r9d
  addq $8, %rsp
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  addq $8, %rsp
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
foo:
  subq $8, %rsp
  movl $2, %r10d
  movl %r10d, -12(%rbp)
  movl $3, %r10d
  movl %r10d, -16(%rbp)
  movl -12(%rbp), %r15d
  imul  -16(%rbp), %r15d
  movl %r15d, %r10d
  addq $8, %rsp
  movl %r10d, %edi
  ret
  addq $8, %rsp
  movl $0, %edi
  ret
