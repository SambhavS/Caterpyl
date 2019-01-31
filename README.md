# Caterpyl

Hi! This is a C compiler I'm writing from scratch in Python. It compiles the source to x86_64 assembly code.

I probably (read:definitely) won't implement the entire language, but rather the most important subset.

Currently, it has the following features:
- compiles single main method
- returns value from main
- int variables, integer literals, integer expressions
- arithmetic operations
- comparators (eg. ==, <, >=, !=)
- allows for use of control structures (if, else, while)
