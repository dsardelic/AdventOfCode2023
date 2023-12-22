import unittest

from aoc2023 import day_22_part_1


class TestDay22Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_22_example.txt", 5),
            ("input/day_22.txt", 530),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_22_part_1.solution(input_file_rel_uri), exp_solution
                )
