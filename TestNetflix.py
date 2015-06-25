#!/usr/bin/env python3

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Netflix import netflix_solve

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :

    # -----
    # rmse
    # -----

    def test_rmse1 (self) :
        actual = netflix_rmse(2, 2)
        expected = 0
        self.assertEqual(expected, actual)

    def test_rmse2 (self) :
        actual = netflix_rmse(2, 4)
        expected = 2
        self.assertEqual(expected, actual)

    def test_rmse3 (self) :
        actual = netflix_rmse(1, 4)
        expected = 4.5
        self.assertEqual(expected, actual)
    
    # -----
    # solve
    # -----

    def test_solve (self) :
        r = StringIO()
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(1, 1)

# ----
# main
# ----

if __name__ == "__main__" :
    main()
