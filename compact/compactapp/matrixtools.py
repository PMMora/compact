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
def BlankMatrix(sublists, items):
    return [[0 for i in range(items)] for j in range(sublists)]


# Create a short identity matrix
# e.g. 3 sublists and 3 items returns [[1,0,0],[0,1,0],[0,0,1]]
def IdentityMatrix(sublists, items):
    Blank = BlankMatrix(sublists, items)
    for i in range(sublists):
        Blank[i][i] = 1
    return Blank


# Turn a long matrix (i.e. list of values) into a short matrix (i.e. list of sublists of values)
def ShortToLong(ShortMatrix):
    return [[item for sublist in ShortMatrix for item in sublist], len(ShortMatrix), len(ShortMatrix[0])]


# Turn a short matrix (i.e. list of sublists of values) into a long matrix (i.e. list of values)
def LongToShort(LongMatrix):
    return [i for i in map(list, zip(*[iter(LongMatrix[0])]*LongMatrix[2]))]


# Test if two short matrices have the same number of rows and columns
def ShortMatricesCompatible(MatrixA, MatrixB):
    ALong = ShortToLong(MatrixA)
    BLong = ShortToLong(MatrixB)
    output = [0, 0, 0]
    # Check for same number of sublists
    if ALong[1] == BLong[1]:
        output[0] = 1
    else:
        output[0] = 0
    # Check for same number of values
    if ALong[2] == BLong[2]:
        output[1] = 1
    else:
        output[1] = 0
    # Check for same total length
    if len(ALong[0]) == len(BLong[0]):
        output[2] = 1
    else:
        output[2] = 0
    return output


# Turn a list into a list of sublists where sublist contents are repeated list values
# e.g. turns [[0, 1, 2], 3] into [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
def ListToSublists(List, Repeat):
    return [[j for i in range(Repeat)] for j in List]

# Turns a list of sublists into a list of sums
# e.g. turns [[0, 0, 0], [1, 1, 1], [2, 2, 2]] into [0, 3, 6]
def ListOfSublistsToListOfSums(ListOfSublists):
    return [sum(i) for i in ListOfSublists]


# Positionally add the values in one matrix to the values in a second matrix
def AddShort(ShortA, ShortB):
    if ShortMatricesCompatible(ShortA, ShortB) == [1, 1, 1]:
        LongA, LongB = ShortToLong(ShortA), ShortToLong(ShortB)
        LongC = [[LongA[0][i] + LongB[0][i] for i in range(len(LongA[0]))], LongA[1], LongA[2]]
        return LongToShort(LongC)

    else:
        raise Exception('Tried positionally adding two matrices of different dimensions')


# Positionally subtract the values in one matrix for the values in a second matrix
def SubtractShort(ShortA, ShortB):
    if ShortMatricesCompatible(ShortA, ShortB) == [1, 1, 1]:
        LongA, LongB = ShortToLong(ShortA), ShortToLong(ShortB)
        LongC = [[LongA[0][i] - LongB[0][i] for i in range(len(LongA[0]))], LongA[1], LongA[2]]
        return LongToShort(LongC)

    else:
        raise Exception('Tried positionally subtracting two matrices of different dimensions')

# Positionally multiply the values in one matrix by the values in a second matrix
def MultiplyShort(ShortA, ShortB):
    if ShortMatricesCompatible(ShortA, ShortB) == [1, 1, 1]:
        LongA, LongB = ShortToLong(ShortA), ShortToLong(ShortB)
        LongC = [[LongA[0][i] * LongB[0][i] for i in range(len(LongA[0]))], LongA[1], LongA[2]]
        return LongToShort(LongC)

    else:
        raise Exception('Tried positionally multiplying two matrices of different dimensions')


# Positionally divide the values in one matrix by the values in a second matrix
def DivideShort(ShortA, ShortB):
    if ShortMatricesCompatible(ShortA, ShortB) == [1, 1, 1]:
        LongA, LongB = ShortToLong(ShortA), ShortToLong(ShortB)
        LongC = [[LongA[0][i] / LongB[0][i] for i in range(len(LongA[0]))], LongA[1], LongA[2]]
        return LongToShort(LongC)

    else:
        raise Exception('Tried positionally dividing two matrices of different dimensions')

