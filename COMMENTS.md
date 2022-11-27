# MSc Group Project Commenting Style Guide

## General Guide
Comments should always be written in complete sentences, and should be detailed enough for the reader to reasonably interpret any code without further research. All comments should remain within the 80 character line limit.    

Given the nature of the project, code should be thoroughly commented to the point that a team member working on a different area could understand it.    

When functions or classes from libraries are used for the first time in a file, they should be accompanied with a comment explaining their functionality and use-case. If the same function or class is used for a different purpose elsewhere, this should also be commented.    

Comments for classes, functions, loops and if/else statements should be placed  on the line **below** their definition. Other code can be commented in-line or on the line below if the 80 character limit may be exceeded.    

**Remember**, people are using languages for the first time so may not be  familiar with language-specific syntax. However obvious it may seem, comments will help avoid possible confusion on these situations.

#### Headers
Headers should be placed at the top of every file. Below is an example of the layout that should be used (delete sections as neccesary). The summary should contain information about the contents of the file and the intended use of the  file. The subject 'this file' is infered and should not be written.
```
File:
Author1:
Author2:
Creation Date: 
Last Edit Date:
Last Edit By:

Classes:
Functions:

Summary of File:

```
#### Classes
Every class should paired with a comment that describes what it is and how to use it. They should be written with an implied subject of 'this function' and should start with a verb phrase.   

If the class inherits from another, this should be followed by an 'Inherits' section listing the base class(es) and where they are from so their  documentation can be consulted.

If the class has member variables, these should be listed in a 'Vars' section with a type and short description along with their access modifier.

#### Functions
Function comments should start with a brief description what the function does and how to use it. They should be written with an implied subject of 'this function' and should start with a verb phrase.  

This should be followed by an 'Args' section where argument names, types and descriptions are listed.   

Finally, there should be a 'Returns' section which gives the return types and short descriptions of each return variable.

#### Loops
Every loop should have a short comment describing its purpose. The subject of 'this loop' is implied and need not be included.   

An 'Iterated Value' section should be included below this with a type and short description for any non-obvious iterated values.

#### If/else Statements
Every conditional statement should have a short comment describing its purpose. The subject of 'this statement' is implied and need not be included.   

## Python
Below are some examples of how the commenting style would be implemented in Python. These are obviously a bit silly as the code is very obvious, but the same premise should be applied to the more complex code we'll be writing.
#### Header
```
File:           stats.py
Author:         Ted Jenks
Creation Date:  12/01/2022
Last Edit Date: 14/01/2022
Last Edit By:   Ted Jenks

Classes:        MoreTools(Base)
Functions:      average(vars)

Summary of File:

        Contains statistical tools to calculate means, .... etc. The intended 
        use is for analysis of Physics experiment results.

```
#### Class

```
def MoreTools(Base):
    """
    Contains a set of statistical tools which can be applied to a set of
    data for analysis.

    Inherits:
        Base: from base.py.

    Vars:
        PRIVATE data (arr<int>): the data to analyse.
    """
```
#### Function

```
def average(vars):
    """
    Calculates and returns the mean of an array of integers.

    Args:
        vars (arr<int>): an array of integer values.

    Returns:
        (int): the mean of the values in the array.
    """
```
#### Loops
```
for i in range(vars.len()):
    """
    Iterate though all cells of the array 'vars'.

    Iterated Value:
        i (int): index of array.
    """
```
#### If/else Statements
```
if vars[1] > vars[0]:
    """
    Check if second entry of the array 'vars' is bigger than first entry.
    """
    <code>
else:
    <else-code>
```

