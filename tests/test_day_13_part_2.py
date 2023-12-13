import unittest

from aoc2023 import day_13_part_2


class TestDay13Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_13_example.txt", 400),
            ("input/day_13.txt", 40995),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_13_part_2.solution(input_file_rel_uri), exp_solution
                )
