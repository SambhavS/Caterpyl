  #   Setup stack/base pointer, base offset
  .global start
start:
  movq %rsp, %rbp
main:
  movl $10, %r9d
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r9d, %r15d
  movl %r15d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r9d
  addq $4, %rsp
  #----------
  addq $4, %rsp
  movl %r9d, %edi
  movl $0x2000001, %eax
  syscall
  movl $0, %edi
  movl $0x2000001, %eax
  syscall
fact:
  subq $4, %rsp
  movl $0, %r10d
  movl -4(%rbp), %r15d
  cmp %r10d, %r15d
  je e11
  movl $0, %r10d
  jmp aft11
e11:
  movl $1, %r10d
aft11:
  cmpl $0, %r10d
  jne T1
  cmpl $0, %r10d
  je E3
  jmp A2
T1:
  movl $2, %r10d
  addq $4, %rsp
  movl %r10d, %edi
  ret
  jmp A2
E3:
  movl $1, %r11d
  movl $1, %r12d
  movl -4(%rbp), %r15d
  sub  %r12d, %r15d
  movl %r15d, %r12d
  #----------
  subq $8, %rsp
  movq %rbp, 0(%rsp)
  movq %rsp, %rbp
  subq $4, %rsp
  movl %r12d, %r15d
  movl %r15d, 0(%rsp)
  call fact
  movq %rbp, %rsp
  movq 0(%rsp), %rbp
  movl %edi, %r12d
  addq $4, %rsp
  #----------
  addq $4, %rsp
  movl %r11d, %r15d
  add  %r12d, %r15d
  movl %r15d, %r11d
  addq $4, %rsp
  movl %r11d, %edi
  ret
  jmp A2
A2:
  addq $4, %rsp
  movl $0, %edi
  ret
