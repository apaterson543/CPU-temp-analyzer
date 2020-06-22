# CPU-temp-analyzer
Generate linear approximation, piecewise interpolation, and cubic spline for each core n in CPU from collected data

# Requirements
  * Python 3.7

# Input File Format

>Column represents CPU core. Each line should represent a reading at increments of 30 seconds.

>With Labels: 
```
+85.0Â°C +82.0Â°C +71.0Â°C +80.0Â°C
+70.0Â°C +65.0Â°C +58.0Â°C +65.0Â°C
+70.0Â°C +72.0Â°C +55.0Â°C +63.0Â°C
+91.0Â°C +86.0Â°C +76.0Â°C +85.0Â°C
+87.0Â°C +83.0Â°C +73.0Â°C +79.0Â°C
+89.0Â°C +88.0Â°C +78.0Â°C +84.0Â°C
+87.0Â°C +84.0Â°C +73.0Â°C +77.0Â°C
```
> Without Labels:
```
90.0 89.0 75.0 83.0
79.0 75.0 66.0 77.0
70.0 72.0 59.0 65.0
73.0 73.0 59.0 69.0
87.0 86.0 74.0 85.0
85.0 86.0 66.0 84.0
```
> Included Sample Files
```
sampledata.txt  <-- with labels
testdata.txt	<-- without lables

```

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

# For additional information
>please utitize pydoc for the main executable file 'processtemps' from within the project directory

```
	pydoc processtemps
```