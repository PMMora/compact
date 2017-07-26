import unittest
from matrixtools import BlankMatrix, \
    IdentityMatrix, \
    ShortToLong, \
    LongToShort, \
    ShortMatricesCompatible, \
    ListToSublists,\
    ListOfSublistsToListOfSums,\
    AddShort, \
    SubtractShort, \
    MultiplyShort, \
    DivideShort


class testBlankMatrix(unittest.TestCase):
    # Test BlankMatrix by creating three different blank matrices of different dimensions
    def testBlankMatrixSquare(self):
        assert BlankMatrix(2, 2) == [[0, 0], [0, 0]]

    def testBlankMatrixTall(self):
        assert BlankMatrix(3, 6) == [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    def testBlankMatrixWide(self):
        assert BlankMatrix(6, 3) == [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


class testIdentityMatrix(unittest.TestCase):
    # Test IdentityMatrix by creating a square identity matrix
    def testIdentityMatrixSquare(self):
        assert IdentityMatrix(2, 2) == [[1, 0], [0, 1]]


class testShortToLong(unittest.TestCase):
    # Test ShortToLong by converting a 3x3 matrix from short form to long form
    def testShortToLong(self):
        assert ShortToLong([[0, 1, 2], [3, 4, 5], [6, 7, 8]]) == [[0, 1, 2, 3, 4, 5, 6, 7, 8], 3, 3]


class testLongToShort(unittest.TestCase):
    # Test LongToShort
    def testLongToShort(self):
        assert LongToShort([[0, 1, 2, 3, 4, 5, 6, 7, 8], 3, 3]) == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


class testShortMatricesCompatible(unittest.TestCase):
    # Test ShortMatricesCompatible
    def testShortMatricesCompatible(self):
        assert ShortMatricesCompatible([[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]) == [1, 1, 1]

    # Assert that different numbers of sublists == {True, False, True]
    def testShortMatricesCompatibleFailLength(self):
        assert ShortMatricesCompatible([[0, 0]], [[0, 0], [0, 0], [0, 0]]) == [0, 1, 0]

    # Assert that different numbers of values == {True, False, False]
    def testShortMatricesCompatibleFailLength(self):
        assert ShortMatricesCompatible([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]]) == [1, 0, 0]


class testListToSublists(unittest.TestCase):
    def testListToSublists(self):
        assert ListToSublists([0, 1, 2], 3) == [[0, 0, 0], [1, 1, 1], [2, 2, 2]]

    def testListToSublistsTall(self):
        assert ListToSublists([0, 1, 2], 5) == [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2]]

    def testListToSublistsWide(self):
        assert ListToSublists([0, 1, 2], 2) == [[0, 0], [1, 1], [2, 2]]


class testListOfSublistsToListOfSums(unittest.TestCase):
    def testListOfSublistsToListOfSums(self):
        assert ListOfSublistsToListOfSums([[0, 0, 0], [1, 1, 1], [2, 2, 2]]) == [0, 3, 6]

    def testListOfSublistsToListOfSumsNegatives(self):
        assert ListOfSublistsToListOfSums([[0, -1, 0], [1, 1, -1], [2, 2, -2]]) == [-1, 1, 2]

    def testListOfSublistsToListOfSumsMixedLists(self):
        assert ListOfSublistsToListOfSums([[0, -4], [1], [109, 1, 1, -1]]) == [-4, 1, 110]


class testAddShort(unittest.TestCase):
    def testAddShort(self):
        assert AddShort([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

    def testAddShortError(self):
        with self.assertRaises(Exception) as context:
            AddShort([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally adding two matrices of different dimensions' in str(context.exception))


class testSubtractShort(unittest.TestCase):
    def testSubtractShort(self):
        assert SubtractShort([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def testSubtractShortError(self):
        with self.assertRaises(Exception) as context:
            SubtractShort([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally subtracting two matrices of different dimensions' in str(context.exception))


class testMultiplyShort(unittest.TestCase):
    def testMultiplyShort(self):
        assert MultiplyShort([[3, 2, 2], [2, 3, 2], [2, 2, 3]], [[3, 3, 3], [3, 3, 3], [3, 3, 3]]) \
               == [[9, 6, 6], [6, 9, 6], [6, 6, 9]]

    def testMultiplyShortError(self):
        with self.assertRaises(Exception) as context:
            MultiplyShort([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally multiplying two matrices of different dimensions' in str(context.exception))


class testDivideShort(unittest.TestCase):
    def testDivideShort(self):
        assert DivideShort([[4, 2, 2], [2, 4, 2], [2, 2, 4]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[2, 1, 1], [1, 2, 1], [1, 1, 2]]

    def testDivideShortError(self):
        with self.assertRaises(Exception) as context:
            DivideShort([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally dividing two matrices of different dimensions' in str(context.exception))

