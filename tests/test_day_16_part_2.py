import unittest

from aoc2023 import day_16_part_2


class TestDay16Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_16_example.txt", 51),
            ("input/day_16.txt", 7324),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_16_part_2.solution(input_file_rel_uri), exp_solution
                )
