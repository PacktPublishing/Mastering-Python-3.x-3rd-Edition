cython -3 -o main.c --embed --line-directives main.py

# This is for compiling on Linux or a similar system. The procedure
# for compiling a C program can vary quite a lot between systems.
gcc `python-config --libs --cflags` -o oware-client main.c
