# Icosoku Solver in Python


## Presentation
What is the Icosoku? 

[![Icosoku Video](http://img.youtube.com/vi/ksVBkZwnSJ4/0.jpg)](http://www.youtube.com/watch?v=ksVBkZwnSJ4)

The solver tries to find for each triangle a white brick which satisfies the constraint, i.e. the sum of black dots of bricks is equql to the sum of the yellow vertex.

Approach is brute-force, and the program will return as soon as a valid solution is found. 

## Cython
Generate the C file

```cython --embed solver.py```

Compile the C file with Python 3

```gcc `python3m-config --cflags` solver.c -o solver `python3m-config --ldflags```

Run the binary

```./solver```