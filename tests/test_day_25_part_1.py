import unittest

from aoc2023 import day_25_part_1


class TestDay25Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_25_example.txt", 54),
            ("input/day_25.txt", 568214),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_25_part_1.solution(input_file_rel_uri), exp_solution
                )
