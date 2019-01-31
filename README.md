# Caterpyl

Hi! This is a compiler I'm writing from scratch to compile the core subset of C to x86_64 assembly code.

Currently, it has the following features:
- finds and compiles main function
- returns value from main
- int variables, integer literals, integer expressions (like `int x = 10;` and `int y = (2 * 10 + 7 * (3 + 1)) - 200;`)
- arithmetic operators (`+`, `*`, `-`, `/`)
- comparators (eg. `==`, `<`, `>=`, `!=`)
- control structures (`if`, `else`, `while`)
