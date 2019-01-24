.text

.global start

start:
  movl $0x2000004, %eax           # Preparing syscall 4
  movq str@GOTPCREL(%rip), %rsi   # The string to print
  movq $100, %rdx                 # The size of the value to print
  syscall

  movl $52, %edi                  # return value in edi
  movl $0x2000001, %eax           # exit 0
  syscall

.data
str:
  .asciz "Hello World!\n"
