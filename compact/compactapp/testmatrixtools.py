import unittest
from matrixtools import blank_matrix, \
    identity_matrix, \
    short_to_long, \
    long_to_short, \
    short_matrices_compatible, \
    list_to_sublists,\
    list_of_sublists_to_list_of_sums,\
    add_short, \
    subtract_short, \
    multiply_short, \
    divide_short, \
    transpose


class testblank_matrix(unittest.TestCase):
    # Test blank_matrix by creating three different blank matrices of different dimensions
    def testblank_matrixSquare(self):
        assert blank_matrix(2, 2) == [[0, 0], [0, 0]]

    def testblank_matrixTall(self):
        assert blank_matrix(3, 6) == [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    def testblank_matrixWide(self):
        assert blank_matrix(6, 3) == [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


class testidentity_matrix(unittest.TestCase):
    # Test identity_matrix by creating a square identity matrix
    def testidentity_matrixSquare(self):
        assert identity_matrix(2, 2) == [[1, 0], [0, 1]]


class testshort_to_long(unittest.TestCase):
    # Test ShortToLong by converting a 3x3 matrix from short form to long form
    def testshort_to_long(self):
        assert short_to_long([[0, 1, 2], [3, 4, 5], [6, 7, 8]]) == [[0, 1, 2, 3, 4, 5, 6, 7, 8], 3, 3]


class testlong_to_short(unittest.TestCase):
    # Test LongToShort
    def testlong_to_short(self):
        assert long_to_short([[0, 1, 2, 3, 4, 5, 6, 7, 8], 3, 3]) == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


class testshort_matrices_compatible(unittest.TestCase):
    # Test ShortMatricesCompatible
    def testshort_matrices_compatible(self):
        assert short_matrices_compatible([[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]) == [1, 1, 1]

    # Assert that different numbers of sublists == {True, False, True]
    def testshort_matrices_compatible_fail_sublists(self):
        assert short_matrices_compatible([[0, 0]], [[0, 0], [0, 0], [0, 0]]) == [0, 1, 0]

    # Assert that different numbers of values == {True, False, False]
    def testshort_matrices_compatible_fail_values(self):
        assert short_matrices_compatible([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]]) == [1, 0, 0]


class testlist_to_sublists(unittest.TestCase):
    def testlist_to_sublists(self):
        assert list_to_sublists([0, 1, 2], 3) == [[0, 0, 0], [1, 1, 1], [2, 2, 2]]

    def testlist_to_sublists_tall(self):
        assert list_to_sublists([0, 1, 2], 5) == [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2]]

    def testlist_to_sublists_wide(self):
        assert list_to_sublists([0, 1, 2], 2) == [[0, 0], [1, 1], [2, 2]]


class testlist_of_sublists_to_list_of_sums(unittest.TestCase):
    def testlist_of_sublists_to_list_of_sums(self):
        assert list_of_sublists_to_list_of_sums([[0, 0, 0], [1, 1, 1], [2, 2, 2]]) == [0, 3, 6]

    def testlist_of_sublists_to_list_of_sums_negatives(self):
        assert list_of_sublists_to_list_of_sums([[0, -1, 0], [1, 1, -1], [2, 2, -2]]) == [-1, 1, 2]

    def testlist_of_sublists_to_list_of_sums_mixed(self):
        assert list_of_sublists_to_list_of_sums([[0, -4], [1], [109, 1, 1, -1]]) == [-4, 1, 110]


class testadd_short(unittest.TestCase):
    def testadd_short(self):
        assert add_short([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

    def testadd_short_error(self):
        with self.assertRaises(Exception) as context:
            add_short([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally adding two matrices of different dimensions' in str(context.exception))


class testsubtract_short(unittest.TestCase):
    def testsubtract_short(self):
        assert subtract_short([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def testsubtract_short_error(self):
        with self.assertRaises(Exception) as context:
            subtract_short([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally subtracting two matrices of different dimensions' in str(context.exception))


class testmultiply_short(unittest.TestCase):
    def testmultiply_short(self):
        assert multiply_short([[3, 2, 2], [2, 3, 2], [2, 2, 3]], [[3, 3, 3], [3, 3, 3], [3, 3, 3]]) \
               == [[9, 6, 6], [6, 9, 6], [6, 6, 9]]

    def testmultiply_short_error(self):
        with self.assertRaises(Exception) as context:
            multiply_short([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally multiplying two matrices of different dimensions' in str(context.exception))


class testdivide_short(unittest.TestCase):
    def testdivide_short(self):
        assert divide_short([[4, 2, 2], [2, 4, 2], [2, 2, 4]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]]) \
               == [[2, 1, 1], [1, 2, 1], [1, 1, 2]]

    def testdivide_short_error(self):
        with self.assertRaises(Exception) as context:
            divide_short([[0], [0], [0]], [[0, 0], [0, 0], [0, 0]])
        self.assertTrue('Tried positionally dividing two matrices of different dimensions' in str(context.exception))


class testtranspose(unittest.TestCase):
    def testtranspose(self):
        assert transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

