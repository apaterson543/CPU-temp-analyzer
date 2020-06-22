# CPU-temp-analyzer
Generate linear approximation, piecewise interpolation, and cubic spline for each core n in CPU from collected data

# Requirements
  * Python 3.7

# Execution

```
python3 processtemps.py /testfilepath #

Where # is a number 1-4 to select:
1: Global Linear Approximation
2: Piecewise Interpolation
3: Cubic Spline	
4: All of the Above
```

# Output in files similar to:

```
0    <= x <   630; y_0 = 81.50 +  -0.000613x; Linear Approximation
0.0  <= x <  30.0; y_0 = 82.00 +  -0.566667x; Piecewise Interpolation
90.0 <= x < 150.0; y_3 = 86.0  +  -0.083333x + 0.000000x^2 + -0.000005x^3; Cubic Spline

Linear Approximation and Piecewise Interpolation will be printed to the same file while
Cubic Splines will be printed to different files. All files will represent a single core.

The output locations will be in SemesterProject/outputfiles/ 

On execution of the program, the directories to which the files are saved and written will 
be displayed

```

# For additional information, please utitize pydoc for the main executable file 'processtemps' from within the project directory

```
	pydoc processtemps
```