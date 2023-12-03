import unittest

from aoc2023 import day_03_part_2


class TestDay03Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_03_example.txt", 467835),
            ("input/day_03.txt", 78236071),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_03_part_2.solution(input_file_rel_uri), exp_solution
                )
