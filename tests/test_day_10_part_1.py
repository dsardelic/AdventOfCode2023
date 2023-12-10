import unittest

from aoc2023 import day_10_part_1


class TestDay10Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_10_example.txt", 4),
            ("input/day_10_example1.txt", 8),
            ("input/day_10.txt", 6897),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_10_part_1.solution(input_file_rel_uri), exp_solution
                )
