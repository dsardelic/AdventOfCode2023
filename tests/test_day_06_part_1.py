import unittest

from aoc2023 import day_06_part_1


class TestDay06Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_06_example.txt", 288),
            ("input/day_06.txt", 393120),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_06_part_1.solution(input_file_rel_uri), exp_solution
                )
