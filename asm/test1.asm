  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $31, %r9d
  movl %r9d, -8(%rbp)
  movl -8(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
fib:
  movl $1, %r9d
  movl %r9d, -24(%rbp)
  movl $2, %r9d
  movl %r9d, -32(%rbp)
  movl -32(%rbp), %edi
  ret
  movl $0, %edi
  ret
