  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  #----------
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r9d
  #----------
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
foo:
  #----------
  subq $4, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  call bar
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r10d
  #----------
  movl %r10d, %edi
  ret
  movl $0, %edi
  ret
bar:
  movl $5, %r11d
  movl %r11d, %edi
  ret
  movl $0, %edi
  ret
