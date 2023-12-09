import unittest

from aoc2023 import day_09_part_1


class TestDay09Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_09_example.txt", 114),
            ("input/day_09.txt", 1842168671),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_09_part_1.solution(input_file_rel_uri), exp_solution
                )
