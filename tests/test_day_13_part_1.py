import unittest

from aoc2023 import day_13_part_1


class TestDay13Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_13_example.txt", 405),
            ("input/day_13.txt", 37718),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_13_part_1.solution(input_file_rel_uri), exp_solution
                )
