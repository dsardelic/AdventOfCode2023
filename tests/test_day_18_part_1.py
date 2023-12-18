import unittest

from aoc2023 import day_18_part_1


class TestDay18Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_18_example.txt", 62),
            # ("input/day_18.txt", 46394),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_18_part_1.solution(input_file_rel_uri), exp_solution
                )
