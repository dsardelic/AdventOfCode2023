import unittest

from aoc2023 import day_10_part_2


class TestDay10Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_10_example2.txt", 4),
            ("input/day_10_example3.txt", 4),
            ("input/day_10_example4.txt", 8),
            ("input/day_10_example5.txt", 10),
            ("input/day_10.txt", 367),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_10_part_2.solution(input_file_rel_uri), exp_solution
                )
