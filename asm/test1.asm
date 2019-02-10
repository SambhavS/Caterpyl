  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $0, %r9d
  movl %r9d, -8(%rbp)
  movl $0, %r9d
  movl %r9d, -16(%rbp)
W1:
  movl -16(%rbp), %r15d
  cmp $0, %r15d
  je e7
  movl $0, %r9d
  jmp aft7
e7:
  movl $1, %r9d
aft7:
  cmpl $0, %r9d
  je A2
  movl $10, %r9d
  movl -8(%rbp), %r15d
  add  %r9d, %r15d
  movl %r15d, %r9d
  movl %r9d, -8(%rbp)
  movl $100, %r9d
  movl -8(%rbp), %r15d
  cmp %r9d, %r15d
  jg e13
  movl $0, %r9d
  jmp aft13
e13:
  movl $1, %r9d
aft13:
  cmpl $0, %r9d
  jne T3
  jmp A4
T3:
  movl $1, %r9d
  movl %r9d, -16(%rbp)
  jmp A4
A4:
  jmp W1
A2:
  movl -8(%rbp), %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
