import unittest

from aoc2023 import day_01_part_1


class TestDay01Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_01_example.txt", 142),
            ("input/day_01.txt", 55447),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_01_part_1.solution(input_file_rel_uri), exp_solution
                )
