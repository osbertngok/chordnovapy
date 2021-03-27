import unittest
from chordnovacore.functions import (
    MAX_SUPPORTED_NUM_NOTES,
    MAX_NUM_EXPANSIONS,
    legacy_initialize_expansion_indexes,
    initialize_expansion_indexes,
)


class TestFunctions(unittest.TestCase):
    def test_initialize_expansion_indexes(self):
        a = legacy_initialize_expansion_indexes()
        b = initialize_expansion_indexes()
        for i in range(1, MAX_SUPPORTED_NUM_NOTES + 1):
            for j in range(i, MAX_SUPPORTED_NUM_NOTES + 1):
                for k in range(MAX_NUM_EXPANSIONS):
                    for l in range(MAX_SUPPORTED_NUM_NOTES):
                        self.assertEqual(
                            a[i][j][k][l],
                            b[i][j][k][l],
                            f"{i} {j} {k} {l}, {a[i][j][k][l]} {b[i][j][k][l]}",
                        )


if __name__ == "__main__":
    unittest.main()
