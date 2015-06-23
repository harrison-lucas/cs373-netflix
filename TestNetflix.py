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
