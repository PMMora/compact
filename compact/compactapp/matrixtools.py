# The tools in this script positionally calculate operations on matrices,
# create blank and identity matrices, and convert short matrices to and from long matrices.
#
# Matrices use the following example notation:
# [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
#
# Which can be visually expressed as:
# [[0, [3, [6,
#   1,  4,  7,
#   2], 5], 8]]
#
# That is, a short matrix is composed of a list of sublists, where the sublists are lists of values in a column

# Creates a matrix of zeroes with a given number of rows and columns
def blank_matrix(sublists, items):
    return [[0 for i in range(items)] for j in range(sublists)]


# Create a short identity matrix
# e.g. 3 sublists and 3 items returns [[1,0,0],[0,1,0],[0,0,1]]
def identity_matrix(sublists, items):
    Blank = blank_matrix(sublists, items)
    for i in range(sublists):
        Blank[i][i] = 1
    return Blank


# Turn a long matrix (i.e. list of values) into a short matrix (i.e. list of sublists of values)
def short_to_long(shortMatrix):
    return [[item for sublist in shortMatrix for item in sublist], len(shortMatrix), len(shortMatrix[0])]


# Turn a short matrix (i.e. list of sublists of values) into a long matrix (i.e. list of values)
def long_to_short(longMatrix):
    return [i for i in map(list, zip(*[iter(longMatrix[0])]*longMatrix[2]))]


# Test if two short matrices have the same number of rows and columns
def short_matrices_compatible(MatrixA, MatrixB):
    Along = short_to_long(MatrixA)
    Blong = short_to_long(MatrixB)
    output = [0, 0, 0]
    # Check for same number of sublists
    if Along[1] == Blong[1]:
        output[0] = 1
    else:
        output[0] = 0
    # Check for same number of values
    if Along[2] == Blong[2]:
        output[1] = 1
    else:
        output[1] = 0
    # Check for same total length
    if len(Along[0]) == len(Blong[0]):
        output[2] = 1
    else:
        output[2] = 0
    return output


# Turn a list into a list of sublists where sublist contents are repeated list values
# e.g. turns [[0, 1, 2], 3] into [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
def list_to_sublists(List, Repeat):
    return [[j for i in range(Repeat)] for j in List]

# Turns a list of sublists into a list of sums
# e.g. turns [[0, 0, 0], [1, 1, 1], [2, 2, 2]] into [0, 3, 6]
def list_of_sublists_to_list_of_sums(ListOfSublists):
    return [sum(i) for i in ListOfSublists]


# Positionally add the values in one matrix to the values in a second matrix
def add_short(shortA, shortB):
    if short_matrices_compatible(shortA, shortB) == [1, 1, 1]:
        longA, longB = short_to_long(shortA), short_to_long(shortB)
        longC = [[longA[0][i] + longB[0][i] for i in range(len(longA[0]))], longA[1], longA[2]]
        return long_to_short(longC)

    else:
        raise Exception('Tried positionally adding two matrices of different dimensions')


# Positionally subtract the values in one matrix for the values in a second matrix
def subtract_short(shortA, shortB):
    if short_matrices_compatible(shortA, shortB) == [1, 1, 1]:
        longA, longB = short_to_long(shortA), short_to_long(shortB)
        longC = [[longA[0][i] - longB[0][i] for i in range(len(longA[0]))], longA[1], longA[2]]
        return long_to_short(longC)

    else:
        raise Exception('Tried positionally subtracting two matrices of different dimensions')

# Positionally multiply the values in one matrix by the values in a second matrix
def multiply_short(shortA, shortB):
    if short_matrices_compatible(shortA, shortB) == [1, 1, 1]:
        longA, longB = short_to_long(shortA), short_to_long(shortB)
        longC = [[longA[0][i] * longB[0][i] for i in range(len(longA[0]))], longA[1], longA[2]]
        return long_to_short(longC)

    else:
        raise Exception('Tried positionally multiplying two matrices of different dimensions')


# Positionally divide the values in one matrix by the values in a second matrix
def divide_short(shortA, shortB):
    if short_matrices_compatible(shortA, shortB) == [1, 1, 1]:
        longA, longB = short_to_long(shortA), short_to_long(shortB)
        longC = [[longA[0][i] / longB[0][i] for i in range(len(longA[0]))], longA[1], longA[2]]
        return long_to_short(longC)

    else:
        raise Exception('Tried positionally dividing two matrices of different dimensions')


# Turn a list of columns into a list of rows
def transpose(shortA):
    transposed = [list(i) for i in zip(*shortA)]
    print(transposed)
    return transposed
